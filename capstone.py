"""
Fundamentals of Computing - Capstone Exam
July 2016

@author: Ruben Dorado
"""

import math
import random


### Question 1

# Enter the value returned by the function

def test_01():
    print
    print "Question 1"

    def f():
        return

    print f()


### Question 2

# What global names are created during execution of this code snippet? What
# local names are created during execution of this code snippet?
def test_02():
    print
    print "Question 2"

    var1 = 7
    var2 = 5

    def var0(var1, var2):
        print "var2", var2
        var3 = var1 + var2
        var1 = 118
        global var4
        var4 = 17
        return var3 + var4

    print var0(var1, var1)

    print var0, var1, var2, var4


### Question 3

# Which of the following Python expressions can be used as a key to a dictionary in Python?
def test_03():
    print
    print "Question 3"
    a = "0"
    my_dic = dict([[a, 'it works']])
    print my_dic[a]

    a = [0]
    #my_dic = dict([[a, 'it works']])
    #print my_dic[a]

    a = (0)
    my_dic = dict([[a, 'it works']])
    print my_dic[a]

    a = False
    my_dic = dict([[a, 'it works']])
    print my_dic[a]

    a = set([0])
    #my_dic = dict([[a, 'it works']])
    #print my_dic[a]

    a = 0
    my_dic = dict([[a, 'it works']])
    print my_dic[a]


### Question 4:

def test_04():
    print
    print "Question 4"

    print "Increasing the first coordinate moves the point right. Increasing the second coordinate moves the point downward."


# Question 5:

class BankAccount:
    def __init__(self, initial_balance):
        """
        Creates an account with the given balance.
        """
        self._balance = initial_balance
        self._fees = 0

    def deposit(self, amount):
        """
        Deposits the amount into the account.
        """
        self._balance += amount

    def withdraw(self, amount):
        """
        Withdraws the amount from the account.
        Each withdrawal resulting in a balance of
        less than 10 dollars (before any fees) also
        deducts a penalty fee of 5 dollars from the balance.
        """
        self._balance -= amount

        if self._balance < 10:
            self._balance -= 5
            self._fees += 5

    def get_balance(self):
        """
        Returns the current balance in the account.
        """
        return self._balance

    def get_fees(self):
        """
        Returns the total fees ever deducted from the account.
        """
        return self._fees

def test_05():
    print
    print "Question 5"

    account1 = BankAccount(20)
    account1.deposit(10)
    account2 = BankAccount(10)
    account2.deposit(10)
    account2.withdraw(50)
    account1.withdraw(15)
    account1.withdraw(10)
    account2.deposit(30)
    account2.withdraw(15)
    account1.deposit(5)
    account1.withdraw(20)
    account2.withdraw(15)
    account2.deposit(25)
    account2.withdraw(15)
    account1.deposit(10)
    account1.withdraw(50)
    account2.deposit(25)
    account2.deposit(25)
    account1.deposit(30)
    account2.deposit(10)
    account1.withdraw(15)
    account2.withdraw(10)
    account1.withdraw(10)
    account2.deposit(15)
    account2.deposit(10)
    account2.withdraw(15)
    account1.deposit(15)
    account1.withdraw(20)
    account2.withdraw(10)
    account2.deposit(5)
    account2.withdraw(10)
    account1.deposit(10)
    account1.deposit(20)
    account2.withdraw(10)
    account2.deposit(5)
    account1.withdraw(15)
    account1.withdraw(20)
    account1.deposit(5)
    account2.deposit(10)
    account2.deposit(15)
    account2.deposit(20)
    account1.withdraw(15)
    account2.deposit(10)
    account1.deposit(25)
    account1.deposit(15)
    account1.deposit(10)
    account1.withdraw(10)
    account1.deposit(10)
    account2.deposit(20)
    account2.withdraw(15)
    account1.withdraw(20)
    account1.deposit(5)
    account1.deposit(10)
    account2.withdraw(20)
    print account1.get_balance(), account1.get_fees(), account2.get_balance(), account2.get_fees()

### Question 6

def test_06():
    print
    print "Question 6"

    print "WTF is a cycle in this context? A loop? "
    print "crazy = [1, 1]"
    print "crazy[1] = crazy"
    print "(crazy[1] = crazy[1] is WRONG)"


### Question 7

def test_07():
    print
    print "Question 7"

    print "Error in line 66, lacks parenthesis. It should be:"
    print "difference = (comp_number - player_number) % 5"
    print "http://www.codeskulptor.org/#user41_jRpZqKvSV9_0.py"


### Question 8

def test_08():
    print
    print "Question 8"

    print "Error in lines 63 to 67, doesn't refers paddle1_pos, paddle2_pos"
    print "http://www.codeskulptor.org/#user41_jRpZqKvSV9_1.py"


### Question 9

def test_09():
    print
    print "Question 9"

    print "Error in line 86, don't create properly a Card object. It should be:"
    print "self.deck.append(Card(suit, rank))"
    print "http://www.codeskulptor.org/#user41_jRpZqKvSV9_3.py"

### Question 10

