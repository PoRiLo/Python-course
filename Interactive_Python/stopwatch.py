"""
Introduction to Interactive Programming - Part 1
Week 4 - June 2016

Miniproject: Stopwatch

@author: Ruben Dorado
http://www.codeskulptor.org/#user38_cmoYCuqsC17S3OZ_5.py

I added a little visual help for the player in the form of a
very simple progress bar. I only added a line of text over the
stopwatch, that is stored in the global string variable 'message'.
"""

# importing modules and defining global variables

import simplegui

t = 0
tries = 0
success = 0
message = ''
timerstatus = False

# helper functions

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
    if minutes // 10 == 0:
        minutestr = '0' + str(minutes)
    else:
        minutestr = str(minutes)

    if seconds // 10 == 0:
        secondstr = '0' + str(seconds)
    else:
        secondstr = str(seconds)

    # formats the timer in h:mm:ss.t format
    return str(hours) + ':' + minutestr + ':' + secondstr + '.' + str(tenths)


# event handlers

def startbutton():
    """ starts the timer """
    global timerstatus

    timer.start()
    timerstatus = True

def stopbutton():
    """
    Stops the timer, checks if the game is a success and prints
    the outcome. To avoid weird behaviour when the stop button is
    pressed repeatedly with the timer stopped, I use the switch
    'timerstatus'
    """
    global t, tries, success, message, timerstatus

    if timerstatus:
        timer.stop()
        timerstatus = False
        tries += 1
        if t % 10 == 0:
            success += 1
            message += '  Bravo!'
        else:
            message += '  Nope!'

def resetbutton():
    """
    sets all the global variables to their starting values
    it also stops the timer if it's running
    """
    global t, success, tries, timestr, message, timerstatus

    timer.stop()
    t = 0
    tries = 0
    success = 0
    message = ''
    timerstatus = False

def timerhandler():
    """
    adds one counter to the time variable 't', calls the format
    function and sets the message for the progress bar.
    """
    global t, message

    message = '>'
    t += 1

    for dummy_i in range((t - 1) % 10):
        message += '>'

# draw handler
def drawhandler(canvas):
    """
    draws three lines of text: the formatted time string, the success/tries
    status, and the progress bar message
    """
    global t, success, tries, message

    canvas.draw_text(timeformat(t), [50, 90], 72, 'Cyan')
    canvas.draw_text(str(success) + ' / ' + str(tries) , [340, 30], 24, 'Yellow')
    canvas.draw_text(message, [50, 30], 24, 'Yellow')

# create the frame and populate it
StopWatchFrame = simplegui.create_frame("The Stopwatch Game", 400, 120)
StopWatchFrame.add_button('Start', startbutton, 100)
StopWatchFrame.add_button('Stop', stopbutton, 100)
StopWatchFrame.add_button('Reset', resetbutton, 100)
StopWatchFrame.set_draw_handler(drawhandler)

# create the timer
timer = simplegui.create_timer(100, timerhandler)

# start frame
StopWatchFrame.start()