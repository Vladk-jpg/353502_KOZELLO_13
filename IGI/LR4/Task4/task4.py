from .triangle import Triangle
from utils.inputs import valid_input
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math


def draw_triangle(triangle_obj, label=None):
    """
    Draws a triangle based on the given `Triangle` object and displays it.

    Args:
        triangle_obj (Triangle): The triangle object with side lengths and
        color.
        label (str, optional): Label to display on the triangle. Defaults to
        None.
    """
    a, b, c = triangle_obj.get_sides()
    color = '#' + triangle_obj.get_color()

    A = (0, 0)
    B = (c, 0)
    cos_angle = (a**2 + c**2 - b**2) / (2 * a * c)
    angle = math.acos(cos_angle)
    C = (a * math.cos(angle), a * math.sin(angle))

    fig, ax = plt.subplots()
    triangle_patch = patches.Polygon([A, B, C], closed=True, facecolor=color)
    ax.add_patch(triangle_patch)

    center_x = (A[0] + B[0] + C[0]) / 3
    if label:
        label_y = min(A[1], B[1], C[1]) - max(a, b, c) * 0.1
        ax.text(center_x, label_y, label,
                ha='center', va='top', color='black', fontsize=12)

    ax.set_aspect('equal')
    padding = max(a, b, c) * 0.2
    ax.set_xlim(min(A[0], B[0], C[0]) -
                padding, max(A[0], B[0], C[0]) + padding)
    ax.set_ylim(min(A[1], B[1], C[1]) -
                padding, max(A[1], B[1], C[1]) + padding)

    plt.axis('off')
    plt.savefig("Task4/triangle.png")
    plt.show()


def task4():
    """
    Provides an interactive menu for triangle-related operations:
    1. Create a triangle by entering side lengths and color.
    2. Display triangle information.
    3. Draw the triangle figure.

    Loops until the user chooses to exit.
    """
    triang = None
    while True:
        print("======================")
        choose = valid_input("Choose action:\n"
                             "0 - exit\n"
                             "1 - make triangle\n"
                             "2 - get info about triangle\n"
                             "3 - show figure\n", int, 0, 4)
        print("======================")
        if choose == 0:
            break
        elif choose == 1:
            a = valid_input("Enter first side: ", float, 0.0)
            b = valid_input("Enter second side: ", float, 0.0)
            c = valid_input("Enter third side: ", float, 0.0)
            color = valid_input("Enter color (HEX format): ", str)
            if len(color) != 6 and int(color, 16):
                print("Invalid input")
                continue
            try:
                triang = Triangle(a, b, c, color)
                print("Success!")
            except ValueError:
                print("Invalid color format")
        elif choose == 2:
            if not triang:
                print("Firstly, make triangle!")
                continue
            print(triang.get_info())
        else:
            if not triang:
                print("Firstly, make triangle!")
                continue
            title = valid_input("Enter title: ", str)
            draw_triangle(triang, title)