def test_10():
    print
    print "Question 10"

    print "Exercise on enqueue/dequeue"
    print "Add(4), Add(8), Rem(), Add(7), Add(6), Add(5), Rem(), Rem(), Add(2), Rem(), Add(3), Add(7)"
    print "Answer on queue= 7325"
    print "Answer on stack= 4737"


###  Question 11

def test_11():
    print
    print "Question 11"

    print "What is the probability of rolling a Yahtzee (five of a kind) on a single roll of 5 six-sided dice?"

    p = (1.0/6.0)**4.0
    print p


### Question 12

def probability(outcomes):
    prob = 1
    dist = dict([[1, .1], [2, .2], [3, .3], [4, .15], [5, .05], [6, .2]])

    for outcome in outcomes:
        prob *= dist[outcome]

    return prob

def test_12():
    print
    print "Question 12"
    print "Careful! They change the list!"
    print probability([5])
    print probability([4, 2, 6, 4, 2, 4, 5, 5, 5, 5, 1, 2, 6, 2, 6, 6, 4, 6, 2,
                       3, 5, 5, 2, 1, 5, 5, 3, 2, 1, 4, 4, 1, 6, 6, 4, 6, 2, 4,
                       3, 2, 5, 1, 3, 5, 4, 1, 2, 3, 6, 1])
    print probability([4, 2, 6, 4, 2, 4, 5, 5, 5, 5, 1, 2, 2, 6, 6, 4, 6, 2, 3,
                       5, 5, 2, 1, 5, 5, 3, 2, 1, 4, 4, 1, 6, 6, 4, 6, 2, 4, 3,
                       2, 5, 1, 3, 5, 4, 1, 2, 3, 6, 1])

###  Question 13

def test_13():
    print
    print "Question 13"

    print "Which arithmetic sum models the number of nodes in T after time step n?"
    print "1 + 2 + 4 + ... + 2^n"


### Question 14

def test_14():
    print
    print "Question 14"

    print "Math expression equivalent to the arithmetic sum in #13?"
    print "2^(n+1) - 1"


### Question 15

def test_15():
    print
    print "Question 15"

    print "Given that a tree height is the num of edges from the root, the num of leaves in a n-height tree = (n + 1)!"
    for i in range(1, 5):
        print "I.e.: in height", i, "there are up to (" + str(i) + " + 1)! =", math.factorial(i+1), "leaves"


### Question 16

def test_16():
    print
    print "Question 16"

    print "Breadth first search from square 15"
    print "15, 14, 21, 9, 16, 20, 13, 10, 17, 19, 7, 12, 4, 23, 1, 5, 2, 0"
    print "15, 21, 9, 16, 14, 20, 10, 17, 13, 19, 4, 23, 12, 7, 5, 1, 0, 2"
    print "15, 9, 14, 16, 21, 10, 13, 20, 17, 4, 7, 12, 19, 23, 5, 1, 0, 2"


### Question 17

def pick_a_number(board):
    """
    From 'Coins in a line' in leetcode
    http://articles.leetcode.com/coins-in-line/
    """
    if not board:
        return 0, 0

    if len(board) == 1:
        return board[0], 0

    a = pick_a_number(board[2:])[0]
    b = pick_a_number(board[1:-1])[0]
    c = pick_a_number(board[:-2])[0]

    my_max = max(board[0] + min(a, b), board[-1] + min(b, c))
    opponent_max = sum(board) - my_max

    return my_max, opponent_max

def test_17():
    print
    print "Question 17"
    print "For a description of the problem check http://articles.leetcode.com/coins-in-line/"

    print "test has to return (6, 5) ->?", pick_a_number([3, 5, 2, 1])

    test = [random.randint(1, 6) for i in range(6)]
    print "test", test, "; solution", pick_a_number(test)
    test = [random.randint(1, 6) for i in range(6)]
    print "test", test, "; solution", pick_a_number(test)
    test = [random.randint(1, 6) for i in range(6)]
    print "test", test, "; solution", pick_a_number(test)
    print
    print "problem board = [12, 9, 7, 3, 4, 7, 4, 3, 16, 4, 8, 12, 1, 2, 7, 11, 6, 3, 9, 7, 1]"
    print "solution", pick_a_number([12, 9, 7, 3, 4, 7, 4, 3, 16, 4, 8, 12, 1, 2, 7, 11, 6, 3, 9, 7, 1])
    print "problem board = [12, 9, 7, 3, 4, 7, 4, 7, 3, 16, 4, 8, 12, 1, 2, 7, 11, 6, 3, 9, 7, 1])"
    print "solution", pick_a_number([12, 9, 7, 3, 4, 7, 4, 7, 3, 16, 4, 8, 12, 1, 2, 7, 11, 6, 3, 9, 7, 1])


### Question 18

def test_18():
    print
    print "Question 18"

    print "1- O(k^n); 2- O(n^2); 3- O(n^1000); 4- O(n); 5- O(n!^n)"
    print "solution: 4 2 3 1 5"


### Question 19

def test_19():
    print
    print "Question 19"

    print "This is known as the handshaking lemma"
    print "https://en.wikipedia.org/wiki/Handshaking_lemma"
    print "solution: 2m"


