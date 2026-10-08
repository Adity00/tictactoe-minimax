"""
Tic-Tac-Toe Board Representation and Game Logic
Core module for the Minimax AI project.
"""

from typing import List, Optional
from enum import Enum


class Player(Enum):
    """Player symbols"""
    X = "X"
    O = "O"
    EMPTY = " "


class GameResult(Enum):
    """Game result states"""
    ONGOING = "ongoing"
    X_WINS = "x_wins"
    O_WINS = "o_wins"
    DRAW = "draw"


# Winning combinations (indices 0-8)
WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
    (0, 4, 8), (2, 4, 6),             # Diagonals
]


class Board:
    """Tic-Tac-Toe board with game logic"""
    
    def __init__(self, state: Optional[List[str]] = None):
        if state is None:
            self.state = [Player.EMPTY.value] * 9
        else:
            self.state = state.copy()
    
    def copy(self) -> 'Board':
        """Return a deep copy of the board"""
        return Board(self.state)
    
    def get(self, index: int) -> str:
        """Get value at index"""
        return self.state[index]
    
    def set(self, index: int, player: Player) -> bool:
        """Set value at index if empty. Returns True if successful."""
        if self.state[index] == Player.EMPTY.value:
            self.state[index] = player.value
            return True
        return False
    
    def is_empty(self, index: int) -> bool:
        """Check if position is empty"""
        return self.state[index] == Player.EMPTY.value
    
    def available_moves(self) -> List[int]:
        """Return list of available move indices"""
        return [i for i, v in enumerate(self.state) if v == Player.EMPTY.value]
    
    def is_full(self) -> bool:
        """Check if board is full"""
        return Player.EMPTY.value not in self.state
    
    def check_winner(self) -> Optional[Player]:
        """Check if there's a winner. Returns Player.X, Player.O, or None"""
        for a, b, c in WINNING_LINES:
            if (self.state[a] != Player.EMPTY.value and 
                self.state[a] == self.state[b] == self.state[c]):
                return Player(self.state[a])
        return None
    
    def get_result(self) -> GameResult:
        """Get current game result"""
        winner = self.check_winner()
        if winner == Player.X:
            return GameResult.X_WINS
        elif winner == Player.O:
            return GameResult.O_WINS
        elif self.is_full():
            return GameResult.DRAW
        return GameResult.ONGOING
    
    def is_terminal(self) -> bool:
        """Check if game is over"""
        return self.get_result() != GameResult.ONGOING
    
    def __str__(self) -> str:
        """Pretty print the board"""
        rows = []
        for i in range(3):
            row = " | ".join(self.state[i*3:(i+1)*3])
            rows.append(f" {row} ")
        return "\n---+---+---\n".join(rows)
    
    def __repr__(self) -> str:
        return f"Board({self.state})"


def opponent(player: Player) -> Player:
    """Return the opponent player"""
    return Player.O if player == Player.X else Player.X