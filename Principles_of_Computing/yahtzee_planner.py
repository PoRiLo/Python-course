"""
Principles of Computing - Part 1
Week 4 - June 2016

Miniproject: Yahtzee planner
Simplifications: only allow discard and roll, only score against upper level

@author: Ruben Dorado
http://www.codeskulptor.org/#user41_C5PDKEIJVUfS7Lx.py
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    """

    max_score = 0

    for slot in range(len(hand)):
        total = 0
        for die in hand:
            if die == hand[slot]:
                total += die
        if total > max_score:
            max_score = total

    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    count = 0.0
    accumulated_value = 0.0
    possible_outcomes = gen_all_sequences(range(1, num_die_sides + 1),
                                          num_free_dice)

    for outcome in possible_outcomes:
        full_hand = list(held_dice)
        for die in outcome:
            full_hand.append(die)
        full_hand.sort()
        hand_tuple = tuple(full_hand)
        outcome_score = score(hand_tuple)
        accumulated_value += outcome_score
        count += 1

    return accumulated_value / count


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """

    binary_mask = []
    dice = len(hand)

    # creating a binary mask
    for idx in range(2**dice):
        binary_mask.append(str(bin(idx))[2:].rjust(dice, '0'))

    # applying the binary mask to the hand
    all_holds = set([()])
    for mask in binary_mask:
        hold = []
        for die in range(dice):
            if mask[die] == '1':
                hold.append(hand[die])
            hold.sort()
            all_holds.add(tuple(hold))

    return all_holds


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    best_hold = (0.0, ())

    for possible_hold in gen_all_holds(hand):
        num_free_dice = len(hand) - len(possible_hold)
        this_hold = (expected_value(possible_hold, num_die_sides, num_free_dice), possible_hold)
        if this_hold[0] > best_hold[0]:
            best_hold = this_hold

    return best_hold


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (5, 5, 5, 6, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand
    print "is to hold", hold
    print "with expected score", hand_score


#run_example()

#import user39_2H7QHvgblW_23 as my_testsuite
#my_testsuite.test_score(score)
#my_testsuite.test_expected_value(expected_value)
#my_testsuite.test_gen_all_holds(gen_all_holds)
#my_testsuite.test_strategy(strategy)
