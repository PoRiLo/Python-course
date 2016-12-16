"""
Introduction to Interactive Python - Part 1
Week 5 - June 2016

Miniproject: Classic Pong

@author: Ruben Dorado
http://www.codeskulptor.org/#user41_g9zQ80TveudFq5H.py

Now with green phosphore look! Feels like 1984!
With pause in game start for your convenience!
"""

# Imports
import simplegui
import random

# Global definitions
FIELD_WIDTH = 600.0
FIELD_HEIGHT = 400.0
BALL_RADIUS = 10.0
PAD_WIDTH = 10.0
PAD_HEIGHT = 80.0
left= False
right= True

# Helper functions
def spawn_ball(direction):
    """
    Spawns a new ball

    Input
    direction: boolean that indicates if the ball is to be spawned left or right
    """
    # Initialize global variables
    global ball_pos, ball_vel

    # Position the ball in the center of the screen and shoot it against the
    # player who won the last game with randomized initial velocity
    ball_pos = [FIELD_WIDTH / 2, FIELD_HEIGHT / 2]
    ball_vel = [3 + 3 * random.random(), - 2 - 3 * random.random()]
    if not direction:
        ball_vel[0] *= -1    # change direction to the left if required

# event handlers
def new_game():
    """
    New Game button handler

    Clears the screen and scores and starts a new game
    """
    global pad1_pos, pad2_pos, pad1_vel, pad2_vel
    global ball_pos, ball_vel
    global score1, score2
    global GameStop

    score1 = 0
    score2 = 0
    pad1_pos = [0.0, (FIELD_HEIGHT / 2) - PAD_HEIGHT / 2]
    pad2_pos = [FIELD_WIDTH - PAD_WIDTH, (FIELD_HEIGHT / 2) - PAD_HEIGHT / 2]
    pad1_vel = 0.0
    pad2_vel = 0.0

    GameStop = True

    spawn_ball(random.choice([False, True]))

def keydown(key):
    """Key down event handler"""
    global pad1_vel, pad2_vel

    if key == simplegui.KEY_MAP["w"]:
        pad1_vel += -8
    if key == simplegui.KEY_MAP["s"]:
        pad1_vel += 8
    if key == simplegui.KEY_MAP["up"]:
        pad2_vel += -8
    if key == simplegui.KEY_MAP["down"]:
        pad2_vel += 8

def keyup(key):
    """Key up event handler"""
    global pad1_vel, pad2_vel, GameStop

    if GameStop:
        if key == simplegui.KEY_MAP["space"]:
            GameStop = False

    if key == simplegui.KEY_MAP["w"]:
        pad1_vel += 8
    if key == simplegui.KEY_MAP["s"]:
        pad1_vel += -8
    if key == simplegui.KEY_MAP["up"]:
        pad2_vel += 8
    if key == simplegui.KEY_MAP["down"]:
        pad2_vel += -8

