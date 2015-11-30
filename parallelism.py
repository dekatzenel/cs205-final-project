import numpy as np

from multiprocessing import Process, Queue, Pipe
from annealing_helper_functions import distance, anneal_once

def parallel_tempering(graph, function, X, T, iterr, prev_E, history, swap_function, nswaps, 
                       nbefore, process_number, process_count, queues_A, pipes_swap, send_ret_val):
    best_path = []
    best_path_length = float('inf')

    for step in range(iterr):
        # Run nbefore steps of simulated annealing
        X, prev_E, delta_E, history = anneal_once(graph, function, X, T, prev_E, history, 
                                                   swap_function, nswaps)
        newest_distance = distance(graph, X)
        if newest_distance < best_path_length:
            best_path = X
            best_path_length = newest_distance

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
                A = np.exp(min(np.log(1), ((delta_E - next_delta_E)/T) +
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

def parallel_parallel_tempering(graph, function, initial_Xs, initial_temps, 
                                iterr, swap_function, nswaps, nbefore):
    # Make sure inputs are ok
    assert(len(initial_temps) == len(initial_Xs)), "Mismatched input dimensions"
    assert(initial_temps[0] == 1), "First temperature should be one"

    # Initialize stuff
    nsystems = len(initial_temps)
    Xs = initial_Xs
    Ts = initial_temps
    prev_Es = [function(graph, Xs[i]) for i in range(nsystems)]
    delta_Es = [0] * nsystems
    history = [[] for i in xrange(nsystems)]
    processes = []
    queues_A = []
    prev_conn = None
    pipes_swap = []
    send_ret_vals = []
    recv_ret_vals = []
    best_paths = []
    final_histories = []

    for i in xrange(nsystems - 1, -1, -1):
        swap_pipes = []
        history[i].append(prev_Es[i])
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
        p = Process(target=parallel_tempering, args=(graph, function, Xs[i], Ts[i], iterr, 
                                                     prev_Es[i], history[i], swap_function, 
                                                     nswaps, nbefore, i, nsystems, queues_A,
                                                     pipes_swap[i], send_ret_vals[i]))
        processes.append(p)
        p.start()

    for i in range(nsystems):
        path, history = recv_ret_vals[i].recv()
        best_paths.append(path)
        final_histories.append(history)
        
    for p in processes:
        p.join()

    #Return final X and history from thread where T = 1
    distances = [distance(graph, path) for path in best_paths]
    index_of_shortest_path = min(xrange(len(distances)),key=distances.__getitem__)
    return best_paths[index_of_shortest_path], final_histories