class TableBuilder:
    """
    A class for printing data in a formatted table.
    """
    @staticmethod
    def print_table(data):
        """
        Prints the given data in a formatted table with headers "x", "n",
        "F(x)", "Math F(x)", "eps".

        Args:
            data (list of lists): The data to be displayed in the table. Each
            inner list represents a row.
        """
        headers = ["x", "n", "F(x)", "Math F(x)", "eps"]

        def format_item(item):
            """Formats an item to 6 decimal places if it's a float, otherwise
            returns it as a string."""
            if isinstance(item, float):
                return f"{item:.6f}"
            return str(item)

        # Format the data
        formatted_data = [[format_item(item) for item in row] for row in data]

        # Calculate column widths
        col_widths = [max(len(str(item)) for item in col)
                      for col in zip(*([headers] + formatted_data))]

        def print_row(row):
            """Prints a single row with the appropriate formatting."""
            print("| " + " | ".join(f"{str(item):<{col_widths[i]}}"
                                    for i, item in enumerate(row)) + " |")

        # Print the table
        print("-" * (sum(col_widths) + len(col_widths) * 3 + 1))
        print_row(headers)
        print("-" * (sum(col_widths) + len(col_widths) * 3 + 1))
        for row in formatted_data:
            print_row(row)
        print("-" * (sum(col_widths) + len(col_widths) * 3 + 1))
