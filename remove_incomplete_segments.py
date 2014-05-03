import unicodecsv as csv
import sys
import argparse
from collections import Counter

def already_in(s, uniques, directed):
    '''
    Check if a segment already exists in the list of unique rows. Consider 
    whether directionality is being taken into account. 

    If the candidate segment is already in the list, increment that row's
    weighting field by one.
    '''
    for row in uniques:
        if directed:
            for row in uniques:
                if row[2] == s[2] and row[5] == s[5]:
                    row[-1] += 1
                    return uniques
        else:
            if set([row[2], row[5]]) == set([s[2], s[5]]):
                row[-1] += 1
                return uniques

    else:
        return False

def unique(valid_segments, directionality):
    '''
    Return only unique movements
    '''
    unique_segments = []
    for segment in valid_segments:
        segment.append(1)
        result = already_in(segment, unique_segments, directionality)
        if result:
            unique_segments = result
        else:
            unique_segments.append(segment)
    print '>> Wrote {0} unique geocoded movements'.format(len(unique_segments)) 
    return unique_segments

def set_up_arguments():
    '''
    Define arguments for parser.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str)
    parser.add_argument('outfile', type=str)
    parser.add_argument('--directed', action="store_true")
    parser.add_argument('--force_unique', action="store_true")

    return parser.parse_args()  

if __name__ == '__main__':
    args = set_up_arguments()
    print '\n---  Mediterranean Movements Validator ---'
    print '>> Execution Parameters:'
    if args.force_unique:
        print '   | - Returning unique segments only'
    if args.directed:
        print '   | - Considering directionality'
    else:
        print '   > Ignoring directionality\n'

    raw_data = [row for row in csv.reader(open(args.infile, 'rU'))]
    print '>> Retrieved {0} total movements'.format(len(raw_data))
    
    valid_segments = [row for row in raw_data if row[3] != '' and row[4] != '' \
                      and row[6] != '' and row[7] != '']

    print '>> Filtered {0} geocoded movements'.format(len(valid_segments))
    
    with open(args.outfile, 'w') as outf:
        writer = csv.writer(outf)
        if args.force_unique:
            writer.writerows(unique(valid_segments, args.directed))
        else:
            print '>> Wrote {0} valid movements'.format(len(valid_segments))
            writer.writerows(valid_segments)