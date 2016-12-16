# -*- coding: utf-8 -*-
"""
Created on Fri Sep 02 23:51:48 2016

@author: Ruben
"""

import datetime

def delta(arrival, departure):
    """Returns the number of days between two dates"""

    dif = departure - arrival

    return dif.days


arrival = datetime.date(2012, 3, 28)
departure = datetime.date(2016, 9, 6)
print delta(arrival, departure), "days"

she_left = datetime.date(2016, 5, 1)
i_go = datetime.date(2016, 9, 3)
print delta(she_left, i_go), "days"

nacimiento = datetime.date(1975, 6, 12)
print delta(nacimiento, datetime.date.today()) /7, "weeks old"