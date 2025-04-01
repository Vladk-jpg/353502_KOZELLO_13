import inputs


def start_menu():
    while True:
        option = inputs.valid_input("Choose number of task (1-5, 0 - exit): ",
                                    int, 0, 5)
        match option:
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass
            case _:
                break
