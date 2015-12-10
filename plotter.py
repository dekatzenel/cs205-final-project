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

plt.plot(time_hist_ppt, dist_hist_ppt, color='b', label = "Parallel Parallel")
plt.plot(time_hist_spt, dist_hist_spt, color='g', label = "Serial Parallel")
plt.plot(time_hist_sa , dist_hist_sa,  color='r', label = "Simulated Annealing")

# plt.xlim([0,np.min(np.max(time_hist_sa), np.max(time_hist_spt), np.max(time_hist_ppt))])
plt.ylim([optimum - 50 ,dist_hist_ppt[0]])
# plt.xscale('log')

axis_font = {'fontname':'Arial', 'size':30}

plt.yscale('log', **axis_font)
plt.axhline(optimum, color = 'm', label = "True Optimum")
plt.legend(loc = 'best', prop = {'size': 20})
plt.title('Convergence Comparison (Average of 25 runs of 50,000 iterations)', **axis_font)
plt.ylabel('Distance (log scale)', **axis_font)

plt.xlabel('Elapsed Time', **axis_font)
plt.show()

# plt.plot(hist_best_ppt[:50000], color='b', label = "Parallel Parallel")
# plt.plot(hist_best_spt[:50000], color='g', label = "Serial Parallel")
# plt.plot(hist_best_sa[:200000][0::4],  color='r', label = "Simulated Annealing")

# plt.xlim([0,50000])
# plt.ylim([optimum - 50 ,hist_best_ppt[0]])
# # plt.xscale('log')

# axis_font = {'fontname':'Arial', 'size':30}

# plt.yscale('log', **axis_font)
# plt.axhline(optimum, color = 'm', label = "True Optimum")
# plt.legend(loc = 'best', prop = {'size': 20})
# plt.title('Convergence Comparison (Average of 25 runs)', **axis_font)
# plt.ylabel('Distance (log scale)', **axis_font)

# plt.xlabel('Total Number of Computations', **axis_font)
# plt.show()


# np.save('hist_best_ppt.npy', hist_best_ppt)
# np.save('hist_best_spt.npy', hist_best_spt)
# np.save('hist_best_sa.npy',  hist_best_sa)




# hist_best_ppt_20 = np.load('hist_best_ppt_20.npy')
# hist_best_spt_20 = np.load('hist_best_spt_20.npy')
# hist_best_sa_20  = np.load('hist_best_sa_20.npy')

# hist_ppt_5_3 = np.load('hist_best_ppt_5_3.npy')
# hist_spt_5_3 = np.load('hist_best_spt_5_3.npy')
# hist_sa_5_3  = np.load('hist_best_sa_5_3.npy')

# hist_best_ppt = (hist_ppt_5_3 + 5*hist_best_ppt_20)/6.
# hist_best_spt = (hist_spt_5_3 + 5*hist_best_spt_20)/6.
# hist_best_sa  = (hist_sa_5_3  + 5*hist_best_sa_20)/6.


# hist_best_ppt_5_1 = np.load('hist_best_ppt_5_1.npy')
# hist_best_spt_5_1 = np.load('hist_best_spt_5_1.npy')
# hist_best_sa_5_1  = np.load('hist_best_sa_5_1.npy')

# hist_best_ppt_5_2 = np.load('hist_best_ppt_5_2.npy')
# hist_best_spt_5_2 = np.load('hist_best_spt_5_2.npy')
# hist_best_sa_5_2  = np.load('hist_best_sa_5_2.npy')

# hist_best_ppt_1_1 = np.load('hist_best_ppt_1_1.npy')
# hist_best_spt_1_1 = np.load('hist_best_spt_1_1.npy')
# hist_best_sa_1_1  = np.load('hist_best_sa_1_1.npy')

# hist_best_ppt_1_2 = np.load('hist_best_ppt_1_2.npy')
# hist_best_spt_1_2 = np.load('hist_best_spt_1_2.npy')
# hist_best_sa_1_2  = np.load('hist_best_sa_1_2.npy')

# hist_best_ppt_1_3 = np.load('hist_best_ppt_1_3.npy')
# hist_best_spt_1_3 = np.load('hist_best_spt_1_3.npy')
# hist_best_sa_1_3  = np.load('hist_best_sa_1_3.npy')

# hist_best_ppt_1_4 = np.load('hist_best_ppt_1_4.npy')
# hist_best_spt_1_4 = np.load('hist_best_spt_1_4.npy')
# hist_best_sa_1_4  = np.load('hist_best_sa_1_4.npy')

# hist_best_ppt_1_5 = np.load('hist_best_ppt_1_5.npy')
# hist_best_spt_1_5 = np.load('hist_best_spt_1_5.npy')
# hist_best_sa_1_5  = np.load('hist_best_sa_1_5.npy')

# hist_best_ppt_1_6 = np.load('hist_best_ppt_1_6.npy')
# hist_best_spt_1_6 = np.load('hist_best_spt_1_6.npy')
# hist_best_sa_1_6  = np.load('hist_best_sa_1_6.npy')

# hist_best_ppt_2_1 = np.load('hist_best_ppt_2_1.npy')
# hist_best_spt_2_1 = np.load('hist_best_spt_2_1.npy')
# hist_best_sa_2_1  = np.load('hist_best_sa_2_1.npy')

# hist_best_ppt_2_2 = np.load('hist_best_ppt_2_2.npy')
# hist_best_spt_2_2 = np.load('hist_best_spt_2_2.npy')
# hist_best_sa_2_2  = np.load('hist_best_sa_2_2.npy')

# hist_best_ppt = (5*hist_best_ppt_5_1 + 5*hist_best_ppt_5_2 + hist_best_ppt_1_1 + hist_best_ppt_1_2 + hist_best_ppt_1_3 + hist_best_ppt_1_4 + 
# 	hist_best_ppt_1_5 + hist_best_ppt_1_6 + 2*hist_best_ppt_2_1 + 2*hist_best_ppt_2_2)/20.

# hist_best_spt = (5*hist_best_spt_5_1 + 5*hist_best_spt_5_2 + hist_best_spt_1_1 + hist_best_spt_1_2 + hist_best_spt_1_3 + hist_best_spt_1_4 + 
# 	hist_best_spt_1_5 + hist_best_spt_1_6 + 2*hist_best_ppt_2_1 + 2*hist_best_ppt_2_2)/20.

# hist_best_sa  = (5*hist_best_sa_5_1  + 5*hist_best_sa_5_2  + hist_best_sa_1_1  + hist_best_sa_1_2  + hist_best_sa_1_3  + hist_best_sa_1_4  + 
# 	hist_best_sa_1_5 +  hist_best_sa_1_6 +  2*hist_best_sa_2_1 +  2*hist_best_sa_2_2)/20.
