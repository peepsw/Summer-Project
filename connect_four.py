from tkinter import *
import tkinter as tk
from enum import Enum

# Enum to represent the state of the Game
class GameState(Enum):
    PLAYING = 0
    WON = 1
    DRAWN = 2

# setting the value for the disc colour, for use in the board
EMPTY = 0
YELLOW = 1
RED = 2

# Game constants
ROWS = 6
COLUMNS = 7
CELL_SIZE = 100 # pixels
WIN_LENGTH = 4
MAX_TURNS = ROWS*COLUMNS # derived but useful to have

# GUI constants and settings
BOARD_BACKGROUND = "blue"
BACKGROUND = "light blue"
GUTTER = 50
BOARD_BORDER = 15
BUTTON_FONT = ("Arial", 10, "bold")
 #HUD is the status panel to the right of the board
HUD_WIDTH = 300
HUD_LEFT = (COLUMNS*CELL_SIZE)+(2*GUTTER)+(2*BOARD_BORDER)
HUD_RIGHT = (HUD_LEFT+HUD_WIDTH)
HUD_FONT = ("Arial", 18, "bold")
HUD_SPACER = 35

 #Variables represent game state
turns = 0 # turns taken so far
player = EMPTY # next player - init'd by reset function
board = [] # reset function builds it based on ROWS and COLUMNS
# structure to hold winning coordinates
winning_pos = {
    'start_row': -1,
    'start_column': -1,
    'end_row': -1,
    'end_column': -1 
}
game_state = GameState.PLAYING # controls the state of the game


