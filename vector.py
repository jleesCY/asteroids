import math

class Vector:

    magnitude = 0
    rotation = 0

    def __init__(self, m, r):
        self.magnitude = m
        self.rotation = r
    
    def add_magnitude(self, addition):
        self.magnitude += addition
    
    def set_magnitude(self, magnitude):
        self.magnitude = magnitude
    
    def rotate(self, degrees):
        self.rotation = (self.rotation + degrees) % 360
        
    def add(self, vector):
        x1 = self.x()
        y1 = self.y()

        x2 = vector.x()
        y2 = vector.y()

        xRes = x1 + x2
        yRes = y1 + y2

        mag = round(math.sqrt(xRes**2 + yRes**2),3)
        deg = round(math.degrees(math.atan2(yRes, xRes)) % 360,3)

        return Vector(mag, deg)

    def displacement(self, vector, dt, mass):
        a = Vector(vector.magnitude, vector.rotation)
        a.magnitude = (a.magnitude * 0.5) / mass #* dt**2

        return self.add(a)

    def x(self):
        return self.magnitude * math.cos(math.radians(self.rotation))
    
    def y(self):
        return self.magnitude * math.sin(math.radians(self.rotation))