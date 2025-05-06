import pickle


class PickleService:
    def __init__(self, path):
        """
        Initializes the PickleService with the given file path.

        Args:
            path (str): Path to the file for serialization.
        """
        self._path = path

    def write(self, items):
        """
        Serializes and writes a collection of dictionaries to the file.

        Args:
            items (list[dict]): List of dictionaries to be saved.
        """
        with open(self._path, "wb") as file:
            pickle.dump(items, file)

    def read(self):
        """
        Reads and deserializes the data from the file.

        Returns:
            list[dict]: List of dictionaries read from the file.
        """
        with open(self._path, "rb") as file:
            return pickle.load(file)

    def find(self, key, value):
        """
        Finds dictionaries in the file where the given key has the specified
        value.

        Args:
            key (str): Key to search for.
            value (Any): Value to match.

        Returns:
            list[dict]: List of dictionaries that match the key-value
            condition.
        """
        items = self.read()
        found_items = []
        for item in items:
            if key in item and item[key] == value:
                found_items.append(item)
        return found_items

    def sort(self, key, reverse=False):
        """
        Sorts the CSV data by a specified key and rewrites the file.

        Args:
            key (str): The key (column name) to sort by.
            reverse (bool, optional): Sort in descending order if True.
                Defaults to False.

        Returns:
            list: The sorted list of rows (each row is a dictionary).
        """
        items = self.read()

        is_numeric = False
        for row in items:
            value = row.get(key)
            if value is not None:
                if isinstance(value, int):
                    is_numeric = True
                    break
                if isinstance(value, str) and value.strip().isdigit():
                    is_numeric = True
                    break
        
        if is_numeric:
            sorted_items = sorted(
                items,
                key=lambda x: int(x.get(key)) if x.get(key) is not None else 0,
                reverse=reverse
            )
        else:
            sorted_items = sorted(
                items,
                key=lambda x: x.get(key),
                reverse=reverse
            )
        
        self.write(sorted_items)
        return sorted_items
