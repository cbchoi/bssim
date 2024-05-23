from pyevsim import SystemSimulator
from pyevsim.definition import Infinite
from bssim.position import Position
from bssim.stationary import Stationary
from bssim.mobility import Mobility
from bssim.utility_func import euclidian_dist, next_position

class BSSimEngine():
    def __init__(self, tstep):
        self.station_list  = []
        self.mobility_list = []
        self.time_step = tstep
        self.ss = SystemSimulator()
        self.ss.register_engine("bssim", "REAL_TIME", tstep)
        self.se = self.ss.get_engine("bssim")
        self.se.insert_input_port("start")

    def insert_stationary(self, _station):
        self.station_list.append(_station)
        self.se.register_entity(_station)
        self.se.coupling_relation(None, "start", _station, "start")
        pass

    def insert_mobility(self, _mobility):
        self.mobility_list.append(_mobility)
        self.se.register_entity(_mobility)
        self.se.coupling_relation(None, "start", _mobility, "start")
        
        pass

    def reset_connection(self):
        for station in self.station_list:
            if (station, "broadcast") in self.se.port_map:
                self.se.port_map[(station, "broadcast")].clear()

        for mobility in self.mobility_list:
            if (mobility, "send") in self.se.port_map:
                self.se.port_map[(mobility, "send")].clear()

    def connection_configure(self):
        for station in self.station_list:
            for mobility in self.mobility_list:
                if station.reachability_check(mobility.get_info()[0]):
                    self.se.coupling_relation(station, "broadcast", mobility, "recv")
                    self.se.coupling_relation(mobility, "send", station, "recv")

        pass

    def run(self):
        self.se.insert_external_event("start", None)
        while not self.se.is_terminated():
            self.connection_configure()
            self.se.simulate(self.time_step)
            self.reset_connection()