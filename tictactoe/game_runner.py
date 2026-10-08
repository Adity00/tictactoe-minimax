"""
Game Runner - Plays 10 games between Minimax AI and Random Opponent
Fulfills assignment requirement: "Play 10 games vs random opponent"
"""

from typing import List
from .board import Board, Player, GameResult
from .minimax import MinimaxAI
from .random_player import create_random_player


def opponent(player: Player) -> Player:
    """Return the opponent player"""
    return Player.O if player == Player.X else Player.X


def play_game(ai_player: Player, game_num: int, verbose: bool = False) -> dict:
    """
    Play a single game between Minimax AI and Random opponent.
    Returns dict with game results.
    """
    board = Board()
    ai = MinimaxAI(ai_player)
    random_player = create_random_player(
        Player.O if ai_player == Player.X else Player.X, 
        game_num
    )
    
    current_player = Player.X  # X always starts
    moves = 0
    
    if verbose:
        print(f"\n=== Game {game_num} ===")
        print(f"AI plays as {ai_player.value}, Random plays as {opponent(ai_player).value}")
        print(board)
    
    while board.get_result() == GameResult.ONGOING:
        if current_player == ai_player:
            move, _ = ai.get_best_move(board)
        else:
            move = random_player.get_move(board)
        
        board.set(move, current_player)
        moves += 1
        
        if verbose:
            print(f"\n{current_player.value} plays at {move}:")
            print(board)
        
        current_player = opponent(current_player)
    
    result = board.get_result()
    
    if verbose:
        print(f"\nResult: {result.value}")
    
    return {
        "game_num": game_num,
        "ai_player": ai_player,
        "winner": result,
        "moves": moves,
        "nodes_evaluated": ai.nodes_evaluated
    }


def run_tournament(num_games: int = 10, verbose: bool = False) -> List[dict]:
    """
    Run a tournament of games.
    AI alternates between X and O (odd games = X, even games = O).
    Returns list of game results.
    """
    results = []
    
    print(f"\n{'='*50}")
    print(f"TOURNAMENT: {num_games} games - Minimax AI vs Random")
    print(f"{'='*50}")
    
    for i in range(1, num_games + 1):
        ai_player = Player.X if i % 2 == 1 else Player.O
        result = play_game(ai_player, i, verbose)
        results.append(result)
        print(f"Game {result['game_num']}: AI({result['ai_player'].value}) - "
              f"{result['winner'].value.replace('_', ' ').title()} "
              f"in {result['moves']} moves, nodes: {result['nodes_evaluated']}")
    
    return results


def print_summary(results: List[dict]):
    """Print tournament summary"""
    ai_wins = sum(1 for r in results if 
                  (r["ai_player"] == Player.X and r["winner"] == GameResult.X_WINS) or
                  (r["ai_player"] == Player.O and r["winner"] == GameResult.O_WINS))
    ai_losses = sum(1 for r in results if
                    (r["ai_player"] == Player.X and r["winner"] == GameResult.O_WINS) or
                    (r["ai_player"] == Player.O and r["winner"] == GameResult.X_WINS))
    draws = sum(1 for r in results if r["winner"] == GameResult.DRAW)
    total_moves = sum(r["moves"] for r in results)
    total_nodes = sum(r["nodes_evaluated"] for r in results)
    
    print(f"\n{'='*50}")
    print(f"TOURNAMENT SUMMARY ({len(results)} games)")
    print(f"{'='*50}")
    print(f"AI Wins:    {ai_wins}")
    print(f"AI Losses:  {ai_losses}")
    print(f"Draws:      {draws}")
    print(f"Win Rate:   {ai_wins/len(results)*100:.1f}%")
    print(f"Avg Moves:  {total_moves/len(results):.1f}")
    print(f"Avg Nodes:  {total_nodes/len(results):.0f}")
    print(f"{'='*50}")
    
    # Verify unbeatable (core requirement)
    if ai_losses == 0:
        print("[OK] AI is UNBEATABLE (0 losses)!")
    else:
        print(f"[FAIL] AI LOST {ai_losses} game(s) - NOT unbeatable!")


if __name__ == "__main__":
    results = run_tournament(10, verbose=False)
    print_summary(results)