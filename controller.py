import numpy as np

from annealing_helper_functions import distance
from xml_parse import parse_xml_graph

graph = parse_xml_graph('fri26.xml')
# Hardcoded best path to validate distance calculations, zero-indexed
bestpath = [x-1 for x in [1, 25, 24, 23, 26, 22, 21, 17, 18, 20, 19, 16, 11, 12, 13, 15, 14, 10, 9, 8, 7, 5, 6, 4, 3, 2]]
print distance(graph, bestpath)
