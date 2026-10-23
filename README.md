# Hangman

A feature-rich terminal Hangman game built in Python with colored output, multiple word categories, difficulty levels, hints, and session statistics.

## Features

- **6 Word Categories**: Technology, Animals, Countries, Movies & TV, Science, Food & Drink (plus Random Mix)
- **3 Difficulty Levels**: Easy (8 guesses), Normal (6 guesses), Hard (4 guesses + no hints)
- **Hint System**: Reveal a hidden letter at the cost of one wrong guess
- **Colored Terminal Output**: Color-coded feedback, progress bars, and hangman art (via colorama)
- **Session Statistics**: Tracks wins, losses, win rate, current streak, and best streak
- **Clean Interface**: Clear-screen transitions, formatted menus, and visual progress bar

## Preview

```
  Category: Technology    Difficulty: Normal
  ─────────────────────────────────────────────

       +---+
       |   |
       O   |
      /|   |
           |
           |
     =========

  Word:  P _ T H O N

  Wrong:  A   E   I

  Remaining: ████████████░░░░░░░░ 3/6
  Hints: 2 left (type ? to use)
  ─────────────────────────────────────────────
```

## Requirements

- Python 3.7+
- **colorama** (optional, the game works without it, just no colors)

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MursheenDurkin/Hangman.git
   cd Hangman
   ```

2. **Install dependencies** (optional, for colored output):
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game:**
   ```bash
   python hangman.py
   ```

## How to Play

1. Select **New Game** from the main menu
2. Choose a word category (or Random Mix for all categories)
3. Pick a difficulty level
4. Guess letters one at a time, correct letters are revealed, wrong guesses build the hangman
5. Type `?` to use a hint (reveals a random letter, costs one guess)
6. Guess the full word before the hangman is complete to win!

## Controls

| Input | Action |
|-------|--------|
| `a-z` | Guess a letter |
| `?` | Use a hint (Easy/Normal only) |
| `1-7` | Menu and category selections |

## Project Structure

```
Hangman/
├── hangman.py          # Main game file
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```
