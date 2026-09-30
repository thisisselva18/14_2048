from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.best_score = 0
        self.history = []

    def display(self):
        print("\n" + "+------+------+------+------+")
        for row in self.board.grid:
            print("|" + "|".join(f"{x:^6}" if x else f"{' ':^6}" for x in row) + "|")
            print("+------+------+------+------+")
        print("Score:", self.board.score, " Best:", self.best_score)

    def move(self, key):
        moves = {"a": self.board.move_left, "d": self.board.move_right,
                 "w": self.board.move_up, "s": self.board.move_down}
        if key not in moves:
            return False
        changed = moves[key]()
        if changed:  # an unchanged board never receives a new tile
            self.board.add_random_tile()
        return changed

    def status(self):
        """Return "won", "lost", or None while the game can continue."""
        if self.board.has_won():
            return "won"
        if not self.board.can_move():
            return "lost"
        return None

    def run(self):
        print("2048 — W/A/S/D to move, U to undo, Q to quit.")
        while True:
            self.display()
            status = self.status()
            if status == "won":
                print("You reached 2048! You win.")
                return
            if status == "lost":
                print("No legal moves remain. Game over.")
                return
            try:
                key = input("> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye.")
                return
            if key == "q":
                print("Goodbye.")
                return
            if key == "u":
                print("Undo is not implemented yet.")
                continue
            if key not in ("w", "a", "s", "d"):
                print(f"Unknown command {key!r}. Use W/A/S/D to move, U to undo, Q to quit.")
                continue
            if self.move(key):
                self.best_score = max(self.best_score, self.board.score)
