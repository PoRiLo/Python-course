"""
Introduction to Interactive Programming - Part 2
Week 4 - June 2016

Miniproject: Rice Rocks

@author: Ruben Dorado
http://www.codeskulptor.org/#user41_V7MDQE6caI_0.py

PLEASE READ!
I added a few upgrades to the game. Mainly, a two-player mode (hey we have a
whole class for ships, why not to use it?). You can play in collaborative mode
or in arena mode. It's much funnier to kick your brother ass than brainlessly
demolishing asteroids, to be true.
"""

import simplegui
import math
import random

# global constants for fine-tuning the game settings
WIDTH = 800
HEIGHT = 600
THRUST_POWER = .15
ANGLE_VEL_MODULE = .125
HULL = 5
MISSILE_VEL = 15
RATE_OF_FIRE = 10
MISSILE_LIFESPAN = 35
ROCK_VEL = 6
MODES = {# : ["mode text", rock_limit, tick_rate]
         0 : ["Game Over", 0, 999],
         1 : ["1 player", 12, 5],
         2 : ["2 players", 18, 3],
         3 : ["  Arena  ", 4, 20]}

# initializing global variables
time = 0
tick = 0
game_mode = 0
rock_limit = 12
tick_rate = 4
started = False
players = set([])
rocks = set([])
missiles = set([])
explosions = set([])
score = [0, 0]



# define Image class
class ImageInfo:
    """Class to handle images"""

    def __init__(self, center, size, radius = 0, lifespan = None, columns = 1, rows = 1):
        """Initializes the image"""
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.columns = columns
        self.rows = rows

    def get_center(self):
        """Returns the center of the image"""
        return self.center

    def get_size(self):
        """Returns the size of the image"""
        return self.size

    def get_radius(self):
        """Returns the collision radius of the image"""
        return self.radius

    def get_lifespan(self):
        """Returns the lifespan of the image"""
        return self.lifespan

    def get_columns(self):
        """Returns the columns the image occupy"""
        return self.columns

    def get_rows(self):
        """Returns the rows the image occupy"""
        return self.rows


