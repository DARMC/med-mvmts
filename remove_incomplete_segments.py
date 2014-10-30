import argparse
import unicodecsv as csv

def already_in(s, uniques, directed):
    """
    Check if a segment already exists in the list of unique rows. Consider 
    whether directionality is being taken into account. 

    If the candidate segment is already in the list, increment that row's
    weighting field by one.

    Parameters
    ----------
    s: a single movement segment to be considered for inclusion in the list of unique movements.
    uniques: a list of unique movements against which s is compared
    directed: a boolean parameter to define whether direction is considered in identifying unique segments.
        If True, this function will consider (x1, y1) -> (x2, y2) to be a distinct movement from
        (x2, y2) -> (x1, y1).
    """
    for row in uniques:
        if directed:
            if row[2] == s[2] and row[5] == s[5]:
                row[-1] += 1
                return uniques
        else:
            if {row[2], row[5]} == {s[2], s[5]}:
                row[-1] += 1
                return uniques

    else:
        return False


def unique(geocoded_segments, directionality):
    """
    Return only unique movements.

    Parameters
    ----------
    geocoded_segments: a complete list of geocoded movement segments, which may or may not contain
        duplicate movements.
    directionality: a boolean parameter to define whether direction is considered in identifying
        unique segments. If True, this function will consider (x1, y1) -> (x2, y2) to be a distinct
        movement from (x2, y2) -> (x1, y1).
    """
    unique_segments = []

    for segment in geocoded_segments:
        segment.append(1)
        result = already_in(segment, unique_segments, directionality)
        if result:
            unique_segments = result
        else:
            unique_segments.append(segment)

    print "| - Wrote {0} unique geocoded movements".format(len(unique_segments))
    return unique_segments


def set_up_arguments():
    """
    Set parameters and parse command-line arguments.
    USAGE: remove_incomplete_segments.py [infile] [outfile] {--force_unique} {--directed}
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=str)
    parser.add_argument('outfile', type=str)
    parser.add_argument('--directed', action="store_true")
    parser.add_argument('--force_unique', action="store_true")

    return parser.parse_args()  

if __name__ == '__main__':
    args = set_up_arguments()
    print '\n---  Mediterranean Movements Validator ---'

    if args.force_unique:
        print '| - Optional Execution Parameters:'
        print '   | - Returning unique segments only'
        if args.directed:
            print '   | - Considering directionality as a criteria for uniqueness'
        else:
            print '   | - Ignoring directionality as a criteria for uniqueness'

    raw_data = [row for row in csv.reader(open(args.infile, 'rU'))]
    print '| - Retrieved {} total movements'.format(len(raw_data))
    
    valid_segments = [row for row in raw_data if row[3] != '' and row[4] != '' \
                      and row[6] != '' and row[7] != '']

    print '| - Filtered {} geocoded movements'.format(len(valid_segments))
    
    with open(args.outfile, 'w') as outf:
        writer = csv.writer(outf)
        if args.force_unique:
            writer.writerows(unique(valid_segments, args.directed))
        else:
            print '| - Wrote {} valid movements'.format(len(valid_segments))
            writer.writerows(valid_segments)
