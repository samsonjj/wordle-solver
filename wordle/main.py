import re
from typing import List

class Knowledge:
    def __init__(self):
        self.letters_left = 'abcdefghijklmnopqrstuvwxyz'
        self.must_have = ''
        self.known_letters = '.....'
    
    def get_regex(self):
        expression = "".join(self.known_letters.replace('.', f'[{self.letters_left}]'))
        return re.compile(expression)


def possible_words(words: List[str], knowledge: Knowledge) -> List[str]:
    reg = knowledge.get_regex()
    words = filter(lambda w: reg.match(w), words)

    for c in knowledge.must_have:
        words = [w for w in words if c in w]

    return words


def score(word: str, knowledge: Knowledge):
    """returns a score on how optimal the guess is, based on the knowledge it provides
    """
    s = 0
    for c in word:
       if c in knowledge.letters_left:
           s += 1
    for i in range(0,5):
        if word[i] in word[i+1:]:
            s -= 1
    return s


def optimal_guess(words: List[str], knowledge: Knowledge):
    guesses = words.copy()
    guesses.sort(key=lambda w: score(w, knowledge))
    return guesses[:5]


def main():
    # assert file only has 5 letter words
    with open('words5.txt', 'r') as f:
        words = [w.lower() for w in f.read().split(',')]

    possible = words.copy()

    knowledge = Knowledge()

    while True:
        wrong = input('wrong letters: ')
        half = input('half correct: ')
        known = input('known: ')

        knowledge.letters_left = "".join([c for c in knowledge.letters_left if c not in wrong])
        knowledge.must_have += half
        knowledge.known_letters = known

        possible = possible_words(possible, knowledge)
        print(possible)
        print("optimal guess is: ", optimal_guess(words, knowledge))


def gen_file():
    # read words from file
    with open('words.txt', 'r') as f:
        words = [line.strip().lower() for line in f.readlines()]

    # filter 5 letter words
    five_letter_words = filter(lambda w: len(w) == 5, words)
    five_letter_words = filter(lambda w: w.isalpha(), five_letter_words)

    # format output
    output = ",".join(five_letter_words)

    # save back to file
    with open('words5.txt', 'w') as f:
        f.write(output)


if __name__ == "__main__":
    main()