# Ship class
class Ship:
    """Ship Class"""

    def __init__(self, pos, vel, angle, image, info, fire, hull, player):
        """Initializes a ship"""
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.collided = False
        self.fire = False
        self.hull = hull    # the hull is equivalent to the number of lives
        self.player = player
        self.shield = 180    # the ship is spawned with the shield on
        self.score = 0
        self.parent = None

    def get_radius(self):
        """Returns the collision radius of the ship"""
        return self.radius

    def ship_thrust(self, gas = False):
        """Switches on and off the ship's thrusters"""
        self.thrust = not self.thrust
        if gas:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()

    def update_angle_vel(self, a_vel):
        """Updates the ship angle"""
        self.angle_vel += a_vel

    def draw(self,canvas):
        """Draws the ship in the canvas"""
        if self.thrust:    # draws the ship with burners on
            canvas.draw_image(self.image,
                              [self.image_center[0] + self.image_size[0], self.image_center[1]],
                              self.image_size,
                              self.pos,
                              self.image_size,
                              self.angle)
        else:    # draws the ship with burners off
            canvas.draw_image(self.image,
                              self.image_center,
                              self.image_size,
                              self.pos,
                              self.image_size,
                              self.angle)
        if self.shield > 0:    # if the shield is active, draws a semitransparent color cylcling circle around the ship
            color = 'hsla(' + str((time + 20 * self.player) * 6 % 360) + ', 50%, 80%, 0.3)'
            canvas.draw_circle(self.pos, self.radius + 15, 6, color, color)

    def update(self):
        """Updates the ship status"""
        global missiles, score

        if started:    # If a game is ongoing

            # Displacement and rotation of the ship
            self.angle += self.angle_vel    # rotates the ship
            for d in [0, 1]:
                if self.thrust:
                    self.vel[d] += THRUST_POWER * angle_to_vector(self.angle)[d]    # accelerates the ship in the direction it's facing
                self.pos[d] += self.vel[d]    # displaces ship
                self.vel[d] *= .99    # "friction" term to eventually stop the ship if uncomanded

            # Shooting missiles
            if self.fire and (time % RATE_OF_FIRE == 0):    # While the fire button is pressed, the ship is continuelly shooting.
                am_pos = [.0, .0]
                am_vel = [.0, .0]
                if (time // RATE_OF_FIRE) % 2 == 0:    # alternates left and right gun
                    gun = 1
                else:
                    gun = -1
                if self.player == 0:    # draws a different missile icon for each player
                    missile_image = missile1_image
                    missile_info = missile1_info
                elif self.player == 1:
                    missile_image = missile2_image
                    missile_info = missile2_info
                for dim in [0, 1]:    # gets the parameters of position, angle and velocity for the missile and creates it
                    am_pos[dim] = self.pos[dim] + .8 * self.radius * angle_to_vector(self.angle + gun * .7)[dim]
                    am_vel[dim] = self.vel[dim] + MISSILE_VEL * angle_to_vector(self.angle)[dim]
                missile = Sprite(am_pos,
                                   am_vel,
                                   self.angle,
                                   0,
                                   missile_image,
                                   missile_info,
                                   missile_sound,
                                   self)
                missiles.update([missile])    # adds the missile to the proper set

            # Updating the ship's shield
            if self.shield > 0: self.shield -= 1    # if the shield is active, decrease its time counter

            # Toroidal space: warping the ship through the edges of the screen
            if self.pos[0] < -self.radius:    # wraps the objects around the edges. I choose to leave the object dissapear completely in one side before spawning it in the other corner of the screen
                self.pos[0] = WIDTH + self.radius
            if self.pos[0] > WIDTH + self.radius:
                self.pos[0] = -self.radius
            if self.pos[1] < -self.radius:
                self.pos[1] = HEIGHT + self.radius
            if self.pos[1] > HEIGHT + self.radius:
                self.pos[1] = -self.radius

            # Updating the score
            score[self.player] = self.score    # updates the gobal score variable to reflect the current player score



# Sprite class
class Sprite:
    """Sprite Class"""

    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None, parent = None):
        """Initializes the Sprite object"""
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.columns = info.get_columns()
        self.rows = info.get_rows()
        self.age = 0
        self.parent = parent    # tracks who fired a missile
        self.collided = False
        if sound:
            sound.rewind()
            sound.play()

    def get_radius(self):
        """Returns the collision radius of the Sprite"""
        return self.radius

    def draw(self, canvas):
        """Draws the sprite on the canvas"""
        current_i = ((self.age / 4) % self.columns) // 1
        current_j = ((self.age / 4) % self.rows) // 1
        canvas.draw_image(self.image,
                          [self.image_center[0] + current_i * self.image_size[0], self.image_center[1] + current_j * self.image_size[0]],
                          self.image_size,
                          self.pos,
                          self.image_size,
                          self.angle)

    def update(self):
        """Updates the sprite status"""
        self.age += 1
        self.angle += self.angle_vel
        for d in [0, 1]:
            self.pos[d] += self.vel[d]
        if self.pos[0] < -self.radius:
            self.pos[0] = WIDTH + self.radius
        if self.pos[0] > WIDTH + self.radius:
            self.pos[0] = -self.radius
        if self.pos[1] < -self.radius:
            self.pos[1] = HEIGHT + self.radius
        if self.pos[1] > HEIGHT + self.radius:
            self.pos[1] = -self.radius

# helper functions to handle transformations
def angle_to_vector(ang):
    """Returns the [x, y] parameter of angle ang"""
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    """Returns the distance between two points p and q"""
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def collision_detector(group1, group2):
    """
    Checks if the objects in group1 are in collision with objects in group2
    Updates the _collided attribute of objects in group1 and group2
    """
    for i in group1:
        for j in group2:
            if not i == j:    # to avoid an object "colliding" against itself
                if dist(i.pos, j.pos) < i.get_radius() + j.get_radius():
                    if not j.parent == i:    # to avoid a ship hit itself with its own missiles
                        i.collided = True
                        j.collided = True

