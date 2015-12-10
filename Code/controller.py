import numpy as np
from multiprocessing import freeze_support

from annealing_helper_functions import distance, changepath, simulated_annealing
from parallel_tempering import serial_parallel_tempering, parallel_parallel_tempering
from utils.plotting import get_plots
from utils.timer import Timer
from utils.xml_parse import parse_xml_graph

if __name__ == '__main__':
	# Necessary to make multiprocessing work on Windows:
	freeze_support()

	# Uncomment and/or move this to generate plots
	# get_plots(history, graph=None, best=bestpath, 
	#           best_dist=distance(graph, bestpath))

	graph = parse_xml_graph('resources/fri26.xml')

	# Square matrix
	assert graph.shape[0] == graph.shape[1]
	size = graph.shape[0]

	# Hardcoded best path to validate distance calculations, zero-indexed
	bestpath = np.asarray([x-1 for x in [1, 25, 24, 23, 26, 22, 21, 17, 18,
                                          20, 19, 16, 11, 12, 13, 15, 14, 10,
                                          9, 8, 7, 5, 6, 4, 3, 2]])
	print "Best path: " + str(bestpath)
	print "Best path length: " + str(distance(graph, bestpath)) + "\n"

	# Initial values, probably need to be tuned
	initial_path = np.random.permutation(size)
	print "Initial path: " + str(initial_path)
	print "Initial path length: " + str(distance(graph, initial_path)) + "\n"
	initial_temp = 2.
	cool = 0.9
	nbefore = 480
	nswaps = 1
	reheat = np.sqrt(5)

	# Run simulated annealing
	print "\nSimulated Annealing\n"
	for iterr in [10**x for x in [3, 4, 5]]:
		with Timer() as t:
			solution, history = simulated_annealing(graph, distance,
	                                                   initial_path,
                                                         initial_temp, nbefore,
                                                         iterr, changepath,
                                                         nswaps, reheat, cool)
		print "Iterations: {:.2E}".format(iterr)
		print "Calculated path: " + str(solution)
		print "Calculated path length: " + str(distance(graph, solution))
		print "Time: " + str(t.interval) + "\n"
		
	# Reuse copy of initial path for all trials
	nsystems = 4
	initial_paths = []
	for i in xrange(nsystems):
	    initial_paths.append(np.asarray(initial_path))

	initial_temps = [1., np.sqrt(5), np.sqrt(5)**2, np.sqrt(5)**3]

	# Run parallel tempering in serial
	print "\nSerial Parallel Tempering\n"
	for iterr in [10**x for x in [3,4,5]]:
		with Timer() as t:
			solution, history = serial_parallel_tempering(graph, distance,
	                                                         initial_paths, 
	                                                         initial_temps, 
                                                               iterr,
                                                               changepath,
                                                               nswaps, nbefore)

		print "Iterations: {:.2E}".format(iterr)
		print "Calculated path: " + str(solution)
		print "Calculated path length: " + str(distance(graph, solution)) 
		print "Time: " + str(t.interval) + "\n"


	# Run parallel tempering in parallel
	print "\nParallel Parallel Tempering\n"
	for iterr in [10**x for x in [3, 4, 5]]:
		with Timer() as t:
			solution, history = parallel_parallel_tempering(graph, distance,
	                                                           initial_paths, 
	                                                           initial_temps,
	                                                           iterr,
                                                                 changepath,
	                                                           nswaps, nbefore)

		print "Iterations: {:.2E}".format(iterr)
		print "Calculated path: " + str(solution)
		print "Calculated path length: " + str(distance(graph, solution)) 
		print "Time: " + str(t.interval) + "\n"
