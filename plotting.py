import numpy as np
import matplotlib.pyplot as plt
from xml_parse import parse_xml_graph
import networkx as nx

def plot_graph(graph=None, path=None, dist=None, best=None, best_dist=None,
			   save=False, name=None, title=None):
	"""
	Plot a TSP graph.

	Parameters
	----------
	graph: An XML TSP graph. If None, use the default graph from parse_xml_graph.
	path: An ordered list of node indices. If given, plot the path. Otherwise, plot
		the underlying graph.
	dist: Distances of the paths in path.
	best: Empirical best path.
	best_dist: Empirical best path distance.
	save: If True, saves the graph as name.png. Otherwise, draws the graph.
	name: Graph is saved as name.png
	title: Caption of the graph.
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
	edges = list()
	edge_colors = list()
	if path is not None:
		edges.extend([(path[i], path[i+1]) for i in range(len(path)-1)])
		edges.append((path[-1], path[0]))
		edge_colors.extend(['r' for i in range(len(path))])
	if best is not None:
		edges.extend([(best[i], best[i+1]) for i in range(len(best)-1)])
		edges.append((best[-1], best[0]))
		edge_colors.extend(['b' for i in range(len(best))])
	if path is None and best is None:
		edges = G.edges()

	plt.clf()
	fig = plt.figure(figsize=(14, 5.5))
	ax1 = fig.add_subplot(121)
	ax2 = fig.add_subplot(122)
	nx.draw_graphviz(G, edgelist=edges, edge_color=edge_colors, with_labels=None,
		node_color='k', node_size=100, ax=ax1)
	ax1.set_title(title)
	ax2.plot(np.arange(1, len(dist)+1), dist, color='r', alpha=0.9, label='Best found path')
	ax2.hlines(best_dist, 0, len(dist)+1, color='b', label='Best path')
	ax2.set_xlim(1, max(len(dist), 2));
	ax2.legend()

	if not save:
		plt.show()
	else:
		plt.savefig('temp/{}.png'.format(name))
