#"""
#Recursion according to the "Cat in the Hat"
#"""
#count = 0
#
#def get_next_cat(current_cat):
#    """
#    Helper function to get next cat
#    """
#    if current_cat == "Cat in the Hat":
#        return "Little Cat A"
#    elif current_cat != "Little Cat Z":
#        return "Little Cat " + chr(ord(current_cat[-1]) + 1)
#    else:
#        return "Voom"
#
#
#def clean_up(helper_cat):
#    """
#    Recursive function that prints out story
#    """
#    global count
#
#    count += 1
#
#    if helper_cat == "Voom":
#        print helper_cat + ": I got this. Mess is all cleaned up!"
#    else:
#        next_cat = get_next_cat(helper_cat)
#        print helper_cat + ": I'll have", next_cat, "clean up!"
#        clean_up(next_cat)
#
## get those cats to work!!!!!
##clean_up("Cat in the Hat")
##print "Calls to clean_up =", count
##print
##count = 0
#
#def fib(num):
#    global count
#    count +=1
#    if num == 0:
#        return 0
#    elif num == 1:
#        return 1
#    else:
#        return fib(num - 1) + fib(num - 2)
#
#def run_fib(n):
#    global count
#    for i in range(n):
#        count = 0
#        num = fib(i)
#        print "fib(" + str(i) +") = " + str(num) + "; calls = "+ str(count)
#
##run_fib(15)
##print
##count = 0
#
#def memoized_fib(num, memo_dict):
#    global count
#    count +=1
#    if num in memo_dict:
#        return memo_dict[num]
#    else:
#        sum1 = memoized_fib(num - 1, memo_dict)
#        sum2 = memoized_fib(num - 2, memo_dict)
#        memo_dict[num] = sum1 + sum2
#        return sum1 + sum2
#
#def run_memoized_fib(n):
#    global count
#    for i in range(n):
#        count = 0
#        num = memoized_fib(i, {0 : 0, 1 : 1})
#        print "memoized_fib(" + str(i) +") = " + str(num) + "; calls = "+ str(count)
#
##run_memoized_fib(15)
#
#def permutations(outcomes):
#    if len(outcomes) == 1:
#        return outcomes[0]
#    else:
#        rest_permutations = set(outcomes[1:])
#        for perm in rest_permutations:
#            for position in range(len(perm)):
#                perm.add(outcomes[0])
#
#
#def my_format(t):
#
#    # finding how many hours, minutes, seconds and tenths there are in t
#    hours = int(t / 36000)
#    minutes = int(t / 600) - hours * 60
#    seconds = int(t / 10) - minutes * 60 - hours * 3600
#    tenths = t % 10
#
#    # checking if we need leading 0s for minutes and/or seconds
#    minutestr = str(minutes)
#
#    if int(seconds/10) == 0:
#        secondstr = '0' + str(seconds)
#    else:
#        secondstr = str(seconds)
#
#    # formats the timer in a nice h:mm:ss.t format
#    return minutestr + ':' + secondstr + '.' + str(tenths)
#
#def format(t):
#    a = (t // 600)
#    b = (((t % 600) / 10) / 10)
#    c = '0'
#    if (t > 10):
#        c = str(t)[(-2)]
#    d = str(t)[(-1)]
#    formatedTime = (((((str(a) + ':') + str(b)) + c) + '.') + d)
#    return formatedTime
#
#
#TEST_CASES = [0, 10, 99, 100, 599, 613, 670, 3599, 3675, 5999]
#
#for TEST in TEST_CASES:
##    print my_format(TEST)
#    print format(TEST)
#
#for test in range(6000):
#    outcome = format(test)
#    my_outcome = my_format(test)
#    if outcome != my_outcome:
#        print 'error at', test
#        break

