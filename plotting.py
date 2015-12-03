import numpy as np
import matplotlib.pyplot as plt
from xml_parse import parse_xml_graph
import networkx as nx
import graphviz as gvz

def tsp_graph(graph=None):
	""" Plot a TSP graph. """
	# If graph is None, use the default graph from parse_xml_graph.
	if graph is not None:
		g = parse_xml_graph(graph)

	else:
		g = parse_xml_graph()

	G = nx.from_numpy_matrix(g)
	nx.draw(G)
	plt.show()