'''
    Entry point for a two Player game
    variable scope for the GUI components
'''
def pvp_start():
    # closes the initial startup screen
    navigationMenuWin.destroy() 

    # calculate the window size of the main game window, including HUD
    window_width = (COLUMNS*CELL_SIZE)+(3*GUTTER)+HUD_WIDTH+(2*BOARD_BORDER)
    window_height = (ROWS*CELL_SIZE)+(2*GUTTER)+(2*BOARD_BORDER)

    # initialise and configure game window
    pvp_window = Tk()
    pvp_window.title("Connect Four PvP")
    pvp_window.geometry(str(window_width)+"x"+str(window_height))
    pvp_window.configure(background=BACKGROUND)

    # frame for GUI components
    pvp_frame = Frame(pvp_window).pack()

    # Canvases - using highlightthickness 0 so no weird border
    # outer shell for the game board, purely to create an easy border
    border_canvas = tk.Canvas(pvp_window, width=(COLUMNS*CELL_SIZE)+(2*BOARD_BORDER), height=(ROWS*CELL_SIZE)+(2*BOARD_BORDER), bg=BOARD_BACKGROUND, highlightthickness=0)
    border_canvas.place(x=GUTTER, y=GUTTER)

    # actual game canvas where we draw the discs
    board_canvas = tk.Canvas(pvp_window, width=(COLUMNS*CELL_SIZE), height=(ROWS*CELL_SIZE), bg=BOARD_BACKGROUND, highlightthickness=0)
    board_canvas.place(x=GUTTER+BOARD_BORDER, y=GUTTER+BOARD_BORDER)

    # buttons at the top of each column for placing discs
    buttons = []

    # creating a button for each column, and assigning event handlers and styles
    for column in range(COLUMNS):
        # on button click call the drop disc function with the column now in local scope via the lambda
        btn = Button(pvp_frame, text="Drop", command=lambda c=column: drop_disc(c)) #without local variable always uses last column!!!
        btn.config(width=8,font=BUTTON_FONT)
        
        # odd numbers are trial and error to get the buttons visually nicer
        btn.place(x=(66+(column*CELL_SIZE)+BOARD_BORDER),y=15)
        
        # keep buttons in array for later access indexed by their column
        buttons.append(btn)
    
    
    '''
        Status panel to show turns, player and winner
    '''
    # text variable for current_player_label so it can change the text depending on game state
    current_player_var = StringVar(pvp_frame, "") 

    # shows next player, or the winner, or if its a draw
    current_player_label = tk.Label(pvp_frame, textvariable=current_player_var, font=HUD_FONT, bg=BACKGROUND).place(x=HUD_LEFT, y=GUTTER+HUD_SPACER)
    
    # canvas to draw the disc of the next player, or winning player - reuses the draw disc function
    current_player_canvas = tk.Canvas(pvp_window, width=CELL_SIZE, height=CELL_SIZE, bg=BACKGROUND, bd = 0, highlightthickness=0)
    current_player_canvas.place(x=HUD_RIGHT-CELL_SIZE, y=GUTTER)
    
    # fixed label for number of turns
    turns_taken_label = tk.Label(pvp_frame, text="Turns taken:", font=HUD_FONT, bg=BACKGROUND).place(x=HUD_LEFT, y=GUTTER+HUD_SPACER+CELL_SIZE)

    # text variable for turns_taken_counter label, updated each turn
    turns_var = StringVar(pvp_frame, "")
    # right aligned label showing turns
    turns_taken_counter = tk.Label(pvp_frame, textvariable=turns_var, font=HUD_FONT, bg=BACKGROUND, anchor="e", width=4).place(x=HUD_RIGHT-CELL_SIZE, y=GUTTER+HUD_SPACER+CELL_SIZE)
    
    # this button resets the game 
    reset_btn = Button(pvp_frame, text="Reset", width=10, height=2, font=BUTTON_FONT,command=lambda: reset_game())
    # placed low down out the way to avoid accidents
    reset_btn.place(x=HUD_RIGHT-100,y=((ROWS)*CELL_SIZE))
    
    '''
        takes the value of player and returns a colour
        if unrecognised player defaults to black
        this is exploited to show dots on the winning line
    '''
    def get_player_colour(player):
        if player == EMPTY:
            return BACKGROUND # empty cell is drawn as a hole
        if player == YELLOW:
            return "yellow"
        elif player == RED:
            return "red"
        else:
            return "black"


    '''
        multipurpose function to draw all discs
        row is inverted so row 0 is at the bottom which the way the game works
        disc is drawn in centre of the cell and the scale controls the size of it
        used for board, winning dots, and next player
    '''
    def draw_disc(canvas, player, row, column, scale=0.8):
        gap = ((1-scale)*CELL_SIZE*0.5) # how many pixels in from cell edge
        canvas.create_oval(
            (column*CELL_SIZE)+gap, # x is left edge
            (((ROWS-1)-row)*CELL_SIZE)+gap, # y is bottom egde
            ((column+1)*CELL_SIZE)-gap, # x is right edge
            ((ROWS-row)*CELL_SIZE)-gap, # y is top edge
            fill=get_player_colour(player), 
        )
        
    '''
        updates number of turns, and checks if draw, and alternates player
    '''
    def next_turn():
        global turns # globaled so turns can be updated
        turns += 1
        turns_var.set(str(turns)) # this will update the label 

        # checks if maximum number of turns have been played, because thats a draw.
        if turns == MAX_TURNS:
            declare_draw()
            return None # stops player updating
        
        # updates player order is fixed by turns
        global player
        if turns%2 == 0:
            player = YELLOW
        elif turns%2 == 1:
            player = RED

    '''
        inits game, clears last game
        called at the beginning and when reset game is clicked
        so its all in one place
    '''
    def reset_game():
        # clear any winning data
        winning_pos["start_row"] = -1
        winning_pos["start_column"] = -1
        winning_pos["end_row"] = -1
        winning_pos["end_column"] = -1

        # resets game state
        global game_state
        game_state = GameState.PLAYING
        
        # builds the board based on the constants, each cell is initially EMPTY
        global board
        board = [[EMPTY for i in range(COLUMNS)] for i in range(ROWS)]

        # reset turns to zero and the label
        global turns
        turns = 0
        turns_var.set(str(turns))

        # gives first move to yellow
        global player
        player = YELLOW # Yellow always starts
        current_player_var.set("Next Player:") # updates label

        # loop through each drop button and reenables them
        for i in range(COLUMNS):
            buttons[i].config(state=NORMAL)
        
        #redraw everything
        render_game()

    '''
        saves winning coords, and sets winning game state
    '''
    def declare_winner(start_row, start_column, end_row, end_column):
        # the start and end, row and column of the winning run
        winning_pos["start_row"] = start_row
        winning_pos["start_column"] = start_column
        winning_pos["end_row"] = end_row
        winning_pos["end_column"] = end_column

        # sets game_state to WON
        global game_state
        game_state = GameState.WON 

        # changes player label to show winner, disc not updated so shows last player
        current_player_var.set("Winner!")

        # disables all buttons - prevents moves
        for i in range(COLUMNS):
            buttons[i].config(state=DISABLED)

    '''
        sets game state to draw
        you've run out of moves when this happens!
    '''
    def declare_draw():
        # set game state to draw 
        global game_state
        game_state = GameState.DRAWN

        # sets player label to draw 
        current_player_var.set("Draw!")
        
        # no next player
        global player
        player = EMPTY

    '''
        updates the board based on the state
        clear the canvases and redraw from scratch
    '''
    def render_game():
        # clears the board
        board_canvas.delete("all")

        # loop through every cell and draw its contents
        for column in range(COLUMNS):
            for row in range(ROWS):
                draw_disc(board_canvas, board[row][column], row, column) # empty drawn as a hole

        # clear the current player disc in the HUD        
        current_player_canvas.delete("all")

        # ROWS-1 because inversion, 0.6 for smaller scale
        draw_disc(current_player_canvas, player, ROWS-1, 0, 0.6)

        # draws a line through the winning cells 
        if game_state == GameState.WON:
            board_canvas.create_line(
                (winning_pos["start_column"] + 0.5) * CELL_SIZE, # 0.5 to put the line in the middle of the cell
                ((ROWS-winning_pos["start_row"]) - 0.5) * CELL_SIZE,
                (winning_pos["end_column"] + 0.5) * CELL_SIZE,
                ((ROWS-winning_pos["end_row"]) - 0.5) * CELL_SIZE,
                width=4
            )
            
            # draw small black disc at the beginning and end of a winning line
            draw_disc(board_canvas, -1, winning_pos["start_row"], winning_pos["start_column"], 0.2)
            draw_disc(board_canvas, -1, winning_pos["end_row"], winning_pos["end_column"], 0.2)
            

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
                                declare_winner(row, column, (row+i), column)
                                return True
                    for i in range(WIN_LENGTH):
                        if column+WIN_LENGTH > COLUMNS:
                            break
                        if board[row][column+i] != player:
                            break
                        else:
                            if i == (WIN_LENGTH-1):
                                declare_winner(row, column, row, (column+i))
                                return True
                    for i in range(WIN_LENGTH):
                        if row+WIN_LENGTH > ROWS or column+WIN_LENGTH > COLUMNS:
                            break
                        if board[row+i][column+i] != player:
                            break
                        else:
                            if i == (WIN_LENGTH-1):
                                declare_winner(row, column, (row+i), (column+i))
                                return True
                    for i in range(WIN_LENGTH):
                        if row+WIN_LENGTH > ROWS or  column-i < 0:
                            break
                        if board[row+i][column-i] != player:
                            break
                        else:
                            if i == (WIN_LENGTH-1):
                                declare_winner(row, column, (row+i), (column-i))
                                return True
        return False # default return value


    def drop_disc(column):
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
    pvp_window.mainloop()



navigationMenuWin = Tk()
navigationMenuWin.title("Connect Four Navigation")
navigationMenuWin.geometry("400x650")
navigationMenuWin.configure(background=BACKGROUND)

frame1 = Frame(navigationMenuWin).pack()

b1 = Button(frame1, text="Player VS Player", font=("Arial", 28),command=pvp_start).pack()




navigationMenuWin.mainloop()