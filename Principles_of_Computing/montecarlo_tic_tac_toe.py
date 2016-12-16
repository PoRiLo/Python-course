"""
Principles of Computing - Part 1
Week 3 - June 2016

Miniproject: Montecarlo Tic-Tac-Toe


@author: Ruben Dorado
http://www.codeskulptor.org/#user41_HfEeEgP7aLH1SK7_2.py
http://www.codeskulptor.org/#user39_xOiI9JFstGCcAgX.py
    - from another student, interesting way of building lists/dictionaries
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
# do not change their names.
NTRIALS = 25       # Number of trials to run
SCORE_CURRENT = 2  # Score for squares played by the current player
SCORE_OTHER = 1    # Score for squares played by the other player

EMPTY = 1
PLAYERX = 2
PLAYERO = 3
DRAW = 4

def mc_trial(board, player):
    """
    This function takes a current board and the next player to move.
    The function should play a game starting with the given player by making
    random moves, alternating between players. The function should return when
    the game is over. The modified board will contain the state of the game, so
    the function does not return anything. In other words, the function should
    modify the board input.
    """

    winner = None

    # Run game
    while not winner:
        # Move
        empty_squares = board.get_empty_squares()
        random_square = random.choice(empty_squares)
        board.move(random_square[0], random_square[1], player)

        # Update state
        winner = board.check_win()
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores, a board from a completed game,
    and which player the machine player is. The function score the
    completed board and update the scores grid.
    """
    # first, let's determine who's who
    winner = board.check_win()
    other = provided.switch_player(player)
    loser = provided.switch_player(winner)

    # changing signs whether we lose or win
    if winner == player:
        winner_score = SCORE_CURRENT
        loser_score = -SCORE_OTHER
    elif winner == other:
        winner_score = SCORE_OTHER
        loser_score = -SCORE_CURRENT
    else:
        return

    # cycling through the board and counting points
    for tic in range(board.get_dim()):
        for tac in range(board.get_dim()):
            if board.square(tic, tac) == winner:
                scores[tic][tac] += winner_score
            if board.square(tic, tac) == loser:
                scores[tic][tac] += loser_score

def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores. The function
    find all of the empty squares with the maximum score and randomly
    return one of them as a (row, column) tuple.
    """
    # Calls the provided function to create a list of empty squares
    empty_squares = board.get_empty_squares()

    # Creates a dictionary with the scores for each empty square
    scores_dict = dict([[square, scores[square[0]][square[1]]]
                        for square in empty_squares])

    # Finds the max score and remove from dictionary all other squares
    max_score = max(scores_dict.values())

    for key, value in scores_dict.items():
        if value < max_score:
            scores_dict.pop(key)

    # choose a random key (tuple) from these dictionary of maximums
    return random.choice(scores_dict.keys())

def mc_move(board, player, trials):
    """
    This function takes a current board, which player the machine player is,
    and the number of trials to run. The function use the Monte Carlo
    simulation to return a move for the machine player in the form of a
    (row, column) tuple.
    """
    # starts a new scores grid
    scores_grid = [[0 for dummy_i in range(board.get_dim())]
                      for dummy_j in range(board.get_dim())]

    # cicles through trials number of iterations and updates the scores
    for dummy in range(trials):
        test_board = board.clone()
        mc_trial(test_board, player)
        mc_update_scores(scores_grid, test_board, player)

    # returns the best move calculated
    return get_best_move(board, scores_grid)


# Test game with the console or the GUI. Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
