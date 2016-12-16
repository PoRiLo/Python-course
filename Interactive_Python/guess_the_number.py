"""
Introduction to Interactive Programming - Part 1
Week 3 - June 2016

Miniproject: Guess the Number

@author: Ruben Dorado
http://www.codeskulptor.org/#user41_5LU3uvry7W7X5O9.py

PLEASE READ WHEN GRADING!!!
I intentionally modify the game's suggested behaviour. When
you play this game in common language, generally, you choose
between 1 and [limit], let's say between 1 and 10. Including
10 but not including 0. The mechanics of the game are exactly
the same save for that +1 in the upper and lower limits.
"""

#importing modules and starting global variables

import math
import random
import simplegui

interval = 100
secret_number = 0
num_guesses = 0


# helper function to start and restart the game

def new_game(new_interval):
    """
    Selects a new number in the interval [new_interval] and
    starts a new game
    """

    global secret_number, num_guesses
    secret_number = random.randint(1, new_interval)
    num_guesses = int(math.log(new_interval, 2)) + 1

    print
    print '=============================================='
    print
    print 'New game begins! Choose a number between 1 and', new_interval
    print 'You have', num_guesses, 'guesses'
    print


# define event handlers for control panel

def range_100():
    """Click event handler for the range_100 button"""
    global interval

    interval = 100
    new_game(interval)


def range_1000():
    """Click event handler for the range_1000 button"""
    global interval

    interval = 1000
    new_game(interval)


def custom_range(custom_interval):
    """Enter text event handler for the custom_range text control"""
    global interval

    interval = int(custom_interval)
    new_game(interval)


def input_guess(guess):
    """
    Enter text event handler for the input_guess text control
    It compares the entry to the secret number and prints the
    outcome
    """
    global num_guesses

    player_guess = int(guess)
    print 'Your guess is', player_guess

    if player_guess == secret_number:
        print 'Correct! Congratulations, human!'
        new_game(interval)
        return
    elif player_guess < secret_number:
        print 'Nope! Higher!'
    elif player_guess > secret_number:
        print 'Nay, lower!'

    num_guesses -= 1
    if num_guesses == 0:
        print 'You have no guesses left. You lose!'
        print
        print 'The secret number was', secret_number
        print
        new_game(interval)
    else:
        print 'You have', num_guesses, 'guesses left'
        print

# create frame
f = simplegui.create_frame("Guess the number", 0, 300)

# register event handlers for control elements and start frame
f.add_button('Range 1 - 100', range_100, 200)
f.add_button('Range 1 - 1000', range_1000, 200)
f.add_input('Or you can choose your own interval. Type the higher limit of your range here:', custom_range, 200)
f.add_label('')
f.add_input('Your guess here:', input_guess, 200)

f.start()

# call new_game
new_game(interval)