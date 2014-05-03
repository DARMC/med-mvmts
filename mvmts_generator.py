import unicodecsv as csv
import itertools
import os
import sys
from time import time

class NoNextPointException(Exception):
    """
    An exception to stop iteration when no 'next point' is found during parsing of trip segments
    """
    pass

def read_input(infile):
    """
    Return a list of lists from a csv file 'infile', attempting to provide a graceful
    and informative exist if the file cannot be read.

    Parameters
    ----------
    infile: path to file to read.
    """
    print '| - Reading data from input spreadsheet...'
    try:
        database = [line for line in csv.reader(open(infile, 'rU'))][1:]

    except IOError:
        if not os.path.isfile(infile):
            sys.exit('> No file found matching path {}'.format(infile))
        else:
            sys.exit('> An error occurred trying to open {}'.format(infile))

    return database

class Voyage:
    def __init__(self, raw_movements, trip_id):
        self.data = raw_movements
        self.uid = trip_id
        self.segments = []

    def __repr__(self):
        return 'Voyage object for trip ID {}'.format(self.uid)

    def new_parse_trip(self):
        self.data = [x for x in self.data if x[2] not in ['', ' ']]

        correct_trip_segments = []
        # loop until no trip segment with id current_trip_segment + 1 can be found
        try:
            current_trip_segment = 1
            while True:
                current_point_variations = [x for x in self.data if int(float(x[2])) == current_trip_segment]
                next_point_variations = [x for x in self.data if int(float(x[2])) == current_trip_segment+1]
                if len(next_point_variations) == 0:
                    raise NoNextPointException
                for x in current_point_variations:
                    for y in next_point_variations:
                        wkt_string = 'LINESTRING({0} {1}, {2} {3})'.format(x[6], x[5], y[6], y[5])
                        correct_trip_segments.append([self.uid, str(len(correct_trip_segments)+1),
                                                      x[4], x[5], x[6], y[4], y[5], y[6], x[21], x[24],
                                                      x[27][0:254], '?' if len(x) > 1 or len(y) > 1 else '',
                                                      wkt_string])
                current_trip_segment += 1

        except NoNextPointException:
            return correct_trip_segments


if __name__ == '__main__':
    start = time()
    try:
        database = read_input(sys.argv[1])
    except IndexError:
        sys.exit('USAGE: mvmts_generator.py [infile]')

    print '| - Parsing point data to line segments...',
    output = []
    for trip in {x[1] for x in database}:
        v = Voyage([p for p in database if p[1] == trip], trip)
        output.append(v.new_parse_trip())
    output = list(itertools.chain(*output))
    print 'interpreted {} total segments'.format(len(output))


    print '| - Writing trips to output file...'
    with open('movements.csv', 'w') as outf:
        writer = csv.writer(outf)
        writer.writerow(['TRIP_ID', 'STAGE', 'START', 'ST_LAT', 'ST_LNG',
                         'END', 'END_LAT', 'END_LNG', 'TRAVELER', 'PURPOSE',
                         'DESCR', 'Q', 'WKT'])
        writer.writerows(output)
    print '| - Runtime {0:.2f} seconds.'.format(time() - start)
