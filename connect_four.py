from tkinter import *



def PvP_start():
    navigationMenuWin.destroy()

    PvPWin = Tk()
    PvPWin.title("Connect Four PvP")
    PvPWin.geometry("800x650")
    PvPWin.configure(background="light blue")



navigationMenuWin = Tk()
navigationMenuWin.title("Connect Four Navigation")
navigationMenuWin.geometry("400x650")
navigationMenuWin.configure(background="light blue")

frame1 = Frame(navigationMenuWin)
frame1.pack()


b1 = Button(frame1, text="Player VS Player", font=("Arial", 28),command=PvP_start)
b1.pack()



navigationMenuWin.mainloop()