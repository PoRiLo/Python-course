"""
Algorithmic Thinking Part 2, Module 3 - February 2016
Application 3

Created on Sat Mar 05 11:23:14 2016

@author: Ruben

"""

import time
import random
import alg_cluster
import matplotlib.pyplot as plt
import AlgThink_Project3 as project3
import alg_project3_viz


### Question 1 ###

def gen_random_clusters(num_clusters):
    """
    Creates a list of clusters where each cluster in this list corresponds to
    one randomly generated point in the square with corners (±1,±1).

    Input:
    num_clusters = number of clusters in the list

    Output:
    cluster_list = a list of randomly generated clusters
    """

    cluster_list = []

    for dummy_i in range(num_clusters):
        cluster_x = random.random() * 2 - 1
        cluster_y = random.random() * 2 - 1
        cluster_list.append(alg_cluster.Cluster(set(), cluster_x, cluster_y, 0, 0))

    return cluster_list

def question1_plot():
    """
    Calculates the running time of the clustering process for randomly generated
    sets of clusters ranging in size from 2 to 200. Plots the outcome
    """

    # Initializing the data series
    xvals = range(2, 201)
    slow_times = []
    fast_times = []

    for size in xvals:
        cluster_list = gen_random_clusters(size)
        cluster_list.sort(key = lambda cluster: cluster.horiz_center())

        # Calculating the running time of slow_closest_pair for this iteration
        start_clock = time.clock()
        project3.slow_closest_pair(cluster_list)
        end_clock = time.clock() - start_clock
        slow_times.append(end_clock * 1000)

        # Calculating the running time of fast_closest_pair for this iteration
        start_clock = time.clock()
        project3.fast_closest_pair(cluster_list)
        end_clock = time.clock() - start_clock
        fast_times.append(end_clock * 1000)

    # Plotting the outcome
    plt.plot(xvals, slow_times, '-c',
             label='slow_closest_pair')
    plt.plot(xvals, fast_times, '-y',
             label='fast_closest_pair')
    plt.legend(loc='upper left')
    plt.title('Processing times to run clustering methods (desktop Python)')
    plt.ylabel('Running time (milliseconds)')
    plt.xlabel('Number of initial clusters')
    plt.show()

# Plots the answer to question 1
question1_plot()


### Question 2 ###

# Plots the answer to question 2
#alg_project3_viz.run_example(3108, "hierarchical", True)


### Question 3 ###

# Plots the answer to question 3
#alg_project3_viz.run_example(3108, "k-means", True)


### Question 5 ###

# Plots the answer to question 5
#alg_project3_viz.run_example(111, "hierarchical", True)


### Question 6 ###

# Plots the answer to question 5
#alg_project3_viz.run_example(111, "k-means", True)


### Question 7 ###

def compute_distortion(data, k):
    """
    Computes the distortion of a cluster as the sum of errors associated to its
    clusters. The error of a cluster is the sum of the squared distance from
    each element to the cluster center, weighted by the element weight (in the
    example, the county's population).
    """

    if data == 3108:
        data_url = alg_project3_viz.DATA_3108_URL
    if data == 896:
        data_url = alg_project3_viz.DATA_896_URL
    if data == 290:
        data_url = alg_project3_viz.DATA_290_URL
    if data == 111:
        data_url = alg_project3_viz.DATA_111_URL

    data_table = alg_project3_viz.load_data_table(data_url)

    cluster_list = []
    for line in data_table:
        cluster_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

    cluster_list_copy = [cluster.copy() for cluster in cluster_list]
    hierarchical_cluster = project3.hierarchical_clustering(cluster_list_copy, k)

    cluster_list_copy = [cluster.copy() for cluster in cluster_list]
    kmeans_cluster = project3.kmeans_clustering(cluster_list_copy, k, 5)

    hierarchical_distortion = 0.0
    kmeans_distortion = 0.0

    for cluster in hierarchical_cluster:
        hierarchical_distortion += cluster.cluster_error(data_table)

    for cluster in kmeans_cluster:
        kmeans_distortion += cluster.cluster_error(data_table)

    return (hierarchical_distortion/10**9, kmeans_distortion/10**9)

#print compute_distortion(290, 16)
#print compute_distortion(111, 9)

### Question 10 ###

def question10_plot(data_set):
    """
    Calculates the running time of the clustering process for randomly generated
    sets of clusters ranging in size from 2 to 200. Plots the outcome
    """

    # Initializing the data series
    xvals = range(6, 21)
    hierarchical_distortion = []
    kmeans_distortion = []

    # building the data series
    for size in xvals:
        distortion = compute_distortion(data_set, size)
        hierarchical_distortion.append(distortion[0])
        kmeans_distortion.append(distortion[1])

    # Plotting the outcome
    plt.clf()
    plt.plot(xvals, hierarchical_distortion, '-c',
             label='Hierarchical clustering distortion')
    plt.plot(xvals, kmeans_distortion, '-y',
             label='k-means clustering distortion (iterations = 5)')
    plt.legend(loc='upper left')
    plt.title('Distortion for the ' + str(data_set) + ' counties data set')
    plt.ylabel('Distortion')
    plt.xlabel('Number of clusters')
    plt.show()

# Plots the answer to question 1
#question10_plot(111)
#question10_plot(290)
#question10_plot(896)
