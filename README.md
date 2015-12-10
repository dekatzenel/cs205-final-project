#Parallel Tempering and the Traveling Salesman Problem
##CS205 Fall 2015
###Jonathan Friedman, Christian Junge, Dana Katzenelson

####Directory structure:

```
cs205-final-project     
+-- Writeup     
|   +-- final.gif     
|   +-- presentation.key     
|   +-- presentation.pdf     
|   +-- results.txt     
|   +-- script.txt     
+-- resources
|   +-- a280.xml.zip
|   +-- fri26.xml.zip
|   +-- ipython_source_files.zip
+-- utils     
|   +-- __init__.py     
|   +-- plotting.py     
|   +-- timer.py     
|   +-- xml_parse.py     
+-- README.md     
+-- annealing_helper_functions.py     
+-- comparison.py     
+-- controller.py     
+-- parallel_tempering.py
```   

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

SOMEONE WHO IS NOT DANA SHOULD TALK ABOUT THE WRITEUP FILES. BUT FIRST WE NEED TO ADD CHRISTIAN'S FILES TO THE WRITEUP FILES FOLDER.