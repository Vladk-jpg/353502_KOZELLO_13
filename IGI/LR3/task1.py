import math
import inputs


def print_table(data):
    """Function for printing beautiful result table

    Args:
        data (list): list constists 5 items in direction:
                     x, n, F(x), Math F(x), eps
    """
    headers = ["x", "n", "F(x)", "Math F(x)", "eps"]
    col_widths = [max(len(str(item)) for item in col)
                  for col in zip(*([headers] + [data]))]

    def print_row(row):
        print("| " + " | ".join(f"{str(item):<{col_widths[i]}}"
                                for i, item in enumerate(row)) + " |")

    print("-" * (sum(col_widths) + len(col_widths) * 3 + 1))
    print_row(headers)
    print("-" * (sum(col_widths) + len(col_widths) * 3 + 1))

    print_row(data)

    print("-" * (sum(col_widths) + len(col_widths) * 3 + 1))


def task1():
    """Function for calculation sum of Tailor series and comparing with
    build-in math.py function
    """
    x = inputs.valid_input("Enter function argument x: ", float, 0.0, 1.0)
    eps = inputs.valid_input("Enter epsilon: ", float, 0.0)
    n = 0
    m_fx = math.log(1 + x)
    fx = 0.0
    for i in range(1, 501):
        fx += (-1) ** (i - 1) * (x ** i) / i
        n += 1
        if math.fabs(fx - m_fx) < eps:
            break

    print_table([x, n, fx, m_fx, eps])


if __name__ == "__main__":
    task1()
