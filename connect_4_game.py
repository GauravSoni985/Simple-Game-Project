import tkinter as tk
from tkinter import messagebox

ROWS = 6
COLS = 7

class ConnectFourGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Connect Four")
        self.board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
        self.turn = 0  # 0 for Red, 1 for Yellow
        self.canvas = tk.Canvas(root, width=700, height=600, bg="blue")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)
        self.draw_board()

        self.reset_button = tk.Button(root, text="Reset Game", command=self.reset_game, bg="gray", fg="white")
        self.reset_button.pack(pady=10)

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                x1 = c * 100
                y1 = r * 100
                x2 = x1 + 100
                y2 = y1 + 100
                self.canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10,
                                        fill=self.get_color(self.board[r][c]))

    def get_color(self, piece):
        if piece == "R":
            return "red"
        elif piece == "Y":
            return "yellow"
        else:
            return "white"

    def handle_click(self, event):
        col = event.x // 100
        if col < 0 or col >= COLS:
            return

        row = self.get_available_row(col)
        if row is not None:
            piece = "R" if self.turn % 2 == 0 else "Y"
            self.board[row][col] = piece
            self.draw_board()

            if self.check_winner(piece):
                winner = "Red" if piece == "R" else "Yellow"
                messagebox.showinfo("Game Over", f"{winner} wins!")
                self.canvas.unbind("<Button-1>")
                return
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                return

            self.turn += 1

    def get_available_row(self, col):
        for r in reversed(range(ROWS)):
            if self.board[r][col] == " ":
                return r
        return None

    def check_winner(self, piece):
        # Horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(self.board[r][c + i] == piece for i in range(4)):
                    return True

        # Vertical
        for r in range(ROWS - 3):
            for c in range(COLS):
                if all(self.board[r + i][c] == piece for i in range(4)):
                    return True

        # Diagonal /
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(self.board[r - i][c + i] == piece for i in range(4)):
                    return True

        # Diagonal \
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(self.board[r + i][c + i] == piece for i in range(4)):
                    return True

        return False

    def is_draw(self):
        return all(self.board[0][c] != " " for c in range(COLS))

    def reset_game(self):
        self.board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
        self.turn = 0
        self.canvas.bind("<Button-1>", self.handle_click)
        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    game = ConnectFourGUI(root)
    root.mainloop()
