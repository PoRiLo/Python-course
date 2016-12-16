"""
Algorithmic Thinking Part 1, Module 1 - January 2016
Project 1
Ruben Dorado
"""

# Global constant graphs for testing

EX_GRAPH0 = {0: set([1, 2]), 
             1: set([]), 
             2: set([])}

EX_GRAPH1 = {0: set([1, 4, 5]), 
             1: set([2, 6]), 
             2: set([3]), 
             3: set([0]),
             4: set([1]), 
             5: set([2]), 
             6: set([])}

EX_GRAPH2 = {0: set([1, 4, 5]), 
             1: set([2, 6]), 
             2: set([3, 7]), 
             3: set([7]),
             4: set([1]), 
             5: set([2]),
             6: set([]),
             7: set([3]),
             8: set([1, 2]),
             9: set([0, 3, 4, 5, 6, 7])}

GRAPH0 = {0: set([1]),
          1: set([2]),
          2: set([3]),
          3: set([0])}

GRAPH1 = {0: set([]),
          1: set([0]),
          2: set([0]),
          3: set([0]),
          4: set([0])}

GRAPH2 = {0: set([1, 2, 3, 4]),
          1: set([]),
          2: set([]),
          3: set([]),
          4: set([])}

GRAPH3 = {0: set([1, 2, 3, 4]),
          1: set([0, 2, 3, 4]),
          2: set([0, 1, 3, 4]),
          3: set([0, 1, 2, 4]),
          4: set([0, 1, 2, 3])}

GRAPH4 = {"dog": set(["cat"]),
          "cat": set(["dog"]),
          "monkey": set(["banana"]),
          "banana": set([])}

GRAPH5 = {1: set([2, 4, 6, 8]),
          2: set([1, 3, 5, 7]),
          3: set([4, 6, 8]),
          4: set([3, 5, 7]),
          5: set([6, 8]),
          6: set([5, 7]),
          7: set([8]),
          8: set([7])}

GRAPH6 = {1: set([2, 5]),
          2: set([1, 7]),
          3: set([4, 6, 9]),
          4: set([6]),
          5: set([2, 7]),
          6: set([4, 9]),
          7: set([1, 5]),
          9: set([3, 4])}

GRAPH7 = {0: set([1, 2, 3, 4]), 
          1: set([0, 2, 3, 4]), 
          2: set([0, 1, 3, 4]), 
          3: set([0, 1, 2, 4]), 
          4: set([0, 1, 2, 3]), 
          5: set([2, 3, 4]), 
          6: set([0, 1, 4]), 
          7: set([0, 1, 2, 3]), 
          8: set([0, 1, 4, 7]), 
          9: set([2, 4]), 
          10: set([1, 2, 4]), 
          11: set([1, 3, 4, 7]), 
          12: set([0, 2, 3]), 
          13: set([0, 2, 4, 10]), 
          14: set([0, 2, 3, 4, 13])}

GRAPH8 = {0: set([1, 2]), 
          1: set([0, 2]), 
          2: set([0, 1]), 
          3: set([0]), 
          4: set([1, 2]), 
          5: set([0, 2]), 
          6: set([1, 2, 4]), 
          7: set([0, 3]), 
          8: set([0, 1]), 
          9: set([0, 7]), 
          10: set([0]), 
          11: set([0, 1, 3]), 
          12: set([0, 4, 7]), 
          13: set([0, 5]), 
          14: set([0, 1, 8]), 
          15: set([0, 1, 3]), 
          16: set([1, 14, 6]), 
          17: set([0, 8]), 
          18: set([0, 1]), 
          19: set([0, 1, 17])}

