from math import cos, sin, pi, asin, copysign, acos

from angem.matrix import Matrix


class Vector2(Matrix):
    def __init__(self, x, y):
        super().__init__(
            (x,),
            (y,),
        )

    @property
    def x(self):
        return self.strings[0][0]

    @property
    def y(self):
        return self.strings[1][0]

#     def __add__(self, other):
#         return Vector(
#             self.x + other.x,
#             self.y + other.y
#         )
#
#     def __neg__(self):
#         return Vector(
#             -self.x,
#             -self.y
#         )
#
#     def __sub__(self, other):
#         return self + -other
#
#     def __mul__(self, other):
#         if isinstance(other, Vector):
#             return self.x * other.x + self.y * other.y
#
#         return Vector(
#             self.x * other,
#             self.y * other
#         )
#
#     def __rmul__(self, other):
#         return self * other
#
#     def __truediv__(self, other):
#         return self * (1 / other)
#
#     def squared_magnitude(self):
#         return self.x ** 2 + self.y ** 2
#
#     def __abs__(self):
#         return self.squared_magnitude() ** 0.5
#
#     def __eq__(self, other):
#         return self.x == other.x and self.y == other.y
#
#     def __pow__(self, power, modulo=None):
#         if power == 0:
#             return self / abs(self) if self != zero else zero
#         if power % 2 == 0:
#             return abs(self) ** power
#         raise Exception
#
#     def __invert__(self):
#         return Vector(self.y, self.x)
#
#     def project(self, other):
#         return self * other / other.squared_magnitude() * other
#
#     def scalar_project(self, other):
#         return self * other / abs(other)
#
#     def rotated(self, angle):
#         if not angle:
#             return self
#
#         cs = cos(angle)
#         sn = sin(angle)
#
#         return Vector(
#             self.x * cs - self.y * sn,
#             self.x * sn + self.y * cs)
#
#     def angle(self):
#         return copysign(
#             acos(self.x / abs(self)),
#             asin(self.y / abs(self))
#         )
#
#     def __repr__(self):
#         return f'{{{round(self.x, 2)}; {round(self.y, 2)}}}'
#
#     def __bool__(self):
#         return self != zero


zero = Vector2(0, 0)
# one = Vector(1, 1)
#
# up    = Vector( 0, -1)
# down  = Vector( 0,  1)
# right = Vector( 1,  0)
# left  = Vector(-1,  0)
