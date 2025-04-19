from utils.inputs import valid_input
import zipfile
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


class file_service:
    @staticmethod
    def read_file(name):
        with open(name, 'r', encoding='utf-8') as f:
            text = f.read()
        return text

    @staticmethod
    def write_file(lines, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(lines)

    @staticmethod
    def zip_file(filename, zipname):
        with zipfile.ZipFile(zipname, 'w') as zipf:
            zipf.write(filename)

    @staticmethod
    def get_zip_info(zipname, filename):
        with zipfile.ZipFile(zipname, 'r') as zipf:
            info = zipf.getinfo(filename)

        return (zipf.namelist(), info.filename, info.file_size,
                info.compress_size, info.date_time)


def task2():
    while (True):
        print("======================")
        choose = valid_input("Choose action:\n"
                             "0 - exit\n"
                             "1 - find info about text\n"
                             "2 - archive results\n"
                             "3 - print archive info\n", int, 0, 4)
        print("======================")
        if choose == 0:
            break
        elif choose == 1:
            text = file_service.read_file("Task2/text.txt")
            lines = []
            lines.append("Count of sentences: "
                         f"{re_service.find_sentences_count(text)}\n")
            lines.append("Count of questions: "
                         f"{re_service.find_questions_count(text)}\n")
            lines.append("Count of exclamations: "
                         f"{re_service.find_exclamations_count(text)}\n")
            lines.append("Average count of symbols in sentence: "
                         f"{re_service.find_av_sentence_length(text)}\n")
            lines.append("Average count of symbols in word: "
                         f"{re_service.find_av_word_length(text)}\n")
            lines.append("Count of smiles: "
                         f"{re_service.find_smiles_count(text)}\n")
            lines.append("List of hexadecimal numbers: "
                         f"{re_service.find_hex(text)}\n")
            lines.append("If plus after number: "
                         f"{re_service.check_if_plus_after_number(text)}\n")
            lines.append("Four-symbol words count: "
                         f"{re_service.find_four_symbol_words(text)}\n")
            lines.append("Words with vowels and consonants count match: "
                         f"{re_service.find_match_vowels_consonants(text)}\n")
            lines.append("All words in reverse order: "
                         f"{re_service.find_words_reverse_length(text)}\n")

            file_service.write_file(lines, "Task2/result.txt")
            for line in lines:
                print(line)
        elif choose == 2:
            file_service.zip_file("Task2/result.txt", "Task2/result.zip")
            print("File 'result.txt' successfully archived!")
        else:
            try:
                info = file_service.get_zip_info("Task2/result.zip",
                                                 "Task2/result.txt")
                files, name, act_size, zip_size, date = info
                year, month, day, hours, minutes, sec = date
                print(f"Files: {files}")
                print(f"Filename: {name}")
                print(f"Size: {act_size}")
                print(f"Compress size: {zip_size}")
                print(f"Created date: {day}-{month}-{year}",
                      f"{hours}:{minutes}:{sec}")

            except FileNotFoundError:
                print("Error accured while reading zip")
