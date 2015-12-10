import zipfile

import xml.etree.ElementTree as ET
import numpy as np

"""
Converts a zipped or unzipped xml file to the graph structure used by the rest
    of the code
Called directly by controller/comparison files
Arguments:
    filename - the name of the unzipped xml file that you wish to use,
               regardless of whether it currently is zipped or unzipped
               ex: fri26.xml
Returns:
    edge-matrix graph structure stored as a numpy 2D array
"""
def parse_xml_graph(filename):

    #Unzip file if not yet unzipped
    try: 
        tree = ET.parse(filename)
    except IOError:
        zipped_filename = filename + '.zip'    
        zf = zipfile.ZipFile(zipped_filename, 'r')
        zf.extractall('resources/')
        tree = ET.parse(filename)
    
    #Parse XML file to graph
    root = tree.getroot()
    graph_structure = root.find('graph')

    #Placeholder for edge-matrix representation of graph, implemented using numpy arrays
    graph = []

    #For each vertex, add one row to the array with ordered distances from that vertex
    vertex_index = 0
    vertices = graph_structure.findall('vertex')
    N = len(vertices)
    for vertex in vertices:
        vertex_edges = []
        for edge in vertex:
            distance = edge.get('cost')
            vertex_edges.append(float(distance))

        #Add in edge to itself in the correct place
        vertex_edges.insert(vertex_index, 0.0)

        #Append row to master graph
        if len(graph) == 0:
            graph = np.asarray(vertex_edges).reshape((1,N))
        else:
            graph = np.append(graph, np.asarray(vertex_edges).reshape((1,N)), axis=0)
        vertex_index += 1
    return graph
