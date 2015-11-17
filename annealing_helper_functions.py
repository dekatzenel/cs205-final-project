import numpy as np
import math

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

def simulated_annealing(graph, function, initial_X, initial_temp, cool,
                        reanneal, iterr, swap_function, nswaps):
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

def prob(a, b):
    return np.exp(a / b)

# Adapted from Lecture14_Parallel_Tempering_and_Emcee.ipynb
def parallel_tempering(graph, function, initial_Xs, initial_temps, 
                       iterr, swap_function, nswaps, nbefore):
    # Make sure inputs are ok
    assert(len(initial_temps) == len(initial_Xs)), "Mismatched input dimensions"
    assert(initial_temps[0] == 1), "First temperature should be one"

    # Initialize stuff
    nsystems = len(initial_temps)
    Xs = initial_Xs
    Ts = initial_temps
    P = [lambda d: np.exp(d / Ts[c]) for c in range(nsystems)]
    prev_Es = [function(graph, Xs[i]) for i in range(nsystems)]
    history = [[] for i in xrange(nsystems)]

    for c in xrange(nsystems):
        history[c].append(prev_Es[c])

    for step in range(iterr):
        # Run nbefore steps of simulated annealing
        X_stars = [swap_function(Xs[i], nswaps) for i in xrange(nsystems)]
        new_Es = [function(graph, X_stars[i]) for i in xrange(nsystems)]
        delta_Es = [i - j for i, j in zip(new_Es, prev_Es)]
        
        # Do a normal update
        for c in range(nsystems):
            if np.random.uniform() < P[c](-delta_Es[c]):
                history[c].append(new_Es[c])
                Xs[c] = X_stars[c]
                prev_Es[c] = new_Es[c]

        # Decide which chains, if any, to exchange
        if step % nbefore == 0:
            for c in range(nsystems - 1):
                # Acceptance probability
                A = min(1, np.exp(((delta_Es[c] - delta_Es[c+1])/Ts[c]) +
                                  ((delta_Es[c+1] - delta_Es[c])/Ts[c+1])))

                if np.random.uniform() < A:
                    # Exchange most recent updates and paths
                    prev = prev_Es[c]
                    prev_Es[c] = prev_Es[c+1]
                    prev_Es[c+1] = prev
                    prev = Xs[c]
                    Xs[c] = Xs[c+1]
                    Xs[c+1] = prev

    return Xs[0], history[0]