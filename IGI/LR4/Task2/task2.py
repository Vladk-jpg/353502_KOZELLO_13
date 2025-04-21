from utils.inputs import valid_input
from .re_service import ReService
from .file_service import FileService


def task2():
    """
    Main function for task 2, which provides an interactive interface for
    analyzing text and archiving the results. It performs the following
    actions:
    - Allow the user to choose different options for text analysis and
    archiving.
    - Option 1: Perform text analysis (count sentences, questions, smiles...).
    - Option 2: Archive the results in a zip file.
    - Option 3: Print archive information (details of the zip file).

    The loop continues until the user selects option 0 (exit).
    """
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
            text = FileService.read_file("Task2/text.txt")
            lines = []
            lines.append("Count of sentences: "
                         f"{ReService.find_sentences_count(text)}\n")
            lines.append("Count of questions: "
                         f"{ReService.find_questions_count(text)}\n")
            lines.append("Count of exclamations: "
                         f"{ReService.find_exclamations_count(text)}\n")
            lines.append("Average count of symbols in sentence: "
                         f"{ReService.find_av_sentence_length(text)}\n")
            lines.append("Average count of symbols in word: "
                         f"{ReService.find_av_word_length(text)}\n")
            lines.append("Count of smiles: "
                         f"{ReService.find_smiles_count(text)}\n")
            lines.append("List of hexadecimal numbers: "
                         f"{ReService.find_hex(text)}\n")
            lines.append("If plus after number: "
                         f"{ReService.check_if_plus_after_number(text)}\n")
            lines.append("Four-symbol words count: "
                         f"{ReService.find_four_symbol_words(text)}\n")
            lines.append("Words with vowels and consonants count match: "
                         f"{ReService.find_match_vowels_consonants(text)}\n")
            lines.append("All words in reverse order: "
                         f"{ReService.find_words_reverse_length(text)}\n")

            FileService.write_file(lines, "Task2/result.txt")
            for line in lines:
                print(line)
        elif choose == 2:
            FileService.zip_file("Task2/result.txt", "Task2/result.zip")
            print("File 'result.txt' successfully archived!")
        else:
            try:
                info = FileService.get_zip_info("Task2/result.zip",
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
