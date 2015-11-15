import numpy as np

from annealing_helper_functions import distance, changepath, simulated_annealing
from xml_parse import parse_xml_graph
from timer import Timer

graph = parse_xml_graph('fri26.xml')
#Square matrix
assert graph.shape[0] == graph.shape[1]
size = graph.shape[0]

# Hardcoded best path to validate distance calculations, zero-indexed
bestpath = np.asarray([x-1 for x in [1, 25, 24, 23, 26, 22, 21, 17, 18, 20, 19, 16, 11, 12, 13, 15, 14, 10, 9, 8, 7, 5, 6, 4, 3, 2]])
print "Best path: " + str(bestpath)
print "Best path length: " + str(distance(graph, bestpath))

#Initial values, probably need to be tuned
initial_path = np.random.permutation(size)
initial_temp = 2.
cool = 0.9
reanneal = 100
iterr = 100000
nswaps = 3

for iterr in [10**x for x in [3,4,5,6]]:
	with Timer() as t:
		solution, history = simulated_annealing(graph, distance, initial_path, initial_temp, cool, reanneal, iterr, changepath, nswaps)
	print "\nIterations: " + str(iterr)
	print "Calculated path: " + str(solution)
	print "Calculated path length: " + str(distance(graph, solution))
	print "Time: " + str(t.interval)
