"""
Algorithmic Thinking Part 2, Module 3 - February 2016
Project 3

Created on Mon Feb 29 17:12:35 2016
@author: Ruben Dorado Sanchez-Castillo

Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster


######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a
    list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices
    for two clusters

    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]),
            min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters

    Output: tuple of the form (dist, idx1, idx2) where the centers of the
    clusters cluster_list[idx1] and cluster_list[idx2] have minimum distance
    dist.
    """
    closest_pair = (float('inf'), -1, -1)
    index_list = range(len(cluster_list))

    for point_u in index_list:
        for point_v in index_list:
            if point_u != point_v:
                closest_pair = min(closest_pair,
                                   pair_distance(cluster_list, point_u, point_v))
    return closest_pair


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip

    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal
    distance that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the
    clusters cluster_list[idx1] and cluster_list[idx2] lie in the strip and
    have minimum distance dist.
    """
    # creating a list of the indexes of the clusters in the strip
    strip_points = [p_idx for p_idx in range(len(cluster_list)) if abs(cluster_list[p_idx].horiz_center() - horiz_center) <= half_width]
    strip_points.sort()

    # initializing variables
    points_in_strip = len(strip_points)
    closest_pair = (float('inf'), -1, -1)

    for u_idx in range(points_in_strip - 1):
        for v_idx in range(u_idx + 1, points_in_strip):
            closest_pair = min(closest_pair,
                               pair_distance(cluster_list, strip_points[u_idx], strip_points[v_idx]))

    return closest_pair


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal
    positions of their centers are in ascending order

    Output: tuple of the form (dist, idx1, idx2) where the centers of the
    clusters cluster_list[idx1] and cluster_list[idx2] have minimum distance
    dist.
    """
    num_points = len(cluster_list)
    closest_pair = (float('inf'), -1, -1)

    if num_points <= 3:
        return slow_closest_pair(cluster_list)
    else:
        split_point = num_points/2
        left_cluster = [cluster_list[idx_l] for idx_l in range(split_point)]
        right_cluster = [cluster_list[idx_r] for idx_r in range(split_point, num_points)]
        left_best = fast_closest_pair(left_cluster)
        right_best = fast_closest_pair(right_cluster)
        closest_pair = min(left_best,
                           (right_best[0], right_best[1] + split_point, right_best[2] + split_point))
        mid_distance = .5*(cluster_list[split_point - 1].horiz_center() + cluster_list[split_point].horiz_center())
        closest_pair = min(closest_pair,
                           closest_pair_strip(cluster_list, mid_distance, closest_pair[0]))
    return closest_pair


######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list

    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """

    total_clusters = len(cluster_list)

    while total_clusters > num_clusters:
        cluster_list.sort(key = lambda cluster: cluster.horiz_center())
        closest_pair = fast_closest_pair(cluster_list)
        cluster_1 = cluster_list[closest_pair[1]]
        cluster_2 = cluster_list[closest_pair[2]]
        merged_clusters = cluster_1.merge_clusters(cluster_2)
        cluster_list.append(merged_clusters)
        cluster_list.remove(cluster_1)
        cluster_list.remove(cluster_2)
        total_clusters = len(cluster_list)

    return cluster_list


######################################################################
# Code for k-means clustering


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list

    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    clusters = list(cluster_list)

    # position initial clusters at the location of clusters with largest populations
    clusters.sort(reverse = True,
                  key = lambda cluster: cluster.total_population())
    old_clusters = [clusters[idx] for idx in range(num_clusters)]

#    Initialize old cluster using large population counties
#    For number of iterations
#          Initialize the new clusters to be empty
#          For each county
#              Find the old cluster center that is closest
#              Add the county to the corresponding new cluster
#          Set old clusters equal to new clusters
#    Return the new clusters

    for dummy_i in range(num_iterations):
        new_clusters = [alg_cluster.Cluster(set(), 0, 0, 0, 0) for dummy_k in range(num_clusters)]
        for county in cluster_list:
            county_x = county.horiz_center()
            county_y = county.vert_center()
            l_idx = [float('inf'), -1]
            for cluster in old_clusters:
                distance = math.sqrt((county_x - cluster.horiz_center()) ** 2 + (county_y - cluster.vert_center()) ** 2)
                l_idx = min(l_idx, [distance, old_clusters.index(cluster)])
            new_clusters[l_idx[1]] = new_clusters[l_idx[1]].merge_clusters(county)
        old_clusters = new_clusters

    return new_clusters

