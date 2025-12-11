# game_pkg/player.py
import random

class Player:
    """Base Parent Class"""
    def __init__(self, name):
        self.name = name
        self.marked = [False] * 25
        self.card_numbers = self.generate_valid_bingo_card()
        
        # Set Free Space
        self.card_numbers[12] = "FREE"
        self.marked[12] = True

    def generate_valid_bingo_card(self):
        col_b = random.sample(range(1, 16), 5)
        col_i = random.sample(range(16, 31), 5)
        col_n = random.sample(range(31, 46), 5)
        col_g = random.sample(range(46, 61), 5)
        col_o = random.sample(range(61, 76), 5)

        rows = list(zip(col_b, col_i, col_n, col_g, col_o))
        flat_board = []
        for row in rows:
            flat_board.extend(row)
        return flat_board

    def check_match(self, drawn_number):
        if drawn_number in self.card_numbers:
            idx = self.card_numbers.index(drawn_number)
            self.marked[idx] = True
            return idx
        return -1

    def get_winning_indices(self):
        """
        Returns a list of indices that form a Bingo line.
        Returns empty list [] if no Bingo.
        """
        # Rows
        for i in range(5):
            indices = [i*5 + j for j in range(5)]
            if all(self.marked[k] for k in indices): return indices
        # Cols
        for j in range(5):
            indices = [i*5 + j for i in range(5)]
            if all(self.marked[k] for k in indices): return indices
        # Diagonals
        diag1 = [i*6 for i in range(5)]
        if all(self.marked[k] for k in diag1): return diag1
        
        diag2 = [(i+1)*4 for i in range(5)]
        if all(self.marked[k] for k in diag2): return diag2
        
        return []

    def has_bingo(self):
        """Checks if a winning line exists."""
        return len(self.get_winning_indices()) > 0

class ComputerPlayer(Player): 
    def react(self):
        return f"{self.name} is scanning..."