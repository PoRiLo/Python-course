"""
Algorithmic Thinking Part 1, Module 2 - February 2016
Project 2
Ruben Dorado
"""

# Import modules
import random
from collections import deque

# Functions
def bfs_visited(ugraph, start_node):
    """
    Performs a breadth-first search in an undirected graph, starting at
    the given node.
    
    ugraph = an undirected graph
    start_node = the starting node in the undirected graph for the search
    
    Returns a set of all the nodes visited by the algorithm
    """
    
    # Initialize Q to an empty queue;
    queue = deque()
    
    # Visited <- {i};
    visited = set([start_node])
    
    # Enqueue(Q, i);
    queue.append(start_node)
    
    # While Q is not empty do
    # |  j <- dequeue(Q);
    # |  for each neighbour h of j do 
    # |  |  if h is not in Visited then
    # |  |  |  Visited <- Visited U {h};
    # |_ |_ |_ enqueue(Q, h);
    while queue:
        j_node = queue.pop()
        neighbours = ugraph[j_node]
        for h_neighbour in neighbours:
            if h_neighbour not in visited:
                visited.add(h_neighbour)
                queue.append(h_neighbour)
    
    # Return Visited;
    return visited


def cc_visited(ugraph):
    """
    Finds the groups of nodes mutually connected.
    
    ugraph = an undirected graph

    Returns a list of sets, where each set consists of all the nodes in a 
    connected component, and there is exactly one set in the list for each 
    connected component in ugraph and nothing else.
    """
    
    # RemainingNodes <- V;
    remaining_nodes = ugraph.keys()
    
    # CC <- 0;
    connected_components = []
    
    # While RemainingNodes <> 0 do
    # |  Let i be an arbitrary node in RemainingNodes;
    # |  W <- BFS-visited(g, i);
    # |  CC <- CC ∪ {W};
    # |_ RemainingNodes <- RemainingNodes−W;
    while remaining_nodes:
        i_node = random.choice(remaining_nodes)
        i_connected_set = bfs_visited(ugraph, i_node)
        connected_components.append(i_connected_set)
        for node in i_connected_set: 
            remaining_nodes.remove(node)
    
    return connected_components


def largest_cc_size(ugraph):
    """
    Finds the size of the largest connected component
    
    ugraph = an undirected graph
    
    Returns the size (an integer) of the largest connected component in ugraph.
    """
    
    # Initialize variables
    size = 0
    connected_components = cc_visited(ugraph)
    
    # Goes through the list of components and stores the value of the longest
    for component in connected_components:
        if len(component) > size:
            size = len(component)
    
    return size


def compute_resilience(ugraph, attack_order):
    """
    For each node in the ordered attack list, the function removes the given 
    node and its edges from the graph and then computes the size of the largest
    connected component for the resulting graph.
    
    ugraph = an undirected graph
    attack_order = a list of nodes
    
    Returns a list whose (k+1)th entry is the size of the largest connected
    component in the graph after the removal of the first k nodes in 
    attack_order. The first entry (indexed by zero) is the size of the largest
    connected component in the original graph.
    """
    
    #Initialize variables
    resilience = []
    resilience.append(largest_cc_size(ugraph))
    
    attack = list(attack_order)
    graph = dict(ugraph)
    
    # Go through the attack list, remove the nodes and its edges
    # and calculate the resulting maximum connected component size
    while attack:
        graph.pop(attack[0])    # Removes node from the graph
        for node in graph.keys():    # Removes edges from other nodes
            graph[node].discard(attack[0])
        resilience.append(largest_cc_size(graph))    # Calculates size and adds to list
        attack.remove(attack[0])    # Removes node from attack list
    
    return resilience

