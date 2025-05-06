from .figure import Figure
from .color import FigureColor
import math


class RepaintableMixin:
    def repaint(self, new_color_hex):
        """
        Repaints the object with the new color.

        Args:
            new_color_hex (str): The new color code in hexadecimal format.
        """
        self._color = FigureColor(new_color_hex)


class Triangle(Figure, RepaintableMixin):
    
    name = "Undefined"

    def __init__(self, a, b, c, color_hex):
        """
        Initializes a Triangle instance with the given sides and color.

        Args:
            a (float): The length of side a.
            b (float): The length of side b.
            c (float): The length of side c.
            color_hex (str): The color of the triangle in hexadecimal format.

        Raises:
            ValueError: If the sides do not form a valid triangle.
        """
        super().__init__()
        self.name = "Triangle"
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("Invalid triangle sides")
        self._a = a
        self._b = b
        self._c = c
        self._color = FigureColor(color_hex)

    def square(self):
        """
        Calculates the area of the triangle using Heron's formula.

        Returns:
            float: The area of the triangle.
        """
        p = (self._a + self._b + self._c) / 2
        return math.sqrt(p * (p - self._a) *
                         (p - self._b) * (p - self._c))

    def get_name(self):
        """
        Returns the name of the figure.

        Returns:
            str: The name of the figure ("Triangle").
        """
        return self.name

    def get_color(self):
        """
        Returns the color of the triangle.

        Returns:
            str: The hexadecimal color code.
        """
        return self._color._color

    def get_sides(self):
        """
        Returns the lengths of the sides of the triangle.

        Returns:
            tuple: A tuple containing the lengths of the three sides (a, b, c).
        """
        return (self._a, self._b, self._c)

    def get_info(self):
        """
        Returns a string with the triangle's information.

        Returns:
            str: A string containing the name, sides, area, and color.
        """
        return "{}: ({},{},{}), S = {:.3f}, color_hex({})".format(
            self.name, self._a, self._b, self._c, self.square(), self._color)

    def __str__(self):
        """
        Returns a string representation of the triangle.

        Returns:
            str: The string returned by get_info().
        """
        return self.get_info()
