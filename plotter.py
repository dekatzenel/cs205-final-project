import numpy as np
import matplotlib.pyplot as plt
from annealing_helper_functions import distance
from xml_parse import parse_xml_graph

graph = parse_xml_graph('fri26.xml')
bestpath = np.asarray([x-1 for x in [1, 25, 24, 23, 26, 22, 21, 17, 18, 20, 19, 16, 11, 12, 13, 15, 14, 10, 9, 8, 7, 5, 6, 4, 3, 2]])
optimum = distance(graph, bestpath)

time_hist_ppt = np.load('time_hist_ppt.npy')
time_hist_spt = np.load('time_hist_spt.npy')
time_hist_sa  = np.load('time_hist_sa.npy')

dist_hist_ppt = np.load('dist_hist_ppt.npy')
dist_hist_spt = np.load('dist_hist_spt.npy')
dist_hist_sa  = np.load('dist_hist_sa.npy')

# plt.plot(time_hist_ppt, dist_hist_ppt, color='b', label = "Parallel Parallel")
# plt.plot(time_hist_spt, dist_hist_spt, color='g', label = "Serial Parallel")
# plt.plot(time_hist_sa , dist_hist_sa,  color='r', label = "Simulated Annealing")

# plt.plot(time_hist_ppt[0:50000], range(0, 200000, 4), color='b', label = "Parallel Parallel")
# plt.plot(time_hist_spt[0:50000], range(0, 200000, 4), color='g', label = "Serial Parallel")
# plt.plot(time_hist_sa[0:200000][0::4], range(0, 200000, 4),  color='r', label = "Simulated Annealing")


# plt.xlim([0,4]) #np.min([np.max(time_hist_sa), np.max(time_hist_spt), np.max(time_hist_ppt)])])
# plt.ylim([optimum - 50, dist_hist_ppt[0]])

axis_font = {'fontname':'Arial', 'size':30}

# plt.yscale('log', **axis_font)
# # plt.axhline(optimum, color = 'm', label = "True Optimum")
# plt.legend(loc = 'best', prop = {'size': 20})
# # plt.title('Convergence Comparison (Average of 25 runs), Between 0 and 4 seconds of Run Time', **axis_font)
# plt.title('Elapsed Time versus Computation', **axis_font)
# # plt.ylabel('Distance (log scale)', **axis_font)
# plt.xlabel('Elapsed time (seconds)', **axis_font)
# plt.ylabel('Total Computations', **axis_font)
# plt.xlabel('Elapsed Time (seconds)', **axis_font)
# plt.xticks(range(0,5))

# plt.bar(range(3), [, , ], width=0.6)

rate_sa = 1000./(time_hist_sa[1001]-time_hist_sa[1])
rate_spt= 4000./(time_hist_spt[1001]-time_hist_spt[1])
rate_ppt= 4000./(time_hist_ppt[1010]-time_hist_ppt[10])

rects1 = plt.bar(1, rate_sa, color = 'r', label = "SA")
rects2 = plt.bar(2, rate_spt, color = 'g', label = "SPT")
rects3 = plt.bar(3, rate_ppt, color = 'b', label = "PPT")
plt.legend(loc='best', prop = {'size': 20})
plt.xlim([0.8,4])
plt.xticks([])
plt.ylabel('Speed: Computations per second', **axis_font)
plt.title('Computation Speed', **axis_font)
# plt.xlim([-0.5,3])
# plt.xticks(np.arange(3)+0.6, ['SA', 'SPT', 'PPT'])
plt.show()
