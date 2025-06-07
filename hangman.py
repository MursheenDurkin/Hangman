import random

# List of words for the game
WORD_LIST = [
    "python", "programming", "computer", "developer", "algorithm",
    "keyboard", "monitor", "software", "hardware", "internet",
    "variable", "function", "loop", "condition", "debugging"
]

# ASCII art for the hangman figure (progresses as incorrect guesses increase)
HANGMAN_PICS = [
    """
       +---+
       |   |
           |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """
]

def get_random_word(word_list):
    """Chooses a random word from the given list."""
    return random.choice(word_list).lower() # Ensure word is lowercase

def display_game_state(secret_word_letters, guessed_letters, incorrect_guesses):
    """
    Displays the current state of the game: hangman, word progress, and guessed letters.
    """
    print(HANGMAN_PICS[len(incorrect_guesses)]) # Show appropriate hangman stage

    # Display the word with guessed letters revealed
    display_word = ""
    for letter in secret_word_letters:
        if letter in guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "
    print(display_word)

    # Display already guessed letters
    print(f"\nGuessed letters: {', '.join(sorted(guessed_letters))}")
    print(f"Incorrect guesses left: {len(HANGMAN_PICS) - 1 - len(incorrect_guesses)}") # Max attempts - current incorrect


def play_hangman():
    """Main function to play a round of Hangman."""
    print("Welcome to Hangman!")
    secret_word = get_random_word(WORD_LIST)
    secret_word_letters = list(secret_word) # Convert word to a list of characters

    guessed_letters = set() # Use a set for faster lookup of guessed letters
    incorrect_guesses = [] # List to store incorrect guesses

    max_incorrect_guesses = len(HANGMAN_PICS) - 1 # 6 incorrect guesses allowed (0-indexed list)

    while True:
        print("\n" + "="*40)
        display_game_state(secret_word_letters, guessed_letters, incorrect_guesses)
        print("="*40)

        # Check for win/loss conditions
        if "".join([letter for letter in secret_word_letters if letter in guessed_letters]) == secret_word:
            print(f"\nCongratulations! You guessed the word: {secret_word.upper()}!")
            break
        elif len(incorrect_guesses) >= max_incorrect_guesses:
            print(HANGMAN_PICS[max_incorrect_guesses]) # Show final hangman
            print(f"\nGame Over! You ran out of guesses. The word was: {secret_word.upper()}")
            break

        guess = input("Guess a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print(f"You already guessed '{guess}'. Try a different letter.")
            continue

        guessed_letters.add(guess) # Add the new guess to the set

        if guess in secret_word_letters:
            print(f"Good guess! '{guess}' is in the word.")
        else:
            print(f"Sorry, '{guess}' is not in the word.")
            incorrect_guesses.append(guess)

# Run the game
if __name__ == "__main__":
    play_hangman()