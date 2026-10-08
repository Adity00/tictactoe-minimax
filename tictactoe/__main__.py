"""
Main Entry Point for Tic-Tac-Toe Minimax AI
"""

from .cli import main_menu
from .game_runner import run_tournament, print_summary


def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) > 1:
        # Command line arguments for automated testing
        if sys.argv[1] == "tournament":
            num_games = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            verbose = "--verbose" in sys.argv or "-v" in sys.argv
            results = run_tournament(num_games, verbose)
            print_summary(results)
            
            # Exit with error code if AI lost any games
            ai_losses = sum(1 for r in results if
                          (r.ai_player == r.winner == "X_WINS") or  # This is wrong, fix
                          (r.ai_player == "X" and r.winner.value == "o_wins") or
                          (r.ai_player == "O" and r.winner.value == "x_wins"))
            # Actually check properly
            from .board import Player, GameResult
            ai_losses = sum(1 for r in results if
                          (r.ai_player == Player.X and r.winner == GameResult.O_WINS) or
                          (r.ai_player == Player.O and r.winner == GameResult.X_WINS))
            sys.exit(1 if ai_losses > 0 else 0)
        elif sys.argv[1] == "demo":
            # Quick demo: AI vs Random, 3 games
            results = run_tournament(3, verbose=True)
            print_summary(results)
        else:
            print("Usage: python -m tictactoe [tournament [num_games] [--verbose]] | [demo]")
            sys.exit(1)
    else:
        # Interactive mode
        main_menu()


if __name__ == "__main__":
    main()