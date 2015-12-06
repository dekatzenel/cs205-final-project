import numpy as np
import matplotlib.pyplot as plt
from annealing_helper_functions import distance
from xml_parse import parse_xml_graph

graph = parse_xml_graph('fri26.xml')
bestpath = np.asarray([x-1 for x in [1, 25, 24, 23, 26, 22, 21, 17, 18, 20, 19, 16, 11, 12, 13, 15, 14, 10, 9, 8, 7, 5, 6, 4, 3, 2]])
optimum = distance(graph, bestpath)

hist_best_ppt_1 = np.load('hist_best_ppt_1.npy')
hist_best_spt_1 = np.load('hist_best_spt_1.npy')
hist_best_sa_1  = np.load('hist_best_sa_1.npy')


hist_best_ppt_5 = np.load('hist_best_ppt_5.npy')
hist_best_spt_5 = np.load('hist_best_spt_5.npy')
hist_best_sa_5  = np.load('hist_best_sa_5.npy')


hist_best_ppt_2_1 = np.load('hist_best_ppt_2_1.npy')
hist_best_spt_2_1 = np.load('hist_best_spt_2_1.npy')
hist_best_sa_2_1  = np.load('hist_best_sa_2_1.npy')

# hist_best_ppt = np.zeros_like(hist_best_ppt_1)
# hist_best_spt = np.zeros_like(hist_best_spt_1)
# hist_best_sa  = np.zeros_like(hist_best_sa_1)

hist_best_ppt = (hist_best_ppt_1 + 5*hist_best_ppt_5 + 2*hist_best_ppt_2_1)/8.
hist_best_spt = (hist_best_spt_1 + 5*hist_best_spt_5 + 2*hist_best_spt_2_1)/8.
hist_best_sa  = (hist_best_sa_1  + 5*hist_best_sa_5) + 2*hist_best_sa_2_1/8.

plt.plot(hist_best_ppt, color='b', label = "Parallel Parallel")
plt.plot(hist_best_spt, color='g', label = "Serial Parallel")
plt.plot(hist_best_sa,  color='r', label = "Simulated Annealing")

plt.ylim([optimum - 50 ,hist_best_ppt[1]])
plt.xscale('log')
plt.yscale('log')
plt.axhline(optimum, color = 'm', label = "True Optimum")
plt.legend(loc = 'best')
plt.title('Convergence Comparison (Average of 30 runs)')
plt.ylabel('Distance (log scale)')
plt.xlabel('Iterations')
plt.show()
