#!/usr/bin/env python3
"""
Hangman - A feature-rich terminal word guessing game.
Features: 6 word categories, 3 difficulty levels, hints, score tracking, colored output.
"""

import random
import os
import time

# ─── Color Setup (graceful fallback if colorama not installed) ────────────────

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class _NoColor:
        """Stub so the game works without colorama — just no colors."""
        def __getattr__(self, _):
            return ""
    Fore = Style = _NoColor()

# ─── Constants ────────────────────────────────────────────────────────────────

TITLE = f"""{Fore.CYAN}
    ╔═══════════════════════════════════╗
    ║         H A N G M A N             ║
    ║       Terminal Word Game          ║
    ╚═══════════════════════════════════╝{Style.RESET_ALL}"""

HANGMAN_STAGES = [
    """
       +---+
       |   |
           |
           |
           |
           |
     =========""",
    """
       +---+
       |   |
       O   |
           |
           |
           |
     =========""",
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
     =========""",
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
     =========""",
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
     =========""",
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
     =========""",
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
     =========""",
]

CATEGORIES = {
    "Technology": [
        "algorithm", "bluetooth", "compiler", "database", "encryption",
        "firewall", "graphics", "hardware", "interface", "javascript",
        "keyboard", "linux", "malware", "network", "operating",
        "protocol", "quantum", "router", "software", "terminal",
        "upload", "virtual", "wireless", "python", "cybersecurity",
    ],
    "Animals": [
        "elephant", "giraffe", "penguin", "dolphin", "chameleon",
        "flamingo", "cheetah", "buffalo", "scorpion", "octopus",
        "wolverine", "kangaroo", "tortoise", "jellyfish", "crocodile",
        "butterfly", "hedgehog", "platypus", "mongoose", "anaconda",
    ],
    "Countries": [
        "australia", "brazil", "canada", "denmark", "ethiopia",
        "finland", "germany", "honduras", "indonesia", "jamaica",
        "portugal", "singapore", "thailand", "ukraine", "argentina",
        "colombia", "malaysia", "philippines", "switzerland", "zimbabwe",
    ],
    "Movies & TV": [
        "inception", "gladiator", "interstellar", "avatar", "terminator",
        "predator", "jurassic", "stranger", "breaking", "mandalorian",
        "wednesday", "succession", "narcos", "vikings", "severance",
        "oppenheimer", "deadpool", "avengers", "parasite", "jaws",
    ],
    "Science": [
        "molecule", "quantum", "chromosome", "telescope", "evolution",
        "neutron", "specimen", "hypothesis", "catalyst", "ecosystem",
        "organism", "asteroid", "isotope", "electron", "pathogen",
        "photon", "genome", "plasma", "velocity", "friction",
    ],
    "Food & Drink": [
        "spaghetti", "chocolate", "avocado", "croissant", "espresso",
        "hamburger", "pancakes", "cinnamon", "mushroom", "pineapple",
        "jalapeno", "artichoke", "pistachio", "mozzarella", "kombucha",
        "quesadilla", "tiramisu", "bruschetta", "guacamole", "sourdough",
    ],
}

DIFFICULTIES = {
    "1": {"name": "Easy",   "max_wrong": 8, "hints": True},
    "2": {"name": "Normal", "max_wrong": 6, "hints": True},
    "3": {"name": "Hard",   "max_wrong": 4, "hints": False},
}

# ─── Utility Functions ────────────────────────────────────────────────────────

def clear():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def divider(width=45):
    """Print a horizontal divider."""
    print(f"  {Fore.CYAN}{'─' * width}{Style.RESET_ALL}")


def header(text, width=45):
    """Print a formatted section header."""
    print(f"\n  {Fore.CYAN}{'─' * width}")
    print(f"    {text}")
    print(f"  {'─' * width}{Style.RESET_ALL}")


def progress_bar(current, maximum, width=20):
    """Render a colored progress bar string."""
    filled = int(width * current / maximum) if maximum > 0 else 0
    bar = "█" * filled + "░" * (width - filled)
    ratio = current / maximum if maximum > 0 else 0
    if ratio > 0.5:
        color = Fore.GREEN
    elif ratio > 0.25:
        color = Fore.YELLOW
    else:
        color = Fore.RED
    return f"{color}{bar}{Style.RESET_ALL} {current}/{maximum}"


def get_stage_index(wrong_count, max_wrong):
    """Map the wrong-guess count to a hangman art stage, scaled to difficulty."""
    if wrong_count == 0:
        return 0
    max_stage = len(HANGMAN_STAGES) - 1
    return min(max_stage, wrong_count * max_stage // max_wrong)

# ─── Display Functions ────────────────────────────────────────────────────────

def show_title():
    """Show the title screen."""
    clear()
    print(TITLE)


def show_menu():
    """Display the main menu and return the user's choice."""
    print(f"\n  {Fore.WHITE}[1]{Style.RESET_ALL} New Game")
    print(f"  {Fore.WHITE}[2]{Style.RESET_ALL} How to Play")
    print(f"  {Fore.WHITE}[3]{Style.RESET_ALL} Quit\n")
    while True:
        choice = input(f"  {Fore.CYAN}> {Style.RESET_ALL}").strip()
        if choice in ("1", "2", "3"):
            return choice
        print(f"  {Fore.RED}Enter 1, 2, or 3.{Style.RESET_ALL}")


def show_how_to_play():
    """Display game instructions."""
    clear()
    header("HOW TO PLAY")
    print(f"""
  Guess the hidden word one letter at a time.

  {Fore.GREEN}Correct guess{Style.RESET_ALL}  - Letter is revealed in the word
  {Fore.RED}Wrong guess{Style.RESET_ALL}    - Hangman progresses one step
  {Fore.MAGENTA}Hint (?){Style.RESET_ALL}      - Reveals a letter (costs one guess)

  {Fore.YELLOW}Difficulty levels:{Style.RESET_ALL}
    Easy   - 8 wrong guesses allowed, hints enabled
    Normal - 6 wrong guesses allowed, hints enabled
    Hard   - 4 wrong guesses allowed, no hints

  Win by revealing every letter before the hangman is complete!
""")
    input(f"  Press {Fore.CYAN}Enter{Style.RESET_ALL} to return... ")


def show_stats(stats):
    """Display session statistics."""
    played = stats["played"]
    won = stats["won"]
    lost = played - won
    rate = f"{won / played * 100:.0f}%" if played > 0 else "N/A"
    header("STATISTICS")
    print(f"""
  Games Played  : {Fore.WHITE}{played}{Style.RESET_ALL}
  Wins          : {Fore.GREEN}{won}{Style.RESET_ALL}
  Losses        : {Fore.RED}{lost}{Style.RESET_ALL}
  Win Rate      : {Fore.YELLOW}{rate}{Style.RESET_ALL}
  Win Streak    : {Fore.CYAN}{stats['streak']}{Style.RESET_ALL}
  Best Streak   : {Fore.CYAN}{stats['best_streak']}{Style.RESET_ALL}
""")


def display_game(word, guessed, wrong_letters, wrong_total, max_wrong,
                 category, diff_name, hints_left):
    """Render the full game state to the terminal."""
    clear()
    remaining = max_wrong - wrong_total

    # Info bar
    print(f"\n  {Fore.CYAN}Category:{Style.RESET_ALL} {category}    "
          f"{Fore.CYAN}Difficulty:{Style.RESET_ALL} {diff_name}")
    divider()

    # Hangman figure
    stage = get_stage_index(wrong_total, max_wrong)
    print(f"{Fore.YELLOW}{HANGMAN_STAGES[stage]}{Style.RESET_ALL}")

    # Word display
    display = ""
    for ch in word:
        if ch in guessed:
            display += f" {Fore.GREEN}{ch.upper()}{Style.RESET_ALL} "
        else:
            display += f" {Fore.WHITE}_{Style.RESET_ALL} "
    print(f"  Word: {display}")

    # Wrong letters
    if wrong_letters:
        wrong_str = "  ".join(f"{Fore.RED}{l.upper()}{Style.RESET_ALL}" for l in wrong_letters)
        print(f"\n  Wrong: {wrong_str}")

    # Progress bar
    print(f"\n  Remaining: {progress_bar(remaining, max_wrong)}")

    # Hint indicator
    if hints_left > 0:
        print(f"  {Fore.MAGENTA}Hints: {hints_left} left (type ? to use){Style.RESET_ALL}")
    elif hints_left == 0:
        print(f"  {Fore.RED}No hints left{Style.RESET_ALL}")
    # hints_left < 0 means disabled (Hard mode) — show nothing

    divider()

# ─── Game Logic ───────────────────────────────────────────────────────────────

def choose_category():
    """Let the player pick a word category."""
    clear()
    header("CHOOSE CATEGORY")
    names = list(CATEGORIES.keys())
    for i, name in enumerate(names, 1):
        print(f"  {Fore.WHITE}[{i}]{Style.RESET_ALL} {name}  ({len(CATEGORIES[name])} words)")
    print(f"  {Fore.WHITE}[{len(names) + 1}]{Style.RESET_ALL} Random Mix")
    print()
    while True:
        choice = input(f"  {Fore.CYAN}> {Style.RESET_ALL}").strip()
        if choice.isdigit():
            n = int(choice)
            if 1 <= n <= len(names):
                return names[n - 1]
            if n == len(names) + 1:
                return "Random"
        print(f"  {Fore.RED}Invalid choice.{Style.RESET_ALL}")


def choose_difficulty():
    """Let the player pick a difficulty level."""
    clear()
    header("CHOOSE DIFFICULTY")
    for key, d in DIFFICULTIES.items():
        hints = "hints enabled" if d["hints"] else "no hints"
        print(f"  {Fore.WHITE}[{key}]{Style.RESET_ALL} {d['name']}  "
              f"- {d['max_wrong']} guesses, {hints}")
    print()
    while True:
        choice = input(f"  {Fore.CYAN}> {Style.RESET_ALL}").strip()
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        print(f"  {Fore.RED}Invalid choice.{Style.RESET_ALL}")


def pick_word(category):
    """Pick a random word from the selected category."""
    if category == "Random":
        pool = [w for words in CATEGORIES.values() for w in words]
    else:
        pool = CATEGORIES[category]
    return random.choice(pool)


def play_round(stats):
    """Play a single round of Hangman."""
    category = choose_category()
    difficulty = choose_difficulty()
    word = pick_word(category)

    guessed = set()          # correctly guessed letters
    wrong_letters = []       # wrong letter guesses (display)
    hints_used = 0           # hints count toward wrong total
    max_wrong = difficulty["max_wrong"]
    hints_left = 3 if difficulty["hints"] else -1  # -1 = disabled

    while True:
        wrong_total = len(wrong_letters) + hints_used
        display_game(word, guessed, wrong_letters, wrong_total,
                     max_wrong, category, difficulty["name"], hints_left)

        # ── Win check ──
        if all(ch in guessed for ch in set(word)):
            print(f"\n  {Fore.GREEN}{'═' * 40}")
            print(f"    WIN!  The word was: {word.upper()}")
            print(f"  {'═' * 40}{Style.RESET_ALL}")
            stats["played"] += 1
            stats["won"] += 1
            stats["streak"] += 1
            stats["best_streak"] = max(stats["streak"], stats["best_streak"])
            break

        # ── Lose check ──
        if wrong_total >= max_wrong:
            print(f"\n  {Fore.RED}{'═' * 40}")
            print(f"    GAME OVER!  The word was: {word.upper()}")
            print(f"  {'═' * 40}{Style.RESET_ALL}")
            stats["played"] += 1
            stats["streak"] = 0
            break

        # ── Player input ──
        guess = input(f"\n  Guess a letter: ").strip().lower()

        # Hint request
        if guess == "?":
            if hints_left < 0:
                print(f"  {Fore.RED}Hints disabled on Hard.{Style.RESET_ALL}")
                time.sleep(0.8)
                continue
            if hints_left == 0:
                print(f"  {Fore.RED}No hints remaining.{Style.RESET_ALL}")
                time.sleep(0.8)
                continue
            unrevealed = [ch for ch in set(word) if ch not in guessed]
            if not unrevealed:
                print(f"  {Fore.YELLOW}All letters already revealed!{Style.RESET_ALL}")
                time.sleep(0.8)
                continue
            hint = random.choice(unrevealed)
            guessed.add(hint)
            hints_used += 1
            hints_left -= 1
            print(f"  {Fore.MAGENTA}Hint: '{hint.upper()}' revealed!{Style.RESET_ALL}")
            time.sleep(0.8)
            continue

        # Validate
        if len(guess) != 1 or not guess.isalpha():
            print(f"  {Fore.RED}Enter a single letter.{Style.RESET_ALL}")
            time.sleep(0.8)
            continue

        if guess in guessed or guess in wrong_letters:
            print(f"  {Fore.YELLOW}Already guessed '{guess.upper()}'.{Style.RESET_ALL}")
            time.sleep(0.8)
            continue

        # Process guess
        if guess in word:
            guessed.add(guess)
            print(f"  {Fore.GREEN}'{guess.upper()}' is correct!{Style.RESET_ALL}")
        else:
            wrong_letters.append(guess)
            print(f"  {Fore.RED}'{guess.upper()}' is not in the word.{Style.RESET_ALL}")
        time.sleep(0.5)

    # Post-round
    print()
    show_stats(stats)
    input(f"  Press {Fore.CYAN}Enter{Style.RESET_ALL} to continue... ")

# ─── Entry Point ──────────────────────────────────────────────────────────────

def main():
    """Main game loop."""
    stats = {"played": 0, "won": 0, "streak": 0, "best_streak": 0}
    try:
        while True:
            show_title()
            choice = show_menu()
            if choice == "1":
                play_round(stats)
            elif choice == "2":
                show_how_to_play()
            elif choice == "3":
                clear()
                show_stats(stats)
                print(f"  {Fore.CYAN}Thanks for playing Hangman!{Style.RESET_ALL}\n")
                break
    except KeyboardInterrupt:
        print(f"\n\n  {Fore.CYAN}Thanks for playing!{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
