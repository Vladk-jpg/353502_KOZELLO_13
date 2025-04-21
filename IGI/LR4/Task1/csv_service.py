import csv


class CsvService:
    """
    A service for reading, writing, finding, and sorting CSV data.

    Attributes:
        _path (str): Path to the CSV file.
    """

    def __init__(self, path):
        """
        Initializes the CsvService with the given file path.

        Args:
            path (str): Path to the CSV file.
        """
        self._path = path

    def write(self, items):
        """
        Writes a list of dictionaries to the CSV file.

        Args:
            items (list): List of dictionaries to write.
        """
        with open(
            self._path, mode="w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(file, fieldnames=items[0].keys())
            writer.writeheader()
            writer.writerows(items)

    def read(self):
        """
        Reads data from the CSV file and returns it as a list of dictionaries.

        Returns:
            list: List of rows (each row is a dictionary).
        """
        with open(self._path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

    def find(self, key, value):
        """
        Finds rows where a specified key has a given value.

        Args:
            key (str): The key (column name) to search for.
            value (str): The value to match.

        Returns:
            list: List of matching rows (each row is a dictionary).
        """
        with open(self._path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            found_items = []
            for row in reader:
                if key in row and row[key] == value:
                    found_items.append(row)
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
        sorted_items = sorted(
            items, key=lambda x: x.get(key), reverse=reverse
        )
        self.write(sorted_items)
        return sorted_items
