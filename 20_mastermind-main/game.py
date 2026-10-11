import random
from logic import feedback


DIFFICULTIES = {
    "easy": {
        "code_length": 4,
        "min_symbol": 1,
        "max_symbol": 6,
        "guess_limit": 12,
    },
    "medium": {
        "code_length": 4,
        "min_symbol": 1,
        "max_symbol": 8,
        "guess_limit": 10,
    },
    "hard": {
        "code_length": 6,
        "min_symbol": 1,
        "max_symbol": 9,
        "guess_limit": 8,
    },
}


class Mastermind:
    def __init__(self):
        self.difficulty = None
        self.code_length = 0
        self.symbols = ()
        self.guess_limit = 0
        self.code = []
        self.history = []
        self.turns = 0
        self.ended = False

    def _choose_difficulty(self):
        choices = ", ".join(
            f"{name.title()} ({settings['code_length']} symbols, "
            f"{settings['min_symbol']}-{settings['max_symbol']}, "
            f"{settings['guess_limit']} guesses)"
            for name, settings in DIFFICULTIES.items()
        )
        while True:
            choice = input(f"Choose difficulty: {choices} > ").strip().lower()
            if choice in DIFFICULTIES:
                return choice, DIFFICULTIES[choice]
            print("Invalid difficulty. Choose Easy, Medium, or Hard.")

    def _start_game(self):
        self.difficulty, settings = self._choose_difficulty()
        self.code_length = settings["code_length"]
        self.symbols = tuple(
            str(symbol)
            for symbol in range(settings["min_symbol"], settings["max_symbol"] + 1)
        )
        self.guess_limit = settings["guess_limit"]
        self.code = [random.choice(self.symbols) for _ in range(self.code_length)]
        self.turns = self.guess_limit

    def _print_history(self):
        print("Guess | Code guess | Exact | Partial")
        print("------+------------+-------+--------")
        for guess_number, (guess, exact, partial) in enumerate(self.history, start=1):
            print(
                f"{guess_number:>5} | {guess:^10} | {exact:^5} | {partial:^7}"
            )

    def run(self):
        if self.ended:
            return

        self._start_game()
        print(
            f"Mastermind — enter {self.code_length} symbols from "
            f"{self.symbols[0]} to {self.symbols[-1]}."
        )
        while self.turns > 0 and not self.ended:
            raw = input(f"{self.turns} turns left > ").strip()
            if raw.lower() == "q":
                self.ended = True
                print("You quit the game.")
                return
            if (
                len(raw) != self.code_length
                or not raw.isascii()
                or not raw.isdigit()
                or any(ch not in self.symbols for ch in raw)
            ):
                print(
                    f"Enter exactly {self.code_length} digits from "
                    f"{self.symbols[0]} to {self.symbols[-1]}."
                )
                continue
            guess = list(raw)
            exact, partial = feedback(self.code, guess)
            self.history.append((raw, exact, partial))
            self.turns -= 1
            print("Exact:", exact, " Partial:", partial)
            self._print_history()
            if exact == len(self.code):
                self.ended = True
                print("You win! You cracked the code.")
                return

        if not self.ended:
            self.ended = True
            print("You lose! The code was", "".join(self.code))
