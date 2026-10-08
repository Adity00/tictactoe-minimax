"""
Main Entry Point for Tic-Tac-Toe Minimax AI
Runs 10-game tournament vs Random opponent (assignment requirement).
"""

import sys
from .game_runner import run_tournament, print_summary
from .gui import launch_gui


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "tournament":
            num_games = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            verbose = "--verbose" in sys.argv or "-v" in sys.argv
            results = run_tournament(num_games, verbose)
            print_summary(results)
            
            # Exit with error code if AI lost any games (for CI/testing)
            ai_losses = sum(1 for r in results if
                          (r["ai_player"] == "X" and r["winner"].value == "o_wins") or
                          (r["ai_player"] == "O" and r["winner"].value == "x_wins"))
            sys.exit(1 if ai_losses > 0 else 0)
            
        elif sys.argv[1] == "demo":
            # Quick demo: 3 games with board output
            results = run_tournament(3, verbose=True)
            print_summary(results)
        elif sys.argv[1] == "gui":
            # Launch GUI
            launch_gui()
        else:
            print("Usage: python -m tictactoe [tournament [num_games] [--verbose]] | [demo] | [gui]")
            sys.exit(1)
    else:
        # Default: run 10-game tournament
        results = run_tournament(10, verbose=False)
        print_summary(results)


if __name__ == "__main__":
    main()