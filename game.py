from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.best_score = 0
        self.history = []  # at most one snapshot: one-level undo

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
        before = self.snapshot()
        changed = moves[key]()
        if changed:  # an unchanged board never receives a new tile
            self.board.add_random_tile()
            self.best_score = max(self.best_score, self.board.score)
            self.history = [before]
        return changed

    def snapshot(self):
        return [row[:] for row in self.board.grid], self.board.score, self.best_score

    def undo(self):
        """Restore the state before the last successful move, if any."""
        if not self.history:
            return False
        grid, score, best = self.history.pop()
        self.board.grid = grid
        self.board.score = score
        self.best_score = best
        return True

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
                print("Undid last move." if self.undo() else "Nothing to undo.")
                continue
            if key not in ("w", "a", "s", "d"):
                print(f"Unknown command {key!r}. Use W/A/S/D to move, U to undo, Q to quit.")
                continue
            self.move(key)
