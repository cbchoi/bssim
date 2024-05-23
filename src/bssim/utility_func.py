import math
from bssim.position import Position 
def euclidian_dist(_src, _dst):
    return math.sqrt(  math.pow(_src.x - _dst.x, 2) 
                        + math.pow(_src.y - _dst.y, 2) 
                        + math.pow(_src.z - _dst.z, 2))


def next_position(_spos, _tpos, _vel):
    dis_x = _tpos.x - _spos.x
    dis_y = _tpos.y - _spos.y
    rad = math.atan2(dis_y, dis_x)
    return Position(_spos.x + _vel*math.cos(rad), 
                    _spos.y + _vel*math.sin(rad), 
                    _spos.z)