### Question 20

def test_20():
    print
    print "Question 20"

    print "This solution for the transitive closure is using the Warshall's Algorithm"
    print "http://cs.winona.edu/lin/cs440/ch08-2.pdf"
    print "solution: R(k−1)[i,j] or (R(k−1)[i,k] and R(k−1)[k,j])"


### Question 21

def test_21():
    print
    print "Question 21"

    print "The Mystery algorithm looks for a subset of nodes where all the edges are included"
    print "solution: in g1, {1, 2, 4, 6} and {1, 3, 5, 7}"


### Question 22

def test_22():
    print
    print "Question 22"

    print "solution: in g2#1, only {1} as the algorithm searches for the minimum size set"
    print "solution: in g2#2, only {2, 4, 5}"


### Question 23

def test_23():
    print
    print "Question 23"

    print "A subset V′⊆V of minimum size such that every edge in E has at least one of its endpoints in V′."


### Question 24

def test_24():
    print
    print "Question 24"

    print "O(mn) is WRONG (!?)"
    print "O(n^2) is also WRONG"


### Question 25

from foc_q25_provided import mystery

def test_25():

    print
    print "Question 25"

    print "solution requested for GRAPH5 = 10"
    print "solution requested for GRAPH6 = 11"

    # Example graphs
    GRAPH1 = {1 : set([]), 2 : set([3, 7]), 3 : set([2, 4]), 4 : set([3, 5]), 5 : set([4, 6]), 6 : set([5, 7]), 7 : set([2, 6])}
    GRAPH2 = {1 : set([2, 3, 4, 5, 6, 7]), 2 : set([1]), 3 : set([1]), 4 : set([1]), 5 : set([1]), 6 : set([1]), 7 : set([1])}
    GRAPH3 = {0: set([4, 7, 10]), 1: set([5, 6]), 2: set([7, 11]), 3: set([10]), 4: set([0, 7, 11]), 5: set([1, 7]), 6: set([1]), 7: set([0, 2, 4, 5, 9, 11]), 8: set([9]), 9: set([7, 8]), 10: set([0, 3]), 11: set([2, 4, 7])}
    GRAPH4 = {0: set([4, 7, 10, 12, 13]), 1: set([5, 6, 12]), 2: set([7, 11, 12, 14]), 3: set([10, 14, 15]), 4: set([0, 7, 11, 12, 13, 14]), 5: set([1, 7, 15]), 6: set([1, 13]), 7: set([0, 2, 4, 5, 9, 11, 14]), 8: set([9, 14, 15]), 9: set([7, 8]), 10: set([0, 3]), 11: set([2, 4, 7]), 12: set([0, 1, 2, 4]), 13: set([0, 4, 6, 15]), 14: set([2, 3, 4, 7, 8]), 15: set([3, 5, 8, 13])}
    GRAPH5 = {0: set([4, 7, 10, 12, 13, 16]), 1: set([5, 6, 12]), 2: set([7, 11, 12, 14]), 3: set([10, 14, 15]), 4: set([0, 7, 11, 12, 13, 14, 17]), 5: set([1, 7, 15]), 6: set([1, 13]), 7: set([0, 2, 4, 5, 9, 11, 14, 18]), 8: set([9, 14, 15]), 9: set([7, 8, 19]), 10: set([0, 3]), 11: set([2, 4, 7]), 12: set([0, 1, 2, 4]), 13: set([0, 4, 6, 15, 16]), 14: set([2, 3, 4, 7, 8]), 15: set([3, 5, 8, 13]), 16: set([0, 13, 19]), 17: set([4]), 18: set([7]), 19: set([9, 16])}
    GRAPH6 = {0: set([4, 7, 10, 12, 13, 16]), 1: set([5, 6, 12]), 2: set([7, 11, 12, 14]), 3: set([10, 14, 15]), 4: set([0, 7, 11, 12, 13, 14, 17]), 5: set([1, 7, 15]), 6: set([1, 13]), 7: set([0, 2, 4, 5, 9, 11, 14, 18]), 8: set([9, 14, 15]), 9: set([7, 8, 19]), 10: set([0, 3]), 11: set([2, 4, 7]), 12: set([0, 1, 2, 4]), 13: set([0, 4, 6, 15, 16]), 14: set([2, 3, 4, 7, 8]), 15: set([3, 5, 8, 13]), 16: set([0, 13, 17, 19]), 17: set([4, 16]), 18: set([7]), 19: set([9, 16])}

    # Testing
#    print len(mystery(GRAPH1))     # answer should be 3
#    print len(mystery(GRAPH2))     # answer should be 1
#    print len(mystery(GRAPH3))     # answer should be 6
#    print len(mystery(GRAPH4))     # answer should be 9
#    print len(mystery(GRAPH5))
    print len(mystery(GRAPH6))


### Run tests
test_01()
test_02()
test_03()
test_04()
test_05()
test_06()
test_07()
test_08()
test_09()
test_10()
test_11()
test_12()
test_13()
test_14()
test_15()
test_16()
test_17()
test_18()
test_19()
test_20()
test_21()
test_22()
test_23()
test_24()
test_25()