#"""
#Functions to enumerate sequences of outcomes
#Repetition of outcomes is allowed
#"""
#
#
#def gen_all_sequences(outcomes, length):
#    """
#    Iterative function that enumerates the set of all sequences of
#    outcomes of given length
#    """
#
#    ans = set([()])
#    for dummy_idx in range(length):
#        temp = set()
#        for seq in ans:
#            for item in outcomes:
#                new_seq = list(seq)
#                new_seq.append(item)
#                temp.add(tuple(new_seq))
#        ans = temp
#    return ans
#
#
## example for digits
#def run_example1():
#    """
#    Example of all sequences
#    """
#    outcomes = set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
#    #outcomes = set(["Red", "Green", "Blue"])
#    #outcomes = set(["Sunday", "Mondy", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
#    #outcomes = set(["Heads", "Tails"])
#
#    length = 5
#    seq_outcomes = gen_all_sequences(outcomes, length)
#    print "Computed", len(seq_outcomes), "sequences of", str(length), "outcomes"
##    print "Sequences were", seq_outcomes
#
##run_example1()
#
#
#def gen_sorted_sequences(outcomes, length):
#    """
#    Function that creates all sorted sequences via gen_all_sequences
#    """
#    all_sequences = gen_all_sequences(outcomes, length)
#    sorted_sequences = [tuple(sorted(sequence)) for sequence in all_sequences]
#    return set(sorted_sequences)
#
#
#def run_example2():
#    """
#    Examples of sorted sequences of outcomes
#    """
#    # example for digits
#    outcomes = set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
#    #outcomes = set(["Red", "Green", "Blue"])
#    #outcomes = set(["Sunday", "Mondy", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
#    #outcomes = set(["Heads", "Tails"])
#
#    length = 5
#    seq_outcomes = gen_sorted_sequences(outcomes, length)
#    print "Computed", len(seq_outcomes), "sorted sequences of", str(length) ,"outcomes"
##    print "Sequences were", seq_outcomes
#
##run_example2()
#
#def question_2():
#    outcomes = set([1.0, 2.0, 3.0, 4.0])
#    length = 4
#    base = 0
#    seq_outcomes = gen_all_sequences(outcomes, length)
#    for outcome in seq_outcomes:
#        base += outcome[0]*outcome[1]
#    return base/len(seq_outcomes)
#
##print question_2()
#
#
#def gen_permutations(outcomes, num_trials):
#    """
#    Iterative function that enumerates the set of all sequences of
#    outcomes of given length
#    """
#
#    ans = set([()])
#    for dummy_idx in range(num_trials):
#        temp = set()
#        for seq in ans:
#            for item in outcomes:
#                if item not in seq:
#                    new_seq = list(seq)
#                    new_seq.append(item)
#                    temp.add(tuple(new_seq))
#        ans = temp
#    return ans
#
#def run_example3():
#    """
#    Example of all permutations
#    """
#    outcomes = set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
#    #outcomes = set(["Red", "Green", "Blue"])
#    #outcomes = set(["Sunday", "Mondy", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
#    #outcomes = set(["Heads", "Tails"])
#
#    num_trials = 5
#    seq_outcomes = gen_permutations(outcomes, num_trials)
#    print "Computed", len(seq_outcomes), "permutations of", str(num_trials), "outcomes"
#    #print "Sequences were", seq_outcomes
#
##run_example3()
#
#import math
#
#def permutations(m, n):
#    return math.factorial(m)/math.factorial(m - n)
#
#def combinations(m, n):
#    return math.factorial(m)/(math.factorial(n)*math.factorial(m - n))
#
##print 12.0/permutations(10.0, 5.0)
#
#def question_8():
#    return float(combinations(4.0, 1.0) * combinations (13.0, 5.0)) \
#    / float(combinations(52.0, 5.0))
#
#print question_8()

def timeformat(t):
    """
    Takes an amount of tenths of second and formats it like 0:00:00.0

    t= tenths of second
    """

    # finding how many hours, minutes, seconds and tenths there are in t
    hours = t // 36000
    minutes = t // 600 % 60
    seconds = t // 10 % 60
    tenths = t % 10

    # checking if we need leading 0s for minutes and/or seconds
    if int(minutes/10) == 0:
        minutestr = '0' + str(minutes)
    else:
        minutestr = str(minutes)

    if int(seconds/10) == 0:
        secondstr = '0' + str(seconds)
    else:
        secondstr = str(seconds)

    # formats the timer in h:mm:ss.t format
    return str(hours) + ':' + minutestr + ':' + secondstr + '.' + str(tenths)

print timeformat(75097)