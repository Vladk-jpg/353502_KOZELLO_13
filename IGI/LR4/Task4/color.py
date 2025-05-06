class FigureColor:
    def __init__(self, color_hex):
        """
        Initializes a FigureColor instance.

        Args:
            color_hex (str): The color code in hexadecimal format.
        """
        int(color_hex, 16)
        self._color = color_hex

    @property
    def color(self):
        """Gets the current color."""
        return self._color

    @color.setter
    def color(self, color_hex):
        """
        Sets a new color.

        Args:
            color_hex (str): The new color code in hexadecimal format.
        """
        int(color_hex, 16)
        self._color = color_hex

    def __str__(self):
        """Returns the string representation of the color."""
        return self._color
