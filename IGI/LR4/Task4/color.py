class FigureColor:
    def __init__(self, color_hex):
        int(color_hex, 16)
        self._color = color_hex

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color_hex):
        int(color_hex, 16)
        self._color = color_hex

    def __str__(self):
        return self._color
