import math

class Vec:
    x = 0.0
    y = 0.0
    
    def __init__(self, otherVec, Y=None):
        # Assume that providing only one argument is the copy constructor intention:
        if None == Y:
            self.x = otherVec.x
            self.y = otherVec.y
        else:
            X = otherVec
            self.x = X
            self.y = Y
        
    def get_orientation_angle(self):
        """ Get angle of orientation in degrees """
        return math.degrees(math.atan2(self.y, self.x))
        
    def as_tuple(self):
        """ Get (x,y) """
        return (self.x,self.y)
    
    def __add__(self, other):
        """ Add two vectors. """
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """ Subtract two vectors. """
        return Vec(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        """ Multiply vector by a scalar. """
        return Vec(self.x * scalar, self.y * scalar)

    def dot(self, other):
        """ Dot product of two vectors. """
        return self.x * other.x + self.y * other.y

    def magnitude(self):
        """ Return the magnitude of the vector. """
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        """ Normalize the vector. """
        mag = self.magnitude()
        if mag != 0:
            return Vec(self.x / mag, self.y / mag)
        return Vec(self.x, self.y)

    def rotate(self, angle_degrees):
        """ Rotate this vector by 'angle' degrees. """
        radians = math.radians(angle_degrees)
        cos_angle = math.cos(radians)
        sin_angle = math.sin(radians)
        return Vec(
            cos_angle * self.x - sin_angle * self.y,
            sin_angle * self.x + cos_angle * self.y
        )

    def __repr__(self):
        return f"Vec({self.x}, {self.y})"