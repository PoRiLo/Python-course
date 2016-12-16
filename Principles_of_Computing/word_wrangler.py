"""
Fundamentals of Computing Part 2
Week 2 - June 2016

Miniproject: Word Wrangler

@author: Ruben Dorado
http://www.codeskulptor.org/#user41_uIQJqItrJ3LhTS4_0.py
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"
#codeskulptor.set_timeout(60)

# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.
    """
    temp_list = []

    # for each element in list1 check if is already in the temp list
    # if it is not yet there, copy it.
    for item in list1:
        if item not in temp_list:
            temp_list.append(item)

    return temp_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.
    """
    intersect_list = []

    # check if the items in list1 are in list2 and add them to the list
    for item1 in list1:
        if item1 in list2:
            intersect_list.append(item1)

    return intersect_list


# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.
    """
    merge_list = []
    l1_copy = list(list1)
    l2_copy = list(list2)

    # cycling through list1 and list2: we check the first element in
    # list2, if it's smaller than the first element in list1 we copy it to
    # the merge list and pop it out of list2. Else we break the loop and
    # copy the first element of list1, then pop it and proceed again
    while l1_copy:
        while l2_copy:
            if l2_copy[0] < l1_copy[0]:
                merge_list.append(l2_copy[0])
                l2_copy.pop(0)
            else:
                break
        merge_list.append(l1_copy[0])
        l1_copy.pop(0)

    # if list2 is not empty once list1 is, add the remaining elements to the
    # end of the merge list
    if l2_copy:
        merge_list.extend(l2_copy)

    return merge_list

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.
    """
    if list1 == []:
        return list1
    else:
        pivot = list1[0]
        lesser = [item for item in list1 if item < pivot]
        pivots = [item for item in list1 if item == pivot]
        greater = [item for item in list1 if item > pivot]
        return merge_sort(lesser) + pivots + merge_sort(greater)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.
    """
    anagrams = []

    # if the word has a length of 0, append an empty string
    if len(word) == 0:
        anagrams.append('')

    else:
        # split the word in first letter + rest
        first = word[0]
        rest = word[1 :]

        # generate the strings for the rest of the word
        rest_strings = gen_all_strings(rest)

        # add the strings to the anagrams list
        anagrams.extend(rest_strings)

        # create new strings by relocating the first character
        # in every possible position
        for string in rest_strings:
            for idx in range(len(string) + 1):
                new_string = string[: idx] + first + string[idx :]
                anagrams.append(new_string)

    return anagrams

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """

    url = codeskulptor.file2url(WORDFILE)
    netfile = urllib2.urlopen(url)
    data = netfile.read()
    return data

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates,
                                     intersect, merge_sort,
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
#run()
