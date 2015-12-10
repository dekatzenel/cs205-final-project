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

+ `comparison.py` runs parallel tempering in both serial and parallel 
+ `controller.py` runs each of simulated annealing, parallel tempering in serial, and parallel tempering in parallel for iteration counts of 10^3, 10^4, and 10^5.
 Both types of parallel tempering run with 4 systems and for the parallel version, these systems are each in a separate process. `controller.py` prints to console the
 known optimum path and its length, as well as the best path found and its length for each iteration count of each algorithm.