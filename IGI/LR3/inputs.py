import os
import random
import string


def valid_input(text, value_type, min_value=None, max_value=None):
    """Function for user input and validation

    Args:
        text (string): Text prined before user input
        value_type (type): Type of data
        min_value (int/float/str, optional): Minimum input value.
                                             Defaults to None.
        max_value (int/float/str, optional): Maximum input value.
                                             Defaults to None.

    Raises:
        ValueError: Input data not in such scope

    Returns:
        int/float/str: Validated user input
    """
    while True:
        try:
            value = value_type(input(text))
            if min_value is not None and value < min_value:
                raise ValueError(f"Invalid input data. Mast be in "
                                 f"[{min_value}, {max_value}]")
            if max_value is not None and value > max_value:
                raise ValueError(f"Invalid input data. Mast be in "
                                 f"[{min_value}, {max_value}]")
            return value
        except ValueError as error:
            print(f"Error: {error}. Please, enter valid data")


def random_generator(value_type, min_value=None, max_value=None):
    """Generates random value with 'value_type' type

    Args:
        value_type (type): Type of generating value
        min_value (int/string/float, optional): Minimum input data value.
                                                Defaults to None.
        max_value (int/string/float, optional): Maximum input data value.
                                                Defaults to None.

    Raises:
        TypeError: Usupported data type

    Returns:
        int/str/float: Randomly generated value
    """
    if value_type == str:
        if min_value is None:
            min_value = 1
        if max_value is None:
            max_value = 10

        random.seed(os.urandom())
        length = random.randint(min_value, max_value)
        characters = string.ascii_letters + string.digits + string.punctuation
        random_string = ''.join(random.choice(characters)
                                for _ in range(length))
        return random_string

    else:
        if min_value is None:
            min_value = float('-100.0')
        if max_value is None:
            max_value = float('100.0')

        if value_type == int:
            random_num = random.randint(int(min_value), int(max_value))
        elif value_type == float:
            random_num = round(random.uniform(min_value, max_value), 2)
        else:
            raise TypeError("Unsupported data type. Please enter int/string"
                            "/float")

        return random_num


def is_float(s):
    """Check is string converting in float

    Args:
        s (str): String for checking

    Returns:
        bool: Result of checking
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_list_numbers(s):
    """Converts string to float number list

    Args:
        s (str): String for converting

    Raises:
        ValueError: If string is empty
        ValueError: If at least one element isn't float

    Returns:
        list: list of float numbers
    """
    if not s:
        raise ValueError
    arr = s.split(' ')
    for i in range(len(arr)):
        arr[i] = arr[i].strip()
        if not arr[i]:
            del arr[i]
        elif not is_float(arr[i]):
            raise ValueError
        else:
            arr[i] = float(arr[i])
    return arr
