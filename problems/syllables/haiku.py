"""Haiku challenge scaffold. Python 3.10+, standard library only.

Run:
    python haiku.py words.json STARTER1 STARTER2 STARTER3 STARTER4 STARTER5

words.json must contain the challenge's official word attributes:
    [
        {"text": "here", "syllables": 1, "part_of_speech": "adverb"},
        {"text": "challenging", "syllables": 3, "part_of_speech": "adjective"}
    ]

The entries above illustrate the format only; replace them with the full list.
Implement generate_haiku() to return three lists of Word objects.
"""

import json

LINE_SYLLABLES = (5, 7, 5)
REQUIRED_PARTS = {"adjective", "adverb", "noun", "verb"}
WORD_LIST = "words.json"
STARTERS = ["A", "Absolute", "Accelerate", "Always", "Animal"]


def generate_haiku(starter, words):
    """Return three lines, each a list of word records. Fill this in."""
    # TODO: keep this dummy for now
    return []


def print_haiku(haiku):
    for line in haiku:
        text = " ".join(word["word"] for word in line)
        syllables = sum(word["syllables"] for word in line)
        print(f"{text} ({syllables})")


if __name__ == "__main__":
    with open(WORD_LIST, encoding="utf-8") as file:
        words = json.load(file)

    words_by_name = {word["word"].casefold(): word for word in words}

    for name in STARTERS:
        haiku = generate_haiku(words_by_name[name.casefold()], words)
        print_haiku(haiku)
        print()
