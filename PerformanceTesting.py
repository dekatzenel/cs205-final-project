import numpy as np
from annealing_helper_functions import distance, changepath, simulated_annealing, serial_parallel_tempering
from parallelism import parallel_parallel_tempering
from timer import Timer
from xml_parse import parse_xml_graph
from multiprocessing import freeze_support
from matplotlib import pylab as plt

# Helper function to return the history of the lowest value found
def hist_best(history):
	mindist = history[0][0]
	dist_hist=[]
	for i in history:
		if i[0] < mindist:
			mindist = i[0]
		dist_hist.append(mindist)
	return dist_hist

if __name__ == '__main__':
	# Necessary to make multiprocessing work on Windows:
	freeze_support()

    # Load graph
	graph = parse_xml_graph('fri26.xml')
	
	#Square matrix
	assert graph.shape[0] == graph.shape[1]
	size = graph.shape[0]

	# Hardcoded best path to validate distance calculations, zero-indexed
	bestpath = np.asarray([x-1 for x in [1, 25, 24, 23, 26, 22, 21, 17, 18, 20, 19, 16, 11, 12, 13, 15, 14, 10, 9, 8, 7, 5, 6, 4, 3, 2]])
	optimum = distance(graph, bestpath)
	
	#Initial values for parallel tempering
	num_processes = 4
	ratio = np.sqrt(5) #Ratio of temperatures between processes
	iterr=1000000
	nswaps = 1
	nbefore = 480
	initial_temps = [ratio**i for i in range(num_processes)]

	#Initial values for simulated annealing
	initial_temp = initial_temps[num_processes-1] # As hot as the hottest parallel tempering process
	cool = 1./ratio                               # Cools at a rate equal to the ratio between the PT process temperatures
	reheat = initial_temps[0]                     # Reheats when it is as cold as the coldest PT process

	# Number of runs per method:
	runs = 2

	with Timer() as t:

		# Collect all the distances that are calculated in each run:
		distances = []
		hist_best_ppt = []
		hist_best_spt = []
		hist_best_sa  = []
		for i in range(runs):
			initial_Xs = [np.random.permutation(size) for a in range(num_processes)]

			solution_ppt, histories_ppt = parallel_parallel_tempering(graph, distance, initial_Xs, initial_temps, iterr, changepath, nswaps, nbefore)
			hist_best_ppt.append(hist_best(histories_ppt[0]))
			print 'ppt, ', i

			solution_spt, histories_spt = serial_parallel_tempering(graph, distance, initial_Xs, initial_temps, iterr, changepath, nswaps, nbefore)
			hist_best_spt.append(hist_best(histories_spt[0]))
			print 'spt, ', i

			solution_sa, history_sa = simulated_annealing(graph, distance, initial_Xs[0], initial_temps[0], nbefore, iterr, changepath, nswaps, reheat, cool)
			hist_best_sa.append(hist_best(history_sa))
			print 'sa , ', i

		hist_best_ppt = np.mean(hist_best_ppt, 0)
		np.save('hist_best_ppt_2_1.npy', hist_best_ppt)
		print 'saved ppt'

		hist_best_spt = np.mean(hist_best_spt, 0)
		np.save('hist_best_spt_2_1.npy', hist_best_spt)
		print 'saved spt'
		
		hist_best_sa  = np.mean(hist_best_sa, 0)
		np.save('hist_best_sa_2_1.npy' , hist_best_sa)
		print 'saved sa '

	print "Time: " + str(t.interval) + "\n"

