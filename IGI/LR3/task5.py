import inputs


def print_introduction(func):
    def wrapper():
        print("This function will count sum of odd index items and items "
              "between min negative and max negative number.")
        func()
        print("End of task")
    return wrapper


def show_list(arr):
    """Print list of float numbers

    Args:
        arr (list): list for printing
    """
    print("List:")
    print(" ".join(map(str, arr)))


@print_introduction
def task5():
    """Count sum of odd index items and items between min negative
    and max negative number
    """
    lst = []
    mode = inputs.valid_input("Enter mode for input "
                              "(0 - keyboard, 1 - auto): ", int, 0, 1)
    if mode:
        count = inputs.valid_input("Enter count of numbers: ", int, 1, 100)
        for i in inputs.random_sequence(float, count=count):
            lst.append(i)
    else:
        while True:
            s = input("Enter a list of float numbers separated with space:\n")
            try:
                lst = inputs.get_list_numbers(s)
            except ValueError:
                print("Invalid input")
                continue
            break
    odd_sum = 0.0
    between_sum = 0.0
    first_neg = None
    last_neg = None
    for i in range(len(lst)):
        if i % 2 == 1:
            odd_sum += lst[i]
        if first_neg is None and lst[i] < 0:
            first_neg = i
        if lst[i] < 0:
            last_neg = i
    if first_neg is not None:
        for i in range(first_neg + 1, last_neg):
            between_sum += lst[i]

    show_list(lst)
    print(f"Sum of odd index items = {odd_sum:.2f}")
    print(f"Sum of items between min negative and max negative = "
          f"{between_sum:.2f}")


if __name__ == "__main__":
    task5()
