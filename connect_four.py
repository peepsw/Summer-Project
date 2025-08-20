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

BACKGROUND = "light blue"
GUTTER = 50
HUD_WIDTH = 300
HUD_LEFT = (COLUMNS*CELL_SIZE)+(2*GUTTER)
HUD_RIGHT = (HUD_LEFT+HUD_WIDTH)
HUD_FONT = ("Arial", 18, "bold")
HUD_SPACER = 35

turns = 0
player = EMPTY
board = []




def pvp_start():
    navigationMenuWin.destroy()

    window_width = (COLUMNS*CELL_SIZE)+(3*GUTTER)+HUD_WIDTH
    window_height = (ROWS*CELL_SIZE)+(2*GUTTER)

    PvPWin = Tk()
    PvPWin.title("Connect Four PvP")
    PvPWin.geometry(str(window_width)+"x"+str(window_height))
    PvPWin.configure(background=BACKGROUND)

    frame2 = Frame(PvPWin).pack()
    
    board_canvas = tk.Canvas(PvPWin, width=(COLUMNS*CELL_SIZE), height=(ROWS*CELL_SIZE), bg="white", highlightthickness=0)
    board_canvas.place(x=GUTTER, y=GUTTER)

    buttons = []
    for column in range(COLUMNS):
        btn = Button(frame2, text="drop", command=lambda c=column: drop_disk(c))
        btn.place(x=(80+(column*CELL_SIZE)),y=15)
        buttons.append(btn)
    
    
    # HUD

    next_player_label = tk.Label(frame2, text="Next Player:", font=HUD_FONT, bg=BACKGROUND).place(x=HUD_LEFT, y=GUTTER+HUD_SPACER)
    next_player_canvas = tk.Canvas(PvPWin, width=CELL_SIZE, height=CELL_SIZE, bg=BACKGROUND, bd = 0, highlightthickness=0)
    next_player_canvas.place(x=HUD_RIGHT-CELL_SIZE, y=GUTTER)
    
    
    
    
    reset_btn = Button(frame2, text="Reset", width=8, height=2 ,command=lambda: reset_game())
    reset_btn.place(x=((COLUMNS*CELL_SIZE)),y=(80+(ROWS*CELL_SIZE)))
    
    def get_player_colour(player):
        if player == YELLOW:
            return "yellow"
        elif player == RED:
            return "red"
        else:
            return "white"



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

        global player
        player = YELLOW #Yellow always starts

        for i in range(COLUMNS):
            buttons[i].config(state=NORMAL)
        
        render_game()

    def declare_winner():
        print(player, "Wins!")
        for i in range(COLUMNS):
            buttons[i].config(state=DISABLED)

    def render_game():
        board_canvas.delete("all")

        for i in range(COLUMNS+1):
            board_canvas.create_line((CELL_SIZE*i), (ROWS*CELL_SIZE), (CELL_SIZE*i), 0, fill="black", width=2)
        for i in range(ROWS+1):
            board_canvas.create_line((COLUMNS*CELL_SIZE), (CELL_SIZE*i), 0, (CELL_SIZE*i), fill="black", width=2)
        
        for column in range(COLUMNS):
            for row in range(ROWS):
                if board[row][column] != EMPTY:
                    draw_disk(board_canvas, board[row][column], row, column)
        
        next_player_canvas.delete("all")
        draw_disk(next_player_canvas, player, ROWS-1, 0, 0.6)

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
                                return None
                    for i in range(WIN_LENGTH):
                        if column+WIN_LENGTH > COLUMNS:
                            break
                        if board[row][column+i] != player:
                            break
                        else:
                            if i == (WIN_LENGTH-1):
                                declare_winner()
                                return None
                    for i in range(WIN_LENGTH):
                        if row+WIN_LENGTH > ROWS or column+WIN_LENGTH > COLUMNS:
                            break
                        if board[row+i][column+i] != player:
                            break
                        else:
                            if i == (WIN_LENGTH-1):
                                declare_winner()
                                return None
                    for i in range(WIN_LENGTH):
                        if row+WIN_LENGTH > ROWS or  column-i < 0:
                            break
                        if board[row+i][column-i] != player:
                            break
                        else:
                            if i == (WIN_LENGTH-1):
                                declare_winner()
                                return None            
    def drop_disk(column):
        for row in range(ROWS):
            if board[row][column] == 0:
                board[row][column] = player
                if row == ROWS-1:
                    buttons[column].config(state=DISABLED)
                break
        check_winner()
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