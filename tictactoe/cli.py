"""
CLI Interface for Interactive Play
"""

from .board import Board, Player, GameResult
from .minimax import MinimaxAI
from .random_player import RandomPlayer
from .game_runner import run_tournament, print_summary
from .gui import launch_gui


def print_board_with_indices():
    """Print board with position indices for reference"""
    print("\nPosition indices:")
    print(" 0 | 1 | 2 ")
    print("---+---+---")
    print(" 3 | 4 | 5 ")
    print("---+---+---")
    print(" 6 | 7 | 8 \n")


def get_human_move(board: Board, player: Player) -> int:
    """Get move from human player"""
    while True:
        try:
            move = input(f"Player {player.value}, enter move (0-8): ").strip()
            move = int(move)
            if 0 <= move <= 8 and board.is_empty(move):
                return move
            print("Invalid move. Choose an empty position 0-8.")
        except ValueError:
            print("Please enter a number 0-8.")
        except KeyboardInterrupt:
            print("\nGame cancelled.")
            exit(0)


def play_human_vs_ai(ai_player: Player = Player.O, verbose: bool = True):
    """Play a single game: Human vs AI"""
    board = Board()
    ai = MinimaxAI(ai_player)
    human_player = Player.O if ai_player == Player.X else Player.X
    current_player = Player.X  # X always starts
    
    print(f"\n{'='*40}")
    print(f"HUMAN vs AI")
    print(f"Human: {human_player.value}  |  AI: {ai_player.value}")
    print(f"{'='*40}")
    print_board_with_indices()
    print(board)
    
    while board.get_result() == GameResult.ONGOING:
        if current_player == ai_player:
            print(f"\nAI ({ai_player.value}) is thinking...")
            move, score = ai.get_best_move(board)
            print(f"AI plays at {move} (score: {score})")
        else:
            move = get_human_move(board, current_player)
        
        board.set(move, current_player)
        print(board)
        current_player = Player.O if current_player == Player.X else Player.X
    
    result = board.get_result()
    print(f"\n{'='*40}")
    if result == GameResult.DRAW:
        print("RESULT: DRAW!")
    elif result == GameResult.X_WINS:
        print(f"RESULT: X WINS! {'AI' if ai_player == Player.X else 'Human'} wins!")
    else:
        print(f"RESULT: O WINS! {'AI' if ai_player == Player.O else 'Human'} wins!")
    print(f"{'='*40}")


def play_human_vs_random():
    """Play a single game: Human vs Random"""
    board = Board()
    random_player = RandomPlayer(Player.O)
    current_player = Player.X
    
    print(f"\n{'='*40}")
    print(f"HUMAN vs RANDOM")
    print(f"Human: X  |  Random: O")
    print(f"{'='*40}")
    print_board_with_indices()
    print(board)
    
    while board.get_result() == GameResult.ONGOING:
        if current_player == Player.O:
            move = random_player.get_move(board)
            print(f"\nRandom plays at {move}:")
        else:
            move = get_human_move(board, current_player)
        
        board.set(move, current_player)
        print(board)
        current_player = Player.O if current_player == Player.X else Player.X
    
    result = board.get_result()
    print(f"\n{'='*40}")
    if result == GameResult.DRAW:
        print("RESULT: DRAW!")
    elif result == GameResult.X_WINS:
        print("RESULT: HUMAN WINS!")
    else:
        print("RESULT: RANDOM WINS!")
    print(f"{'='*40}")


def main_menu():
    """Main menu loop"""
    while True:
        print(f"\n{'='*40}")
        print("TIC-TAC-TOE MINIMAX AI")
        print(f"{'='*40}")
        print("1. Human vs AI (AI as O, Human as X) - CLI")
        print("2. Human vs AI (AI as X, Human as O) - CLI")
        print("3. Human vs Random - CLI")
        print("4. Run Tournament (10 games: AI vs Random)")
        print("5. Run Tournament with verbose output")
        print("6. Launch GUI (Desktop Window)")
        print("7. Exit")
        print(f"{'='*40}")
        
        choice = input("Select option (1-7): ").strip()
        
        if choice == "1":
            play_human_vs_ai(Player.O)
        elif choice == "2":
            play_human_vs_ai(Player.X)
        elif choice == "3":
            play_human_vs_random()
        elif choice == "4":
            results = run_tournament(10, verbose=False)
            print_summary(results)
        elif choice == "5":
            results = run_tournament(10, verbose=True)
            print_summary(results)
        elif choice == "6":
            print("Launching GUI...")
            launch_gui()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-7.")


if __name__ == "__main__":
    main_menu()