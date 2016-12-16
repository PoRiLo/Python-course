"""
This module creates an undirected UPA graph
"""

import random
import alg_upa_trial
import AlgThink_Project1 as my_mod

# Functions

def create_UPA_graph(total_nodes, num_connections):
    """
    Creates an undirected node from an initial group of nodes by adding
    secuentially new nodes, each of them connected to a fixed number of
    previously existing nodes.

    total_nodes = total nodes in the finished UPA graph
    num_connections = m, integer that indicates to how many of the previous
        nodes are the new nodes connected

    Returns a graph in its dictionary representation
    """

    # Initialzing the graph as a complete graph in m nodes
    upa_graph = my_mod.make_complete_graph(num_connections)

    # Initializing the UPATrial class
    upa_trial = alg_upa_trial.UPATrial(num_connections)

    # growing the graph until num_nodes
    for new_node in range(num_connections, total_nodes):
        neighbors = upa_trial.run_trial(num_connections)
        upa_graph[new_node] = neighbors
        for neighbour in neighbors:
            upa_graph[neighbour].add(new_node)

    return upa_graph

# Tests
# print create_UPA_graph(10, 3)
        
        
