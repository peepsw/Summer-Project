from tkinter import *
import tkinter as tk

Yellow = 1
Red = 2
#setting the value for the disc colour, for use in the board

global turns
turns = 0

def playchange():
    global player
    if turns%2 == 0:
        player = Yellow
    elif turns%2 == 1:
        player = Red
playchange()
board = [[0 for i in range(7)] for i in range(6)]



def PvP_start():
    navigationMenuWin.destroy()

    PvPWin = Tk()
    PvPWin.title("Connect Four PvP")
    PvPWin.geometry("800x800")
    PvPWin.configure(background="light blue")

    frame2 = Frame(PvPWin).pack()
    

    canvas = tk.Canvas(PvPWin, width=700, height=600, bg="white")
    canvas.place(relx=0.5, rely=0.45, anchor="center")

    #canvas.create_oval(100, 100, 0, 0, fill="red",) note for me

    def redraw():
        for i in range(7):
            canvas.create_line((100*i), 600, (100*i), 0, fill="black", width=3)
        for i in range(6):
            canvas.create_line(700, (100*i), 0, (100*i), fill="black", width=3)
        
        for column in range(7):
            for row in range(6):
                if board[row][column] == Red:
                    canvas.create_oval(column*100, (6-row)*100, (column+1)*100, (5-row)*100, fill="red",)
                elif board[row][column] == Yellow:
                    canvas.create_oval(column*100, (6-row)*100, (column+1)*100, (5-row)*100, fill="yellow",)
                    
    def drop(column):
        for row in range(6):
            if board[row][column] == 0:
                if player == Red:
                    board[row][column] = Red
                    break
                elif player == Yellow:
                    board[row][column] = Yellow
                    break
        redraw()
        global turns
        turns += 1
        playchange()

    drop0 = Button(frame2, text="drop", command=lambda: drop(0))
    drop0.pack()
    
    
    redraw()
    PvPWin.mainloop()



navigationMenuWin = Tk()
navigationMenuWin.title("Connect Four Navigation")
navigationMenuWin.geometry("400x650")
navigationMenuWin.configure(background="light blue")

frame1 = Frame(navigationMenuWin).pack()

b1 = Button(frame1, text="Player VS Player", font=("Arial", 28),command=PvP_start).pack()




navigationMenuWin.mainloop()