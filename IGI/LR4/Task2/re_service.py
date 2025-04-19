import re


class re_service:
    @staticmethod
    def find_sentences_count(text):
        pattern = r'.+?[.!?]+'
        matches = re.findall(pattern, text)
        return len(matches)

    @staticmethod
    def find_questions_count(text):
        pattern = r'.+?\?+'
        matches = re.findall(pattern, text)
        return len(matches)

    @staticmethod
    def find_exclamations_count(text):
        pattern = r'.+?\!+'
        matches = re.findall(pattern, text)
        return len(matches)

    @staticmethod
    def find_av_sentence_length(text):
        pattern = r'.+?[.!?]+'
        matches = re.findall(pattern, text)
        sum = 0
        for line in matches:
            sum += len(re.findall(r'\w', line))
        return sum // len(matches)

    @staticmethod
    def find_av_word_length(text):
        pattern = r'\b\w+\b'
        matches = re.findall(pattern, text)
        sum = 0
        for line in matches:
            sum += len(line)
        return sum // len(matches)

    @staticmethod
    def find_smiles_count(text):
        pattern = r'[:;]-*(?:\)+|\(+|\[+|\]+)'
        matches = re.findall(pattern, text)
#        for line in matches:
#            print(line)
        return len(matches)

    @staticmethod
    def find_hex(text):
        pattern = r'\b[0-9a-fA-F]+\b'
        matches = re.findall(pattern, text)
        return matches

    @staticmethod
    def check_if_plus_after_number(text):
        pattern = r'[0-9]\s*\+'
        matches = re.findall(pattern, text)
        return len(matches) != 0

    @staticmethod
    def find_four_symbol_words(text):
        pattern = r'\b\w{4}\b'
        matches = re.findall(pattern, text)
        return len(matches)

    @staticmethod
    def find_match_vowels_consonants(text):
        pattern = r'\b\w+\b'
        words = re.findall(pattern, text)
        vowels_pattern = r'[аёуеыоэяиюЁУЕЫАОЭЯИЮ]'
        pos_arr = []
        for i in range(len(words)):
            vowels = len(re.findall(vowels_pattern, words[i]))
            consonants = len(words[i]) - vowels
            if consonants == vowels and vowels != 0:
                pos_arr.append(f"{words[i]} - {i}")
        return pos_arr

    @staticmethod
    def find_words_reverse_length(text):
        pattern = r'\b\w+\b'
        words = re.findall(pattern, text)
        res = ", ".join(sorted(words, key=len, reverse=True))
        return res
