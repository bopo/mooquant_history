# -*- coding: utf-8 -*-
import math

from .holiday import *
from .symbol import *

def get_quarter(month):
    return math.ceil(int(month) / 3)

