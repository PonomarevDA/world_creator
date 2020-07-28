#!/usr/bin/env python3

from copy import deepcopy
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __truediv__(self, other):
        answer = deepcopy(self)
        answer.x = self.x / other
        answer.y = self.y / other
        return answer
    
    def __sub__(self, other):
        answer = deepcopy(self)
        answer.x = self.x - other.x
        answer.y = self.y - other.y
        return answer
      
    def __add__(self, other):
        answer = deepcopy(self)
        answer.x = self.x + other.x
        answer.y = self.y + other.y
        return answer
        
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, scalar):
        self.x *= scalar
        self.y *= scalar
        return self

    def __idiv__(self, scalar):
        self.x /= scalar
        self.y /= scalar
        return self

    def __str__(self):
        return "[{0}, {1}]".format(self.x, self.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @staticmethod
    def from_list(data: list):
        return Vector2D(data[0], data[1])
        
    def as_list(self):
        return list([self.x, self.y])

class Point2D(Vector2D):
    pass

class Size2D(Vector2D):
    pass
