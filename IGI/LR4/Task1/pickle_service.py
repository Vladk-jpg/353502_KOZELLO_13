import pickle


class PickleService:
    def __init__(self, path):
        self._path = path
        pass

    def write(self, items):
        with open(self._path, "wb") as file:
            pickle.dump(items, file)

    def read(self):
        with open(self._path, "rb") as file:
            return pickle.load(file)

    def find(self, key, value):
        items = self.read()
        found_items = []
        for item in items:
            if key in item and item[key] == value:
                found_items.append(item)
        return found_items

    def sort(self, key, reverse=False):
        items = self.read()
        sorted_items = sorted(items, key=lambda x: x.get(key), reverse=reverse)
        self.write(sorted_items)
        return sorted_items
