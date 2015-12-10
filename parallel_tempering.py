import numpy as np

from multiprocessing import Process, Queue, Pipe
from annealing_helper_functions import anneal_once

###############################################################################
# Functions below adapted from Lecture14_Parallel_Tempering_and_Emcee.ipynb
###############################################################################


"""
Runs parallel tempering ***in serial*** for given inputs
Called directly by controller/comparison files
Arguments:
    graph - a 2D numpy array where graph[A,B] is the distance from city A to
            city B
    function - a function that takes in values for graph and X_star and returns
               an energy (E) value. ex: distance()
    initial_Xs - initial ordered paths, one for each "system"
    initial_temps - initial system temperatures, one for each "system", affect
                    probability of update
    iterr - number of iterations to perform for each system of parallel 
            tempering algorithm
    swap_function - a function that takes in values for X and nswaps and
                    returns a new ordering of X. ex: changepath()
    nswaps - number of swaps to perform when calculating updated path
    nbefore - number of iterations prior to checking if systems should swap
              values
Returns:
    -value of X with minimum associated value of E across all systems
    -each system's history of E and X values
"""
def serial_parallel_tempering(graph, function, initial_Xs, initial_temps, 
                              iterr, swap_function, nswaps, nbefore):
    # Make sure inputs are as expected
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
    best_path_value = float('inf')

    for i in xrange(nsystems):
        history[i].append((prev_Es[i], initial_Xs[i]))

    for step in range(iterr):
        for i in range(nsystems):
            # Run nbefore steps of simulated annealing
            Xs[i], prev_Es[i], delta_Es[i], history[i] = anneal_once(graph,
                                                        function, Xs[i], Ts[i], 
                                                        prev_Es[i], history[i], 
                                                        swap_function, nswaps)
            # Store best path
            if prev_Es[i] < best_path_value:
                best_path = Xs[i]
                best_path_value = prev_Es[i]

        # Decide which chains, if any, to exchange
        if step % nbefore == 0:
            for i in range(nsystems - 1, 0, -1):
                # Acceptance probability
                # 0 = ln(1)                
                A = np.exp(min(0, ((delta_Es[i] - delta_Es[i-1])/Ts[i]) +
                              ((delta_Es[i-1] - delta_Es[i])/Ts[i-1])))
                if np.random.uniform() < A:
                    # Exchange most recent updates and paths
                    prev_Es[i], prev_Es[i-1] = prev_Es[i-1], prev_Es[i]
                    Xs[i], Xs[i-1] = Xs[i-1], Xs[i]

    return best_path, history


"""
Function run by each process generated in parallel_parallel_tempering()
Arguments:
    graph - a 2D numpy array where graph[A,B] is the distance from city A to
            city B
    function - a function that takes in values for graph and X_star and returns
               an energy (E) value. ex: distance()
    X - initial ordered path
    T - initial system temperature, affects probability of update
    prev_E - initial energy
    history - empty list to serve as record of all steps taken in process
    swap_function - a function that takes in values for X and nswaps and
                    returns a new ordering of X. ex: changepath()
    nswaps - number of swaps to perform when calculating updated path
    nbefore - number of iterations prior to checking if processes should swap
              values
    process_number - index value of current process
    process_count - total number of processes created by the calling function
    queues_A - queues to use for calculating A. 1 queue per process in
               process_count
    pipes_swap - pipes to use for swapping values between processes. For
                 process_number > 0, the last pipe communicates with the prior
                 process_number. For process_number < max, the first pipe
                 communicates with the subsequent process.
    send_ret_val - pipe to use for sending final results to calling process
No return value
"""
def parallel_tempering(graph, function, X, T, iterr, prev_E, history,
                       swap_function, nswaps, nbefore, process_number,
                       process_count, queues_A, pipes_swap, send_ret_val):
    best_path = []
    best_path_value = float('inf')

    for step in range(iterr):
        # Run nbefore steps of simulated annealing
        X, prev_E, delta_E, history = anneal_once(graph, function, X, T,
                                                  prev_E, history,
                                                  swap_function, nswaps)
        if prev_E < best_path_value:
            best_path = X
            best_path_value = prev_E

        # Decide which chains, if any, to exchange
        if step % nbefore == 0:
            #Each process can swap with prior processes
            if process_number < process_count - 1:
                queues_A[process_number].put(delta_E)
                queues_A[process_number].put(T)
            # Acceptance probability
            if process_number > 0:
                next_delta_E = queues_A[process_number - 1].get()
                next_T = queues_A[process_number - 1].get()
                #0 = ln(1)                
                A = np.exp(min(0, ((delta_E - next_delta_E)/T) +
                                  ((next_delta_E - delta_E)/next_T)))

            #Finish any started swap before going to next one
            if process_number < process_count - 1:
                #Check if need to swap with subsequent process
                swap_bool = pipes_swap[0].recv()
                if swap_bool:
                    #If so, publish info then retrieve info
                    pipes_swap[0].send([prev_E, X])
                    prev_E, X = pipes_swap[0].recv()

            #Only initiate swap from higher-indexed process, i.e. not first process
            if process_number > 0:
                if np.random.uniform() < A:
                    #Swap is happening
                    pipes_swap[-1].send(True)
                    #Send info to next process, then retrieve info
                    pipes_swap[-1].send([prev_E, X])
                    prev_E, X = pipes_swap[-1].recv()
                else:
                    #No swap necessary
                    pipes_swap[-1].send(False)

    send_ret_val.send([best_path, history])
    return


