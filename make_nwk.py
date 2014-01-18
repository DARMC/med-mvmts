import networkx as nx
import unicodecsv as csv
import matplotlib.pyplot as plt 

def load_edge_table(infile):
	"""
	Returns edge table file intact except for header row.
	"""
	return [x for x in csv.reader(open(infile, 'rU'))][1:]

def load_points(infile):
	"""
	Returns only the name string of each point.
	 * A point is unique iff its name does not match any other point.
	"""
	return [x[4] for x in csv.reader(open(infile, 'rU'))]

def make_node_table(all_points):
	"""
	Returns a dict with pairs (key, val) where:
	 * Key: name string of the node
	 * Val: unique integer ID of node
	"""
	dict = {}
	for x in xrange(len(all_points)):
		dict[all_points[x]] = x # assign UID to node
	return dict

if __name__ == '__main__':
	# make edge and node tables
	print '>> Loading edge and node tables...',
	edges = load_edge_table('movements.csv')
	nodes = make_node_table(list(set(load_points('trips.csv'))))
	print 'SUCCEEDED'

	# match start and end nodes to edges
	print '>> Matching edges and nodes...',
	for edge in edges:
		edge.append(nodes[edge[2]])
		edge.append(nodes[edge[5]])
	print 'SUCCEEDED'

	# draw graph
	print '>> Drawing graph...',
	G = nx.Graph()
	for e in edges:
		G.add_edge(e[-2], e[-1])
	print 'COMPLETE'
