"""
Principles of Computing- Part 1
Week 5 - June 2016

Miniproject: Cookie Clicker Simulator

@author: Ruben Dorado
http://www.codeskulptor.org/#user41_Szo1nnmiVM3oyWW.py
"""

import math
import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        """
        Initiates the class variables
        """
        self._baked_cookies = 0.0
        self._current_cookies = 0.0
        self._cps = 1.0
        self._total_time = 0.0
        self._history = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        # Create a dict of built items and their amount
        built_items = {}
        for event in self._history:
            if event[1]:
                if built_items.has_key(event[1]):
                    built_items[event[1]] += 1
                else:
                    built_items[event[1]] = 1

        msg = "Simulation time: " + str(self._total_time) + " seconds\n"
        msg += "Total cookies baked: " + str(self._baked_cookies) + "\n"
        msg += "Current cookies: " + str(self._current_cookies) + "\n"
        msg += "Clicks per second: " + str(self._cps) + "\n"
        msg += "History lenght: " + str(len(self._history)) + "\n"
        msg += "\n"
        for building in built_items.items():
            msg+= building[0] + ": " + str(building[1]) + "\n"

        return msg

    def get_cookies(self):
        """
        Return current number of cookies (float)
        """
        return self._current_cookies

    def get_cps(self):
        """
        Get the current Clicks-Per-Second value (float)
        """
        return self._cps

    def get_time(self):
        """
        Get current time (float)
        """
        return self._total_time

    def get_history(self):
        """
        Return history list. This is list of tuples of the form:
        (time, item, cost of item, total cookies)
        For example: [(0.0, None, 0.0, 0.0)]
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (0.0 if you already have enough cookies)
        (float with no fractional part)
        """
        baking_time = math.ceil((cookies - self._current_cookies) / self._cps)

        if baking_time < 0.0:
            baking_time = 0.0

        return baking_time

    def wait(self, time_to_wait):
        """
        Wait for given amount of time and update state
        """
        if time_to_wait > 0.0:
            self._current_cookies += time_to_wait * self._cps
            self._baked_cookies += time_to_wait * self._cps
            self._total_time += time_to_wait

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state
        """
        if self._current_cookies >= cost:
            purchase = (self._total_time, item_name, cost, self._baked_cookies)
            self._history.append(purchase)
            self._current_cookies -= cost
            self._cps += additional_cps

def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy. Returns a ClickerState
    object corresponding to the final state of the game.
    """
    # creating a clone of the BuildInfo class and a new instance of ClickerState
    info = build_info.clone()
    clicker = ClickerState()

    # starting out-of-the-loop variable
    history_length = 0

    # Loop to simulate the game behaviour
    while clicker.get_time() <= duration:

        # Initialize in-loop variables
        cookies = clicker.get_cookies()
        cps = clicker.get_cps()
        history = clicker.get_history()
        time_left = duration - clicker.get_time()

        # Determine what item to buy next
        next_purchase = strategy(cookies, cps, history, time_left, info)

        # If there is no items to buy, wait until the end and finish
        if not next_purchase:
            clicker.wait(time_left)
            return clicker

        # Guess how long to wait to purchase the next item
        cost = info.get_cost(next_purchase)
        if cost > cookies:
            time_to_wait = clicker.time_until(cost)
        else:
            time_to_wait = 0.0
        if time_to_wait > time_left:
            time_to_wait = time_left

        # Waiting and buying the item
        clicker.wait(time_to_wait)
        clicker.buy_item(next_purchase, cost, info.get_cps(next_purchase))
        info.update_item(next_purchase)

        # Check if something happened in the last loop.
        # If nothing new happened, end the simulation
        if history_length == len(clicker.get_history()):
            return clicker
        else:
            history_length = len(clicker.get_history())

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    # Create a list of lists with the items we can afford to buy in the time left
    build_list = [[item, build_info.get_cost(item)] \
                  for item in build_info.build_items() \
                  if time_left >= math.ceil((build_info.get_cost(item) - cookies) / cps)]

    # Go through the list and select the chceapest item
    purchase = ['', float('inf')]
    for build in build_list:
        if build[1] < purchase[1]:
            purchase = build

    # If there is nothing to buy, say so
    if purchase[0] == '':
        purchase[0] = None

    return purchase[0]

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    # Create a list of lists with the items we can afford to buy in the time left
    build_list = [[item, build_info.get_cost(item)] \
                  for item in build_info.build_items() \
                  if time_left >= math.ceil((build_info.get_cost(item) - cookies) / cps)]

    # Go through the list and select the most expensive item
    purchase = ['', float('-inf')]
    for build in build_list:
        if build[1] > purchase[1]:
            purchase = build

    # If there is nothing to buy, say so
    if purchase[0] == '':
        purchase[0] = None

    return purchase[0]

