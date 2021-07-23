import os
import random

# Random Sentence Generator
# by Ben Baptist 2021

""" This will utilize the built-in words file on *nix-based platforms. If it
does not exist, however, then it will grab an online repository hosting it.

It only depends on requests IF the local words folder does not exist. Otherwise,
it will never try to import the requests module.
"""

paths = [
    "/usr/share/dict/words",
    "/usr/dict/words",
    "https://raw.githubusercontent.com/eneko/data-repository/master/data/words.txt"
]

for path in paths:
    if "https" in path:
        import requests
        r = requests.get(path)

        all_words = r.text
    else:
        if os.path.exists(path):
            with open(path, "r") as f:
                all_words = f.read()

            break

all_words = all_words.split("\n")

def generate_sentence(word_count):
    sentence = [random.choice(all_words).capitalize() for i in range(word_count)]
    return " ".join(sentence)

if __name__ == "__main__":
    print(generate_sentence(5))
