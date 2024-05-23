class Position():
    def __init__(self, _x = 0, _y=0, _z=0):
        self.x = _x
        self.y = _y
        self.z = _z

    def __str__(self):
        return f"({self.x},{self.y},{self.z})"
