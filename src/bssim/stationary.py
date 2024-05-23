from pyevsim import BehaviorModelExecutor, SysMessage
from pyevsim.definition import *
from bssim.position import Position as Pos
from bssim.utility_func import euclidian_dist

class Stationary(BehaviorModelExecutor):
    def __init__(self, inst_t, dest_t, aname, ename, _pos, _channel):
        BehaviorModelExecutor.__init__(self, inst_t, dest_t, aname, ename)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Active", 1)

        self.insert_input_port("start")
        self.insert_input_port("recv")
        self.insert_output_port("broadcast")

        self.pos = _pos
        self.channel = _channel
        

    def ext_trans(self,port, msg):
        if port == "start":
            print(f"{self.get_name()}|[IN]|[{port}] Start Received")
            self._cur_state = "Active"
        if port == "recv":
            print(f"{msg.retrieve()[0]}| Connection Estabilished")

    def output(self):
        msg = SysMessage(self.get_name(), "broadcast")
        msg.insert(f"{self.get_name()}")
        msg.insert(self.pos)
        print(f"SimTime |{self.get_name()}")
        return msg
        
    def int_trans(self):
        if self._cur_state == "Active":
            self._cur_state = "Active"

    def reachability_check(self, pos):
        if euclidian_dist(self.pos, pos) < self.channel:
            return True
        else:
            return False