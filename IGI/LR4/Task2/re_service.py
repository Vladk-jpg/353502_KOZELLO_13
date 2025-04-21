import re


class ReService:
    """
    A service for performing various regular expression-based text analyses.
    """

    @staticmethod
    def find_sentences_count(text):
        """
        Counts the number of sentences in the given text.

        Args:
            text (str): The input text to analyze.

        Returns:
            int: The number of sentences in the text.
        """
        pattern = r'.+?[.!?]+'
        matches = re.findall(pattern, text)
        return len(matches)

    @staticmethod
    def find_questions_count(text):
        """
        Counts the number of questions in the given text.

        Args:
            text (str): The input text to analyze.

        Returns:
            int: The number of questions (sentences ending with '?').
        """
        pattern = r'.+?\?+'
        matches = re.findall(pattern, text)
        return len(matches)

    @staticmethod
    def find_exclamations_count(text):
        """
        Counts the number of exclamatory sentences in the given text.

        Args:
            text (str): The input text to analyze.

        Returns:
            int: The number of exclamatory sentences
            (sentences ending with '!').
        """
        pattern = r'.+?\!+'
        matches = re.findall(pattern, text)
        return len(matches)

    @staticmethod
    def find_av_sentence_length(text):
        """
        Calculates the average sentence length in terms of words.

        Args:
            text (str): The input text to analyze.

        Returns:
            int: The average number of words per sentence.
        """
        pattern = r'.+?[.!?]+'
        matches = re.findall(pattern, text)
        total_words = 0
        for sentence in matches:
            total_words += len(re.findall(r'\w', sentence))
        return total_words // len(matches) if matches else 0

    @staticmethod
    def find_av_word_length(text):
        """
        Calculates the average length of words in the given text.

        Args:
            text (str): The input text to analyze.

        Returns:
            int: The average word length.
        """
        pattern = r'\b\w+\b'
        matches = re.findall(pattern, text)
        total_length = 0
        for word in matches:
            total_length += len(word)
        return total_length // len(matches) if matches else 0

    @staticmethod
    def find_smiles_count(text):
        """
        Counts the number of smiley faces (emoticons) in the given text.

        Args:
            text (str): The input text to analyze.

        Returns:
            int: The number of smiley faces found.
        """
        pattern = r'[:;]-*(?:\)+|\(+|\[+|\]+)'
        matches = re.findall(pattern, text)
        return len(matches)

    @staticmethod
    def find_hex(text):
        """
        Finds all hexadecimal numbers in the text.

        Args:
            text (str): The input text to analyze.

        Returns:
            list: A list of hexadecimal numbers found in the text.
        """
        pattern = r'\b[0-9a-fA-F]+\b'
        matches = re.findall(pattern, text)
        return matches

    @staticmethod
    def check_if_plus_after_number(text):
        """
        Checks if there is a '+' sign immediately after a number in the text.

        Args:
            text (str): The input text to analyze.

        Returns:
            bool: True if there is a '+' after a number, otherwise False.
        """
        pattern = r'[0-9]\s*\+'
        matches = re.findall(pattern, text)
        return len(matches) != 0

    @staticmethod
    def find_four_symbol_words(text):
        """
        Finds all words with exactly four characters in the text.

        Args:
            text (str): The input text to analyze.

        Returns:
            int: The number of four-letter words found.
        """
        pattern = r'\b\w{4}\b'
        matches = re.findall(pattern, text)
        return len(matches)

    @staticmethod
    def find_match_vowels_consonants(text):
        """
        Finds words where the number of vowels is equal to the number of
        consonants.

        Args:
            text (str): The input text to analyze.

        Returns:
            list: A list of words (with their index) where vowels and
            consonants match.
        """
        pattern = r'\b\w+\b'
        words = re.findall(pattern, text)
        vowels_pattern = r'[аёуеыоэяиюЁУЕЫАОЭЯИЮ]'
        pos_arr = []
        for i, word in enumerate(words):
            vowels = len(re.findall(vowels_pattern, word))
            consonants = len(word) - vowels
            if consonants == vowels and vowels != 0:
                pos_arr.append(f"{word} - {i}")
        return pos_arr

    @staticmethod
    def find_words_reverse_length(text):
        """
        Returns all words in the text sorted by length in descending order.

        Args:
            text (str): The input text to analyze.

        Returns:
            str: A string of words sorted by length in descending order.
        """
        pattern = r'\b\w+\b'
        words = re.findall(pattern, text)
        res = ", ".join(sorted(words, key=len, reverse=True))
        return res
