import pandas as pd
import random

# -----------------------------
# Configuration Parameters
# -----------------------------
WORDS_FILE = "words.txt"      # Path to the word list file
ROUNDS_PER_GAME = 6           # Number of guesses allowed per game
NUM_SIMULATIONS = 1000        # Number of games to simulate
VERBOSE = True                # Whether to print each guess and result
# -----------------------------



def get_words_and_stats(words_path):
    words_raw = []
    letter_count = {}
    overall_letter_count = 0

    with open(words_path) as f:
        for word in f:
            words_raw.append(word.strip())
            for letter in word.strip():
                if letter in letter_count:
                    letter_count[letter] += 1
                else:
                    letter_count[letter] = 1
                overall_letter_count += 1

    # Get statistics on each letter:
    letter_stats = {}

    for letter in letter_count.keys():
        letter_stats[letter] = letter_count[letter] / overall_letter_count

    return words_raw, letter_stats


def get_guess_result(guess: str, answer: str):
    """
    gets the next result of the game given the current guess and the answer
    :param guess: the new guess
    :param answer: the correct word
    :return: next state of the game
    """

    letter_accounted_for = [False, False, False, False, False]

    next_state = ''
    final = ''
    for i in range(5):
        if guess[i] == answer[i]:
            next_state += 'G'
            letter_accounted_for[i] = True
            continue
        if guess[i] not in answer:
            next_state += 'B'
            continue
        next_state += '0'

    for i in range(5):
        found = False
        if next_state[i] != '0':
            final += next_state[i]
            continue
        curr_letter = guess[i]
        for j in range(5):
            if answer[j] == curr_letter and not letter_accounted_for[j]:
                final += 'O'
                letter_accounted_for[j] = True
                found = True
                break
        if not found:
            final += 'B'

    return final


class Position:

    def __init__(self, pos: int):
        self.pos = pos
        self.exclude_letters = []
        self.known_letter = '0'

    def exclude_letter(self, letter):
        if letter != self.known_letter:
            self.exclude_letters.append(letter)

    def update_known_letter(self, letter):
        self.known_letter = letter


class Word:

    def __init__(self, words: list, letter_stats: dict):
        self.words = words
        self.letter_stats = letter_stats
        self.known_letters = set()
        self.l1 = Position(1)
        self.l2 = Position(2)
        self.l3 = Position(3)
        self.l4 = Position(4)
        self.l5 = Position(5)
        self.pos_list = [self.l1, self.l2, self.l3, self.l4, self.l5]

    def update_letters(self, guess, result):
        """
        update the parameters of the word according to new information
        """
        for i in range(len(guess)):
            if result[i] == 'G':
                self.known_letters.add(guess[i])
                self.pos_list[i].update_known_letter(guess[i])

            if result[i] == 'O':
                self.known_letters.add(guess[i])
                self.pos_list[i].exclude_letter(guess[i])

        for i in range(len(guess)):

            if result[i] == 'B' and guess[i] not in self.known_letters:
                for pos in self.pos_list:
                    pos.exclude_letter(guess[i])

    def update_words(self):
        """
        update possible words list
        """
        new_words = []
        for word in self.words:
            add_word = True
            for i in range(len(word)):
                if word[i] in self.pos_list[i].exclude_letters:
                    add_word = False
                if self.pos_list[i].known_letter != '0' and self.pos_list[i].known_letter != word[i]:
                    add_word = False
            for letter in self.known_letters:
                if letter not in word:
                    add_word = False

            if add_word:
                new_words.append(word)

        self.words = new_words

    def guess(self):
        """
        returns a guess based on available words left and stats (by max stats)
        try to avoid double letters
        """

        scores = {}
        for word in self.words:
            seen_letters = []
            score = 0
            for letter in word:
                if letter in seen_letters:
                    continue
                seen_letters.append(letter)
                score += self.letter_stats[letter]
            scores[word] = score

        top_keys = sorted(scores, key=scores.get, reverse=True)[:20]
        guess = random.choice(top_keys)


        return guess


class Wordle:

    def __init__(self, words_file):
        self.all_words, self.letter_stats = get_words_and_stats(words_file)
        self.word = Word(self.all_words, self.letter_stats)
        self.round = 0
        self.win = False

    def play_round(self, answer):
        guess = self.word.guess()

        result = get_guess_result(guess, answer)
        self.word.update_letters(guess, result)
        self.word.update_words()

        if result == 'GGGGG':
            self.win = True
        if VERBOSE:
            print(f'Round {self.round + 1}, guess: {guess}, result: {result}')
        self.round = self.round + 1

    def play_game(self):
        answer = random.choice(self.all_words)
        if VERBOSE:
            print(f'answer : {answer}')
        ROUNDS_PER_GAME = 6

        for i in range(ROUNDS_PER_GAME):
            self.play_round(answer)
            if self.win:
                return self.round

        return -1

win_lose = []
rounds = []
for i in range(NUM_SIMULATIONS):
    newGame = Wordle(WORDS_FILE)
    result = newGame.play_game()
    if result > 0:
        win_lose.append(1)
        rounds.append(result)
    else:
        win_lose.append(0)

total_win_ratio = sum(win_lose) / len(win_lose)
avg_rounds = sum(rounds) / len(rounds)

print(f'total win ratio: {total_win_ratio}')
print(f'average rounds: {avg_rounds}')