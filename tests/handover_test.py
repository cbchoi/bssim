import pytest, logging

from pyevsim import SystemSimulator
from pyevsim.definition import Infinite

from bssim.position import Position
from bssim.stationary import Stationary
from bssim.mobility import Mobility
from bssim.utility_func import euclidian_dist, next_position
from bssim.bs_engine import BSSimEngine

bssim = BSSimEngine(tstep=0.1)

station = Stationary(0, Infinite, "BS1", "bssim", Position(0,0,0), 0.7)
station2 = Stationary(0, Infinite, "BS2", "bssim", Position(0,0,0), 0.9)
mobility = Mobility(0, Infinite, "Agent1", "first", Position(1,0,0), [Position(0.6,0,0), Position(1,0,0), Position(1,1,1)], 0.1)
mobility2 = Mobility(0, Infinite, "Agent2", "first", Position(1,0,0), [Position(0.6,0,0), Position(1,0,0), Position(1,1,1)], 0.1)

bssim.insert_stationary(station)
bssim.insert_stationary(station2)
bssim.insert_mobility(mobility)
bssim.insert_mobility(mobility2)

bssim.run()