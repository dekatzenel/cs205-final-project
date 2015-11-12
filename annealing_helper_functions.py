import numpy as np

# Functions below adapted from ac290_tutorial2_simulated_annealing-student.ipynb

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

#Helper function for changepath
def swapindex(cities):
    indices = range(len(cities))
    # take two random indices to swap
    c1,c2 = np.random.choice(indices, 2, replace=False)
    
    # remember the cities to swap
    tmp1 = cities[c1]
    tmp2 = cities[c2]
    
    # do the actual swapping
    changedCities = cities.copy()
    changedCities[c1] = tmp2
    changedCities[c2] = tmp1    
    return changedCities

#Clever updating function for simulated annealing
def changepath(inputcities, n_swaps):
    cities = inputcities.copy()
    # Make n_swaps number of swaps
    for i in range(n_swaps):
        swappedCities = swapindex(cities)
        cities=swappedCities.copy()
    return cities

def simulated_annealing(graph, function, initial_X, initial_temp, cool, reanneal, iterr, swap_function, nswaps):
    
    accepted = 0
    X = initial_X.copy()
    T = initial_temp
    
    history = list()
    # Evaluate E
    prev_E = function(graph, X)
    history.append(prev_E)
    
    for i in xrange(iterr):
        # Stepsize
        L = np.sqrt(T)
        # Randomly update path
        X_star = swap_function(X, nswaps)
        # Evaluate E
        new_E = function(graph, X_star)
        delta_E = new_E - prev_E
        
        # Flip a coin
        U = np.random.uniform()
        if U < np.exp(-delta_E / T):
            accepted += 1
            history.append(new_E)
            # Copy X_star to X
            X = X_star.copy()
            prev_E = new_E

        # Check to cool down
        if accepted % reanneal == 0:
            T *= cool
            if T < 0.001: # Reheat
                T = 1.
            
    return X, history
