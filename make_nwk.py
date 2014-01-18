import networkx as nx
import unicodecsv as csv
import matplotlib.pyplot as plt 

with open('movements.csv','rU') as inf:
	segments = [x for x in csv.reader(inf)][1:]

with open('trips.csv', 'rU') as inf:
	locations = [x[4] for x in csv.reader(inf)][1:]

candidates = list(set(locations))

location_dict = {}

for x in xrange(len(candidates)):
	location_dict[candidates[x]] = x


#print location_dict
for segment in segments:
	segment.append(location_dict[segment[2]])
	segment.append(location_dict[segment[5]])
	print segment

# segments now has to-from information
G = nx.Graph()
for s in segments:
	G.add_edge(s[-2], s[-1])

#nx.draw(G)
print nx.betweenness_centrality(G)

