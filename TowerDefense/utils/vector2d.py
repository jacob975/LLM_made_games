"""
Vector2D class for position and movement calculations
"""

import math

class Vector2D:
    """2D Vector class for handling positions, velocities, and directions"""
    
    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)
    
    def __add__(self, other):
        """Add two vectors"""
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        """Subtract two vectors"""
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        """Multiply vector by scalar"""
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        """Divide vector by scalar"""
        return Vector2D(self.x / scalar, self.y / scalar)
    
    def magnitude(self):
        """Calculate the magnitude (length) of the vector"""
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self):
        """Return a normalized (unit) vector"""
        mag = self.magnitude()
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)
    
    def distance_to(self, other):
        """Calculate distance to another vector"""
        return (other - self).magnitude()
    
    def to_tuple(self):
        """Convert to tuple for pygame compatibility"""
        return (int(self.x), int(self.y))
    
    def __str__(self):
        return f"Vector2D({self.x:.2f}, {self.y:.2f})"