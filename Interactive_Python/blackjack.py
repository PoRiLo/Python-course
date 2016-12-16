"""
Introduction to Interactive Programming - Part 2
Week 2 - June 2016

Miniproject: Blackjack

@author: Ruben Dorado
http://www.codeskulptor.org/#user41_D3uVrcMq0XHS9k3.py
"""

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# positions for drawing the cards
PPOS = (48, 336)
DPOS = (48, 96)

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
          '9': 9, 'T': 10, 'J': 10, 'Q': 10, 'K': 10}

# initialize other global variables
in_play = False
outcome = ""
score = 100
bet = 10

# define card class
class Card:
    """
    Class that defines object type 'Card'

    Properties: suit, _rank

    Methods: get_suit, get_rank, draw
    """
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self._suit = suit
            self._rank = rank
        else:
            self._suit = None
            self._rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self._suit + self._rank

    def get_suit(self):
        """
        Returns the card's suit
        """
        return self._suit

    def get_rank(self):
        """
        Returns the card's rank
        """
        return self._rank

    def draw(self, canvas, pos):
        """
        Draws the Card object in the canvas in the position 'pos'

        Parameters:
        canvas: a canvas objet (GUI)
        pos: a tuple in the form (x, y) indicating the position where the
            card is to be drawn
        """
        card_loc = [CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self._rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self._suit)]
        card_pos = [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]]
        canvas.draw_image(card_images,
                          card_loc, CARD_SIZE,
                          card_pos, CARD_SIZE)

# define hand class
class Hand:
    """
    Class that defines object type 'Hand', being a collection of 'Card' objects

    Properties: cards

    Methods: add_card, get_value, draw
    """
    def __init__(self):
        self._cards = []

    def __str__(self):
        hand_str = '['
        for card in self._cards:
            hand_str += str(card) + ', '
        hand_str = hand_str[:-2]
        hand_str += ']'
        return hand_str

    def add_card(self, card):
        """
        Appends 'card' to the cards list

        Parameters:
        card: a card
        """
        self._cards.append(card)

    def get_value(self):
        """
        Returns the value of the hand
        """
        hand_value = 0
        for card in self._cards:
            hand_value += VALUES[card.get_rank()]
            if card.get_rank() == 'A' and hand_value <= 11:
                hand_value += 10
        return hand_value

    def draw(self, canvas, pos):
        """
        Draws the Hand object in the canvas, in the position 'pos'

        Parameters:
        canvas: a canvas objet (GUI)
        pos: a tuple in the form (x, y) indicating the position where the
            card is to be drawn
        """
        y = 400
        x = 60
        for card in self._cards:
            x += 90
            card.draw(canvas, (x, y))

# define deck class
class Deck:
    """
    Class that defines the object type 'Deck'

    Properties:
    pool: a list of all the cards present in the deck

    Methods: shuffle, deal_card
    """
    def __init__(self):
        self._pool = []
        for s in SUITS:
            for r in RANKS:
                self._pool.append(Card(s, r))

    def __str__(self):
        deck_str = 'The deck is: ['
        for d in self._pool:
            deck_str += str(d) + ', '
        deck_str = deck_str[:-2]
        deck_str += ']'
        return deck_str

    def shuffle(self):
        """
        Shuffles the deck
        """
        random.shuffle(self._pool)

    def deal_card(self):
        """
        Takes a card from the deck
        """
        return self._pool.pop()

#define event handlers for buttons
def deal():
    """
    Starts a new game by shuffling the deck and dealing new cards to both the
    player and the bank
    """
    global deck, dealer, player, score, outcome, in_play

    deck = Deck()
    dealer = Hand()
    player = Hand()
    outcome = ""
    in_play = True
    score -= bet

    deck.shuffle()
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())

    outcome = 'You bet $' + str(bet) + '. Your new hand is ' + str(player.get_value()) + '. Hit or stand?'

def hit():
    """
    Deals a new card from the deck to the player
    """
    global deck, player, score, outcome, in_play

    # if the hand is in play, hit the player
    if in_play:
        player.add_card(deck.deal_card())
        outcome = 'Your hand is ' + str(player.get_value()) + '. Hit or stand?'
        if player.get_value() > 21:
            outcome = "Bummer! You have busted! You lost your $" + str(bet) + ". Deal again?"
            in_play = False
    else:
        outcome = 'New deal? Press "Deal".'

def stand():
    """
    Stands player hand and draws cards for the bank's hand
    Checks the outcome and stops the game
    """
    global deck, player, score, outcome, in_play

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
    else:
        outcome = 'New deal? Press "Deal".'
        return

    # checks the outcome of the game, assign a message, update in_play and score
    if dealer.get_value() > 21:
        outcome = "Dealer busted! You win $" + str(bet) + ". Deal again?"
        score += 2 * bet
    elif dealer.get_value() < player.get_value():
        outcome = str(player.get_value()) + " vs " + str(dealer.get_value()) \
        + ". You win $" + str(bet) + "! Draw again?"
        score += 2 * bet
    elif dealer.get_value() == player.get_value():
        outcome = str(player.get_value()) + " vs " + str(dealer.get_value()) + \
        ". Dealer wins ties, sorry! You lost your $" + str(bet) + ". Draw again?"
    else:
        outcome = str(player.get_value()) + " vs " + str(dealer.get_value()) + \
        ". Dealer wins! You lost your $" + str(bet) + ". Draw again?"

    in_play = False

def change_bet(new_bet):
    """
    When you introduce an amount and hit 'Enter' it places a new bet. If
    in_game is True, player loses the current game.
    """
    global bet
    bet = int(new_bet)
    deal()

# draw handler
def draw(canvas):
    # draw fixed text
    canvas.draw_text('Blackjack', (200, 48), 48, '#ff8800')
    canvas.draw_text('Player', (PPOS[0], PPOS[1] - 10), 24, '#000077')
    canvas.draw_text('Dealer', (DPOS[0], DPOS[1] - 10), 24, '#000077')

    # draw player's and dealer's hands
    ppoint = list(PPOS)
    for pc in player._cards:
        pc.draw(canvas, ppoint)
        ppoint[0] += CARD_SIZE[0] * 1.25

    dpoint = list(DPOS)
    for dc in dealer._cards:
        dc.draw(canvas, dpoint)
        dpoint[0] += CARD_SIZE[0] * 1.25
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (DPOS[0] + CARD_BACK_CENTER[0], DPOS[1] + CARD_BACK_CENTER[1]), CARD_BACK_SIZE)

    # draw score, bet and outcome messages
    bank_color = '#000000'
    if score < 0: bank_color = '#cc0000'
    canvas.draw_text('$' + str(score), (PPOS[0] + 100, PPOS[1] - 10), 24, bank_color)
    canvas.draw_text('Bet: $' + str(bet), (DPOS[0] + 100, DPOS[1] - 10), 24, '#000000')
    canvas.draw_text(outcome, (36, 250), 20, '#ffffff')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 480)
frame.set_canvas_background("#009900")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)
frame.add_input("Change bet?", change_bet, 200)
# get things rolling
deal()
frame.start()