"""
Runs parallel tempering ***in parallel*** for given inputs
Called directly by controller/comparison files
Arguments:
    graph - a 2D numpy array where graph[A,B] is the distance from city A to
            city B
    function - a function that takes in values for graph and X_star and returns
               an energy (E) value. ex: distance()
    initial_Xs - initial ordered paths, one for each process
    initial_temps - initial system temperatures, one for each process, affect
                    probability of update
    iterr - number of iterations to perform for each process running parallel 
            tempering algorithm
    swap_function - a function that takes in values for X and nswaps and
                    returns a new ordering of X. ex: changepath()
    nswaps - number of swaps to perform when calculating updated path
    nbefore - number of iterations prior to checking if processes should swap
              values
Returns:
    -value of X with minimum associated value of E across all processes
    -each process's history of E and X values
"""
def parallel_parallel_tempering(graph, function, initial_Xs, initial_temps, 
                                iterr, swap_function, nswaps, nbefore):
    # Make sure inputs are ok
    assert(len(initial_temps) == len(initial_Xs)), "Mismatched input dimensions"
    assert(initial_temps[0] == 1), "First temperature should be one"

    # Initialize stuff
    nsystems = len(initial_temps)
    Xs = list(initial_Xs)
    Ts = initial_temps
    prev_Es = [function(graph, Xs[i]) for i in range(nsystems)]
    history = [[] for i in xrange(nsystems)]
    processes = []
    queues_A = []
    prev_conn = None
    pipes_swap = []
    send_ret_vals = []
    recv_ret_vals = []
    best_paths = []
    final_histories = []

    # -Initialize history
    # -Assemble communication pipes between current process and to-be-generated
    # processes    
    # -Assemble queues_A and pipes_swap in reverse order, then reverse them
    # -Each swap_pipes has a connection to the subsequent process as its first
    # entry and a connection to the prior system as its last entry (except for
    # final process and first process, respectively)
    for i in xrange(nsystems - 1, -1, -1):
        swap_pipes = []
        history[i].append((prev_Es[i], Xs[i]))
        send_ret_val, recv_ret_val = Pipe()
        send_ret_vals.append(send_ret_val)
        recv_ret_vals.append(recv_ret_val)
        q1 = Queue()
        queues_A.append(q1)
        if i < nsystems - 1:
            #Grab the last process's c2
            swap_pipes.append(prev_conn)
        #Generate one pipe per swap
        if i > 0:
            c1,c2 = Pipe()
            #Keep c1
            swap_pipes.append(c1)
            prev_conn = c2
        pipes_swap.append(swap_pipes)        
    queues_A.reverse()
    pipes_swap.reverse()

    for i in range(nsystems):
        p = Process(target=parallel_tempering, args=(graph, function, Xs[i],
                                                     Ts[i], iterr, prev_Es[i],
                                                     history[i], swap_function,
                                                     nswaps, nbefore, i,
                                                     nsystems, queues_A,
                                                     pipes_swap[i], 
                                                     send_ret_vals[i]))
        processes.append(p)
        p.start()

    for i in range(nsystems):
        path, history = recv_ret_vals[i].recv()
        best_paths.append(path)
        final_histories.append(history)
        
    for p in processes:
        p.join()

    #Return final X and history from thread where T = 1
    distances = [function(graph, path) for path in best_paths]
    index_of_shortest_path = min(xrange(len(distances)),
                                 key=distances.__getitem__)
    return best_paths[index_of_shortest_path], final_histories
