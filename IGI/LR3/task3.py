import inputs


def task3():
    """Function checks your string if it is an octal number
    """
    oct_num = inputs.valid_input("Enter string and program will check it on"
                                 "octal system:\n", str)
    is_oct = True
    for ch in oct_num:
        if ord(ch) < 48 or ord(ch) > 55:
            is_oct = False
            break

    if is_oct:
        print("Yes")
    else:
        print("No")


if __name__ == "__main__":
    task3()
