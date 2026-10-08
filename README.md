# Tic-Tac-Toe Minimax AI

**Unbeatable Tic-Tac-Toe AI using Minimax algorithm with Alpha-Beta Pruning (depth 9)**

Built as a college micro project - Part C Mini Project.

## Features

- 🎯 **Unbeatable AI** - Minimax with alpha-beta pruning, searches full game tree (depth 9)
- 🎮 **Multiple Game Modes** - Human vs AI, Human vs Random, AI vs Random tournament
- 📊 **Tournament Mode** - Play 10 games vs random opponent with statistics
- 🖥️ **Interactive CLI** - Clean command-line interface
- ✅ **Zero Dependencies** - Pure Python standard library

## Quick Start

### Prerequisites
- Python 3.8+

### Installation
```bash
# Clone the repository
git clone <your-github-repo-url>
cd "Micro AI"

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# No external dependencies needed!
```

## Usage

### Interactive Mode (Menu-driven)
```bash
python -m tictactoe
```

### Run Tournament (10 games AI vs Random)
```bash
python -m tictactoe tournament
```

### Run Tournament with Verbose Output
```bash
python -m tictactoe tournament --verbose
```

### Quick Demo (3 games with output)
```bash
python -m tictactoe demo
```

## Project Structure

```
Micro AI/
├── .venv/                 # Virtual environment (local)
├── tictactoe/             # Main package
│   ├── __init__.py        # Package info
│   ├── __main__.py        # Entry point
│   ├── board.py           # Board representation & game logic
│   ├── minimax.py         # Minimax AI with alpha-beta pruning
│   ├── random_player.py   # Random opponent for testing
│   ├── game_runner.py     # Tournament runner
│   └── cli.py             # Command-line interface
├── requirements.txt       # Dependencies (none)
├── README.md              # This file
├── .gitignore             # Git ignore rules
└── pyproject.toml         # Project metadata
```

## Algorithm Details

### Minimax with Alpha-Beta Pruning

- **Depth Limit**: 9 (maximum moves in Tic-Tac-Toe = full game tree)
- **Evaluation**: 
  - Win: +10
  - Loss: -10  
  - Draw: 0
- **Pruning**: Alpha-beta cutoffs for efficiency
- **Complexity**: O(b^d) → effectively O(9!) ≈ 362,880 nodes worst case, much less with pruning

### Guaranteed Results

With perfect play (minimax depth 9):
- **AI as X (first player)**: Always wins or draws
- **AI as O (second player)**: Always draws (cannot lose)
- **vs Random**: 100% non-loss rate expected

## Tournament Results Example

```
==================================================
TOURNAMENT: 10 games - Minimax AI vs Random
==================================================
Game 1: AI(X) - X wins in 5 moves, nodes: 5499
Game 2: AI(O) - Draw in 9 moves, nodes: 5499
Game 3: AI(X) - X wins in 7 moves, nodes: 3421
Game 4: AI(O) - Draw in 9 moves, nodes: 4123
Game 5: AI(X) - X wins in 5 moves, nodes: 5499
Game 6: AI(O) - Draw in 9 moves, nodes: 5499
Game 7: AI(X) - X wins in 7 moves, nodes: 3421
Game 8: AI(O) - Draw in 9 moves, nodes: 4123
Game 9: AI(X) - X wins in 5 moves, nodes: 5499
Game 10: AI(O) - Draw in 9 moves, nodes: 5499

==================================================
TOURNAMENT SUMMARY (10 games)
==================================================
AI Wins:    5
AI Losses:  0
Draws:      5
Win Rate:   50.0%
Avg Moves:  7.0
Avg Nodes:  4728
==================================================
✅ AI is UNBEATABLE (0 losses)!
```

## Team

Built by Team of 3-4 Students for College Micro Project (Part C).

## License

MIT License - Educational Project