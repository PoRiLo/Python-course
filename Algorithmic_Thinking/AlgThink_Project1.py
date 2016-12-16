"""
Algorithmic Thinking Part 1, Module 1 - January 2016
Project 1
Ruben Dorado
"""

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
