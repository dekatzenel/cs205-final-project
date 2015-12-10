import numpy as np
import matplotlib.pyplot as plt
from annealing_helper_functions import distance
from xml_parse import parse_xml_graph

#### This function is a wrapper used to plot data that was created in multiple runs to compare performance.  

graph = parse_xml_graph('fri26.xml')
bestpath = np.asarray([x-1 for x in [1, 25, 24, 23, 26, 22, 21, 17, 18, 20, 19, 16, 11, 12, 13, 15, 14, 10, 9, 8, 7, 5, 6, 4, 3, 2]])
optimum = distance(graph, bestpath)

time_hist_ppt = np.load('time_hist_ppt.npy')
time_hist_spt = np.load('time_hist_spt.npy')
time_hist_sa  = np.load('time_hist_sa.npy')

dist_hist_ppt = np.load('dist_hist_ppt.npy')
dist_hist_spt = np.load('dist_hist_spt.npy')
dist_hist_sa  = np.load('dist_hist_sa.npy')

plt.plot(time_hist_ppt, dist_hist_ppt, color='b', label = "Parallel Parallel")
plt.plot(time_hist_spt, dist_hist_spt, color='g', label = "Serial Parallel")
plt.plot(time_hist_sa , dist_hist_sa,  color='r', label = "Simulated Annealing"

plt.xlim([0, np.min([np.max(time_hist_sa), np.max(time_hist_spt), np.max(time_hist_ppt)])])
plt.ylim([optimum - 50, dist_hist_ppt[0]])

axis_font = {'fontname':'Arial', 'size':30}

plt.yscale('log', **axis_font)
plt.axhline(optimum, color = 'm', label = "True Optimum")
plt.legend(loc = 'best', prop = {'size': 20})
plt.title('Convergence Comparison (Average of 25 runs)', **axis_font)
plt.ylabel('Distance (log scale)', **axis_font)
plt.xlabel('Elapsed time (seconds)', **axis_font)

plt.show()
