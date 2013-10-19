import unicodecsv as ucsv
import os
import sys
import time as t

def load_file(f):
    if not os.path.exists(f):
        sys.exit('Source file not found')
    data = []
    with open(f, 'rU') as inf:
        r = ucsv.reader(inf)
        data = [item for item in r]

    return data

class StaticGeocoder(object):
    def __init__(self, points, centroids):
        self.ctd = centroids
        self.pts = points

    def resolve_conflicted_matches(self, matches):   
        print '{0} Possible Matches:'.format(len(matches))
        # allow users to manually select correct geocode
        for idx, x in enumerate(matches): 
            print '{0}. ({1}) {2} [{3:.4},{4:.4}]'.format(idx+1, x[4], x[5], x[6], x[7])
        target = int(raw_input('Select desired match by index: '))
        #print matches[target-1]
        return matches[target-1]  
  
    def attempt_strict_geocode(self, target, centroid_mode = False):
        exact_matches = []
        c_name, c_lat, c_long = target[4], target[5], target[6]
        print 'Attempting to match {0}'.format(c_name)
        if not centroid_mode:
            for location in self.pts:
                if location[4] == c_name:
                    exact_matches.append(location)
        elif centroid_mode:
            for centroid in self.ctd:
                if centroid[4] == c_name:
                    exact_matches.append(centroid)
        return exact_matches

    def attempt_fuzzy_geocode(self, target, centroid_mode = False):
        #TODO
        pass
 
if __name__ == '__main__':
    st = t.time()
    fuzziness = 2
    # load data
    if len(sys.argv) != 2:
        sys.exit('Usage darmc_geocoder.py <file_to_geocode>')
    locations = load_file('darmc_settlements.csv')
    centroids = load_file('centroids.csv')
    geocode_candidates = load_file(sys.argv[1])
    
    # set up geocoder object
    gc = StaticGeocoder(locations, centroids)

    output = []
    output.append(geocode_candidates[0])
    print output
    # attempt to geocode points
    for candidate in geocode_candidates[1:]:
        matches = gc.attempt_strict_geocode(candidate)
        if len(matches) == 0:
            pass
        # if a match is found
        else:
            # check if list contains mutliple sublists (i.e. multiple matches)
            # improve this?
            if sum(isinstance(el, list) for el in matches) > 1:
                matches = gc.resolve_conflicted_matches(matches)
            # else, pull out the single result
            else:
                matches = matches[0]
            candidate[5] = matches[7]
            candidate[6] = matches[6]
        output.append(candidate)
 
    with open('geocoded_trips.csv','w') as outf:
        wr = ucsv.writer(outf)
        for row in output:
            wr.writerow(row)          
    
    print t.time() - st