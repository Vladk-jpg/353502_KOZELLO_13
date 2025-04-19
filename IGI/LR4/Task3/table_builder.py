class table_builder:
    @staticmethod
    def print_table(data):
        headers = ["x", "n", "F(x)", "Math F(x)", "eps"]

        def format_item(item):
            if isinstance(item, float):
                return f"{item:.6f}"
            return str(item)

        formatted_data = [[format_item(item) for item in row] for row in data]

        col_widths = [max(len(str(item)) for item in col)
                      for col in zip(*([headers] + formatted_data))]

        def print_row(row):
            print("| " + " | ".join(f"{str(item):<{col_widths[i]}}"
                                    for i, item in enumerate(row)) + " |")

        # Печатаем таблицу
        print("-" * (sum(col_widths) + len(col_widths) * 3 + 1))
        print_row(headers)
        print("-" * (sum(col_widths) + len(col_widths) * 3 + 1))
        for row in formatted_data:
            print_row(row)
        print("-" * (sum(col_widths) + len(col_widths) * 3 + 1))
