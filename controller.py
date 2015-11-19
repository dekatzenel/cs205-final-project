import numpy as np

from annealing_helper_functions import distance, changepath, simulated_annealing, parallel_tempering
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
nswaps = 3

# Run simulated annealing
print "\nSimulated Annealing\n"
for iterr in [10**x for x in [3,4,5]]:
	with Timer() as t:
		solution, history = simulated_annealing(graph, distance, initial_path, 
												initial_temp, cool, reanneal, iterr, 
												changepath, nswaps)
	print "\nIterations: {:.2E}".format(iterr)
	print "Calculated path: " + str(solution)
	print "Calculated path length: " + str(distance(graph, solution))
	print "Time: " + str(t.interval)

# Initial values for parallel tempering
nsystems = 3
initial_paths = [np.random.permutation(size) for i in xrange(nsystems)]
initial_temps = [1., 5., 10.]
nbefore = 100

# Run parallel tempering
print "\nParallel Tempering\n"
for iterr in [10**x for x in [3,4,5]]:
	with Timer() as t:
		solution, history = parallel_tempering(graph, distance, initial_paths, initial_temps,
											   iterr, changepath, nswaps, nbefore)

	print "\nIterations: {:.2E}".format(iterr)
	print "Calculated path: " + str(solution)
	print "Calculated path length: " + str(distance(graph, solution)) 
	print "Time: " + str(t.interval)
