import numpy as np
import time

def prob(a, b):
    return np.exp(a / b)

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
        cities = swappedCities.copy()
    return cities

def anneal_once(graph, function, X, T, prev_E, history, swap_function, nswaps, accepted):
    ##### I added an 'accepted' variable that keeps track of how many paths have been accepted.

    # Randomly update path
    X_star = swap_function(X, nswaps)
    # Evaluate E
    new_E = function(graph, X_star)
    delta_E = new_E - prev_E
    
    # Flip a coin
    if np.random.uniform() < prob(-delta_E, T):
        # Copy X_star to X
        X = X_star.copy()
        ##### Increment 'accepted'
        accepted += 1
        prev_E = new_E

    # Maintain history
    ##### Keeping a history of the temperatures to observe cooling and reannealing
    ##### Also keeping a history of the current time to calculate elapsed time for each algorithm


    current_time = time.time()
    history.append([prev_E, X_star, T, current_time])  

    return X, prev_E, delta_E, history, accepted

def simulated_annealing(graph, function, initial_X, initial_temp, nbefore, iterr, 
                        swap_function, nswaps, reheat, cool):
    X = initial_X.copy()
    T = initial_temp

    ##### Number of paths that have been accepted
    accepted = 0
    # Dummy value
    best_path = []
    best_path_length = float('inf')
    
    history = list()
 
    # Evaluate E
    prev_E = function(graph, X)

    #### Starting time
    current_time = time.time()

    history.append([prev_E, X, T, current_time])
    
    for i in range(iterr):
        X, prev_E, delta_E, history, accepted = anneal_once(graph, function, X, T, prev_E, history, swap_function, nswaps, accepted)            

        # Store best path
        newest_distance = distance(graph, X)
        if newest_distance < best_path_length:
            best_path = X
            best_path_length = newest_distance

        ##### Putting reannealing back in
        if i % nbefore == 0:        ##### At the reannealing interval:
            T *= cool               ##### Cool the function down to zero in on a minimum
            if T < reheat:          ##### Re-heat to get out of the local minimum
                T = initial_temp

    return best_path, history

# Adapted from Lecture14_Parallel_Tempering_and_Emcee.ipynb
def serial_parallel_tempering(graph, function, initial_Xs, initial_temps, 
                              iterr, swap_function, nswaps, nbefore):
    # Make sure inputs are ok
    assert(len(initial_temps) == len(initial_Xs)), "Mismatched input dimensions"
    assert(initial_temps[0] == 1), "First temperature should be one"

    # Initialize stuff
    nsystems = len(initial_temps)
    Xs = list(initial_Xs)
    Ts = initial_temps
    prev_Es = [function(graph, Xs[i]) for i in range(nsystems)]
    delta_Es = [0] * nsystems
    history = [[] for i in xrange(nsystems)]
    best_path = []
    best_path_length = float('inf')

    ###### Current time
    current_time = time.time()


    for i in xrange(nsystems):
        history[i].append((prev_Es[i], initial_Xs[i], Ts[i], current_time))

    for step in range(iterr):
        for i in range(nsystems):
            # Run nbefore steps of simulated annealing
            Xs[i], prev_Es[i], delta_Es[i], history[i], a = anneal_once(graph, function, Xs[i], Ts[i], 
                                                        prev_Es[i], history[i], 
                                                        swap_function, nswaps, 0)
            # Store best path
            newest_distance = distance(graph, Xs[i])
            if newest_distance < best_path_length:
                best_path = Xs[i]
                best_path_length = newest_distance

        # Decide which chains, if any, to exchange
        if step % nbefore == 0:
            for i in range(nsystems - 1, 0, -1):
                # Acceptance probability
                A = np.exp(min(np.log(1), ((delta_Es[i] - delta_Es[i-1])/Ts[i]) +
                                  ((delta_Es[i-1] - delta_Es[i])/Ts[i-1])))
                if np.random.uniform() < A:
                    # Exchange most recent updates and paths
                    prev_Es[i], prev_Es[i-1] = prev_Es[i-1], prev_Es[i]
                    Xs[i], Xs[i-1] = Xs[i-1], Xs[i]

    return best_path, history