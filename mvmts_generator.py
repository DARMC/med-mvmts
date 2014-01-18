import unicodecsv as csv
import itertools
import sys

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
                segment = [self.uid, str(seg), ordered_trip[seg][4], 
                        ordered_trip[seg][5], ordered_trip[seg][6], 
                        ordered_trip[seg+1][4], ordered_trip[seg+1][5], 
                        ordered_trip[seg+1][6], ordered_trip[seg][21],
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
    # load  raw data
    database = [line for line in csv.reader(open(sys.argv[1],'rU'))][1:]

    #database = read_input('trips.csv')
    headers = ['TRIP_ID', 'STAGE', 'START', 'ST_LAT', 
               'ST_LNG', 'END', 'END_LAT', 'END_LNG', 
               'TRAVELER', 'PURPOSE', 'DESCR']
    
    output = []
    # convert raw data into line segments
    for trip in set([x[1] for x in database]):
        v = Voyage([p for p in database if p[1] == trip], trip)
        v.parse_trip()
        output.append(v.return_new_string())

    #write csv output
    with open('movements.csv', 'w') as outf:
        writer = csv.writer(outf)
        writer.writerow(headers)       
        writer.writerows(list(itertools.chain(*output)))
