from pyevsim import BehaviorModelExecutor, SysMessage
from pyevsim.definition import *
from bssim.position import Position as Pos
from bssim.utility_func import euclidian_dist, next_position

class Mobility(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, aname, ename, _pos, _ways, _vel):
        BehaviorModelExecutor.__init__(self, inst_t, dest_t, aname, ename)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Active", 1)

        self.insert_input_port("start")
        self.insert_input_port("recv")
        self.insert_output_port("send")

        self.way_index = 0
        self.pos = _pos
        self.velocity = _vel
        self.waypoints = _ways
        
    def ext_trans(self,port, msg):
        if port == "start":
            print(f"{self.get_name()}|[IN]|[{port}] Start Received")
            self._cur_state = "Active"
        if port == "recv":
            #print(f"{msg.retrieve()[0]}:{msg.retrieve()[1]}, {self.get_name():}: {self.pos}")
            print(f"Distance between {msg.retrieve()[0]} and {self.get_name()}: {euclidian_dist(msg.retrieve()[1], self.pos)}")
            self.cancel_rescheduling()
            
    def output(self):
        self.action()
        print(f"{self.get_name()}| Pos:{self.pos}")
        #msg = SysMessage(self.get_name(), "send")
        #msg.insert(self.pos)
        #return msg
        pass
        
    def int_trans(self):
        if self._cur_state == "Active":
            self._cur_state = "Active"

    def action(self):
        if euclidian_dist(self.pos, self.waypoints[self.way_index]) < 0.1:
            self.way_index += 1
        
        if self.way_index < len(self.waypoints):
            self.pos = next_position(self.pos, self.waypoints[self.way_index], self.velocity)
        pass

    def get_info(self):
        return (self.pos, self.velocity)