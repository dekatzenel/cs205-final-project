import numpy as np

#Assumes citypath is a list/1D array of city numeric indices
def distance(graph, citypath):
    distance = 0
    number_of_cities = len(citypath)
    
    # loop over all cities
    for j in xrange(number_of_cities):
        if j == (number_of_cities - 1): # FINAL POINT CONNECTS WITH THE FIRST ONE
            distance += graph[citypath[j], citypath[0]]
        else:
            distance += graph[citypath[j], citypath[j+1]]
    return distance

# Functions below taken from ac290_tutorial2_simulated_annealing-student.ipynb without change

#Helper function for changepath
def swapindex(cities):
    indices = range(len(cities))
    # take two random indices to swap
    c1,c2 = np.random.choice(indices, 2, replace=False)
    
    # remember the cities to swap
    tmp1 = cities[c1,:]
    tmp2 = cities[c2,:]
    
    # do the actual swapping
    changedCities = cities.copy()
    changedCities[c1,:] = tmp2
    changedCities[c2,:] = tmp1    
    return changedCities

#Clever updating function for simulated annealing
def changepath(inputcities, n_swaps):
    cities = inputcities.copy()
    # Make n_swaps number of swaps
    for i in range(n_swaps):
        swappedCities = swapindex(cities)
        cities=swappedCities.copy()
    return cities