def strategy_cps_to_cost(cookies, cps, history, time_left, build_info):
    """
    In this strategy, we always buy the item with best cps-to-cost
    ratio we can afford in the time left.
    """
    # Create a list of lists with the items we can afford to buy in the time left
    # and their cps-to-cost ratio
    build_list = [[item, build_info.get_cps(item) / build_info.get_cost(item)] \
                  for item in build_info.build_items() \
                  if time_left >= math.ceil((build_info.get_cost(item) - cookies) / cps)]

    # Go through the list and select the best ratio item
    purchase = ['', float('-inf')]
    for build in build_list:
        if build[1] > purchase[1]:
            purchase = build

    # If there is nothing to buy, say so
    if purchase[0] == '':
        purchase[0] = None

    return purchase[0]

def strategy_roi(cookies, cps, history, time_left, build_info):
    """
    This strategy buys the item with the best return on investment.
    Notice that this ROI can be negative (cost won't be recovered)
    ROI = (total gain - cost) / cost
    """
    # Create a closure to simplify the calculation of ROI
    def build_roi(building):
        """Returns the return of investment of a building"""
        cost = build_info.get_cost(building)
        yield_time = time_left - math.ceil((build_info.get_cost(building) - cookies) / cps)
        profit = build_info.get_cps(building) * yield_time
        return (profit - cost) / cost

    # Create a list of lists with the items and their ROI
    build_list = [[item, build_roi(item)] for item in build_info.build_items() \
                  if time_left >= math.ceil((build_info.get_cost(item) - cookies) / cps)]

    # Go through the list and select the best ratio item
    purchase = ['', float('-inf')]
    for build in build_list:
        if build[1] > purchase[1]:
            purchase = build

    # If there is nothing to buy, say so
    if purchase[0] == '':
        purchase[0] = None

    return purchase[0]

def strategy_profit(cookies, cps, history, time_left, build_info):
    """
    This strategy buys the item with the highest outcome in the time left.
    """
    # Create a closure to simplify the calculation of profit
    def build_profit(building):
        """Returns the total outcome of a building in the time left"""
        yield_time = time_left - math.ceil((build_info.get_cost(building) - cookies) / cps)
        return build_info.get_cps(building) * yield_time

    # Create a list of lists with the items and their profit
    build_list = [[item, build_profit(item)] for item in build_info.build_items() \
                  if time_left >= math.ceil((build_info.get_cost(item) - cookies) / cps)]

    # Go through the list and select the item with the highest profit
    purchase = ['', float('-inf')]
    for build in build_list:
        if build[1] > purchase[1]:
            purchase = build

    # If there is nothing to buy, say so
    if purchase[0] == '':
        purchase[0] = None

    return purchase[0]

def strategy_acceleration(cookies, cps, history, time_left, build_info):
    """
    If acceleration a = v/t, in this case, a = cps/t
    This strategy buys the item with the highest cps to time-to-buy ratio.
    """
    # Create a closure to simplify the calculation of profit
    def build_acceleration(building):
        """Returns the cps/time_to_buy ratio for a building"""
        time_to_buy = math.ceil((build_info.get_cost(building) - cookies) / cps)
        if not time_to_buy == 0:
            return build_info.get_cps(building) / time_to_buy
        else:
            return float('inf')

    # Create a list of lists with the items and their profit
    build_list = [[item, build_acceleration(item)] for item in build_info.build_items() \
                  if time_left >= math.ceil((build_info.get_cost(item) - cookies) / cps)]

    # Go through the list and select the item with the highest profit
    purchase = ['', float('-inf')]
    for build in build_list:
        if build[1] > purchase[1]:
            purchase = build

    # If there is nothing to buy, say so
    if purchase[0] == '':
        purchase[0] = None

    return purchase[0]

