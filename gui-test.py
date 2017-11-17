import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import ttk
from tkinter.messagebox import showinfo

import time
import donglebert
# import rfid
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2

LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)


class KickerApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.numPlayers = 0

        frame = ButtonFrame(parent=self, controller=self)
        frame.config(bg="white")
        frame.pack()
        
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.config(bg="blue")
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (GamePage, NewGamePage, PlayerPage, NewPlayerPage, AdminPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_rowconfigure(0, weight=2)
            frame.grid_columnconfigure(0, weight=2)
            #frame.pack(side="top", fill="both", expand=True)

            self.frames[page_name] = frame

        self.show_frame("GamePage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class ButtonFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        button1 = tk.Button(self, text="Rangliste",
                           command=lambda: controller.show_frame("PlayerPage"))
        #button1.grid_rowconfigure(0, weight=1)
        #button1.grid_columnconfigure(0, weight=1)       
        
        button2 = tk.Button(self, text="Spiele",
                           command=lambda: controller.show_frame("GamePage"))
        #button2.grid_rowconfigure(0, weight=1)
        #button2.grid_columnconfigure(1, weight=1)        

        button3 = tk.Button(self, text="Admin",
                           command=lambda: controller.show_frame("AdminPage"))
        #button2.grid_rowconfigure(0, weight=1)
        #button2.grid_columnconfigure(1, weight=1)
        button1.pack(side="left", fill="both", expand=True)
        button2.pack(side="left", fill="both", expand=True)
        button3.pack(side="right", fill="both", expand=True)


class GamePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Letzte Spiele:", font="Helvetica 12")
        label.pack(side="top", fill="x", pady=10)

        # Hole Spiele aus db und zeige die letzten x an

        spiel1 = tk.Label(self, text="spiel1", font="Helvetica 12")
        spiel1.pack(side="top", fill="x", pady=10)

        spiel2 = tk.Label(self, text="spiel2", font="Helvetica 12")
        spiel2.pack(side="top", fill="x", pady=10)

        spiel3 = tk.Label(self, text="spiel3", font="Helvetica 12")
        spiel3.pack(side="top", fill="x", pady=10)

        spiel4 = tk.Label(self, text="spiel4", font="Helvetica 12")
        spiel4.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Neues Spiel",
                            command=lambda: newGame())
        button1.pack(side="left", fill="both", expand=True)

        def newGame():
            # spiel-objekt anlegen
            controller.show_frame("NewGamePage")
            
            kickerDB = "kicker_scores.db"

            db = donglebert.Database(kickerDB)

            IDpopup("Bitte Token von Spieler 1 scannen.")
            db.get_player(id)
        
            # read first token
            # spiel.spieler1 = getPlayer(getTokenID())
            # win.destroy
            # controller.numPlayers++
        
            IDpopup("Bitte Token von Spieler 2 scannen.")
            id2 = getID()

            # read second token
            # spiel.spieler2 = getPlayer(getTokenID())
            # check for duplicates
            # win.destroy
            # controller.numPlayers++
        
            IDpopup("Bitte Token von Spieler 3 scannen.")
            id3 = getID()

            # read third token
            # spiel.spieler3 = getPlayer(getTokenID())
            # check for duplicates
            # win.destroy
            # controller.numPlayers++
        
            IDpopup("Bitte Token von Spieler 4 scannen.")
            id4 = getID()

            # read fourth token
            # spiel.spieler4 = getPlayer(getTokenID())
            # check for duplicates
            # win.destroy
            # controller.numPlayers++

        def IDpopup(msg):
            popup = tk.Tk()
            popup.wm_title("!")
            label = tk.Label(popup, text=msg, font=NORM_FONT)
            label.pack(side="top", fill="x", pady=10)
            B1 = tk.Button(popup, text="Okay", command = popup.destroy)
            B1.pack()
            popup.mainloop()

        def getID():
            time.sleep(5)
            return 12345


class NewGamePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Neues Spiel:", font="Helvetica 12")
        label.pack(side="top", fill="x", pady=10)

        # wenn frame in vordergrund kommt, abfrage nach token beginnen
        print("Scan first token")
        # player1 = getPlayer(getTokenID)
        # player2 = getPlayer(getTokenID)
        # player3 = getPlayer(getTokenID)
        # player4 = getPlayer(getTokenID)

        button1 = tk.Button(self, text="Neues Spiel",
                            command=lambda: controller.show_frame("NewGamePage"))
        button1.pack(side="left", fill="both", expand=True)


class PlayerPage(tk.Frame):
 
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            label = tk.Label(self, text="Rangliste:", font="Helvetica 12")
            label.pack(side="top", fill="x", pady=10)
            button = tk.Button(self, text="Neuer Spieler",command=popup_bonus)
            button.pack()
        def popup_bonus():
            win = tk.Toplevel()
            win.wm_title("Window")
        
            l = tk.Label(win, text="Please Scan Token")
            l.grid(row=0, column=0)

            b = tk.Button(win, text="Okay", command=NewGamePlayer)
            b.grid(row=1, column=0)
        def NewGamePlayer():
            win = tk.Toplevel()
            win.wm_title("NameGiver")
            l = tk.Label(win, text="Enter ID:")
            l.grid(row=0, column=0)
            e1 = tk.Entry(win,text="Enter Name")
            e1.grid(row=0, column=1)
            l = tk.Label(win, text="Enter Name:")
            l.grid(row=1, column=0)
            e2 = tk.Entry(win,text="Enter Surname")
            e2.grid(row=1, column=1)
            b = tk.Button(win, text="Okay", command=win.destroy)
            b.grid(row=2, column=0)

        

class NewPlayerPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Neuer Spieler", font="Helvetica 12")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("GamePage"))
        button.pack()


class AdminPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("GamePage"))
        button.pack()


if __name__ == "__main__":
    app = KickerApp()
    app.mainloop()