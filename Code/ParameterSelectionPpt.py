import numpy as np
from multiprocessing import freeze_support

from annealing_helper_functions import distance, changepath, simulated_annealing
from parallel_tempering import parallel_parallel_tempering, serial_parallel_tempering
from utils.timer import Timer
from utils.xml_parse import parse_xml_graph


if __name__ == '__main__':
	# Necessary to make multiprocessing work on Windows:
	freeze_support()

    # Load graph
	graph = parse_xml_graph('resources/fri26.xml')
	
	#Square matrix
	assert graph.shape[0] == graph.shape[1]
	size = graph.shape[0]

	# Hardcoded best path to validate distance calculations, zero-indexed
	bestpath = np.asarray([x-1 for x in [1, 25, 24, 23, 26, 22, 21, 17, 18, 20, 19, 16, 11, 12, 13, 15, 14, 10, 9, 8, 7, 5, 6, 4, 3, 2]])
	print "Best path: " + str(bestpath)
	print "Best path length: " + str(distance(graph, bestpath)) + "\n"

	#Initial values
	num_processes = 4
	initial_Xs = [np.random.permutation(size) for i in range(num_processes)]
	ratios = [np.sqrt(i) for i in range(1,7,1)] #Ratio of temperatures between processes
	iterr=10000
	nswaps = 3
	nbefore = 100

	# Number of runs per parameter combination:
	runs = 30

	with Timer() as t:

		# Find ratio of temperatures that gives the best average results
		mean_dists = []
		for ratio in ratios:
			initial_temps = [ratio**i for i in range(num_processes)]

			# Collect all the distances that are calculated in each run:
			distances = []
			for i in xrange(runs):
				solution, histories = parallel_parallel_tempering(graph, distance, initial_Xs, initial_temps, iterr, changepath, nswaps, nbefore)
				distances.append(distance(graph,solution))

			mean_dists.append(np.mean(distances))

		# Key the ratios by their average performance
		ratio_dict = dict(zip(mean_dists,ratios))   

		# Find the best one:
		best_ratio = np.round((ratio_dict[np.min(mean_dists)])**2)

		print "Best ratio to use is the square root of ", best_ratio

	print "Time: " + str(t.interval) + "\n"

	with Timer() as t:
		initial_temps = [best_ratio**i for i in range(num_processes)]
		nswapses = [1,2,3,4,5,6]

		# Find ratio of temperatures that gives the best average results
		mean_dists = []
		for nswaps in nswapses:

			# Collect all the distances that are calculated in each run:
			distances = []
			for i in xrange(runs):
				solution, histories = parallel_parallel_tempering(graph, distance, initial_Xs, initial_temps, iterr, changepath, nswaps, nbefore)
				distances.append(distance(graph,solution))

			mean_dists.append(np.mean(distances))

		# Key the ratios by their average performance
		nswaps_dict = dict(zip(mean_dists,nswapses))   

		# Find the best one:
		nswaps = nswaps_dict[np.min(mean_dists)]

		print "Best number of swaps to use is ", nswaps

	print "Time: " + str(t.interval) + "\n"

	with Timer() as t:

		initial_temps = [best_ratio**i for i in range(num_processes)]
		nbefores = [80, 160, 320, 480, 640]

		# Find ratio of temperatures that gives the best average results
		mean_dists = []
		for nbefore in nbefores:

			# Collect all the distances that are calculated in each run:
			distances = []
			for i in xrange(runs):
				solution, histories = parallel_parallel_tempering(graph, distance, initial_Xs, initial_temps, iterr, changepath, nswaps, nbefore)
				distances.append(distance(graph,solution))

			mean_dists.append(np.mean(distances))

		# Key the ratios by their average performance
		nbefore_dict = dict(zip(mean_dists,nbefores))   

		# Find the best one:
		nbefore = nbefore_dict[np.min(mean_dists)]

		print "Best swapping interval is ", nbefore
		print nbefore_dict

	print "Time: " + str(t.interval) + "\n"