def explode(element):
    """Creates an explosion sprite and adds it to the sprites group"""
    an_explosion = Sprite(element.pos,
                          [element.vel[0] // 4, element.vel[1] // 4],
                          element.angle,
                          0,
                          explosion_image,
                          explosion_info,
                          explosion_sound)
    explosions.update([an_explosion])

def update_sprites(group, canvas):
    """
    Cicles through the elements in a group, updates and draws them in the canvas
    """
    for element in group:
        element.update()
        if element.age > element.lifespan:
            group.remove(element)
        else:
            element.draw(canvas)

def game_over():
    """Stops the game and summons the splash screen again."""
    global game_mode, rocks, rock_limit, tick_rate, started, players, time
    game_mode = 0
    rock_limit = MODES[game_mode][1]
    tick_rate = MODES[game_mode][2]
    soundtrack.rewind()
    started = 0
    time = 0
    rocks = set([])

# Event handlers
def one_player_button():
    """
    One Player Button handler
    Applies the settings for a single player game
    """
    global game_mode, rock_limit, tick_rate, started, players, player1, rocks,\
           missiles, explosions, time, score
    game_mode = 1
    rock_limit = MODES[game_mode][1]
    tick_rate = MODES[game_mode][2]
    started = False
    rocks = set([])
    missiles = set([])
    explosions = set([])
    time = 0
    score = [0, 0]
    rock_timer.stop()
    player1 = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], -math.pi/2, ship1_image,
                   ship1_info, False, HULL, 0)
    players = set([player1])


def two_player_button():
    """
    Two Player Button handler
    Applies the settings for a two players collaborative game
    """
    global game_mode, rock_limit, tick_rate, started, players, player1,\
           player2, rocks, missiles, explosions, time, score
    game_mode = 2
    rock_limit = MODES[game_mode][1]
    tick_rate = MODES[game_mode][2]
    started = False
    rocks = set([])
    missiles = set([])
    explosions = set([])
    time = 0
    score = [0, 0]
    rock_timer.stop()
    player1 = Ship([WIDTH / 3, HEIGHT / 2], [0, 0], -math.pi/2, ship1_image,
                   ship1_info, False, HULL, 0)
    player2 = Ship([2 * WIDTH / 3, HEIGHT / 2], [0, 0], math.pi/2, ship2_image,
                   ship2_info, False, HULL, 1)
    players = ([player1, player2])


def two_player_arena_button():
    """
    Arena Button handler
    Applies the settings for a player vs player game. Beware the rocks too!
    """
    global game_mode, rock_limit, tick_rate, started, players, player1, \
           player2, rocks, missiles, explosions, time, score
    game_mode = 3
    rock_limit = MODES[game_mode][1]
    tick_rate = MODES[game_mode][2]
    started = False
    rocks = set([])
    missiles = set([])
    explosions = set([])
    time = 0
    score = [0, 0]
    rock_timer.stop()
    player1 = Ship([WIDTH / 3, HEIGHT / 2], [0, 0], -math.pi/2, ship1_image,
                   ship1_info, False, HULL, 0)
    player2 = Ship([2 * WIDTH / 3, HEIGHT / 2], [0, 0], math.pi/2, ship2_image,
                   ship2_info, False, HULL, 1)
    players = ([player1, player2])


def keydown(key):
    """Keyboard input handler. Keydown event."""

    if started:
        if not game_mode == 0:    # player 1 controls
            if key == simplegui.KEY_MAP['a']:
                player1.update_angle_vel(-ANGLE_VEL_MODULE)
            elif key == simplegui.KEY_MAP['d']:
                player1.update_angle_vel(ANGLE_VEL_MODULE)
            elif key == simplegui.KEY_MAP['w']:
                player1.ship_thrust(True)
            elif key == simplegui.KEY_MAP['space']:
                player1.fire = True
        if game_mode > 1:    # player 2 controls
            if key == simplegui.KEY_MAP['left']:
                player2.update_angle_vel(-ANGLE_VEL_MODULE)
            elif key == simplegui.KEY_MAP['right']:
                player2.update_angle_vel(ANGLE_VEL_MODULE)
            elif key == simplegui.KEY_MAP['up']:
                player2.ship_thrust(True)
            elif key == 13:
                player2.fire = True


def keyup(key):
    """Keyboard input handler. Keyup event."""

    if started:
        if not game_mode == 0:
            if key == simplegui.KEY_MAP['a']:
                player1.update_angle_vel(ANGLE_VEL_MODULE)
            elif key == simplegui.KEY_MAP['d']:
                player1.update_angle_vel(-ANGLE_VEL_MODULE)
            elif key == simplegui.KEY_MAP['w']:
                player1.ship_thrust(False)
            elif key == simplegui.KEY_MAP['space']:
                player1.fire = False
        if game_mode > 1:
            if key == simplegui.KEY_MAP['left']:
                player2.update_angle_vel(ANGLE_VEL_MODULE)
            elif key == simplegui.KEY_MAP['right']:
                player2.update_angle_vel(-ANGLE_VEL_MODULE)
            elif key == simplegui.KEY_MAP['up']:
                player2.ship_thrust(False)
            elif key == 13:
                player2.fire = False


