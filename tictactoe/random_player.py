"""
Random Opponent for Testing
Simple opponent that plays random valid moves.
"""

import random
from typing import Optional
from .board import Board, Player


class RandomPlayer:
    """Plays random valid moves"""
    
    def __init__(self, player: Player, seed: Optional[int] = None):
        self.player = player
        if seed is not None:
            random.seed(seed)
    
    def get_move(self, board: Board) -> int:
        """Get a random available move"""
        moves = board.available_moves()
        return random.choice(moves)


def create_random_player(player: Player, game_num: int) -> RandomPlayer:
    """Create a random player with a seed based on game number for reproducibility"""
    return RandomPlayer(player, seed=game_num * 1000)