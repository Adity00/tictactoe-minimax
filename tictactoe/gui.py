"""
Tkinter GUI for Tic-Tac-Toe Minimax AI
Built-in Python GUI - no external dependencies required
"""

import tkinter as tk
from tkinter import messagebox
from typing import Optional
from .board import Board, Player, GameResult
from .minimax import MinimaxAI


class TicTacToeGUI:
    """Tkinter-based GUI for Tic-Tac-Toe"""
    
    # Colors
    BG_COLOR = "#f0f0f0"
    X_COLOR = "#e74c3c"      # Red for X
    O_COLOR = "#3498db"      # Blue for O
    WIN_COLOR = "#2ecc71"    # Green for winning line
    BTN_BG = "#ffffff"
    BTN_HOVER = "#ecf0f1"
    STATUS_BG = "#2c3e50"
    STATUS_FG = "#ecf0f1"
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Tic-Tac-Toe - Minimax AI")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG_COLOR)
        
        # Game state
        self.board = Board()
        self.ai_player = Player.O  # AI plays O by default
        self.human_player = Player.X
        self.ai = MinimaxAI(self.ai_player)
        self.game_over = False
        self.ai_thinking = False
        
        # Stats
        self.stats = {"wins": 0, "losses": 0, "draws": 0}
        
        self._setup_ui()
        self._center_window()
    
    def _setup_ui(self):
        """Create all UI elements"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.BG_COLOR, padx=20, pady=20)
        main_frame.pack()
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Tic-Tac-Toe",
            font=("Segoe UI", 28, "bold"),
            fg="#2c3e50",
            bg=self.BG_COLOR
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 5))
        
        # Subtitle
        self.mode_label = tk.Label(
            main_frame,
            text=f"You: {self.human_player.value}  |  AI: {self.ai_player.value}",
            font=("Segoe UI", 11),
            fg="#7f8c8d",
            bg=self.BG_COLOR
        )
        self.mode_label.grid(row=1, column=0, columnspan=3, pady=(0, 15))
        
        # Board buttons
        self.buttons = []
        self.button_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        self.button_frame.grid(row=2, column=0, columnspan=3)
        
        for i in range(9):
            row, col = divmod(i, 3)
            btn = tk.Button(
                self.button_frame,
                text=" ",
                font=("Segoe UI", 36, "bold"),
                width=3,
                height=1,
                bg=self.BTN_BG,
                fg=self.X_COLOR,
                activebackground=self.BTN_HOVER,
                activeforeground=self.X_COLOR,
                relief="flat",
                bd=2,
                command=lambda idx=i: self._on_cell_click(idx)
            )
            btn.grid(row=row, column=col, padx=4, pady=4)
            self.buttons.append(btn)
        
        # Add subtle grid lines using frames
        for i in range(3):
            self.button_frame.grid_columnconfigure(i, weight=1)
            self.button_frame.grid_rowconfigure(i, weight=1)
        
        # Status label
        self.status_var = tk.StringVar(value="Your turn (X)")
        self.status_label = tk.Label(
            main_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 12, "bold"),
            fg=self.STATUS_FG,
            bg=self.STATUS_BG,
            padx=20,
            pady=10,
            relief="flat"
        )
        self.status_label.grid(row=3, column=0, columnspan=3, pady=15, sticky="ew")
        
        # Stats frame
        stats_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        stats_frame.grid(row=4, column=0, columnspan=3, pady=5)
        
        self.stats_var = tk.StringVar(value="Wins: 0  |  Losses: 0  |  Draws: 0")
        stats_label = tk.Label(
            stats_frame,
            textvariable=self.stats_var,
            font=("Segoe UI", 10),
            fg="#7f8c8d",
            bg=self.BG_COLOR
        )
        stats_label.pack()
        
        # Control buttons
        btn_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        btn_frame.grid(row=5, column=0, columnspan=3, pady=15)
        
        self.new_game_btn = tk.Button(
            btn_frame,
            text="New Game",
            font=("Segoe UI", 11, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            relief="flat",
            padx=25,
            pady=8,
            cursor="hand2",
            command=self._new_game
        )
        self.new_game_btn.pack(side=tk.LEFT, padx=5)
        
        self.switch_btn = tk.Button(
            btn_frame,
            text="Switch Sides (Play as O)",
            font=("Segoe UI", 10),
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self._switch_sides
        )
        self.switch_btn.pack(side=tk.LEFT, padx=5)
        
        # Nodes evaluated label
        self.nodes_var = tk.StringVar(value="")
        nodes_label = tk.Label(
            main_frame,
            textvariable=self.nodes_var,
            font=("Consolas", 9),
            fg="#95a5a6",
            bg=self.BG_COLOR
        )
        nodes_label.grid(row=6, column=0, columnspan=3, pady=(5, 0))
    
    def _center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def _on_cell_click(self, index: int):
        """Handle human player move"""
        if self.game_over or self.ai_thinking:
            return
        if not self.board.is_empty(index):
            return
        if self.board.get_result() != GameResult.ONGOING:
            return
        
        # Human move
        self._make_move(index, self.human_player)
        self._update_board_display()
        
        # Check game over
        if self._check_game_end():
            return
        
        # AI move
        self._ai_move()
    
    def _make_move(self, index: int, player: Player):
        """Make a move on the board"""
        self.board.set(index, player)
    
    def _ai_move(self):
        """Trigger AI move with slight delay for UX"""
        self.ai_thinking = True
        self.status_var.set("AI thinking...")
        self.nodes_var.set("")
        self.root.update()
        
        # Use after() to allow UI to update before computation
        self.root.after(100, self._execute_ai_move)
    
    def _execute_ai_move(self):
        """Execute the AI move"""
        move, score = self.ai.get_best_move(self.board)
        self._make_move(move, self.ai_player)
        self._update_board_display()
        
        # Show nodes evaluated
        self.nodes_var.set(f"AI evaluated {self.ai.nodes_evaluated:,} positions")
        
        self.ai_thinking = False
        self._check_game_end()
    
    def _update_board_display(self):
        """Update button texts and colors from board state"""
        for i, btn in enumerate(self.buttons):
            value = self.board.get(i)
            if value == Player.X.value:
                btn.config(text="X", fg=self.X_COLOR, state="disabled", disabledforeground=self.X_COLOR)
            elif value == Player.O.value:
                btn.config(text="O", fg=self.O_COLOR, state="disabled", disabledforeground=self.O_COLOR)
            else:
                btn.config(text=" ", state="normal")
    
    def _check_game_end(self) -> bool:
        """Check if game ended, update UI, return True if over"""
        result = self.board.get_result()
        
        if result == GameResult.ONGOING:
            current = "Your turn" if not self.ai_thinking else "AI thinking..."
            self.status_var.set(f"{current} ({self.human_player.value})")
            return False
        
        self.game_over = True
        
        if result == GameResult.DRAW:
            self.status_var.set("It's a Draw!")
            self.status_label.config(bg="#f39c12")
            self.stats["draws"] += 1
        elif result == GameResult.X_WINS:
            winner = "You" if self.human_player == Player.X else "AI"
            self.status_var.set(f"{winner} (X) Wins!")
            self.status_label.config(bg=self.WIN_COLOR if winner == "You" else self.X_COLOR)
            if winner == "You":
                self.stats["wins"] += 1
            else:
                self.stats["losses"] += 1
            self._highlight_winning_line(Player.X)
        elif result == GameResult.O_WINS:
            winner = "You" if self.human_player == Player.O else "AI"
            self.status_var.set(f"{winner} (O) Wins!")
            self.status_label.config(bg=self.WIN_COLOR if winner == "You" else self.O_COLOR)
            if winner == "You":
                self.stats["wins"] += 1
            else:
                self.stats["losses"] += 1
            self._highlight_winning_line(Player.O)
        
        self._update_stats()
        self._disable_all_buttons()
        return True
    
    def _highlight_winning_line(self, player: Player):
        """Highlight the winning combination"""
        from .board import WINNING_LINES
        for a, b, c in WINNING_LINES:
            if (self.board.get(a) == player.value and 
                self.board.get(b) == player.value and 
                self.board.get(c) == player.value):
                for idx in (a, b, c):
                    self.buttons[idx].config(bg=self.WIN_COLOR, disabledforeground="white")
                break
    
    def _disable_all_buttons(self):
        """Disable all board buttons"""
        for btn in self.buttons:
            btn.config(state="disabled")
    
    def _enable_all_buttons(self):
        """Enable empty buttons"""
        for i, btn in enumerate(self.buttons):
            if self.board.is_empty(i):
                btn.config(state="normal", bg=self.BTN_BG)
    
    def _update_stats(self):
        """Update stats display"""
        self.stats_var.set(
            f"Wins: {self.stats['wins']}  |  Losses: {self.stats['losses']}  |  Draws: {self.stats['draws']}"
        )
    
    def _new_game(self):
        """Start a new game"""
        self.board = Board()
        self.ai = MinimaxAI(self.ai_player)
        self.game_over = False
        self.ai_thinking = False
        
        # Reset UI
        for btn in self.buttons:
            btn.config(text=" ", state="normal", bg=self.BTN_BG, 
                       disabledforeground=self.X_COLOR if self.human_player == Player.X else self.O_COLOR)
        
        self.status_var.set(f"Your turn ({self.human_player.value})")
        self.status_label.config(bg=self.STATUS_BG)
        self.nodes_var.set("")
        
        # If AI is X, AI goes first
        if self.ai_player == Player.X:
            self._ai_move()
    
    def _switch_sides(self):
        """Switch human/AI sides"""
        # Swap players
        self.human_player, self.ai_player = self.ai_player, self.human_player
        self.ai = MinimaxAI(self.ai_player)
        
        # Update UI
        self.mode_label.config(text=f"You: {self.human_player.value}  |  AI: {self.ai_player.value}")
        self.switch_btn.config(text=f"Switch Sides (Play as {self.human_player.value})")
        
        # Reset game
        self._new_game()


def launch_gui():
    """Launch the Tkinter GUI"""
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()