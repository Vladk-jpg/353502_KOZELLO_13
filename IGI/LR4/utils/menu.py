from .inputs import valid_input
from Task1.task1 import task1
from Task2.task2 import task2
from Task3.task3 import task3
from Task4.task4 import task4
from Task5.task5 import task5


def start_menu():
    while True:
        option = valid_input("Choose number of task (1-5, 0 - exit): ",
                             int, 0, 5)
        match option:
            case 1:
                task1()
            case 2:
                task2()
            case 3:
                task3()
            case 4:
                task4()
            case 5:
                task5()
            case _:
                break
