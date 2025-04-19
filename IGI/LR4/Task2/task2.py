from utils.inputs import valid_input
from .re_service import re_service
from .file_service import file_service


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
