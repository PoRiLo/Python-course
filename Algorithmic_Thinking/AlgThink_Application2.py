"""
Algorithmic Thinking Part 1, Module 2 - February 2016
Applications 2
Ruben Dorado
"""
# Import modules
import random
import time
import AlgThink_Project2 as mod_resilience
import UPA_graph_generator as mod_upa
import alg_application2_provided as graph_provided
import matplotlib.pyplot as plt

# Initializing global invariables
NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"

# Helper functions

def make_random_ugraph(num_nodes, probability = 0.5):
    """
    Takes the number of nodes and returns a dictionary corresponding to 
    an undirected graph with the specified number of nodes where each edge
    has a p probability to exist.
    
    num_nodes = number of nodes in the graph
    probability = the probability that an individual edge exists
    """
    node_list = range(num_nodes)
    ugraph = dict()
    
    for node in node_list:
        ugraph[node] = set()
    
    for node_i in node_list:
        for node_j in node_list:
            if node_i < node_j:
                if random.random() < probability:
                    ugraph[node_i].add(node_j)
                    ugraph[node_j].add(node_i)
    return ugraph

def random_order(ugraph):
    """ 
    takes a graph and returns a list of the nodes in the graph in 
    some random order
    """
    node_list = ugraph.keys()
    random_list = []
    
    while node_list:
        a_node = random.choice(node_list)
        random_list.append(a_node)
        node_list.remove(a_node)
        
    return random_list

def num_edges(graph, directed = False):
    """ Finds the number of edges in an a graph
    """
    nodes = 0
    edges = 0
    for node in graph.keys():
        nodes += 1
        edges += len(graph[node])
    if not directed:
        edges /= 2
    print 'Graph with ' + str(nodes) + ' nodes and ' + str(edges) + ' edges.'
    return edges

def try_graph(nodes, prob, tries, directed = False):
    """ runs a series of trials of a random generated graph and averages the 
    number of edges in them
    """
    count = 0.0
    suma = 0.0
    for i in range(tries):
        count += 1
        suma += num_edges(make_random_ugraph(nodes, prob), directed)
    return suma / count

# Tests
#print random_order(make_random_ugraph(6, .5))
#print num_edges(make_random_ugraph(1239, .004))
#print try_graph(1239, .004, 100, False)

"""
Assignment tasks 
"""

# Question 1
def question1_plot():
    """
    Loads the three graphs in the problem, calculates a sequence of attack
    for each one and calculates the resilience of each graph based on this
    attack. Plots the results.
    """

    # Loading the provided computer network example
    example_graph = graph_provided.load_graph(NETWORK_URL)

    # Creating a random ER graph with 1239 nodes and p = .004
    er_graph = make_random_ugraph(1239, .004)

    # Creating an UPA graph, m=12
    upa_graph = mod_upa.create_UPA_graph(1239, 2)

    #Calculating attack sequences
    example_attack = random_order(example_graph)
    er_attack = random_order(er_graph)
    upa_attack = random_order(upa_graph)

    # Calculating resilience
    example_resilience = mod_resilience.compute_resilience(example_graph, 
                                                           example_attack)
    er_resilience = mod_resilience.compute_resilience(er_graph, 
                                                      er_attack)
    upa_resilience = mod_resilience.compute_resilience(upa_graph, 
                                                       upa_attack)

    # Plotting the outcome 
    xvals = range(1240)

    plt.plot(xvals, example_resilience, '-c', 
             label='computer network example (provided)')
    plt.plot(xvals, er_resilience, '-y', 
             label='generated ER graph (p = .004)')
    plt.plot(xvals, upa_resilience, '-m', 
             label='generated UPA graph (m = 2)')
    plt.legend(loc='upper right')
    plt.title('Graphs resilience')
    plt.xlabel('Nodes removed')
    plt.ylabel('Biggest connected element size')
    plt.show()

# Executes question 1
#question1_plot()

