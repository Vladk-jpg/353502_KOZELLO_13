def del_prep(s):
    """Function for deleting all prepositions in string

    Args:
        s (str): String for formating

    Returns:
        str: Clean string
    """
    clean_text = "".join(c for c in s if c.isalnum() or c.isspace())
    return clean_text


def count_of_words(s):
    """Function for counting all words and only words with odd
       count of letters in 's' string

    Args:
        s (str): String for calculations

    Returns:
        (int, int): Cortage is consisted of count of all words and count of
                    only words with odd count of letters
    """
    new_s = del_prep(s)
    arr = new_s.split(' ')
    odd_count = 0
    for i in arr:
        if len(i) % 2 == 1:
            odd_count += 1

    return len(arr), odd_count


def find_min_word(s, c):
    """Funtion finds minimum specific letter start word

    Args:
        s (str): String for calculations
        c (str): First symbol of word

    Returns:
        str: Min specific letter start word
    """
    new_s = del_prep(s)
    new_s = new_s.lower()
    arr = new_s.split(' ')
    word = ""
    min_length = len(s)
    for w in arr:
        if w[0] == c and len(w) < min_length:
            word = w
            min_length = len(word)

    return word


def get_repeted_words(s):
    """Function calculate repeated words and returns them as a dict

    Args:
        s (str): String for calculations

    Returns:
        dict: Consists of word-count key-value pairs
    """
    new_s = del_prep(s)
    new_s = new_s.lower()
    arr = new_s.split(' ')
    words = {}
    for w in arr:
        if w in words:
            words[w] += 1
        else:
            words[w] = 1
    for w in arr:
        if words[w] == 1:
            del words[w]
    return words


def task4():
    """Function prints count of all words, count of odd words,
       minimum 'i'-start word and all repeating words in build-in string
    """
    s = "So she was considering in her own mind, as well as she could, " \
        "for the hot day made her feel very sleepy and stupid, whether " \
        "the pleasure of making a daisy-chain would be worth the " \
        "trouble of getting up and picking the daisies, when suddenly " \
        "a White Rabbit with pink eyes ran close by her."

    count, odd_count = count_of_words(s)
    min_i_word = find_min_word(s, 'i')
    rep_words = get_repeted_words(s)

    print(f"Count of all words = {count}")
    print(f"Count of odd words = {odd_count}")
    print(f"Minimum 'i'-start word - '{min_i_word}'")
    print("Repeated words:")
    for word, value in rep_words.items():
        print(f"{word} - {value}")
    pass


if __name__ == "__main__":
    task4()
