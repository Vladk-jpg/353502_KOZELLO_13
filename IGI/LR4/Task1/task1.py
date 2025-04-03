import csv
import pickle


class task1:
    def write_csv(self, items):
        with open("data.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=items[0].keys())
            writer.writeheader()
            writer.writerows(items)

    def write_pickle(self, items):
        with open("data.pkl", "wb") as file:
            pickle.dump(items, file)

    def read_csv(self):
        with open("data.csv", mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

    def read_pickle(self):
        with open("data.pkl", "rb") as file:
            return pickle.load(file)

    pass
