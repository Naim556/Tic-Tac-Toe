from tkinter import *

# Constants for game settings
WINDOW_WIDTH = 620
WINDOW_HEIGHT = 650
BUTTON_FONT = ("Garamond", 15, "bold")
LABEL_FONT = ("Garamond", 35, "bold")
SCORE_FONT = ("Garamond", 40, "bold")
BUTTON_COLOR = "white"
LABEL_COLOR = "white"
BACKGROUND_COLOR = "black"
FRAME_COLOR = "white"

class TicTacToe:
    def __init__(self):
        self.main = Tk()
        self.score_user = 0
        self.score_bot = 0
        self.score_user2 = 0
        self.main.title("Tic Tac Toe")
        self.main.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.main.resizable(height=False, width=False)
        self.GUI(self.main)
        self.main.mainloop()

    def GUI(self, main):
        # Create frames for the layout
        self.Frame_Up = Frame(main, background=BACKGROUND_COLOR, width=WINDOW_WIDTH, height=100)
        self.Frame_Up.pack(padx=0, pady=0)

        self.Frame_between = Frame(main, background=FRAME_COLOR, width=WINDOW_WIDTH, height=450)
        self.Frame_between.pack(padx=0, pady=0)

        self.Frame_down = Frame(main, background=BACKGROUND_COLOR, width=WINDOW_WIDTH, height=100)
        self.Frame_down.pack(padx=0, pady=0)

        # Buttons for single and multiplayer modes
        self.btn_single = Button(self.Frame_between, background=BUTTON_COLOR, text="Single", font=BUTTON_FONT,
                                 foreground="black", border=5, borderwidth=5,command=self.single_player)
        self.btn_single.place(relx=0.20, rely=0.3, relwidth=0.25, relheight=0.25, anchor="nw")

        self.btn_multiplayer = Button(self.Frame_between, background=BUTTON_COLOR, text="Multiplayer", font=BUTTON_FONT,
                                     foreground="black", border=5,borderwidth=5,command=self.multi_player)
        self.btn_multiplayer.place(relx=0.8, rely=0.3, relwidth=0.25, relheight=0.25, anchor="ne")

    def back_page(self):
        # Clear the frames and return to the main menu
        for widget in self.Frame_between.winfo_children():
            widget.destroy()
        for widget in self.Frame_Up.winfo_children():
            widget.destroy()
        for widget in self.Frame_down.winfo_children():
            widget.destroy()

        self.btn_single = Button(self.Frame_between, background=BUTTON_COLOR, text="Single", font=BUTTON_FONT,
                                foreground="black", border=5, borderwidth=5, command=self.single_player)
        self.btn_single.place(relx=0.20, rely=0.3, relwidth=0.25, relheight=0.25, anchor="nw")

        self.btn_multiplayer = Button(self.Frame_between, background=BUTTON_COLOR, text="Multiplayer", font=BUTTON_FONT,
                                      foreground="black", border=5, borderwidth=5, command=self.multi_player)
        self.btn_multiplayer.place(relx=0.8, rely=0.3, relwidth=0.25, relheight=0.25, anchor="ne")

    def reset_score_single(self):
        # Reset scores for single player mode
        self.score_user = 0
        self.score_bot = 0
        self.label_score.config(text=f"{self.score_user} : {self.score_bot}")

    def single_player(self):
        # Setup the single player mode UI
        self.label_score = Label(self.Frame_Up, text=f"{self.score_user} : {self.score_bot}", foreground=LABEL_COLOR,
                                 font=SCORE_FONT, background=BACKGROUND_COLOR)
        self.label_score.place(relx=0.350, rely=0.1, relwidth=0.3, relheight=0.8)

        self.label_user = Label(self.Frame_Up, text="User", foreground=LABEL_COLOR, font=LABEL_FONT,
                                background=BACKGROUND_COLOR)
        self.label_user.place(relx=0.05, rely=0.1, relwidth=0.3, relheight=0.8)

        self.label_bot = Label(self.Frame_Up, text="Bot", foreground=LABEL_COLOR, font=LABEL_FONT,
                               background=BACKGROUND_COLOR)
        self.label_bot.place(relx=0.65, rely=0.1, relwidth=0.30, relheight=0.8)

        self.btn_reset_score = Button(self.Frame_down, text="Reset Score", font=BUTTON_FONT, foreground=LABEL_COLOR,
                                      background=BACKGROUND_COLOR, command=self.reset_score_single)
        self.btn_reset_score.place(relx=0.15, rely=0.1, relwidth=0.30, relheight=0.8, anchor="nw")

        self.btn_back = Button(self.Frame_down, text="Back", font=BUTTON_FONT, foreground=LABEL_COLOR,
                               background=BACKGROUND_COLOR, command=self.back_page)
        self.btn_back.place(relx=0.55, rely=0.1, relwidth=0.30, relheight=0.8, anchor="nw")

        self.chart()

    def chart(self):
        # Initialize the game board for single player mode
        self.btn_list = [["" for _ in range(3)] for _ in range(3)]
        self.turn = "X"

        for row in range(3):
            for col in range(3):
                btn = Button(self.Frame_between, text="", font=("arial", 20, "bold"), background=BUTTON_COLOR,
                             foreground="black", width=12, height=4, anchor="center",
                             command=lambda r=row, c=col: self.on_click(r, c))
                btn.grid(row=row, column=col)
                self.btn_list[row][col] = btn

    def on_click(self, row, col):
        # Handle user click in single player mode
        if self.btn_list[row][col]["text"] == "":
            self.btn_list[row][col]["text"] = "X"
            if self.check_winner("X"):
                self.end_game_single("your win ")
                return
            if all(self.btn_list[r][c]["text"] != "" for r in range(3) for c in range(3)):
                self.end_game_single("Draw!")
                return
            self.bot_move()

    def bot_move(self):
        # Bot makes a move using the Minimax algorithm
        best_move = self.find_best_move()
        if best_move:
            row, col = best_move
            self.btn_list[row][col]["text"] = "O"
            if self.check_winner("O"):
                self.end_game_single("bot win")

    def find_best_move(self):
        # Find the best move using the Minimax algorithm
        best_score = -float('inf')
        best_move = None

        for row in range(3):
            for col in range(3):
                if self.btn_list[row][col]["text"] == "":
                    self.btn_list[row][col]["text"] = "O"
                    score = self.minimax(0, False)
                    self.btn_list[row][col]["text"] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        return best_move

    def minimax(self, depth, is_maximizing):
        # Minimax algorithm to determine the best move
        if self.check_winner("O"):
            return 1
        if self.check_winner("X"):
            return -1
        if all(self.btn_list[r][c]["text"] != "" for r in range(3) for c in range(3)):
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for row in range(3):
                for col in range(3):
                    if self.btn_list[row][col]["text"] == "":
                        self.btn_list[row][col]["text"] = "O"
                        score = self.minimax(depth + 1, False)
                        self.btn_list[row][col]["text"] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if self.btn_list[row][col]["text"] == "":
                        self.btn_list[row][col]["text"] = "X"
                        score = self.minimax(depth + 1, True)
                        self.btn_list[row][col]["text"] = ""
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, symbol):
        # Check if the given symbol has won
        for row in range(3):
            if all(self.btn_list[row][col]["text"] == symbol for col in range(3)):
                return True
        for col in range(3):
            if all(self.btn_list[row][col]["text"] == symbol for row in range(3)):
                return True
        if all(self.btn_list[i][i]["text"] == symbol for i in range(3)):
            return True
        if all(self.btn_list[i][2 - i]["text"] == symbol for i in range(3)):
            return True
        return False

    def end_game_single(self, message):
        # Handle end of game in single player mode
        print(message)

        if "your win" in message:
            self.score_user += 1
        elif "bot win" in message:
            self.score_bot += 1

        self.label_score.config(text=f"{self.score_user} : {self.score_bot}")

        for row in range(3):
            for col in range(3):
                self.btn_list[row][col]["command"] = lambda: None
                self.Frame_Up.after(1000, self.single_player)

    def reset_score_multi(self):
        # Reset scores for multiplayer mode
        self.score_user = 0
        self.score_user2 = 0
        self.label_score.config(text=f"{self.score_user} : {self.score_user2}")

    def multi_player(self):
        # Setup the multiplayer mode UI
        self.label_score = Label(self.Frame_Up, text=f"{self.score_user} : {self.score_user2}", foreground=LABEL_COLOR,
                                 font=SCORE_FONT, background=BACKGROUND_COLOR)
        self.label_score.place(relx=0.350, rely=0.1, relwidth=0.3, relheight=0.8)

        self.label_user = Label(self.Frame_Up, text="User1", foreground=LABEL_COLOR, font=LABEL_FONT,
                                background=BACKGROUND_COLOR)
        self.label_user.place(relx=0.05, rely=0.1, relwidth=0.3, relheight=0.8)

        self.label_bot = Label(self.Frame_Up, text="User2", foreground=LABEL_COLOR, font=LABEL_FONT,
                               background=BACKGROUND_COLOR)
        self.label_bot.place(relx=0.65, rely=0.1, relwidth=0.30, relheight=0.8)

        self.btn_reset_score = Button(self.Frame_down, text="Reset Score", font=BUTTON_FONT, foreground=LABEL_COLOR,
                                      background=BACKGROUND_COLOR, command=self.reset_score_multi)
        self.btn_reset_score.place(relx=0.15, rely=0.1, relwidth=0.30, relheight=0.8, anchor="nw")

        self.btn_back = Button(self.Frame_down, text="Back", font=BUTTON_FONT, foreground=LABEL_COLOR,
                               background=BACKGROUND_COLOR, command=self.back_page)
        self.btn_back.place(relx=0.55, rely=0.1, relwidth=0.30, relheight=0.8, anchor="nw")

        self.chart_multiplayer()

    def chart_multiplayer(self):
        # Initialize the game board for multiplayer mode
        self.btn_list = [["" for _ in range(3)] for _ in range(3)]
        self.turn = "X"

        for row in range(3):
            for col in range(3):
                btn = Button(self.Frame_between, text="", font=("arial", 20, "bold"), background=BUTTON_COLOR,
                             foreground="black", width=12, height=4, anchor="center",
                             command=lambda r=row, c=col: self.on_click_multiplayer(r, c))
                btn.grid(row=row, column=col)
                self.btn_list[row][col] = btn

    def on_click_multiplayer(self, row, col):
        # Handle user click in multiplayer mode
        if self.btn_list[row][col]["text"] == "":
            self.btn_list[row][col]["text"] = self.turn

            if self.check_winner(self.turn):
                self.end_game_multi(f"Player {self.turn} wins!")
                return

            if all(self.btn_list[r][c]["text"] != "" for r in range(3) for c in range(3)):
                self.end_game_multi("Draw!")
                return

            self.turn = "O" if self.turn == "X" else "X"

    def end_game_multi(self, message):
        # Handle end of game in multiplayer mode
        print(message)

        if "Player X wins" in message:
            self.score_user += 1
        elif "Player O wins" in message:
            self.score_user2 += 1

        self.label_score.config(text=f"{self.score_user} : {self.score_user2}")

        for row in range(3):
            for col in range(3):
                self.btn_list[row][col]["command"] = lambda: None
                self.Frame_Up.after(1000, self.multi_player)


def start_game():
    print("Hi, I'm Naeem. This project is a personal project. A simple Tic Tac Toe game.")
    start = TicTacToe()

if __name__ == "__main__":
    start_game()