import numpy as np
import time


"""
Calculates the exponential of the quotient of two numbers
Used in anneal_once()
Arguments: 
    a - dividend
    b - divisor
Returns:
    e^(a/b)
"""
def prob(a, b):
    return np.exp(a / b)


###############################################################################
# Functions below adapted from:
# ac290_tutorial2_simulated_annealing-student.ipynb
###############################################################################

"""
Calculates the total distance to traverse a sequence of cities
Comparison metric used for routes in the Traveling Salesman Problem
Arguments:
    graph - a 2D numpy array where graph[A,B] is the distance from city A to
            city B
    citypath - a list/1D array of city numeric indices that correspond to the
               indices of the graph
Returns:
    Sum of the distances between cities along the path
"""
def distance(graph, citypath):
    distance = 0
    number_of_cities = len(citypath)
    
    # loop over all cities
    for j in xrange(number_of_cities):
        if j == (number_of_cities - 1): # FINAL POINT CONNECTS WITH FIRST ONE
            distance += graph[citypath[j], citypath[0]]
        else:
            distance += graph[citypath[j], citypath[j+1]]
    return distance


"""
Randomly selects 2 indices in a 1D array and swaps their contents
Used in changepath()
Arguments:
    cities - ordered 1D array of city index numbers
Returns:
    reordered path
"""
def swapindex(cities):
    indices = range(len(cities))
    # take two random indices to swap
    c1,c2 = np.random.choice(indices, 2, replace=False)
    
    # do the actual swapping on a new copy of the cities
    changedCities = cities.copy()
    changedCities[c1] = cities[c2]
    changedCities[c2] = cities[c1]    
    return changedCities


"""
Performs swaps as part of update step for both simulated annealing and parallel
    tempering
Used in anneal_once() as swap_function
Arguments:
    inputcities - ordered 1D array of city index numbers
    nswaps - number of sequential swaps to perform per update
Returns:
    reordered path after all swaps
"""
def changepath(inputcities, nswaps):
    cities = inputcities.copy()
    # Make n_swaps number of swaps
    for i in range(nswaps):
        swappedCities = swapindex(cities)
        cities = swappedCities.copy()
    return cities


"""
Performs one base step of simulated annealing/parallel tempering
Used in simulated_annealing(), serial_parallel_tempering(), and
    parallel_parallel_tempering()
Arguments:
    graph - a 2D numpy array where graph[A,B] is the distance from city A to
            city B
    function - a function that takes in values for graph and X_star and returns
               an energy (E) value. ex: distance()
    X - current ordered path
    T - current system temperature, affects probability of update
    prev_E - energy of the prior value of X
    history - record of all steps taken thus far in calling function
    swap_function - a function that takes in values for X and nswaps and
                    returns a new ordering of X. ex: changepath()
    nswaps - number of swaps to perform when calculating updated path
Returns:
    post-processing values of X, E, delta_E, and history
"""
def anneal_once(graph, function, X, T, prev_E, history, swap_function, nswaps,
                accepted=0):

    # Randomly calculate updated path
    X_star = swap_function(X, nswaps)
    # Evaluate E for calculated updated path
    new_E = function(graph, X_star)
    delta_E = new_E - prev_E
    
    # Flip a coin to determine if E and X should update to calculated values
    if np.random.uniform() < prob(-delta_E, T):
        X = X_star.copy()
        ##### Increment 'accepted'
        accepted += 1
        prev_E = new_E

    # Maintain history - distance, path, temp, time
    current_time = time.time()
    history.append([prev_E, X_star, T, current_time])  

    return X, prev_E, delta_E, history, accepted


"""
Runs simulated annealing for given inputs
Called directly by controller/comparison files
Arguments:
    graph - a 2D numpy array where graph[A,B] is the distance from city A to
            city B
    function - a function that takes in values for graph and X_star and returns
               an energy (E) value. ex: distance()
    initial_X - initial ordered path
    initial_temp - initial system temperature, affects probability of update
    nbefore - !!!!!NOT CURRENTLY USED!!!!!
    cool - !!!!!NOT CURRENTLY USED!!!!!
    iterr - number of iterations to perform of simulated annealing algorithm
    swap_function - a function that takes in values for X and nswaps and
                    returns a new ordering of X. ex: changepath()
    nswaps - number of swaps to perform when calculating updated path
Returns:
    -value of X with minimum associated value of E
    -history of E and X values
"""
def simulated_annealing(graph, function, initial_X, initial_temp, nbefore, iterr, 
                        swap_function, nswaps, reheat, cool):
    X = initial_X.copy()
    T = initial_temp

    ##### Number of paths that have been accepted
    accepted = 0
    # Dummy value
    best_path = []
    best_path_value = float('inf')
    
    history = list()
 
    # Evaluate E
    prev_E = function(graph, X)

    #### Starting time
    current_time = time.time()

    history.append([prev_E, X, T, current_time])
    
    for i in range(iterr):
        X, prev_E, delta_E, history, accepted = anneal_once(graph, function, X,
                                                            T, prev_E, history,
                                                            swap_function,
                                                            nswaps, accepted)            

        # Store best path
        if prev_E < best_path_value:
            best_path = X
            best_path_value = prev_E

        # Reanneal
        if i % nbefore == 0:        ##### At the reannealing interval:
            T *= cool               ##### Cool the function down to zero in on a minimum
            if T < reheat:          ##### Re-heat to get out of the local minimum
                T = initial_temp

    return best_path, history