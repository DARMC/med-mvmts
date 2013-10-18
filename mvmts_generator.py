import shapefile as shp
import urllib
import unicodecsv as ucsv
from geopy import geocoders
from time import sleep

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
    sf.line(parts = [[[x1,y1],[x2,y2]]])
    sf.records.append(row)

    return sf

class BoundingBox(object):
    def __init__(self, box):
        self.x1 = float(box[0][0])
        self.x2 = float(box[1][0])
        self.y1 = float(box[0][1])
        self.y2 = float(box[1][0])

    def is_in_box(self, point_x, point_y):
        latitude = False
        longitude = False
        if point_x >= min(self.x1, self.x2) and point_x <= max(self.x1, self.x2):
            longitude = True
        if point_y >= min(self.y1, self.y2) and point_y <= max(self.y1, self.y2): 
            latitude = True 
        return True if latitude and longitude else False

class Voyage(object):
    def __init__(self, raw_movements, trip_id):
        self.data = raw_movements
        self.uid = trip_id
        self.segments = []
   
    def describe_trip(self):
        """Optional method for debugging"""
        print 'Processing trip {0}'.format(self.uid)

    def parse_trip(self):
        ordered_trip = {}
        for row in self.data:
            ordered_trip[int(row[2])] = row
        seg = 1
        while True: # a little bit hacky, could be better 
            try:
                segment = [self.uid, str(seg), ordered_trip[seg][4], ordered_trip[seg][5], 
                           ordered_trip[seg][6], ordered_trip[seg+1][4], 
                           ordered_trip[seg+1][5], ordered_trip[seg+1][6], ordered_trip[seg][21],
                           ordered_trip[seg][24], ordered_trip[seg][27][0:254]] # boom, triple indexing
                print "{0}.{1}: {2} to {3}".format(self.uid, str(seg), ordered_trip[seg][4], ordered_trip[seg+1][4])
                self.segments.append(segment)
                seg += 1
            except KeyError:
                break

    def return_new_string(self):
        return self.segments

if __name__ == '__main__':
    f = 'movements'
    database = read_input('trips.csv')
    
    # alas, geocoder is worthless for historical place names
    # failure and error rate is so high that we might as well do it by hand
    """box = ((-13, 25),(52, 60))
    b = BoundingBox(((-13, 25),(52, 60)))
    g = geocoders.GoogleV3()
    for line in database:
        # geocode if it already doesn't have coordinates
        if line[5] == '' and line[6] == '':
            print 'Attempting to geocode {0}'.format(line[4])
            try:
                print g.geocode(line[4], exactly_one=False)
                print '\n' 
                if b.is_in_box(float(lng), float(lat)):
                    print 'Geocoded!'
                    line[5], line[6] = lat, lng
                else:
                    print 'Found point but not in Europe'
            except ValueError:
                print 'No point returned or too many points'
            sleep(2)
        else:
            pass"""

    headers = ['Trip #', 'Stage', 'Start', 'Start_lat', 
               'Start_long', 'End', 'End_lat', 'Eng_long', 
               'Traveler', 'Purpose', 'Description']
    output = []
    for trip in set([x[1] for x in database]):
        v = Voyage([p for p in database if p[1] == trip], trip)
        v.parse_trip()
        output.append(v.return_new_string())

    with open(f+'.csv', 'w') as outf:
        wr = ucsv.writer(outf)
        wr.writerow(headers)       
        for trip in output:
            for part in trip:
                wr.writerow(part)

    # set up shapefile 
    write_prj_file(f)
    shapefile = set_up_shapefile(headers)
    for trip in output:
        for lseg in trip:
            print lseg
            try:
                add_geometry(shapefile, float(lseg[4]), float(lseg[3]), float(lseg[7]),float(lseg[6]), lseg)
            except ValueError:
                pass
    shapefile.save(f)








