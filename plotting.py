import numpy as np
import matplotlib.pyplot as plt
from xml_parse import parse_xml_graph
import networkx as nx

def plot_graph(graph=None, path=None, save=False, name=None):
	"""
	Plot a TSP graph.

	Parameters
	----------
	graph: An XML TSP graph. If None, use the default graph from parse_xml_graph.
	path: An ordered list of node indices. If given, plot the path. Otherwise, plot
		the underlying graph.
	save: If True, saves the graph as name.png. Otherwise, draws the graph.
	name: Graph is saved as name.png
	"""
	# Check input parameters 
	if save:
		assert (name is not None), 'If saving graph, must provide name'

	# Initialize graph
	if graph is not None:
		g = parse_xml_graph(graph)
	else:
		g = parse_xml_graph()
	G = nx.from_numpy_matrix(g)

	# Plot path, if applicable
	if path is not None:
		edges = [(path[i], path[i+1]) for i in len(path)-1]
		edges.append((path[-1], path[0]))
	else:
		edges = G.edges()

	nx.draw_graphviz(G, edgelist=edges, with_labels=None)

	if not save:
		plt.show()
	else:
		plt.savefig('{}.png'.format(name))
