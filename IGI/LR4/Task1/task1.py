from utils.inputs import valid_input
from .pickle_service import PickleService
from .csv_service import CsvService


class Item:
    def __init__(self, name, country, count):
        self._name = name
        self._country = country
        self._count = count

    def __repr__(self):
        return (f"Item (name: {self._name}, country: {self._country}, "
                f"count: {self._count})")

    def to_dict(self):
        return {
            "name": self._name,
            "country": self._country,
            "count": self._count
        }


def find_count(items):
    summary = 0
    for item in items:
        summary += int(item["count"])
    return summary


def task1():
    items = [
        Item("orange", "Zanzibar", "1000"),
        Item("apple", "France", "500"),
        Item("banana", "Ecuador", "1200"),
        Item("mango", "India", "800"),
        Item("kiwi", "New Zealand", "1500"),
        Item("kiwi", "Italy", "700"),
        Item("pineapple", "Costa Rica", "300"),
        Item("watermelon", "USA", "1800"),
        Item("orange", "Argentina", "400"),
        Item("orange", "Spain", "950")
    ]
    items_dict = [item.to_dict() for item in items]
    p_service = PickleService("Task1/data.pkl")
    c_service = CsvService("Task1/data.csv")
    p_service.write(items_dict)
    c_service.write(items_dict)
    while True:
        choose = valid_input("Choose action:\n"
                             "0 - exit\n"
                             "1 - find info about item\n"
                             "2 - items info\n"
                             "3 - sort items\n"
                             "4 - print data\n", int, 0, 4)
        if choose == 0:
            break
        elif choose == 1:
            name = valid_input("Enter name of item: ", str)
            items1 = p_service.find("name", name)
            items2 = c_service.find("name", name)
            count1 = find_count(items1)
            count2 = find_count(items2)
            print("======From pickle=====")
            print("Countries:")
            for item in items1:
                print(item["country"], " - ", item["count"])
            print(f"Total amount = {count1}")
            print("======================")
            print("======From csv=====")
            print("Countries:")
            for item in items2:
                print(item["country"], " - ", item["count"])
            print(f"Total amount = {count2}")
            print("======================")

        elif choose == 2:
            items1 = p_service.read()
            print("======From pickle=====")
            black_list = []
            for item in items1:
                if item["name"] in black_list:
                    continue
                else:
                    black_list.append(item["name"])
                    print(item["name"])
                    print("Countries:")
                    founds = p_service.find("name", item["name"])
                    count = find_count(founds)
                    for found in founds:
                        print(found["country"], " - ", found["count"])
                    print(f"Total amount = {count}")
                    print("------------------------")
            print("======================")

            items2 = c_service.read()
            print("======From csv=====")
            black_list = []
            for item in items2:
                if item["name"] in black_list:
                    continue
                else:
                    black_list.append(item["name"])
                    print(item["name"])
                    print("Countries:")
                    founds = c_service.find("name", item["name"])
                    count = find_count(founds)
                    for found in founds:
                        print(found["country"], " - ", found["count"])
                    print(f"Total amount = {count}")
                    print("------------------------")
            print("======================")

        elif choose == 3:
            name = valid_input(
                "Enter name of field to sort (name, country, count): ",
                str)
            if name != "name" and name != "country" and name != "count":
                print("Invalid input")
                continue
            p_service.sort(name)
            c_service.sort(name)
            print("Sorted!")
        else:
            items1 = p_service.read()
            print("======From pickle=====")
            for item in items1:
                print("Name:", item["name"], "| Country:", item["country"],
                      "| Amount:", item["count"])
            print("======================")

            items2 = c_service.read()
            print("======From csv=====")
            for item in items2:
                print("Name:", item["name"], "| Country:", item["country"],
                      "| Amount:", item["count"])
            print("======================")


if __name__ == "__main__":
    task1()
