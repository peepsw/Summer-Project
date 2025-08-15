from tkinter import *
import tkinter as tk

YELLOW = 1
RED = 2
#setting the value for the disc colour, for use in the board

ROWS = 6
COLUMNS = 7
CELL_SIZE = 100
WIN_LENGTH = 4

global turns
turns = 0

def playchange():
    global player
    if turns%2 == 0:
        player = YELLOW
    elif turns%2 == 1:
        player = RED
playchange()
board = [[0 for i in range(COLUMNS)] for i in range(ROWS)]



def PvP_start():
    navigationMenuWin.destroy()

    window_width = (COLUMNS*CELL_SIZE)+100
    window_height = (ROWS*CELL_SIZE)+150

    PvPWin = Tk()
    PvPWin.title("Connect Four PvP")
    PvPWin.geometry(str(window_width)+"x"+str(window_height))
    PvPWin.configure(background="light blue")

    frame2 = Frame(PvPWin).pack()
    

    canvas = tk.Canvas(PvPWin, width=(COLUMNS*CELL_SIZE), height=(ROWS*CELL_SIZE), bg="white")
    canvas.place(relx=0.5, rely=0.45, anchor="center")

    #canvas.create_oval(CELL_SIZE, CELL_SIZE, 0, 0, fill="RED",) note for me

    def ReDraw():
        for i in range(COLUMNS):
            canvas.create_line((CELL_SIZE*i), (ROWS*CELL_SIZE), (CELL_SIZE*i), 0, fill="black", width=3)
        for i in range(ROWS):
            canvas.create_line((COLUMNS*CELL_SIZE), (CELL_SIZE*i), 0, (CELL_SIZE*i), fill="black", width=3)
        
        for column in range(COLUMNS):
            for row in range(ROWS):
                if board[row][column] == RED:
                    canvas.create_oval(column*CELL_SIZE, (ROWS-row)*CELL_SIZE, (column+1)*CELL_SIZE, ((ROWS-1)-row)*CELL_SIZE, fill="RED",)
                elif board[row][column] == YELLOW:
                    canvas.create_oval(column*CELL_SIZE, (ROWS-row)*CELL_SIZE, (column+1)*CELL_SIZE, ((ROWS-1)-row)*CELL_SIZE, fill="YELLOW",)


    def RunCheck():
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
                                print("win")
                    for i in range(WIN_LENGTH):
                        if column+WIN_LENGTH > COLUMNS:
                            break
                        if board[row][column+i] != player:
                            break
                        else:
                            if i == (WIN_LENGTH-1):
                                print("win")
                    for i in range(WIN_LENGTH):
                        if row+WIN_LENGTH > ROWS or column+WIN_LENGTH > COLUMNS:
                            break
                        if board[row+i][column+i] != player:
                            break
                        else:
                            if i == (WIN_LENGTH-1):
                                print("win")
                    for i in range(WIN_LENGTH):
                        if row+WIN_LENGTH > ROWS or  column-i < 0:
                            break
                        if board[row+i][column-i] != player:
                            break
                        else:
                            if i == (WIN_LENGTH-1):
                                print("win")            
    def drop(column):
        for row in range(ROWS):
            if board[row][column] == 0:
                board[row][column] = player
                break
        else:
            return None
        RunCheck()
        ReDraw()
        global turns
        turns += 1
        playchange()

    buttons = []
    for column in range(COLUMNS):
        btn = Button(frame2, text="drop", command=lambda c=column: drop(c))
        btn.place(x=(80+(column*CELL_SIZE)),y=5)
        buttons.append(btn)

    ReDraw()
    PvPWin.mainloop()



navigationMenuWin = Tk()
navigationMenuWin.title("Connect Four Navigation")
navigationMenuWin.geometry("400x650")
navigationMenuWin.configure(background="light blue")

frame1 = Frame(navigationMenuWin).pack()

b1 = Button(frame1, text="Player VS Player", font=("Arial", 28),command=PvP_start).pack()




navigationMenuWin.mainloop()