from .inputs import valid_input
from Task1.task1 import task1


def start_menu():
    while True:
        option = valid_input("Choose number of task (1-5, 0 - exit): ",
                             int, 0, 5)
        match option:
            case 1:
                task1()
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass
            case _:
                break
