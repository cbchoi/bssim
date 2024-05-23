import pytest, logging

from pyevsim import SystemSimulator
from pyevsim.definition import Infinite
from bssim.position import Position
from bssim.stationary import Stationary
from bssim.mobility import Mobility
from bssim.utility_func import euclidian_dist, next_position

class TestCoreObject():
    @classmethod
    def setup_class(cls):
        cls.ss = SystemSimulator()
        cls.ss.register_engine("bssim", "REAL_TIME", 0.1)
        cls.se = cls.ss.get_engine("bssim")
        cls.se.insert_input_port("start")
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_function(self):
        station1 = Stationary(0, Infinite, "BS1", "bssim", Position(0,0,0))
        TestCoreObject.se.register_entity(station1)
        
        station2 = Stationary(0, Infinite, "BS2", "bssim", Position(2, 2, 0))
        TestCoreObject.se.register_entity(station2)

        mobility1 = Mobility(0, Infinite, "Agent1", "first", Position(0,0,0), [Position(1,0,0), Position(1,1,0), Position(1,1,1)], 0.1)
        self.se.register_entity(mobility1)

        mobility2 = Mobility(0, Infinite, "Agent2", "first", Position(0,0,0), [Position(-1,0,0), Position(-1,-1,0), Position(-1,-1,-1)], 0.1)
        self.se.register_entity(mobility2)

        self.se.coupling_relation(None, "start", station1, "start")
        self.se.coupling_relation(None, "start", mobility1, "start")
        self.se.coupling_relation(None, "start", mobility2, "start")
        self.se.coupling_relation(None, "start", station2, "start")

        self.se.coupling_relation(station1, "broadcast", mobility1, "recv")
        self.se.coupling_relation(station1, "broadcast", mobility2, "recv")

        self.se.coupling_relation(station2, "broadcast", mobility1, "recv")
        self.se.coupling_relation(station2, "broadcast", mobility2, "recv")
        
        self.se.insert_external_event("start", None)
        self.se.simulate()

        assert(euclidian_dist(Position(), Position()) == 0)

#print(next_position(Position(), Position(1, 0, 0), 0.1))

#if __name__ == "__main()__":
testobj = TestCoreObject()
testobj.setup_class()
testobj.test_function()