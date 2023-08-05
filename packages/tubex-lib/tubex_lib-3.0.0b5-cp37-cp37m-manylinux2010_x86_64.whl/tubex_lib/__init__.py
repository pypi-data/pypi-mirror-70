from pyibex import Interval, IntervalVector, Function
from pyibex.geometry import CtcPolar
from tubex_lib.tube import *

# Predefined contractor objects

class ctc:

  deriv = CtcDeriv()
  eval = CtcEval()
  dist = CtcDist()
  polar = CtcPolar()