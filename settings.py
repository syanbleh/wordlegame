# settings.py

# Load words from wordbank.txt
def load_word_list():
    with open('wordbank.txt', 'r') as file:
        return [line.strip().upper() for line in file.readlines()]

WORD_LIST = load_word_list()

# Game settings
MAX_ATTEMPTS = 5
WORD_LENGTH = 5