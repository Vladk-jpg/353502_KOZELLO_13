from .figure import Figure
from .color import FigureColor
import math


class Triangle(Figure):
    name = "Undefined"

    def __init__(self, a, b, c, color_hex):
        super().__init__()
        self.name = "Triangle"
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("Invalid triangle sides")
        self._a = a
        self._b = b
        self._c = c
        self._color = FigureColor(color_hex)

    def square(self):
        p = (self._a + self._b + self._c) / 2
        return math.sqrt(p * (p - self._a) *
                         (p - self._b) * (p - self._c))

    def get_name(self):
        return self.name

    def get_color(self):
        return self._color._color

    def get_sides(self):
        return (self._a, self._b, self._c)

    def get_info(self):
        str = "{}: ({},{},{}), S = {:.3f}, color_hex({})".format(self.name,
                                                                 self._a,
                                                                 self._b,
                                                                 self._c,
                                                                 self.square(),
                                                                 self._color)
        return str

    def __str__(self):
        return self.get_info()
