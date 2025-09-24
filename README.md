# Wordle Solver

This project is an automated solver for the popular word-guessing game **Wordle**.  
It attempts to guess the correct 5-letter word in as few rounds as possible by applying statistical letter frequency analysis and dynamically narrowing down possible words.

---

## Features

- **Letter frequency analysis**: Calculates how common each letter is in the provided word list and scores candidate guesses accordingly. Punishes double letters. 
- **Positional constraints**: Tracks letters that must or must not appear in each position.  
- **Adaptive filtering**: After each guess, the solver updates its list of possible words based on game feedback.  
- **Randomized top guesses**: To avoid predictability, it randomly picks a guess from the top-scoring words.  
- **Performance simulation**: Runs multiple games automatically and reports win rate and average number of rounds.

---

## Project Structure

- `main.py` — The main solver script containing:
  - Word and letter frequency calculation
  - Classes for managing position constraints (`Position`), candidate word lists (`Word`), and the game logic (`Wordle`)
  - A simulation loop to test performance across many games  

- `words.txt` — A plain text file containing valid 5-letter words (one per line). This file must be present in the same directory as `main.py`.

---

## How It Works

1. The script loads a word list from `words.txt` and computes letter frequencies.
2. A `Wordle` object picks a random target word.
3. Each round:
   - The solver chooses a high-scoring guess from the remaining valid words.
   - It evaluates the guess against the target word, simulating Wordle’s feedback:
     - `G` = Correct letter in the correct position  
     - `O` = Correct letter in the wrong position  
     - `B` = Letter not in the word  
   - The solver updates its internal constraints and filters the word list.
4. This repeats for up to 6 rounds or until the word is guessed.

At the end of the simulation, the script prints the **total win ratio** and **average number of rounds** over 1,000 games.

---

## Requirements

- Python 3.7+
- `pandas` (for reading and managing the word list)
- Standard library modules: `random`

Install dependencies with:

```bash
pip install pandas

## Customization

- Word list: Replace words.txt with a different 5-letter word list.
- Simulation count: Change the loop at the bottom of main.py to run more or fewer games.
- Scoring: Modify the guess() method of the Word class to experiment with different scoring strategies.