# Question 2
def fast_targeted_order(ugraph):
    """
    Computes an attack order for calculating the resilience of a graph where, 
    in every iteration, a node of the maximum degree is targeted
    
    ugraph = an undirected graph
    
    Returns attack_order = an ordered list of nodes
    """
    # Initializing the list of sets of nodes by degree
    degree_sets = [set() for dummy_idx in ugraph.keys()]
    
    # Populating the list of sets
    for i_node in ugraph.keys():
        i_degree = len(ugraph[i_node])
        degree_sets[i_degree].add(i_node)
    
    # Initializing other variables
    graph = dict(ugraph)
    attack_list = []
    index = 0
    
    # Iterates through degree_sets in decreasing degree order, adds one of the 
    # top degree nodes left to the list and updates the list and the ugraph
    # before proceeding to the next iteration
    for k_degree in range(len(graph) - 1, -1, -1):
        while degree_sets[k_degree]:
            u_node = random.choice(list(degree_sets[k_degree]))
            attack_list.append(u_node)
            degree_sets[k_degree].remove(u_node)
            for v_neighbor in ugraph[u_node]:
                v_degree = len(ugraph[v_neighbor])
                degree_sets[v_degree].remove(v_neighbor)
                degree_sets[v_degree - 1].add(v_neighbor)
            graph_provided.delete_node(graph, u_node)
            index += 1
    
    return attack_list

# Tests for fast_targeted_order
#my_graph = mod_upa.create_UPA_graph(10, 3)
#print 'my graph = ' + str(my_graph)
#print 'provided attack order = ' + str(graph_provided.targeted_order(my_graph)) 
my_graph = graph_provided.load_graph(NETWORK_URL)
attack = fast_targeted_order(my_graph)
resilience = mod_resilience.compute_resilience(my_graph, attack)

def question3_plot():
    """
    Calculates a series of targeted attacks using both functions (provided and
    the fast targeted implemented one), computes the running time of these 
    processes and plots the outcome
    """
    # Initializing the data series
    xvals = range(10 , 1000, 10)
    targeted_times = []
    fast_targeted_times = []
    
    for size in range(10, 1000, 10):
        upa_graph = mod_upa.create_UPA_graph(size, 5)
        
        # Calculating the running time of targeted_attack for this iteration
        start_clock = time.clock()
        graph_provided.targeted_order(upa_graph)
        end_clock = time.clock() - start_clock
        targeted_times.append(end_clock * 1000)
        
        # Calculating the running time of fast_targeted_attack for this iteration
        start_clock = time.clock()
        fast_targeted_order(upa_graph)
        end_clock = time.clock() - start_clock
        fast_targeted_times.append(end_clock * 1000)
        
    # Plotting the outcome 
    plt.plot(xvals, targeted_times, '-c', 
             label='targeted_order times (O(n**2))')
    plt.plot(xvals, fast_targeted_times, '-y', 
             label='fast_targeted_order times (O(n))')
    plt.legend(loc='upper left')
    plt.title('Processing times to calculate attacks (desktop Python)')
    plt.ylabel('Running time (milliseconds)')
    plt.xlabel('Graph size')
    plt.show()

# Plots the answer to question 3
#question3_plot()

# Question 4
def question4_plot():
    """
    Loads the three graphs in the problem, calculates a sequence of targeted
    attacks using fast_targeted_attack and calculates the resilience of each 
    graph based on this attack. Plots the results.
    """

    # Loading the provided computer network example
    example_graph = graph_provided.load_graph(NETWORK_URL)

    # Creating a random ER graph with 1239 nodes and p = .004
    er_graph = make_random_ugraph(1239, .004)

    # Creating an UPA graph, m=12
    upa_graph = mod_upa.create_UPA_graph(1239, 2)

    # Calculating attack sequences with the provided targeted_order
    #example_attack = graph_provided.targeted_order(example_graph)
    #er_attack = graph_provided.targeted_order(er_graph)
    #upa_attack = graph_provided.targeted_order(upa_graph)

    # Calculating attack sequences with fast_targeted_order
    example_attack = fast_targeted_order(example_graph)
    er_attack = fast_targeted_order(er_graph)
    upa_attack = fast_targeted_order(upa_graph)

    # Calculating resilience
    example_resilience = mod_resilience.compute_resilience(example_graph, 
                                                           example_attack)
    er_resilience = mod_resilience.compute_resilience(er_graph, 
                                                      er_attack)
    upa_resilience = mod_resilience.compute_resilience(upa_graph, 
                                                       upa_attack)

    # Plotting the outcome 
    xvals = range(1240)

    plt.plot(xvals, example_resilience, '-c', 
             label='computer network example (provided)')
    plt.plot(xvals, er_resilience, '-y', 
             label='generated ER graph (p = .004)')
    plt.plot(xvals, upa_resilience, '-m', 
             label='generated UPA graph (m = 2)')
    plt.legend(loc='upper right')
    plt.title('Graphs resilience to targeted attack')
    plt.xlabel('Nodes removed')
    plt.ylabel('Biggest connected element size')
    plt.show()

# Executes question 4
#question4_plot()
