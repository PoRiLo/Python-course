"""
Created on Tue Jun 21 22:08:22 2016

@author: Ruben
"""
import solitaire_mancala
import bad_mancala
import homework4_question10 as tests


def find_error():
    """
    Compares the outcome of the bad implementation and the good implementation
    for all possible board configurations. Returns a configuration which has a
    wrong outcome in BadMancala
    """
    good_game = solitaire_mancala.SolitaireMancala()
    bad_game = bad_mancala.BadMancala()
    configurations = [[0, i, j, k, l, m, n] for i in range(10)
                                      for j in range(10)
                                      for k in range(10)
                                      for l in range(10)
                                      for m in range(10)
                                      for n in range(10)]

    for config in configurations:
        good_game.set_board(config)
        bad_game.set_board(config)
        good_outcome = good_game.plan_moves()
        bad_outcome = bad_game.plan_moves()
        if good_outcome != bad_outcome:
            print "Error in the outcome of configuration", config
            print "      Computed:", bad_outcome
            print "      Expected:", good_outcome
            break

    return config


def test_mancala():
    """
    Test code for the plan_moves method of Solitaire Mancala
    """
    good_game = solitaire_mancala.SolitaireMancala()
    bad_game = bad_mancala.BadMancala()
    error_found = False

    for config in tests.TEST_CASES:
        good_game.set_board(config)
        bad_game.set_board(config)
        good_outcome = good_game.plan_moves()
        bad_outcome = bad_game.plan_moves()
        if good_outcome == bad_outcome:
            print "Test for configuration", config, "passed."
        else:
            print "Test for configuration", config, "failed. Computed:", bad_outcome, "; Expected:", good_outcome
            error_found = True

    if not error_found:
        find_error()

test_mancala()