buy_list = ['Farm', 'Farm', 'Factory', 'Mine', 'Mine', 'Mine', 'Shipment', 'Shipment', 'Shipment', 'Mine', 'Alchemy Lab', 'Alchemy Lab', 'Alchemy Lab', 'Portal', 'Portal', 'Shipment', 'Portal', 'Portal', 'Portal', 'Portal', 'Portal', 'Alchemy Lab', 'Alchemy Lab', 'Portal', 'Portal', 'Mine', 'Shipment', 'Portal', 'Shipment', 'Alchemy Lab', 'Portal', 'Alchemy Lab', 'Portal', 'Portal', 'Portal', 'Portal', 'Shipment', 'Mine', 'Portal', 'Time Machine', 'Time Machine', 'Shipment', 'Portal', 'Alchemy Lab', 'Alchemy Lab', 'Mine', 'Mine', 'Alchemy Lab', 'Time Machine', 'Shipment', 'Time Machine', 'Time Machine', 'Alchemy Lab', 'Alchemy Lab', 'Alchemy Lab', 'Portal', 'Shipment', 'Portal', 'Time Machine', 'Shipment', 'Factory', 'Mine', 'Shipment', 'Shipment', 'Time Machine', 'Alchemy Lab', 'Shipment', 'Shipment', 'Time Machine', 'Time Machine', 'Mine', 'Alchemy Lab', 'Shipment', 'Portal', 'Portal', 'Mine', 'Portal', 'Farm', 'Time Machine', 'Factory', 'Mine', 'Factory', 'Portal', 'Shipment', 'Alchemy Lab', 'Shipment', 'Grandma', 'Time Machine', 'Shipment', 'Portal', 'Mine', 'Factory', 'Cursor', 'Mine', 'Time Machine', 'Cursor', 'Portal', 'Antimatter Condenser', 'Shipment', 'Factory', 'Mine', 'Factory', 'Factory', 'Mine', 'Alchemy Lab', 'Mine', 'Alchemy Lab', 'Mine', 'Shipment', 'Antimatter Condenser', 'Mine', 'Shipment', 'Antimatter Condenser', 'Farm', 'Factory', 'Time Machine', 'Alchemy Lab', 'Grandma', 'Alchemy Lab', 'Shipment', 'Shipment', 'Mine', 'Farm', 'Farm', 'Portal', 'Antimatter Condenser', 'Mine', 'Time Machine', 'Grandma', 'Farm', 'Alchemy Lab', 'Grandma', 'Antimatter Condenser', 'Factory', 'Alchemy Lab', 'Farm', 'Mine', 'Mine', 'Farm', 'Shipment', 'Mine', 'Shipment', 'Factory', 'Antimatter Condenser', 'Portal', 'Time Machine', 'Factory', 'Factory', 'Farm', 'Mine', 'Mine', 'Portal', 'Mine', 'Time Machine', 'Shipment', 'Alchemy Lab', 'Factory', 'Factory', 'Portal', 'Shipment', 'Farm', 'Farm', 'Farm', 'Antimatter Condenser', 'Factory', 'Antimatter Condenser', 'Alchemy Lab', 'Time Machine', 'Farm', 'Shipment', 'Factory', 'Factory', 'Portal', 'Mine', 'Antimatter Condenser', 'Mine', 'Alchemy Lab', 'Time Machine', 'Shipment', 'Factory', 'Farm', 'Mine', 'Factory', 'Farm', 'Portal', 'Alchemy Lab', 'Farm', 'Mine', 'Antimatter Condenser', 'Factory', 'Mine', 'Time Machine', 'Portal', 'Antimatter Condenser', 'Mine', 'Factory', 'Portal', 'Alchemy Lab', 'Factory', 'Mine', 'Farm', 'Alchemy Lab', 'Time Machine', 'Cursor', 'Antimatter Condenser', 'Factory', 'Cursor', 'Portal', 'Time Machine', 'Shipment', 'Portal', 'Antimatter Condenser', 'Farm', 'Alchemy Lab', 'Factory', 'Time Machine', 'Antimatter Condenser', 'Mine', 'Portal', 'Factory', 'Shipment', 'Time Machine', 'Farm', 'Shipment', 'Time Machine', 'Antimatter Condenser', 'Alchemy Lab', 'Alchemy Lab', 'Antimatter Condenser', 'Farm', 'Alchemy Lab', 'Shipment', 'Cursor', 'Shipment', 'Farm', 'Farm', 'Factory', 'Portal', 'Grandma', 'Time Machine', 'Grandma', 'Mine', 'Portal', 'Mine', 'Factory', 'Cursor', 'Antimatter Condenser', 'Antimatter Condenser', 'Cursor', 'Portal', 'Factory', 'Farm', 'Time Machine', 'Grandma', 'Cursor', 'Farm', 'Factory', 'Time Machine', 'Alchemy Lab', 'Alchemy Lab', 'Time Machine', 'Alchemy Lab', 'Factory', 'Farm', 'Factory', 'Alchemy Lab', 'Portal', 'Grandma', 'Antimatter Condenser', 'Antimatter Condenser', 'Time Machine', 'Shipment', 'Farm', 'Antimatter Condenser', 'Time Machine', 'Portal', 'Portal', 'Antimatter Condenser', 'Alchemy Lab', 'Factory', 'Farm', 'Mine', 'Factory', 'Mine', 'Factory', 'Portal', 'Factory', 'Time Machine', 'Portal', 'Antimatter Condenser', 'Time Machine', 'Mine', 'Farm', 'Portal', 'Alchemy Lab', 'Grandma', 'Alchemy Lab', 'Shipment', 'Shipment', 'Factory', 'Farm', 'Shipment', 'Antimatter Condenser', 'Mine', 'Shipment', 'Time Machine', 'Cursor', 'Portal', 'Mine', 'Mine', 'Grandma', 'Farm', 'Antimatter Condenser', 'Shipment', 'Alchemy Lab', 'Shipment', 'Alchemy Lab', 'Portal', 'Mine', 'Grandma', 'Time Machine', 'Alchemy Lab', 'Time Machine', 'Antimatter Condenser', 'Factory', 'Portal', 'Farm', 'Mine', 'Shipment', 'Grandma', 'Grandma', 'Antimatter Condenser', 'Farm', 'Shipment', 'Alchemy Lab', 'Antimatter Condenser', 'Time Machine', 'Portal', 'Time Machine', 'Shipment', 'Factory', 'Antimatter Condenser', 'Time Machine', 'Portal', 'Portal', 'Mine', 'Farm', 'Farm', 'Portal', 'Antimatter Condenser', 'Factory', 'Factory', 'Shipment', 'Time Machine', 'Mine', 'Alchemy Lab', 'Alchemy Lab', 'Shipment', 'Antimatter Condenser', 'Farm', 'Farm', 'Time Machine', 'Mine', 'Factory', 'Grandma', 'Mine', 'Antimatter Condenser', 'Portal', 'Shipment', 'Time Machine', 'Alchemy Lab', 'Shipment', 'Alchemy Lab', 'Grandma', 'Antimatter Condenser', 'Factory', 'Farm', 'Time Machine', 'Factory', 'Grandma', 'Grandma', 'Mine', 'Farm', 'Shipment', 'Portal', 'Farm', 'Grandma', 'Factory', 'Shipment', 'Farm', 'Farm', 'Grandma', 'Portal', 'Mine', 'Antimatter Condenser', 'Time Machine', 'Antimatter Condenser', 'Portal', 'Farm', 'Factory', 'Grandma', 'Farm', 'Factory', 'Grandma', 'Grandma', 'Alchemy Lab', 'Shipment', 'Factory', 'Grandma', 'Grandma', 'Cursor', 'Alchemy Lab', 'Alchemy Lab', 'Mine', 'Mine', 'Portal', 'Mine', 'Time Machine', 'Mine', 'Antimatter Condenser', 'Cursor', 'Grandma', 'Mine', 'Shipment', 'Farm', 'Shipment', 'Cursor', 'Factory', 'Alchemy Lab', 'Shipment', 'Farm', 'Alchemy Lab', 'Farm', 'Farm', 'Time Machine', 'Antimatter Condenser', 'Cursor', 'Farm', 'Factory', 'Farm', 'Grandma', 'Mine', 'Farm', 'Shipment', 'Alchemy Lab', 'Grandma', 'Grandma', 'Mine', 'Grandma', 'Grandma', 'Grandma', 'Time Machine', 'Antimatter Condenser', 'Portal', 'Factory', 'Mine', 'Antimatter Condenser', 'Time Machine', 'Alchemy Lab', 'Time Machine', 'Factory', 'Factory', 'Farm', 'Farm', 'Cursor', 'Farm', 'Portal', 'Antimatter Condenser', 'Grandma', 'Shipment', 'Alchemy Lab', 'Grandma', 'Farm', 'Alchemy Lab', 'Grandma', 'Factory', 'Time Machine', 'Portal', 'Grandma', 'Factory', 'Factory', 'Shipment', 'Farm', 'Mine', 'Factory', 'Farm', 'Grandma', 'Antimatter Condenser', 'Grandma', 'Farm', 'Grandma', 'Grandma', 'Grandma', 'Cursor', 'Portal', 'Cursor', 'Shipment', 'Alchemy Lab', 'Time Machine', 'Cursor', 'Antimatter Condenser', 'Grandma', 'Farm', 'Grandma', 'Grandma', 'Farm', 'Factory', 'Grandma', 'Mine', 'Cursor', 'Cursor', 'Farm', 'Grandma', 'Cursor', 'Farm', 'Factory', 'Portal', 'Cursor', 'Factory', 'Time Machine', 'Mine', 'Portal', 'Farm', 'Cursor', 'Alchemy Lab', 'Cursor', 'Antimatter Condenser', 'Factory', 'Factory', 'Cursor', 'Time Machine', 'Shipment', 'Alchemy Lab', 'Cursor', 'Shipment', 'Antimatter Condenser', 'Shipment', 'Farm', 'Grandma', 'Mine', 'Grandma', 'Cursor', 'Farm', 'Grandma', 'Cursor', 'Portal', 'Grandma', 'Time Machine', 'Farm', 'Mine', 'Antimatter Condenser', 'Shipment', 'Factory', 'Grandma', 'Mine', 'Time Machine', 'Portal', 'Antimatter Condenser', 'Cursor', 'Alchemy Lab', 'Grandma', 'Farm', 'Grandma', 'Cursor', 'Portal', 'Shipment', 'Grandma', 'Farm', 'Grandma', 'Mine', 'Mine', 'Grandma', 'Factory', 'Grandma', 'Factory', 'Farm', 'Grandma', 'Factory', 'Cursor', 'Shipment', 'Grandma', 'Alchemy Lab', 'Cursor', 'Time Machine', 'Farm', 'Mine', 'Grandma', 'Alchemy Lab', 'Grandma', 'Antimatter Condenser', 'Cursor', 'Factory', 'Grandma', 'Portal', 'Grandma', 'Grandma', 'Grandma', 'Antimatter Condenser', 'Cursor', 'Portal', 'Mine', 'Farm', 'Alchemy Lab', 'Time Machine', 'Portal', 'Alchemy Lab', 'Grandma', 'Cursor', 'Time Machine', 'Farm', 'Shipment', 'Factory', 'Mine', 'Antimatter Condenser', 'Time Machine', 'Antimatter Condenser', 'Farm', 'Mine', 'Mine', 'Portal', 'Shipment', 'Portal', 'Shipment', 'Cursor', 'Alchemy Lab', 'Time Machine', 'Grandma', 'Factory', 'Antimatter Condenser', 'Cursor', 'Factory', 'Grandma', 'Farm', 'Portal', 'Cursor', 'Time Machine', 'Cursor', 'Factory', 'Cursor', 'Alchemy Lab', 'Shipment', 'Factory', 'Antimatter Condenser', 'Time Machine', 'Alchemy Lab', 'Cursor', 'Mine', 'Farm', 'Antimatter Condenser', 'Alchemy Lab', 'Shipment', 'Factory', 'Portal', 'Time Machine', 'Mine', 'Antimatter Condenser', 'Shipment', 'Cursor', 'Alchemy Lab', 'Shipment', 'Cursor', 'Farm', 'Portal', 'Alchemy Lab', 'Mine', 'Time Machine', 'Farm', 'Factory', 'Farm', 'Alchemy Lab', 'Antimatter Condenser', 'Grandma', 'Farm', 'Factory', 'Grandma', 'Alchemy Lab', 'Portal', 'Mine', 'Antimatter Condenser', 'Cursor', 'Time Machine', 'Grandma', 'Farm', 'Farm', 'Farm', 'Portal', 'Factory', 'Mine', 'Time Machine', 'Antimatter Condenser', 'Grandma', 'Alchemy Lab', 'Time Machine', 'Alchemy Lab', 'Mine', 'Shipment', 'Portal', 'Portal', 'Antimatter Condenser', 'Shipment', 'Shipment', 'Antimatter Condenser', 'Grandma', 'Cursor', 'Farm', 'Time Machine', 'Grandma', 'Alchemy Lab', 'Grandma', 'Shipment', 'Portal', 'Mine', 'Time Machine', 'Portal', 'Factory', 'Farm', 'Farm', 'Factory', 'Antimatter Condenser', 'Shipment', 'Time Machine', 'Antimatter Condenser', 'Farm', 'Alchemy Lab', 'Factory', 'Portal', 'Factory', 'Shipment', 'Antimatter Condenser', 'Factory', 'Time Machine', 'Shipment', 'Mine', 'Mine', 'Alchemy Lab', 'Time Machine', 'Farm', 'Portal', 'Antimatter Condenser', 'Portal', 'Mine', 'Grandma', 'Cursor', 'Grandma', 'Cursor', 'Alchemy Lab', 'Cursor', 'Mine', 'Grandma', 'Shipment', 'Shipment', 'Mine', 'Grandma', 'Time Machine', 'Portal', 'Farm', 'Alchemy Lab', 'Cursor', 'Antimatter Condenser', 'Factory', 'Time Machine', 'Factory', 'Portal', 'Antimatter Condenser', 'Factory', 'Cursor', 'Alchemy Lab', 'Mine', 'Antimatter Condenser', 'Cursor', 'Mine', 'Cursor', 'Alchemy Lab', 'Cursor', 'Portal', 'Farm', 'Cursor', 'Grandma', 'Shipment', 'Shipment', 'Factory', 'Time Machine', 'Farm', 'Time Machine', 'Cursor', 'Antimatter Condenser', 'Cursor', 'Cursor', 'Farm', 'Grandma', 'Factory', 'Grandma', 'Cursor', 'Cursor', 'Cursor', 'Cursor', 'Mine', 'Mine', 'Cursor', 'Shipment', 'Shipment', 'Alchemy Lab', 'Grandma', 'Cursor', 'Portal', 'Grandma', 'Farm', 'Farm', 'Cursor', 'Time Machine', 'Cursor', 'Antimatter Condenser', 'Shipment', 'Mine', 'Mine', 'Alchemy Lab', 'Time Machine', 'Grandma', 'Factory', 'Portal', 'Factory', 'Portal', 'Antimatter Condenser', 'Alchemy Lab', 'Portal', 'Time Machine', 'Antimatter Condenser', 'Alchemy Lab', 'Shipment', 'Time Machine', 'Alchemy Lab', 'Alchemy Lab', 'Antimatter Condenser', 'Grandma', 'Factory', 'Portal', 'Cursor', 'Mine', 'Farm', 'Mine', 'Antimatter Condenser', 'Time Machine', 'Time Machine', 'Shipment', 'Grandma', 'Mine', 'Factory', 'Shipment', 'Grandma', 'Grandma', 'Cursor', 'Factory', 'Cursor', 'Farm', 'Cursor', 'Cursor', 'Farm', 'Grandma', 'Portal', 'Antimatter Condenser', 'Grandma', 'Portal', 'Cursor', 'Cursor', 'Cursor', 'Cursor', 'Alchemy Lab', 'Factory', 'Shipment', 'Grandma', 'Shipment', 'Factory', 'Farm', 'Grandma', 'Cursor', 'Time Machine', 'Farm', 'Antimatter Condenser', 'Shipment', 'Cursor', 'Alchemy Lab', 'Portal', 'Grandma', 'Mine', 'Time Machine', 'Grandma', 'Farm', 'Cursor', 'Mine', 'Antimatter Condenser', 'Grandma', 'Cursor', 'Grandma', 'Cursor', 'Cursor', 'Mine', 'Shipment', 'Cursor', 'Alchemy Lab', 'Cursor', 'Alchemy Lab', 'Grandma', 'Time Machine', 'Cursor', 'Grandma', 'Cursor', 'Portal', 'Antimatter Condenser', 'Cursor', 'Time Machine', 'Farm', 'Cursor', 'Portal', 'Antimatter Condenser', 'Cursor', 'Shipment', 'Factory', 'Cursor', 'Mine', 'Cursor', 'Farm', 'Cursor', 'Farm', 'Grandma', 'Alchemy Lab', 'Cursor', 'Cursor', 'Factory', 'Factory', 'Cursor', 'Mine', 'Cursor', 'Grandma', 'Cursor', 'Portal', 'Farm', 'Alchemy Lab', 'Shipment', 'Farm', 'Cursor', 'Mine', 'Cursor', 'Time Machine', 'Antimatter Condenser', 'Alchemy Lab', 'Shipment', 'Portal', 'Alchemy Lab', 'Factory', 'Farm', 'Cursor', 'Farm', 'Cursor', 'Grandma', 'Time Machine', 'Mine', 'Farm', 'Antimatter Condenser', 'Portal', 'Antimatter Condenser', 'Time Machine', 'Time Machine', 'Portal', 'Mine', 'Grandma', 'Antimatter Condenser', 'Mine', 'Portal', 'Shipment', 'Factory', 'Time Machine', 'Shipment', 'Alchemy Lab', 'Factory', 'Factory', 'Antimatter Condenser', 'Portal', 'Time Machine', 'Factory', 'Alchemy Lab', 'Farm', 'Portal', 'Mine', 'Factory', 'Cursor', 'Antimatter Condenser', 'Shipment', 'Farm', 'Mine', 'Alchemy Lab', 'Time Machine', 'Alchemy Lab', 'Cursor', 'Antimatter Condenser', 'Grandma', 'Time Machine', 'Cursor', 'Portal', 'Factory', 'Shipment', 'Alchemy Lab', 'Shipment', 'Grandma', 'Alchemy Lab', 'Portal', 'Shipment', 'Factory', 'Mine', 'Farm', 'Grandma', 'Antimatter Condenser', 'Time Machine', 'Farm', 'Alchemy Lab', 'Cursor', 'Antimatter Condenser', 'Portal', 'Cursor', 'Cursor', 'Farm', 'Time Machine', 'Portal', 'Mine', 'Grandma', 'Cursor', 'Shipment', 'Grandma', 'Antimatter Condenser', 'Alchemy Lab', 'Farm', 'Time Machine', 'Antimatter Condenser', 'Time Machine', 'Farm', 'Portal', 'Shipment', 'Antimatter Condenser', 'Grandma', 'Shipment', 'Portal', 'Factory', 'Mine', 'Time Machine', 'Factory', 'Factory', 'Farm', 'Mine', 'Factory', 'Cursor', 'Factory', 'Alchemy Lab', 'Mine', 'Alchemy Lab', 'Portal', 'Shipment', 'Mine', 'Antimatter Condenser', 'Mine', 'Shipment', 'Time Machine', 'Grandma', 'Grandma', 'Antimatter Condenser', 'Mine', 'Portal', 'Cursor', 'Grandma', 'Grandma', 'Alchemy Lab', 'Cursor', 'Time Machine', 'Farm', 'Grandma', 'Shipment', 'Factory', 'Cursor', 'Antimatter Condenser', 'Cursor', 'Factory', 'Shipment', 'Alchemy Lab', 'Grandma', 'Farm', 'Time Machine', 'Portal', 'Farm', 'Farm', 'Alchemy Lab', 'Shipment', 'Mine', 'Grandma', 'Portal', 'Factory', 'Antimatter Condenser', 'Time Machine', 'Antimatter Condenser', 'Portal', 'Factory', 'Factory', 'Grandma', 'Alchemy Lab', 'Shipment', 'Shipment', 'Time Machine', 'Mine', 'Farm', 'Mine', 'Mine', 'Antimatter Condenser', 'Alchemy Lab', 'Time Machine', 'Portal', 'Antimatter Condenser', 'Time Machine', 'Farm', 'Shipment', 'Portal', 'Factory', 'Alchemy Lab', 'Portal', 'Cursor', 'Shipment', 'Cursor', 'Antimatter Condenser', 'Time Machine', 'Alchemy Lab', 'Farm', 'Antimatter Condenser', 'Farm', 'Portal', 'Shipment', 'Factory', 'Cursor', 'Grandma', 'Grandma', 'Mine', 'Alchemy Lab', 'Time Machine', 'Cursor', 'Alchemy Lab', 'Shipment', 'Mine', 'Factory', 'Antimatter Condenser', 'Time Machine', 'Farm', 'Mine', 'Portal', 'Cursor', 'Grandma', 'Mine', 'Factory', 'Antimatter Condenser', 'Portal', 'Alchemy Lab', 'Grandma', 'Grandma', 'Mine', 'Farm', 'Alchemy Lab', 'Cursor', 'Shipment', 'Time Machine', 'Cursor', 'Factory', 'Shipment', 'Grandma', 'Cursor', 'Antimatter Condenser', 'Portal', 'Antimatter Condenser', 'Cursor', 'Farm', 'Alchemy Lab', 'Cursor', 'Factory', 'Farm', 'Mine', 'Cursor', 'Cursor', 'Cursor', 'Factory', 'Shipment', 'Mine', 'Grandma', 'Factory', 'Grandma', 'Farm', 'Time Machine', 'Time Machine', 'Portal', 'Cursor', 'Antimatter Condenser', 'Mine', 'Portal', 'Alchemy Lab', 'Cursor', 'Cursor', 'Time Machine', 'Alchemy Lab', 'Shipment', 'Cursor', 'Grandma', 'Factory', 'Antimatter Condenser', 'Time Machine', 'Alchemy Lab', 'Portal', 'Grandma', 'Shipment', 'Cursor', 'Shipment', 'Grandma', 'Cursor', 'Antimatter Condenser', 'Portal', 'Mine', 'Cursor', 'Cursor', 'Farm', 'Cursor', 'Farm', 'Farm', 'Alchemy Lab', 'Factory', 'Time Machine', 'Portal', 'Grandma', 'Shipment', 'Factory', 'Farm', 'Antimatter Condenser', 'Time Machine', 'Mine', 'Grandma', 'Antimatter Condenser', 'Portal', 'Mine', 'Cursor', 'Time Machine', 'Alchemy Lab', 'Mine', 'Factory', 'Alchemy Lab', 'Shipment', 'Portal', 'Antimatter Condenser', 'Time Machine', 'Shipment', 'Farm', 'Farm', 'Factory', 'Grandma', 'Mine', 'Antimatter Condenser', 'Shipment', 'Alchemy Lab', 'Alchemy Lab', 'Time Machine', 'Portal', 'Grandma', 'Antimatter Condenser', 'Factory', 'Portal', 'Shipment', 'Time Machine', 'Grandma', 'Mine', 'Factory', 'Cursor', 'Antimatter Condenser', 'Cursor', 'Farm', 'Cursor', 'Factory', 'Shipment', 'Cursor', 'Cursor', 'Portal', 'Alchemy Lab', 'Time Machine', 'Mine', 'Farm', 'Antimatter Condenser', 'Mine', 'Grandma', 'Alchemy Lab', 'Grandma', 'Time Machine', 'Cursor', 'Portal', 'Cursor', 'Farm', 'Mine', 'Grandma', 'Shipment', 'Cursor', 'Antimatter Condenser', 'Shipment', 'Farm', 'Grandma', 'Cursor', 'Factory', 'Grandma', 'Grandma', 'Factory', 'Alchemy Lab', 'Shipment', 'Cursor', 'Portal', 'Mine', 'Factory', 'Grandma', 'Factory', 'Farm', 'Cursor', 'Cursor', 'Time Machine', 'Farm', 'Farm', 'Cursor', 'Grandma', 'Cursor', 'Cursor', 'Cursor', 'Alchemy Lab', 'Grandma', 'Factory', 'Cursor', 'Antimatter Condenser', 'Mine', 'Shipment', 'Time Machine', 'Alchemy Lab', 'Shipment', 'Portal', 'Antimatter Condenser', 'Portal', 'Time Machine', 'Mine', 'Antimatter Condenser', 'Factory', 'Farm', 'Alchemy Lab', 'Time Machine', 'Portal', 'Antimatter Condenser', 'Mine', 'Shipment', 'Mine', 'Portal', 'Time Machine', 'Alchemy Lab', 'Antimatter Condenser', 'Portal', 'Time Machine', 'Alchemy Lab', 'Antimatter Condenser', 'Factory', 'Alchemy Lab', 'Shipment', 'Shipment', 'Factory', 'Farm', 'Portal', 'Mine', 'Time Machine', 'Farm', 'Antimatter Condenser', 'Alchemy Lab', 'Grandma', 'Grandma', 'Shipment', 'Mine', 'Farm', 'Portal', 'Time Machine', 'Mine', 'Antimatter Condenser', 'Factory', 'Portal', 'Cursor', 'Factory', 'Farm', 'Farm', 'Alchemy Lab', 'Mine', 'Time Machine', 'Grandma', 'Shipment', 'Antimatter Condenser', 'Factory', 'Shipment', 'Alchemy Lab', 'Farm', 'Grandma', 'Farm', 'Shipment', 'Portal', 'Time Machine', 'Cursor', 'Factory', 'Mine', 'Alchemy Lab', 'Grandma', 'Antimatter Condenser', 'Portal', 'Time Machine', 'Antimatter Condenser', 'Cursor', 'Cursor', 'Farm', 'Portal', 'Shipment', 'Mine', 'Mine', 'Alchemy Lab', 'Grandma', 'Grandma', 'Alchemy Lab', 'Cursor', 'Factory', 'Factory', 'Cursor', 'Cursor', 'Grandma', 'Time Machine', 'Portal', 'Antimatter Condenser', 'Time Machine', 'Portal', 'Grandma', 'Farm', 'Shipment', 'Alchemy Lab', 'Factory', 'Shipment', 'Mine', 'Time Machine', 'Alchemy Lab', 'Mine', 'Portal', 'Shipment', 'Mine', 'Time Machine', 'Alchemy Lab', 'Mine', 'Farm', 'Shipment', 'Factory', 'Factory', 'Portal', 'Farm', 'Grandma', 'Factory', 'Farm', 'Factory', 'Farm', 'Farm', 'Mine', 'Time Machine', 'Shipment', 'Mine', 'Portal', 'Alchemy Lab', 'Time Machine', 'Shipment', 'Portal', 'Alchemy Lab', 'Shipment', 'Time Machine', 'Portal', 'Mine', 'Shipment', 'Portal', 'Mine', 'Alchemy Lab', 'Alchemy Lab', 'Shipment', 'Alchemy Lab', 'Portal', 'Alchemy Lab', 'Shipment', 'Alchemy Lab', 'Portal', 'Alchemy Lab', 'Portal', 'Portal', 'Shipment', 'Portal', 'Alchemy Lab', 'Alchemy Lab', 'Portal', 'Alchemy Lab', 'Shipment', 'Alchemy Lab', 'Portal', 'Alchemy Lab']


def strategy_list(cookies, cps, history, time_left, build_info):
    """
    Buys items in order following a list optimized by user Xiaofei Wen
    to be found in http://www.codeskulptor.org/#user41_VqvZYgExT8Wor4w.py
    """
    global buy_list

    if buy_list:
        return buy_list.pop(0)

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    This function simply calls the best strategy I could come by so far.
    """
    return strategy_cps_to_cost(cookies, cps, history, time_left, build_info)

def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    Some functionality to print the buildings bought in the
    simulation is added
    """

    build = provided.BuildInfo()
    state = simulate_clicker(build, time, strategy)


    # Print the final state of the simulation.
    print
    print "Strategy: " + strategy_name
    print
    print state
    print "----------------------------------------"

def run():
    """
    Run the simulator.
    """
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("CPS to cost ratio", SIM_TIME, strategy_cps_to_cost)
    run_strategy("Return of investment", SIM_TIME, strategy_roi)
    run_strategy("Max profit", SIM_TIME, strategy_profit)
    run_strategy("Max growth acceleration", SIM_TIME, strategy_acceleration)
    run_strategy("Best", SIM_TIME, strategy_best)
    run_strategy("Optimized list", SIM_TIME, strategy_list)

run()
