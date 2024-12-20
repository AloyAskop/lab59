from tkinter import Tk, Button, messagebox
from tkinter.font import Font
from copy import deepcopy

class GameBoard:

    def __init__(self, other=None):
        self.current_player = 'X'
        self.ai_player = 'O'
        self.empty_cell = ' '
        self.board_size = 3
        self.cells = {}
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.cells[col, row] = self.empty_cell

        if other:
            self.__dict__ = deepcopy(other.__dict__)

    def make_move(self, col, row):
        new_board = GameBoard(self)
        new_board.cells[col, row] = new_board.current_player
        (new_board.current_player, new_board.ai_player) = (new_board.ai_player, new_board.current_player)
        return new_board

    def __minimax(self, is_maximizing):
        if self.has_won():
            if is_maximizing:
                return (-1, None)
            else:
                return (+1, None)
        elif self.is_tied():
            return (0, None)
        elif is_maximizing:
            best = (-2, None)
            for col, row in self.cells:
                if self.cells[col, row] == self.empty_cell:
                    value = self.make_move(col, row).__minimax(not is_maximizing)[0]
                    if value > best[0]:
                        best = (value, (col, row))
            return best
        else:
            best = (+2, None)
            for col, row in self.cells:
                if self.cells[col, row] == self.empty_cell:
                    value = self.make_move(col, row).__minimax(not is_maximizing)[0]
                    if value < best[0]:
                        best = (value, (col, row))
            return best

    def best_move(self):
        return self.__minimax(True)[1]

    def is_tied(self):
        for (col, row) in self.cells:
            if self.cells[col, row] == self.empty_cell:
                return False
        return True

    def has_won(self):
        for row in range(self.board_size):
            winning_cells = []
            for col in range(self.board_size):
                if self.cells[col, row] == self.ai_player:
                    winning_cells.append((col, row))
            if len(winning_cells) == self.board_size:
                return winning_cells
        for col in range(self.board_size):
            winning_cells = []
            for row in range(self.board_size):
                if self.cells[col, row] == self.ai_player:
                    winning_cells.append((col, row))
            if len(winning_cells) == self.board_size:
                return winning_cells
        winning_cells = []
        for row in range(self.board_size):
            col = row
            if self.cells[col, row] == self.ai_player:
                winning_cells.append((col, row))
        if len(winning_cells) == self.board_size:
            return winning_cells
        winning_cells = []
        for row in range(self.board_size):
            col = self.board_size - 1 - row
            if self.cells[col, row] == self.ai_player:
                winning_cells.append((col, row))
        if len(winning_cells) == self.board_size:
            return winning_cells
        return None

    def __str__(self):
        representation = ''
        for row in range(self.board_size):
            for col in range(self.board_size):
                representation += self.cells[col, row]
            representation += "\n"
        return representation

class GameGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title('TicTacToe')
        self.window.resizable(width=False, height=False)
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 300  
        window_height = 300
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.window.geometry(f'{window_width}x{window_height}+{x}+{y}')
        self.window.configure(bg='lightblue') 

        self.game_board = GameBoard()
        self.font_style = Font(family="Helvetica", size=32)
        self.cell_buttons = {}
        button_size = 5 
        for col, row in self.game_board.cells:
            handler = lambda col=col, row=row: self.player_move(col, row)
            button = Button(self.window, command=handler, font=self.font_style, width=button_size, height=2, bg='light blue') 
            button.grid(row=row, column=col, sticky="nsew") 
            self.cell_buttons[col, row] = button
        for i in range(self.game_board.board_size):
            self.window.grid_rowconfigure(i, weight=1)
            self.window.grid_columnconfigure(i, weight=1)
        reset_handler = lambda: self.reset_game()
        reset_button = Button(self.window, text='reset', command=reset_handler)
        reset_button.grid(row=self.game_board.board_size + 1, column=0, columnspan=self.game_board.board_size, sticky="WE")
        self.update_display()

    def reset_game(self):
        self.game_board = GameBoard()
        self.update_display()

    def player_move(self, col, row):
        self.window.config(cursor="watch")
        self.window.update()
        self.game_board = self.game_board.make_move(col, row)
        self.update_display()
        ai_move = self.game_board.best_move()
        if ai_move:
            self.game_board = self.game_board.make_move(*ai_move)
            self.update_display()
            self.window.config(cursor="")

    def update_display(self):
        for (col, row) in self.game_board.cells:
            text = self.game_board.cells[col, row]
            self.cell_buttons[col, row]['text'] = text
            self.cell_buttons[col, row]['disabledforeground'] = 'black'

            if text == self.game_board.empty_cell:
                self.cell_buttons[col, row]['state'] = 'normal'
            else:
                self.cell_buttons[col, row]['state'] = 'disabled'

        winning_cells = self.game_board.has_won()
        if winning_cells:
            for col, row in winning_cells:
                self.cell_buttons[col, row]['disabledforeground'] = 'red'
            for (col, row) in self.cell_buttons:
                self.cell_buttons[col, row]['state'] = 'disabled'
            messagebox.showinfo("Победа!", f"Игрок {self.game_board.ai_player} выиграл!")
            return

        if self.game_board.is_tied():
            messagebox.showinfo("Ничья", "Игра закончилась вничью!")
            for (col, row) in self.cell_buttons:
                self.cell_buttons[col, row]['state'] = 'disabled'
            return

    def mainloop(self):
        self.window.mainloop()

GameGUI().mainloop()