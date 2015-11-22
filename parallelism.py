import numpy as np

from multiprocessing import Process, Queue, Pipe
from annealing_helper_functions import anneal_once

def parallel_tempering(graph, function, X, T, iterr, prev_E, history, swap_function, nswaps, 
                       nbefore, process_number, queues_A, pipes_swap, send_ret_val):
    process_count = len(queues_A)
    for step in range(iterr):
        # Run nbefore steps of simulated annealing
        X, prev_E, delta_E, history = anneal_once(graph, function, X, T, prev_E, history, 
                                                   swap_function, nswaps)
        # Decide which chains, if any, to exchange
        if step % nbefore == 0:
            #Each process can swap with subsequent processes
            #print "put for {0} {1}".format(process_number, step)
            queues_A[process_number].put(delta_E)
            queues_A[process_number].put(T)
            # Acceptance probability
            if process_number < process_count - 1:
                #print "get from {0} {1} initiated".format(process_number, step)
                next_delta_E = queues_A[process_number + 1].get()
                next_T = queues_A[process_number + 1].get()
                #print "get from {0} {1} complete".format(process_number, step)
                A = np.exp(min(np.log(1), ((delta_E - next_delta_E)/T) +
                                  ((next_delta_E - delta_E)/next_T)))

            #Finish any started swap before going to next one
            if process_number > 0:
                #Check if need to swap with prior process
                #print "inititate swap recv from {0} {1}".format(process_number, step)
                swap_bool = pipes_swap[0].recv()
                #print "swap recv from {0} {1} completed".format(process_number, step)
                if swap_bool:
                    #If so, publish info then retrieve info
                    pipes_swap[0].send([prev_E, X])
                    prev_E, X = pipes_swap[0].recv()

            #Only initiate swap from lower-indexed process, i.e. not last process
            if process_number < process_count - 1:
                if np.random.uniform() < A:
                    #Swap is happening
                    pipes_swap[-1].send(True)
                    #print "swap send True from {0} {1}".format(process_number, step)
                    #Send info to next process, then retrieve info
                    pipes_swap[-1].send([prev_E, X])
                    prev_E, X = pipes_swap[-1].recv()
                else:
                    #No swap necessary
                    pipes_swap[-1].send(False)
                    #print "swap send False from {0} {1}".format(process_number, step)

    if process_number == 0:
        send_ret_val.send([X, history])

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
    send_ret_val, recv_ret_val = Pipe()

    for i in xrange(nsystems):
        swap_pipes = []
        history[i].append(prev_Es[i])
        q1 = Queue()
        queues_A.append(q1)
        if i > 0:
            #Grab the last process's c2
            swap_pipes.append(prev_conn)
        #Generate one pipe per swap
        if i < nsystems - 1:
            c1,c2 = Pipe()
            #Keep c1
            swap_pipes.append(c1)
            prev_conn = c2
        pipes_swap.append(swap_pipes)
        
    for i in range(nsystems):
        p = Process(target=parallel_tempering, args=(graph, function, Xs[i], Ts[i], iterr, 
                                                     prev_Es[i], history[i], swap_function, 
                                                     nswaps, nbefore, i, queues_A, 
                                                     pipes_swap[i], send_ret_val))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()

    #Return final X and history from thread where T = 1
    return recv_ret_val.recv()
