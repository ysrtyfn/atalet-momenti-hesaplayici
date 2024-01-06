import math


class Nokta:
    def __init__(self, x, y):
        """Defines x and y variables"""
        self.X = x
        self.Y = y

    def move(self, dx, dy):
        """Determines where x and y move"""
        self.X = self.X + dx
        self.Y = self.Y + dy

    def __str__(self):
        return "Point(%s,%s)" % (self.X, self.Y)

    def distance(self, other):
        dx = abs(self.X - other.X)
        dy = abs(self.Y - other.Y)
        return dx, dy, math.hypot(dx, dy)
