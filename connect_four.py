from tkinter import *
import tkinter as tk

EMPTY = 0
YELLOW = 1
RED = 2
#setting the value for the disc colour, for use in the board


ROWS = 6
COLUMNS = 7
CELL_SIZE = 100
WIN_LENGTH = 4

BOARD_BACKGROUND = "blue"
BACKGROUND = "light blue"
GUTTER = 50
BOARD_BORDER = 15
BUTTON_FONT = ("Arial", 10, "bold")
HUD_WIDTH = 300
HUD_LEFT = (COLUMNS*CELL_SIZE)+(2*GUTTER)+(2*BOARD_BORDER)
HUD_RIGHT = (HUD_LEFT+HUD_WIDTH)
HUD_FONT = ("Arial", 18, "bold")
HUD_SPACER = 35

turns = 0
player = EMPTY
board = []




def pvp_start():
    navigationMenuWin.destroy()

    window_width = (COLUMNS*CELL_SIZE)+(3*GUTTER)+HUD_WIDTH+(2*BOARD_BORDER)
    window_height = (ROWS*CELL_SIZE)+(2*GUTTER)+(2*BOARD_BORDER)

    PvPWin = Tk()
    PvPWin.title("Connect Four PvP")
    PvPWin.geometry(str(window_width)+"x"+str(window_height))
    PvPWin.configure(background=BACKGROUND)

    frame2 = Frame(PvPWin).pack()

    border_canvas = tk.Canvas(PvPWin, width=(COLUMNS*CELL_SIZE)+(2*BOARD_BORDER), height=(ROWS*CELL_SIZE)+(2*BOARD_BORDER), bg=BOARD_BACKGROUND, highlightthickness=0)
    border_canvas.place(x=GUTTER, y=GUTTER)

    board_canvas = tk.Canvas(PvPWin, width=(COLUMNS*CELL_SIZE), height=(ROWS*CELL_SIZE), bg=BOARD_BACKGROUND, highlightthickness=0)
    board_canvas.place(x=GUTTER+BOARD_BORDER, y=GUTTER+BOARD_BORDER)

    buttons = []
    for column in range(COLUMNS):
        btn = Button(frame2, text="Drop", command=lambda c=column: drop_disk(c))
        btn.config(width=8,font=BUTTON_FONT)
        btn.place(x=(66+(column*CELL_SIZE)+BOARD_BORDER),y=15)
        buttons.append(btn)
    
    
    # HUD
    current_player_var = StringVar(frame2, "")
    current_player_label = tk.Label(frame2, textvariable=current_player_var, font=HUD_FONT, bg=BACKGROUND).place(x=HUD_LEFT, y=GUTTER+HUD_SPACER)
    current_player_canvas = tk.Canvas(PvPWin, width=CELL_SIZE, height=CELL_SIZE, bg=BACKGROUND, bd = 0, highlightthickness=0)
    current_player_canvas.place(x=HUD_RIGHT-CELL_SIZE, y=GUTTER)
    
    turns_taken_label = tk.Label(frame2, text="Turns taken:", font=HUD_FONT, bg=BACKGROUND).place(x=HUD_LEFT, y=GUTTER+HUD_SPACER+CELL_SIZE)

    turns_var = StringVar(frame2, "")
    turns_taken_counter = tk.Label(frame2, textvariable=turns_var, font=HUD_FONT, bg=BACKGROUND, anchor="e", width=4).place(x=HUD_RIGHT-CELL_SIZE, y=GUTTER+HUD_SPACER+CELL_SIZE)
    
    reset_btn = Button(frame2, text="Reset", width=10, height=2, font=BUTTON_FONT,command=lambda: reset_game())
    reset_btn.place(x=HUD_RIGHT-100,y=((ROWS)*CELL_SIZE))
    
    def get_player_colour(player):
        if player == YELLOW:
            return "yellow"
        elif player == RED:
            return "red"
        else:
            return "light blue"



    def draw_disk(canvas, player, row, column, scale=0.8):
        gap = ((1-scale)*CELL_SIZE*0.5)
        canvas.create_oval(
            (column*CELL_SIZE)+gap, 
            (((ROWS-1)-row)*CELL_SIZE)+gap,
            ((column+1)*CELL_SIZE)-gap, 
            ((ROWS-row)*CELL_SIZE)-gap,  
            fill=get_player_colour(player), 
        )
        

    def next_turn():
        global turns
        turns += 1
        turns_var.set(str(turns))

        global player
        if turns%2 == 0:
            player = YELLOW
        elif turns%2 == 1:
            player = RED

    def reset_game():
        global board
        board = [[EMPTY for i in range(COLUMNS)] for i in range(ROWS)]

        global turns
        turns = 0
        turns_var.set(str(turns))

        global player
        player = YELLOW #Yellow always starts
        current_player_var.set("Next Player:")

        for i in range(COLUMNS):
            buttons[i].config(state=NORMAL)
        
        render_game()

    def declare_winner():
        current_player_var.set("Winner!")
        for i in range(COLUMNS):
            buttons[i].config(state=DISABLED)

    def render_game():
        board_canvas.delete("all")

        for column in range(COLUMNS):
            for row in range(ROWS):
                draw_disk(board_canvas, board[row][column], row, column)
        
        current_player_canvas.delete("all")
        draw_disk(current_player_canvas, player, ROWS-1, 0, 0.6)

        turns_taken_counter

    def check_winner():
        for column in range(COLUMNS):
            for row in range(ROWS):
                if board[row][column] == player:
                    for i in range(WIN_LENGTH):
                        if row+WIN_LENGTH > ROWS:
                            break
                        if board[row+i][column] != player:
                            break
                        else:
                            if i == (WIN_LENGTH-1):
                                declare_winner()
                                return True
                    for i in range(WIN_LENGTH):
                        if column+WIN_LENGTH > COLUMNS:
                            break
                        if board[row][column+i] != player:
                            break
                        else:
                            if i == (WIN_LENGTH-1):
                                declare_winner()
                                return True
                    for i in range(WIN_LENGTH):
                        if row+WIN_LENGTH > ROWS or column+WIN_LENGTH > COLUMNS:
                            break
                        if board[row+i][column+i] != player:
                            break
                        else:
                            if i == (WIN_LENGTH-1):
                                declare_winner()
                                return True
                    for i in range(WIN_LENGTH):
                        if row+WIN_LENGTH > ROWS or  column-i < 0:
                            break
                        if board[row+i][column-i] != player:
                            break
                        else:
                            if i == (WIN_LENGTH-1):
                                declare_winner()
                                return True
        return False # default return value


    def drop_disk(column):
        for row in range(ROWS):
            if board[row][column] == 0:
                board[row][column] = player
                if row == ROWS-1:
                    buttons[column].config(state=DISABLED)
                break
        if check_winner() == False:
            next_turn()
        render_game()


    # start things off
    reset_game()
    PvPWin.mainloop()



navigationMenuWin = Tk()
navigationMenuWin.title("Connect Four Navigation")
navigationMenuWin.geometry("400x650")
navigationMenuWin.configure(background=BACKGROUND)

frame1 = Frame(navigationMenuWin).pack()

b1 = Button(frame1, text="Player VS Player", font=("Arial", 28),command=pvp_start).pack()




navigationMenuWin.mainloop()