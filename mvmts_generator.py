import unicodecsv as ucsv

def read_input(points, delChar=','):
    # just encode the input file as UTF-8 and save yourself the hassle unless special chars are required
    with open(points, 'rU') as inf:
        reader = ucsv.reader(inf, delimiter = delChar)
        data = [line for line in reader]
    return data[1:]

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
    database = read_input('trips.csv')
    headers = ['Trip #', 'Stage', 'Start', 'Start_lat', 
               'Start_long', 'End', 'End_lat', 'Eng_long', 
               'Traveler', 'Purpose', 'Description']
    output = []
    for trip in set([x[1] for x in database]):
        v = Voyage([p for p in database if p[1] == trip], trip)
        v.parse_trip()
        output.append(v.return_new_string())

    with open('segments.csv', 'w') as outf:
        wr = ucsv.writer(outf)
        wr.writerow(headers)       
        for trip in output:
            for segment in trip:
                wr.writerow(segment)








