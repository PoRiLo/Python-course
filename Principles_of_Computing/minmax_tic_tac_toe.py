"""
Principles of Computing - Part 2
Week 3 - June 2016

Miniproject: Min-max Tic-Tac-Toe

@author: Ruben Dorado
http://www.codeskulptor.org/#user39_8SspAYCLBp_18.py
"""

import random
#import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
#import codeskulptor
#codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}
CHECKLIST = [(1, 1), (0, 0), (0, 2), (2, 0), (2, 2), (0, 1), (1, 0), (1, 2), (2, 1)]

def mm_move(board, player):
    """
    Make a move on the board.

    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    score = 0
    next_move = (-1, -1)
    winner = board.check_win()

    if winner:
        score = SCORES[board.check_win()]
    else:
        # Get the possible moves from the current position
        empty_squares = board.get_empty_squares()
        next_player = provided.switch_player(player)

        # Calculating the score of each possible move through recursion
        for square in CHECKLIST:
            if square in empty_squares:
                new_board = board.clone()
                next_move =  (square[0], square[1])
                new_board.move(next_move[0], next_move[1], player)
                score = mm_move(new_board, next_player)[0]
                if score == SCORES[player]:
                    return score, next_move

        for square in CHECKLIST:
            if square in empty_squares:
                new_board = board.clone()
                next_move =  (square[0], square[1])
                new_board.move(next_move[0], next_move[1], player)
                score = mm_move(new_board, next_player)[0]
                if score == SCORES[provided.DRAW]:
                    return score, next_move

    return score, next_move

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
#start_player = random.choice([provided.PLAYERO, provided.PLAYERX])
#provided.play_game(move_wrapper, start_player, False)
#poc_ttt_gui.run_gui(3, start_player, move_wrapper, 1, False)

#print mm_move(provided.TTTBoard(3,
#                          False,
#                          [[provided.EMPTY, provided.PLAYERO, provided.PLAYERX],
#                           [provided.EMPTY, provided.PLAYERX, provided.PLAYERO],
#                           [provided.EMPTY, provided.EMPTY, provided.EMPTY]]),
#        provided.PLAYERX)
#
#print mm_move(provided.TTTBoard(2,
#                          False,
#                          [[provided.EMPTY, provided.EMPTY],
#                           [provided.EMPTY, provided.EMPTY]]),
#              provided.PLAYERO)
#
#print mm_move(provided.TTTBoard(3,
#                                False,
#                                [[provided.EMPTY, provided.EMPTY, provided.PLAYERX],
#                                 [provided.EMPTY, provided.EMPTY, provided.EMPTY],
#                                 [provided.EMPTY, provided.EMPTY, provided.EMPTY]]),
#                provided.PLAYERO) #expected score 0 but received (1, (0, 0))
#print mm_move(provided.TTTBoard(3,
#                                False,
#                                [[provided.EMPTY, provided.PLAYERX, provided.EMPTY],
#                                 [provided.PLAYERO, provided.PLAYERX, provided.EMPTY],
#                                 [provided.PLAYERO, provided.EMPTY, provided.EMPTY]]),
#                 provided.PLAYERO) #expected score -1 but received (1, (0, 0))
