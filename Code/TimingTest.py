import numpy as np
from annealing_helper_functions import distance, changepath, simulated_annealing
from parallel_tempering import parallel_parallel_tempering, serial_parallel_tempering
from timer import Timer
from xml_parse import parse_xml_graph
from multiprocessing import freeze_support
from matplotlib import pylab as plt

# Helper function to return the history of the lowest value found and the elapsed time at that point
def hist_best(history):
	# History as stored as a list of lists: [current distance, current path, temperature, current time]

	# Starting points to calculate the shortest path found and elapsed time at each step
	mindist = history[0][0]
	starttime = history[0][3]

	dist_hist=[]
	time_hist=[]

    # Note: because of the way history is stored, this can not be converted to an array and done with 
    #    a vector operation.  This is because history is a list of lists that is appended to at each 
    #    iteration, and the current path is a list within the list of lists.  
	for i in history:
		if i[0] < mindist:
			mindist = i[0] # Update lowest value in history
		dist_hist.append(mindist)

		time_hist.append(i[3] - starttime) # Update elapsed time

	return dist_hist, time_hist

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
	iterr=50000
	nswaps = 1
	nbefore = 480
	initial_temps = [ratio**i for i in range(num_processes)]

	#Initial values for simulated annealing
	initial_temp = initial_temps[num_processes-1] # As hot as the hottest parallel tempering process
	cool = 1./ratio                               # Cools at a rate equal to the ratio between the PT process temperatures
	reheat = initial_temps[0]                     # Reheats when it is as cold as the coldest PT process

	# Number of runs per method:
	runs = 25

	with Timer() as t:
		# Collect all the distances that are calculated in each run:

		time_hist_ppt = []
		dist_hist_ppt = []

		time_hist_spt = []
		dist_hist_spt = []
		
		time_hist_sa  = []
		dist_hist_sa  = []

		for i in range(runs):
			# Use the same initial paths for all algorithms
			initial_Xs = [np.random.permutation(size) for a in range(num_processes)]

			#Run each algorithm using the specified parameters, take their best values and elapsed times throughout the algorithm,
			#    and append these to a list for each.  
			solution_ppt, histories_ppt = parallel_parallel_tempering(graph, distance, initial_Xs, initial_temps, iterr, changepath, nswaps, nbefore)
			best_hist, time_hist = hist_best(histories_ppt[0])
			time_hist_ppt.append(time_hist)
			dist_hist_ppt.append(best_hist)

			print 'Parallel Parallel Tempering, run ', i, ' complete.'

			solution_spt, histories_spt = serial_parallel_tempering(graph, distance, initial_Xs, initial_temps, iterr, changepath, nswaps, nbefore)
			best_hist, time_hist = hist_best(histories_spt[0])
			time_hist_spt.append(time_hist)
			dist_hist_spt.append(best_hist)
			
			print 'Serial Parallel Tempering, run ', i, ' complete.'

			solution_sa, history_sa = simulated_annealing(graph, distance, initial_Xs[0], initial_temps[0], nbefore, iterr, changepath, nswaps, reheat, cool)
			best_hist, time_hist = hist_best(history_sa)
			time_hist_sa.append(time_hist)
			dist_hist_sa.append(best_hist)

			print 'Simulated Annealing, run ', i, ' complete.'

		# Take the mean of each column, save these outputs so they can be plotted and examined without re-running simulations
		dist_hist_ppt = np.mean(dist_hist_ppt, 0)
		time_hist_ppt = np.mean(time_hist_ppt, 0)
		# Save results to plot in plotter.py
		np.save('./SavedResults/time_hist_ppt.npy', time_hist_ppt)
		np.save('./SavedResults/dist_hist_ppt.npy', dist_hist_ppt)

		dist_hist_spt = np.mean(dist_hist_spt, 0)
		time_hist_spt = np.mean(time_hist_spt, 0)
		np.save('./SavedResults/time_hist_spt.npy', time_hist_spt)
		np.save('./SavedResults/dist_hist_spt.npy', dist_hist_spt)
		
		dist_hist_sa  = np.mean(dist_hist_sa, 0)
		time_hist_sa  = np.mean(time_hist_sa, 0)
		np.save('./SavedResults/time_hist_sa.npy', time_hist_sa)
		np.save('./SavedResults/dist_hist_sa.npy', dist_hist_sa)
		
	print "Time: " + str(t.interval) + "\n"

