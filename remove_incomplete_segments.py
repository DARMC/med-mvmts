import unicodecsv as csv
import sys

if __name__ == '__main__':
	raw_data = [row for row in csv.reader(open(sys.argv[1], 'rU'))]
	valid_segments = [row for row in raw_data if row[3] != '' and row[4] != '' and row[6] != '' and row[7] != '']

	with open(sys.argv[2], 'w') as outf:
		writer = csv.writer(outf)
		writer.writerows(valid_segments)