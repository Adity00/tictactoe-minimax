"""
Minimax Algorithm with Alpha-Beta Pruning for Tic-Tac-Toe
Depth-limited to 9 (full game tree for Tic-Tac-Toe)
Core AI module - unbeatable with perfect play.
"""

from typing import Tuple
from .board import Board, Player, GameResult


# Score constants
WIN_SCORE = 10
LOSS_SCORE = -10
DRAW_SCORE = 0


class MinimaxAI:
    """
    Unbeatable Tic-Tac-Toe AI using Minimax with Alpha-Beta Pruning.
    Depth limited to 9 (maximum possible moves in Tic-Tac-Toe).
    """
    
    def __init__(self, player: Player, max_depth: int = 9):
        self.player = player
        self.max_depth = max_depth
        self.nodes_evaluated = 0
    
    def get_best_move(self, board: Board) -> Tuple[int, int]:
        """
        Get the best move for the current player.
        Returns (move_index, score)
        """
        self.nodes_evaluated = 0
        best_score = float('-inf')
        best_move = -1
        alpha = float('-inf')
        beta = float('inf')
        
        for move in board.available_moves():
            new_board = board.copy()
            new_board.set(move, self.player)
            score = self._minimax(new_board, 1, alpha, beta, False)
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, best_score)
        
        return best_move, best_score
    
    def _minimax(self, board: Board, depth: int, alpha: float, beta: float, 
                 is_maximizing: bool) -> int:
        """
        Minimax with alpha-beta pruning.
        Returns the score from the perspective of self.player.
        """
        self.nodes_evaluated += 1
        
        # Check terminal states
        result = board.get_result()
        if result == GameResult.X_WINS:
            return WIN_SCORE if self.player == Player.X else LOSS_SCORE
        elif result == GameResult.O_WINS:
            return WIN_SCORE if self.player == Player.O else LOSS_SCORE
        elif result == GameResult.DRAW:
            return DRAW_SCORE
        
        # Depth limit reached
        if depth >= self.max_depth:
            return DRAW_SCORE
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in board.available_moves():
                new_board = board.copy()
                new_board.set(move, self.player)
                eval_score = self._minimax(new_board, depth + 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            opp = Player.O if self.player == Player.X else Player.X
            for move in board.available_moves():
                new_board = board.copy()
                new_board.set(move, opp)
                eval_score = self._minimax(new_board, depth + 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval


def minimax_move(board: Board, player: Player, max_depth: int = 9) -> Tuple[int, int]:
    """Convenience function to get best move using minimax."""
    ai = MinimaxAI(player, max_depth)
    return ai.get_best_move(board)