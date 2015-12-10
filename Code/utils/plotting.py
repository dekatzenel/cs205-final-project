import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from utils.xml_parse import parse_xml_graph

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
	fig.clf()

def get_plots(history, graph, best, best_dist):
	""" Generates and saves plots. See plot_graph for parameter descriptions. """
	dist_hist = list()
	mindist = np.inf
	plot_every = 10000 # generate an image every plot_every iterations
	for i in history[0]:
		if i[0] < mindist:
			mindist = i[0]
		dist_hist.append(mindist)

	actual_hist = [i[0] for i in history[0][::plot_every]]
	paths_hist = [i[1] for i in history[0][::plot_every]]

	for i in range(len(paths_hist)):
		title = 'iter={}  dist={}  best={}'.format(i*plot_every, actual_hist[i], 
			    								   best_dist)
		plot_graph(graph=graph, path=paths_hist[i], dist=dist_hist[:plot_every*i+1], best=best,
			       best_dist=best_dist, save=True,
			       name='abcba{}'.format(i), title=title)