def click(pos):
    """Mouse click handler to show/hide the splash screen"""

    global players, player1, player2, started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if not started and not game_mode == 0 and inwidth and inheight:
        rock_timer.start()
        soundtrack.play()
        started = True


def rock_spawner():
    """Rock spawning timer"""
    global tick, rocks
    tick += 1
    if tick % tick_rate == 0:   # the global variable 'tick' is used to tweak how often a new rock is spawned in each game mode
        tick = 0
        if len(rocks) < rock_limit:
            position = [random.random() * WIDTH, -asteroid_info.get_radius()]
            vel = [random.choice([1, -1]) * ROCK_VEL * random.random(),
                   random.choice([1, -1]) * ROCK_VEL * random.random()]
            angle = random.random() * 2 * math.pi
            ang_vel = random.choice([1, -1]) * random.random() * ANGLE_VEL_MODULE / 4
            rock = Sprite(position,
                            vel,
                            angle,
                            ang_vel,
                            asteroid_image,
                            asteroid_info)
            rocks.update([rock])

# draw handler
def draw(canvas):
    """Draw Handler"""
    global time, started, game_mode, rocks, missiles, players, explosions

    # First things first, time passes relentless
    time += 1

    # animate background
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image,
                      nebula_info.get_center(),
                      nebula_info.get_size(),
                      (WIDTH / 2, HEIGHT / 2),
                      (WIDTH, HEIGHT))
    canvas.draw_image(debris_image,
                      center,
                      size,
                      (wtime - WIDTH / 2, HEIGHT / 2),
                      (WIDTH, HEIGHT))
    canvas.draw_image(debris_image,
                      center,
                      size,
                      (wtime + WIDTH / 2, HEIGHT / 2),
                      (WIDTH, HEIGHT))

    # detecting collisions
    collision_detector(rocks, missiles)
    collision_detector(rocks, rocks)
    collision_detector(rocks, players)
    if game_mode == 3:
        collision_detector(players, players)
        collision_detector(players, missiles)

    # checking what collided and applying due behaviour
    for missile in missiles:
        if missile.collided:
            missile.parent.score += 1    # increase the score of the player who shot the missile
            missiles.remove(missile)
    for rock in rocks:
        if rock.collided:
            explode(rock)
            rocks.remove(rock)
    for player in players:
        if player.collided:
            player.collided = False
            if player.shield <= 0:    # checks that the shield is not active
                player.hull -= 1    # Takes out a life (decreses the hull counter)
                player.shield = 120    # activates the shield to give some margin to the player who's been just hit
            if player.hull == 0:    # If hull is 0, the ship is destroyed and the game is over
                player.ship_thrust()    # stops the thrust if the ship is destroyed while accelerating
                explode(player)
                players.remove(player)
                started = False
                game_over()    # It's Game Over, pal!

    # calls to the process function for update and draw the different groups
    update_sprites(rocks, canvas)
    update_sprites(missiles, canvas)
    for player in players:
        player.update()
        player.draw(canvas)
    update_sprites(explosions, canvas)

    # Draw lives (ship hull) and score
    if game_mode == 1:
        canvas.draw_text('Player 1 score: ' + str(score[0]),
                         (WIDTH // 16, HEIGHT // 16),
                         HEIGHT // 24,
                         '#ffffff',
                         'monospace')
        canvas.draw_text('Player 1 hull: ' + str(player1.hull),
                         (WIDTH // 16, HEIGHT // 8),
                         HEIGHT // 24,
                         '#ffffff',
                         'monospace')
    elif game_mode == 2:
        canvas.draw_text('Player 1 score: ' + str(score[0]),
                         (WIDTH // 16, HEIGHT // 16),
                         HEIGHT // 24,
                         '#ffffff',
                         'monospace')
        canvas.draw_text('Player 1 hull: ' + str(player1.hull),
                         (WIDTH // 16, HEIGHT // 8),
                         HEIGHT // 24,
                         '#ffffff',
                         'monospace')
        canvas.draw_text('Player 2 score: ' + str(score[1]),
                         (9 * WIDTH // 16, HEIGHT // 16),
                         HEIGHT // 24,
                         '#ffffff',
                         'monospace')
        canvas.draw_text('Player 2 hull: ' + str(player2.hull),
                         (9 * WIDTH // 16, HEIGHT // 8),
                         HEIGHT // 24,
                         '#ffffff',
                         'monospace')
    elif game_mode == 3:
        canvas.draw_text('Player 1 hull: ' + str(player1.hull),
                         (WIDTH // 16, HEIGHT // 16),
                         HEIGHT // 24,
                         '#ffffff',
                         'monospace')
        canvas.draw_text('Player 2 hull: ' + str(player2.hull),
                         (9 * WIDTH // 16, HEIGHT // 16),
                         HEIGHT // 24,
                         '#ffffff',
                         'monospace')
    else:
        canvas.draw_text('Player 1 score: ' + str(score[0]),
                         (WIDTH // 16, HEIGHT // 16),
                         HEIGHT // 24,
                         '#ffffff',
                         'monospace')
        canvas.draw_text('Player 2 score: ' + str(score[1]),
                         (9 * WIDTH // 16, HEIGHT // 16),
                         HEIGHT // 24,
                         '#ffffff',
                         'monospace')

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(),
                          (WIDTH / 2, HEIGHT / 2),
                          splash_info.get_size())
        canvas.draw_text(MODES[game_mode][0],
                         [WIDTH / 3, HEIGHT / 3],
                         HEIGHT // 12,
                         '#ffffff',
                         'monospace')


# Initializing images and sounds
# When not mentioned otherwise, art assets were created by Kim Lathrop and
# may be freely re-used in non-commercial projects. In that case, please credit Kim

# debris images
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris1_brown.png")

# background image - image source is opengameart.org
# I can't credit the author as I didn't record what user they come from. My
# apologies for that. If it's your image please contact me.
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://i.imgur.com/5K8jCUJ.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ships images - images source is opengameart.org
# reworked by myself using piskelapp.com
# I can't credit the author as I didn't record what user they come from. My
# apologies for that. If it's your image please contact me.
ship1_info = ImageInfo([35, 35], [70, 70], 25)
ship1_image = simplegui.load_image("http://i.imgur.com/wa1UsHW.png")
ship2_info = ImageInfo([35, 35], [70, 70], 25)
ship2_image = simplegui.load_image("http://i.imgur.com/GnbbS9Z.png")

# missile image - pixel art by myself, using piskelapp.com
# feel free to use it if you like it
missile1_info = ImageInfo([5,5], [10, 10], 3, MISSILE_LIFESPAN)
missile1_image = simplegui.load_image("http://i.imgur.com/F9ovkBG.png")
missile2_info = ImageInfo([5,5], [10, 10], 3, MISSILE_LIFESPAN)
missile2_image = simplegui.load_image("http://i.imgur.com/vGo788M.png")

# asteroid images - image source is opengameart, creator is user para
asteroid_info = ImageInfo([64, 64], [128, 128], 40, None, 8, 4)
asteroid_image = simplegui.load_image("http://i.imgur.com/S22uVko.png")

# animated explosion - image source is opengameart.
explosion_info = ImageInfo([64, 64], [128, 128], 17, 68, 17, 1)
explosion_image = simplegui.load_image("http://i.imgur.com/8iUlqSX.png")

# sound assets purchased by Rice University for its Coursera course on
# interactive programming in Python
# Source is sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")


# initialize frame and register handlers
frame = simplegui.create_frame("My Rice Rocks", WIDTH, HEIGHT)

frame.add_button("1 Player", one_player_button, 200)
frame.add_button("2 Player - collaborative", two_player_button, 200)
frame.add_button("2 Player - arena", two_player_arena_button, 200)
frame.add_label("", 200)
frame.add_label("Player 1 controls = w, a, d", 200)
frame.add_label("Player 1 fire: spacebar", 200)
frame.add_label("", 200)
frame.add_label("Player 2 controls = arrows", 200)
frame.add_label("Player 2 fire: enter", 200)
frame.add_label("", 200)
frame.add_label("Keep fire key pressed for continuous fire", 200)

frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

rock_timer = simplegui.create_timer(250.0, rock_spawner)

# get things rolling
frame.start()