def draw(canvas):
    """Canvas draw handler"""
    global score1, score2
    global ball_pos, ball_vel, pad1_pos, pad1_vel, pad2_pos, pad2_vel

    # Drawing mid line and gutters, I use hexadecimal notation for the colors
    canvas.draw_line([FIELD_WIDTH / 2, 0],
                     [FIELD_WIDTH / 2, FIELD_HEIGHT],
                     1,
                     "#008800")
    canvas.draw_line([PAD_WIDTH, 0],
                     [PAD_WIDTH, FIELD_HEIGHT],
                     1,
                     "#008800")
    canvas.draw_line([FIELD_WIDTH - PAD_WIDTH, 0],
                     [FIELD_WIDTH - PAD_WIDTH, FIELD_HEIGHT],
                     1,
                     "#008800")
    canvas.draw_line([PAD_WIDTH, 0],
                     [FIELD_WIDTH - PAD_WIDTH, 0],
                     1,
                     "#008800")
    canvas.draw_line([PAD_WIDTH, FIELD_HEIGHT],
                     [FIELD_WIDTH - PAD_WIDTH, FIELD_HEIGHT],
                     1,
                     "#008800")

    # update paddle's vertical position, keep paddle on the screen
    if pad1_pos[1] <=0:
        pad1_pos[1] = 0
    if pad1_pos[1] >= FIELD_HEIGHT - PAD_HEIGHT:
        pad1_pos[1] = FIELD_HEIGHT - PAD_HEIGHT
    if pad2_pos[1] <=0:
        pad2_pos[1] = 0
    if pad2_pos[1] >= FIELD_HEIGHT - PAD_HEIGHT:
        pad2_pos[1] = FIELD_HEIGHT - PAD_HEIGHT

    pad1_pos[1] += pad1_vel
    pad2_pos[1] += pad2_vel

    # draw paddles
    canvas.draw_polygon((pad1_pos,
                        (pad1_pos[0] + PAD_WIDTH, pad1_pos[1]),
                        (pad1_pos[0] + PAD_WIDTH, pad1_pos[1] + PAD_HEIGHT),
                        (pad1_pos[0], (pad1_pos[1]) + PAD_HEIGHT)),
                         2, "#00cc00", "#008800")
    canvas.draw_polygon((pad2_pos,
                        (pad2_pos[0] + PAD_WIDTH, pad2_pos[1]),
                        (pad2_pos[0] + PAD_WIDTH, pad2_pos[1] + PAD_HEIGHT),
                        (pad2_pos[0], (pad2_pos[1]) + PAD_HEIGHT)),
                         2, "#00cc00", "#008800")

    # update ball, check if there is contact with the gutters or the pads
    if not GameStop:
        if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
            if pad1_pos[1] >= ball_pos[1] or pad1_pos[1] + PAD_HEIGHT <= ball_pos[1]:
                score2 += 1
                spawn_ball(right)
            else:
                ball_vel = [-1.1 * ball_vel[0], 1.1 * ball_vel[1]]
        if ball_pos[0] >= FIELD_WIDTH - PAD_WIDTH - BALL_RADIUS:
            if pad2_pos[1] >= ball_pos[1] or pad2_pos[1] + PAD_HEIGHT <= ball_pos[1]:
                score1 += 1
                spawn_ball(left)
            else:
                ball_vel = [-1.1 * ball_vel[0], 1.1 * ball_vel[1]]
        if ball_pos[1] <= BALL_RADIUS:
            ball_vel[1] *= -1
        if ball_pos[1] >= FIELD_HEIGHT - BALL_RADIUS:
            ball_vel[1] *= -1
        ball_pos = [ball_pos[0] + ball_vel[0], ball_pos[1] + ball_vel[1]]

    # draw ball
    canvas.draw_circle(ball_pos,
                       BALL_RADIUS,
                       2,
                       "#00cc00",
                       "#008800")

    # draw scores
    canvas.draw_text(str(score1),
                     ((FIELD_WIDTH / 3) - FIELD_HEIGHT / 18, FIELD_HEIGHT / 4),
                     FIELD_HEIGHT / 5,
                     "#00cc00",
                     "monospace")
    canvas.draw_text(str(score2),
                     ((FIELD_WIDTH * 2 / 3) - FIELD_HEIGHT / 18, FIELD_HEIGHT / 4),
                     FIELD_HEIGHT / 5,
                     "#00cc00",
                     "monospace")

    # draw the game start message if the game is stopped
    if GameStop:
        canvas.draw_polygon(((FIELD_WIDTH / 8 - 10, FIELD_HEIGHT * 5 / 6 - FIELD_HEIGHT / 12),
                             (FIELD_WIDTH * 7 / 8 + 20, FIELD_HEIGHT * 5 / 6 - FIELD_HEIGHT / 12),
                             (FIELD_WIDTH * 7 / 8 + 20, FIELD_HEIGHT * 5 / 6 + 20),
                             (FIELD_WIDTH / 8 - 10, FIELD_HEIGHT * 5 / 6 + 20)),
                            2,
                            "#008800",
                            "#001100")
        canvas.draw_text("press spacebar to start",
                         (FIELD_WIDTH / 8, FIELD_HEIGHT * 5 / 6),
                         FIELD_HEIGHT / 12,
                         "#00cc00",
                         "monospace")

# create frame
frame = simplegui.create_frame("Pong", FIELD_WIDTH, FIELD_HEIGHT)
ResetButton = frame.add_button("New Game", new_game, 200)
frame.set_canvas_background("#001100")
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame
new_game()
frame.start()