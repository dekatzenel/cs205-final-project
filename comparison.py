import numpy as np

from annealing_helper_functions import distance, changepath, simulated_annealing
from parallel_tempering import serial_parallel_tempering, parallel_parallel_tempering
from plotting import get_plots
from timer import Timer
from multiprocessing import freeze_support
from xml_parse import parse_xml_graph


if __name__ == '__main__':
	# Necessary to make multiprocessing work on Windows:
	freeze_support()
	# Uncomment and/or move this to generate plots
	# get_plots(history, graph=None, best=bestpath, 
	#           best_dist=distance(graph, bestpath))

	graph = parse_xml_graph('fri26.xml')

	# Square matrix
	assert graph.shape[0] == graph.shape[1]
	size = graph.shape[0]

	# Hardcoded best path to validate distance calculations, zero-indexed
	bestpath = np.asarray([x-1 for x in [1, 25, 24, 23, 26, 22, 21, 17, 18, 20, 19,
	                                     16, 11, 12, 13, 15, 14, 10, 9, 8, 7, 5, 6,
	                                     4, 3, 2]])
	print "Best path: " + str(bestpath)
	print "Best path length: " + str(distance(graph, bestpath)) + "\n"

	# Initial values, probably need to be tuned
	initial_path = np.random.permutation(size)
	print "Initial path: " + str(initial_path)
	print "Initial path length: " + str(distance(graph, initial_path)) + "\n"
	nbefore = 100
	nswaps = 3
		
	# Reuse copy of initial path for all trials
	nsystems = 4
	initial_paths = []
	for i in xrange(nsystems):
	    initial_paths.append(np.asarray(initial_path))
	initial_temps = [1., np.sqrt(5), np.sqrt(5)**2, np.sqrt(5)**3]

	# # Run serial parallel tempering
	with open('results.txt', 'w') as f:
		f.write("\nSerial Parallel Tempering\n")
		f.write('Iter   Path   Time\n')
		for iterr in [10**x for x in [3, 4, 5, 6]]:
			for i in xrange(10):
				with Timer() as t:
					solution, history = serial_parallel_tempering(graph,
	                                                  distance, initial_paths,
	                                                  initial_temps, iterr,
	                                                  changepath, nswaps, nbefore)

				f.write('{}  {}  {}\n'.format(iterr, distance(graph, solution),
	                                               str(t.interval)))

		# Run parallel parallel tempering
		f.write("\nParallel Parallel Tempering\n")
		f.write('Iter   Path   Time\n')
		for iterr in [10**x for x in [3, 4, 5, 6]]:
			for i in xrange(10):
				with Timer() as t:
					solution, history = parallel_parallel_tempering(graph,
	                                                    distance, initial_paths,
	                                                    initial_temps, iterr,
	                                                    changepath, nswaps, nbefore)

				f.write('{}  {}  {}\n'.format(iterr, distance(graph, solution),
	                                               str(t.interval)))
