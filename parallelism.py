from multiprocessing import Process, Queue
from annealing_helper_functions import anneal_once

def parallel_tempering(graph, function, X, T, iterr, prev_E, history, swap_function, nswaps, 
                       nbefore, process_number, queues):
    for step in range(iterr):
        # Run nbefore steps of simulated annealing
        X, prev_E, delta_E, history = anneal_once(graph, function, X, T, prev_E, history, 
                                                   swap_function, nswaps)
        # Decide which chains, if any, to exchange
        if step % nbefore == 0:
            #Each process can swap with subsequent processes
            queues[process_number].put(delta_E)
            queues[process_number].put(T)
            for i in range(process_number + 1, len(queues)):
                # Acceptance probability
                next_delta_E = queues[i].get()
                next_T = queues[i].get()
                A = np.exp(min(np.log(1), ((delta_E - next_delta_E)/T) +
                                  ((next_delta_E - delta_E)/next_T)))
                #TODO: Fix the below!!!!
                #The below is the correct condition for initiating the swap. Need to check the condition for receiving the swap, also worry about ordering. Might need synchronization mechanisms.
                if np.random.uniform() < A:
                    # Exchange most recent updates and paths
                    queues[process_number].put((True, i))
                    prev_Es[i], prev_Es[i+1] = prev_Es[i+1], prev_Es[i]
                    Xs[i], Xs[i+1] = Xs[i+1], Xs[i]
            #The below is wrong because can't guarantee the order of the i's for reading
            for i in range(process_number + 1):
                queues[i].get()


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
    queues = []

    for i in xrange(nsystems):
        history[i].append(prev_Es[i])
        q = Queue()
        queues.append(q)
        p = Process(target=parallel_tempering, args=(graph, function, Xs[i], Ts[i], iterr, 
                                                     prev_Es[i], history[i], swap_function, 
                                                     nswaps, nbefore, i, queues))
        processes.append(p)
        p.start()
        p.join()

    #TODO: Make sure these values get updated before return
    return Xs[0], history[0]
