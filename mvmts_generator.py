import shapefile as shp
import urllib
import unicodecsv as ucsv

def read_input(points, delChar=','):
    # just encode the input file as UTF-8 and save yourself the hassle unless special chars are required
    with open(points, 'rU') as inf:
        reader = ucsv.reader(inf, delimiter = delChar)
        data = [line for line in reader]
    return data[1:]

def write_prj_file(fname, epsg=4326):
    """
    Writes .prj file fname associated with target projection epsg.
    Writes to epsg 4326 (WGS 1984) by default. Honestly, kwarg is only included for robustness.
    """
    try:
        wktString  = urllib.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg))
        with open('{0}.prj'.format(fname), 'w') as prjFile:
            prjFile.write(wktString.read())
    except IOError:
        print 'Unable to fetch EPSG string for prj file. Projection can be still be defined on import to GIS client'
    return True

def set_up_shapefile(fieldNames):
    """
    Returns a shapefile with specified field names and a blank,
    well-shaped attribute table
    """
    sf = shp.Writer(shp.POLYLINE)
    sf.autoBalance = 1
    for f in fieldNames:
        sf.field(f, 'C', '255')
        for r in sf.records:
            r.append('')
    return sf

def add_geometry(sf, x1, y1, x2, y2, row):
    """
    Add exactly two points to a shapefile
    """
    sf.line(parts = [[[x1, y1],[x2, y2]]])
    sf.records.append(row)

    return sf

class Voyage(object):
    def __init__(self, raw_movements, trip_id):
        self.data = raw_movements
        self.uid = trip_id
        self.segments = []
    
    def __repr__(self):
        return 'Processing trip {0}'.format(self.uid)  

    def parse_trip(self):
        ordered_trip = {}
        for row in self.data:
            try:
                ordered_trip[int(row[2])] = row
            except ValueError:
                print 'Missing sorting data'
                ordered_trip[1] = row
        seg = 1
        while True: # a little bit hacky, could be better 
            try:
                segment = [self.uid, str(seg), ordered_trip[seg][4], ordered_trip[seg][5], 
                           ordered_trip[seg][6], ordered_trip[seg+1][4], 
                           ordered_trip[seg+1][5], ordered_trip[seg+1][6], ordered_trip[seg][21],
                           ordered_trip[seg][24], ordered_trip[seg][27][0:254]]
                print "{0}.{1}: {2} to {3}".format(self.uid, str(seg), ordered_trip[seg][4], ordered_trip[seg+1][4])
                self.segments.append(segment)
                seg += 1
            except KeyError:
                break
            except UnicodeEncodeError, UnicodeDecodeError:
                print "Encode failed on trip {0}.{1}".format(self.uid, seg)
                seg += 1

    def return_new_string(self):
        return self.segments

if __name__ == '__main__':
    f = 'movements'
    
    # load  raw data
    database = read_input('trips.csv')
    headers = ['Trip #', 'Stage', 'Start', 'Start_lat', 
               'Start_long', 'End', 'End_lat', 'Eng_long', 
               'Traveler', 'Purpose', 'Description']
    output = []

    # convert raw data into line segments
    for trip in set([x[1] for x in database]):
        v = Voyage([p for p in database if p[1] == trip], trip)
        v.parse_trip()
        output.append(v.return_new_string())

    #write csv output
    with open(f+'.csv', 'w') as outf:
        wr = ucsv.writer(outf)
        wr.writerow(headers)       
        for trip in output:
            for part in trip:
                wr.writerow(part)

    # set up shapefile 
    write_prj_file(f)
    shapefile = set_up_shapefile(headers)
    
    # write data to shapefile
    for trip in output:
        for lseg in trip:
            try:
                add_geometry(shapefile, float(lseg[4]), float(lseg[3]), float(lseg[7]), float(lseg[6]), lseg)
            except ValueError:
                pass
    shapefile.save(f)
