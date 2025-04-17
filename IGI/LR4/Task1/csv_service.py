import csv


class csv_service:
    def __init__(self, path):
        self._path = path
        pass

    def write(self, items):
        with open(self._path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=items[0].keys())
            writer.writeheader()
            writer.writerows(items)

    def read(self):
        with open(self._path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

    def find(self, key, value):
        with open(self._path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            found_items = []
            for row in reader:
                if key in row and row[key] == value:
                    found_items.append(row)
            return found_items

    def sort(self, key, reverse=False):
        items = self.read()
        sorted_items = sorted(items, key=lambda x: x.get(key), reverse=reverse)
        self.write(sorted_items)
        return sorted_items
