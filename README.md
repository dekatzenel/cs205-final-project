#Parallel Tempering and the Traveling Salesman Problem
##CS205 Fall 2015
###Jonathan Friedman, Christian Junge, Dana Katzenelson

####Directory structure:

```
cs205-final-project     
+-- Code
|   +-- resources
    |   +-- a280.xml.zip
    |   +-- fri26.xml.zip
    |   +-- ipython_source_files.zip
|   +-- utils     
    |   +-- __init__.py     
    |   +-- plotting.py     
    |   +-- timer.py     
    |   +-- xml_parse.py     
|   +-- ParameterSelectionPpt.py
|   +-- TimingTest.py
|   +-- annealing_helper_functions.py     
|   +-- comparison.py     
|   +-- controller.py     
|   +-- parallel_tempering.py
|   +-- plotter.py
+-- Images	
|   +-- AccuracyVsComputation.png	
|   +-- AccuracyVsIterations.png	
|   +-- AccuracyVsTime0to4sec.png	
|   +-- AccuracyVsTime20sec.png	
|   +-- AccuracyVsTime4to20sec.png
|   +-- AccuracyVsTime_200kIter.png
|   +-- Distribution.png	
|   +-- Efficiency.png
|   +-- ElapsedTimeVsComputation.png	
|   +-- PerformanceComparison1.png	
|   +-- PerformanceComparison2.png	
|   +-- PerformanceComparison3.png	
|   +-- Speed.png
+-- SavedResults
|   +-- IndividualRuns/
    |   +--[Misc files]
|   +-- dist_hist_ppt.npy
|   +-- dist_hist_sa.npy
|   +-- dist_hist_spt.npy
|   +-- hist_best_ppt.npy
|   +-- hist_best_sa.npy
|   +-- hist_best_spt.npy
|   +-- time_hist_ppt.npy
|   +-- time_hist_sa.npy
|   +-- time_hist_spt.npy
+-- .gitignore
+-- README.md     
+-- Report.ipynb
```   

All code for this project is located inside of the `Code\` folder.

There are multiple files that can serve as the starting point for the code in this repository. To run the code, enter `python <NAME_OF_FILE>` into the commandline.
+ `comparison.py` runs parallel tempering in both serial and parallel for iteration counts of 10^3, 10^4, 10^5, and 10^6 on
 http://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/XML-TSPLIB/instances/fri26.xml.zip (also stored in resources). Each iteration count is run 10 times. Both types of parallel
 tempering run with 4 systems and for the parallel version, these systems are each in a separate process. `comparison.py` prints the known optimum path and its length
 to console and then writes to file for each run the number of iterations, the length of the best path found, and the time taken.
+ `controller.py` runs each of simulated annealing, parallel tempering in serial, and parallel tempering in parallel for iteration counts of 10^3, 10^4, and 10^5 on
 http://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/XML-TSPLIB/instances/fri26.xml.zip. Both types of parallel tempering run with 4 systems and for the
 parallel version, these systems are each in a separate process. `controller.py` prints to console the known optimum path and its length, as well as the best path
 found and its length for each iteration count of each algorithm.

There are two files that contain data that can be converted into graphs to be used in TSP. Both are located in `resources/`. 
+ `fri26.xml.zip` is our primary file on which we performed most of our testing. It has 26 nodes.
+ `a280.xml.zip` is a larger file with 280 nodes. We used it to check how our results scaled to larger data sets.

Our code for parallel tempering, both in serial and in parallel, is located in `parallel_tempering.py`. Both functions make extensive use of the `anneal_once()` and
 related functions in `annealing_helper_functions.py`. The code for simulated annealing is also located in `annealing_helper_functions.py`

Several ipython notebooks are referenced as resources throughout the code. They are available at `resources/ipython_source_files.zip`.

`Report.ipynb` 
This is our project website. This notebook gives the background for our project, describes our implementations, interprets our results, and discusses parallelism in
 the context of this project.  

`TimingTest.py` 
Performs many runs of each of the three optimization algorithms, averages their current path and run time at each step among the many iterations, and saves these files
 so that they can be plotted in `plotter.py`

`plotter.py` 
Loads saved test results from `TimingTest.py` and plots them. This function was used to generate all of the performance plots for the report.  

`ParameterSelectionPpt.py`
Performs a gradient descent parameter optimization for parallel parallel tempering. The returned parameters are then used in `TimingTest.py`

`Images/`
Contains all of the images that are referenced in the Report. The images are loaded into the report notebook using IPython's display.Image() command.  

`SavedResults/`
Contains the output from several runs of `TimingTest.py`  These results are included so that the user can generate customized plots and perform analyses on the
 algorithms without having to re-run lengthy simulations. The `IndividualRuns/` subfolder contains the results from a single run of each algorithm, in case the user
 wants to observe individual runs rather than averaged results over many runs. The `time_hist__`, `hist_best__`, and `dist_hist__` files are averaged results from 25 runs.
 The `time_hist__` files contain average elapsed iteration times for 50,000 iteration runs, the `dist_hist__` files contain the average best found distances at each
 iteration for 50,000 iteration runs, and the `dist_hist__` files contain the average best found distances at each iteration for 1,000,000 iteration runs.  