GRAPH9 = {0: set([1, 2, 3, 4, 5, 6]),
          1: set([0, 2, 3, 4, 5, 6]),
          2: set([0, 1, 3, 4, 5, 6]),
          3: set([0, 1, 2, 4, 5, 6]),
          4: set([0, 1, 2, 3, 5, 6]),
          5: set([0, 1, 2, 3, 4, 6]),
          6: set([0, 1, 2, 3, 4, 5]),
          7: set([1, 3, 4, 6]),
          8: set([0, 3, 4, 5, 6]),
          9: set([0, 5, 6, 7]),
          10: set([1, 2, 4, 9]),
          11: set([1, 2, 4, 6]),
          12: set([0, 2, 4, 6]),
          13: set([1, 2, 4, 5]),
          14: set([0, 1, 4, 6]),
          15: set([1, 4, 5, 6]),
          16: set([0, 1, 2, 4, 6]),
          17: set([0, 1, 2, 4, 5, 6]),
          18: set([2, 4, 5, 6, 13]),
          19: set([1, 2, 3, 5, 6]),
          20: set([0, 1, 2, 4, 5]),
          21: set([1, 2, 4, 5, 15]),
          22: set([0, 9, 4, 5, 13]),
          23: set([0, 1, 2, 3, 5, 20]),
          24: set([0, 1, 2, 3, 4, 5, 6]),
          25: set([0, 1, 2, 4, 5]),
          26: set([1, 2, 4, 5, 10, 22]),
          27: set([1, 2, 3, 5, 6]),
          28: set([0, 1, 3, 5]),
          29: set([2, 26, 4, 5, 6]),
          30: set([0, 2, 4, 6, 7]),
          31: set([20, 4, 21, 6]),
          32: set([1, 2, 4, 20, 28]),
          33: set([0, 4, 5, 6, 8, 22]),
          34: set([0, 2, 4, 5, 15]),
          35: set([1, 2, 5, 6, 9, 28]),
          36: set([24, 2, 3, 4, 6]),
          37: set([0, 1, 2, 4, 6, 10, 29]),
          38: set([0, 24, 11, 5, 6]),
          39: set([0, 1, 22, 6, 17]),
          40: set([0, 1, 2, 3, 5, 15]),
          41: set([11, 2, 3, 5, 6]),
          42: set([16, 1, 2, 5]),
          43: set([0, 1, 2, 4, 22]),
          44: set([32, 3, 6, 24, 27, 29]),
          45: set([1, 2, 4, 5, 16, 18, 37]),
          46: set([1, 5, 6, 7, 8, 12, 14]),
          47: set([8, 20, 2, 4]),
          48: set([0, 16, 2, 5, 14]),
          49: set([2, 21, 18, 6, 15])}

# Functions

def make_complete_graph(num_nodes):
    """
    Takes the number of nodes and returns a dictionary corresponding to 
    a complete directed graph with the specified number of nodes.
    
    num_nodes = number of nodes in the graph
    """
    node_list = range(num_nodes)
    graph_lst = list()
    
    for node in node_list:
        edges = set(node_list)
        edges.remove(node)
        graph_lst.append((node, edges))
    
    return dict(graph_lst)


def compute_in_degrees(digraph):
    """
    Takes a directed graph and computes the in-degrees for the nodes in the graph.
    
    digraph = directed graph in dictionary representation
    
    Returns a dictionary with the same set of keys (nodes) as digraph whose 
    corresponding values are the number of edges whose head matches a particular 
    node.
    """
    in_degrees = dict(digraph)
    
    for in_node in in_degrees:
        in_degrees[in_node] = 0
    
    # check for every node in the graph its out-nodes and adds 1 to the count of 
    # those nodes
    for node in digraph.keys():
        for out_node in digraph[node]:
            in_degrees[out_node] += 1
        
    return in_degrees


def in_degree_distribution(digraph):
    """
    Takes a directed graph and computes the unnormalized distribution of the 
    in-degrees of the graph.     

    digraph = directed graph in dictionary representation
    
    Returns a dictionary whose keys correspond to in-degrees of nodes in the graph. 
    The value associated with each particular in-degree is the number of nodes with 
    that in-degree. In-degrees with no corresponding nodes in the graph are not 
    included in the dictionary.
    """
    in_degrees = compute_in_degrees(digraph)
    distribution = dict()
    
    # Checks for every node it's in-degree and ads one to the required entry in the 
    # distribution dictionary
    for node in in_degrees.keys():
        in_nodes = in_degrees[node]
        if distribution.has_key(in_nodes):
            distribution[in_nodes] += 1
        else:
            distribution[in_nodes] = 1
            
    return distribution


# Commands for testing the functions

print make_complete_graph(5)

test_list = (EX_GRAPH0, 
                EX_GRAPH1, 
                EX_GRAPH2, 
                GRAPH0, 
                GRAPH1, 
                GRAPH2, 
                GRAPH3, 
                GRAPH4, 
                GRAPH5, 
                GRAPH6, 
                GRAPH7, 
                GRAPH8, 
                GRAPH9) 
for graph in test_list:
   print graph
   print compute_in_degrees(graph)
   print in_degree_distribution(graph)
   print
