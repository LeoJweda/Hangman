import random

ALPHABET = [chr(chNum) for chNum in list(range(ord('a'), ord('z') + 1))]

def read_words():
  with open('./words.txt') as fp:
    return [line.rstrip().lower() for line in fp.readlines()]

class Solver:
  def __init__(self, words, word_length):
    self.__words = words
    self.__word_length = word_length

    self.__potential_words = []
    self.__preprocess_words()

  def __preprocess_words(self):
    for word in self.__words:
      if len(word) == self.__word_length:
        self.__potential_words.append(word)

  def make_guess(self, right_guesses, wrong_guesses):
    self.__potential_words = self.__filter_potential_words(right_guesses)
    letter_occurrences = self.__count_letter_occurrences(right_guesses + wrong_guesses, self.__potential_words)

    return max(letter_occurrences, key=lambda key: letter_occurrences[key])

  def __filter_potential_words(self, correct_guesses):
    potential_words = []

    for potential_word in self.__potential_words:
      matches = True

      for index, guess in enumerate(correct_guesses):
        if guess != '_' and potential_word[index] != guess:
          matches = False
          break

      if matches:
        potential_words.append(potential_word)

    return potential_words

  def __count_letter_occurrences(self, guesses, words):
    potential_letters = [x for x in ALPHABET if x not in guesses]
    letter_occurrences = {}

    for letter in potential_letters:
      letter_occurrences[letter] = 0

    for letter in potential_letters:
      for potential_word in words:
        if letter in potential_word:
          letter_occurrences[letter] += 1

    return letter_occurrences

class Game:
  def __init__(self, ai_mode=False, word = ''):
    self.__ai_mode = ai_mode

    self.__words = read_words()
    self.__silent = len(word) > 0
    self.__word = word or self.__get_random_word()

    self.__right_guesses = ['_'] * len(self.__word)
    self.__wrong_guesses = []

    for index, character in enumerate(word):
      if character not in ALPHABET:
        self.__right_guesses[index] = character

    if self.__ai_mode:
      self.__solver = Solver(self.__words, len(self.__word))

  def run(self):
    while(not self.__check_win()):
      if not self.__silent:
        self.__display()

      if self.__ai_mode:
        self.__guess(self.__solver.make_guess(self.__right_guesses, self.__wrong_guesses))
      else:
        guess = input('Enter a guess: ')

        if (len(guess) != 1):
          print("Enter one character only, dummy!")
          continue

        self.__guess(guess)

    return len(self.__wrong_guesses)

  def __guess(self, guess):
    if guess in self.__right_guesses or guess in self.__wrong_guesses:
      print("You've already guessed that, dummy!")
    else:
      indices = [i for i, x in enumerate(self.__word) if x == guess]

      if len(indices) > 0:
        for index in indices:
          self.__right_guesses[index] = guess
      else:
        self.__wrong_guesses.append(guess)

  def __check_win(self):
    if '_' in self.__right_guesses:
      return False

    print(self.__word)
    return True

  def __display(self):
    print(''.join(self.__right_guesses))
    print(' '.join(self.__wrong_guesses) + "\n")

  def __get_random_word(self):
    word = self.__words[random.randrange(0, len(self.__words) - 1)]

    return word

class Tester:
  LIMIT = 6

  def __init__(self):
    self.__words = read_words()
    self.__successes = 0

  def test(self):
    for word in self.__words:
      if Game(True, word).run() < self.LIMIT:
        self.__successes += 1

    print('Total words: ', len(self.__words))
    print('Successful words: ', self.__successes)
    print('Success ratio: ', self.__successes / len(self.__words))

Game(True).run()
# Tester().test()
