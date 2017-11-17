import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import ttk
from tkinter.messagebox import showinfo

import time
import donglebert
import rfid
import Game
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2

LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)

kickerDB = "kicker_scores.db"
db = donglebert.Database(kickerDB)

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
        for F in (GamePage, NewGamePage, PlayerPage, AdminPage):
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
        frame.event_generate("<<ShowFrame>>")


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
                            command=lambda: self.newGame())
        button1.pack(side="left", fill="both", expand=True)

    def newGame(self):
        self.Players = []
        self.numPlayers = 1


        self.win = tk.Toplevel()
        self.win.wm_title("Window")

        self.popupMsg = tk.StringVar()
        self.popupMsg.set("Bitte Token von Spieler %d scannen." % (self.numPlayers))

        self.l = tk.Label(self.win, textvariable = self.popupMsg)
        self.l.grid(row=0, column=0)

        self.after(100, self.SkanToken)

        b = tk.Button(self.win, text="Abbrechen", command=self.win.destroy)
        b.grid(row=1, column=0)

    def SkanToken(self):
        reader = rfid.rfid()
        tokenID = reader.TryGetToken()
        if(tokenID != None):
            self.Players.append(db.get_player(tokenID))
            self.numPlayers += 1
            if len(self.Players) == 4:
                # spiel-objekt anlegen
                self.win.destroy()
                spiel = Game.Game()
                spiel.player1 = self.Players[0]
                spiel.player2 = self.Players[1]
                spiel.player3 = self.Players[2]
                spiel.player4 = self.Players[3]
                NewGamePage.game = spiel
                self.controller.show_frame("NewGamePage")
            else:
                self.popupMsg.set("Bitte Token von Spieler %d scannen" % (self.numPlayers))
                self.controller.update_idletasks()
                self.after(2000, self.SkanToken)                
        else:
            self.after(100, self.SkanToken)


class NewGamePage(tk.Frame):

    game = None
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.onShowFrame)

        label = tk.Label(self, text="Neues Spiel:", font="Helvetica 12")
        #label.pack(side="top", fill="x", pady=10)
        label.grid(row=0, column=0)

        self.player1Name = tk.StringVar()
        self.player1Name.set("Player 1")
        labelPlayer1 = tk.Label(self, textvariable = self.player1Name)
        labelPlayer1.grid(row=1, column=0)

        self.player2Name = tk.StringVar()
        self.player2Name.set("Player 2")
        labelPlayer2 = tk.Label(self, textvariable = self.player2Name)
        labelPlayer2.grid(row=2, column=0)

        self.player3Name = tk.StringVar()
        self.player3Name.set("Player 3")
        labelPlayer3 = tk.Label(self, textvariable = self.player3Name)
        labelPlayer3.grid(row=1, column=1)

        self.player4Name = tk.StringVar()
        self.player4Name.set("Player 4")
        labelPlayer4 = tk.Label(self, textvariable = self.player4Name)
        labelPlayer4.grid(row=2, column=1)

        button1 = tk.Button(self, text="Sieg Team 1")
        button1.grid(row=3, column=0)

        button2 = tk.Button(self, text="Sieg Team 2")
        button2.grid(row=3, column=1)

class PlayerPage(tk.Frame):
 
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            label = tk.Label(self, text="Rangliste:", font="Helvetica 12")
            label.pack(side="top", fill="x", pady=10)
            button = tk.Button(self, text="Neuer Spieler",command=self.popup_bonus)
            button.pack()

        def popup_bonus(self):
            self.win = tk.Toplevel()
            self.win.wm_title("Window")
        
            l = tk.Label(self.win, text="Please Scan Token")
            l.grid(row=0, column=0)

            self.after(100, self.SkanToken)

            b = tk.Button(self.win, text="Abbrechen", command=self.win.destroy)
            b.grid(row=1, column=0)

        def SkanToken(self):
            tokenLeser = rfid.rfid()
            self.token = tokenLeser.TryGetToken()
            if(self.token != None):
                self.NewGamePlayer()
            else:
                self.after(100, self.SkanToken)
        
        def NewGamePlayer(self):
            self.win.destroy()
            self.win = tk.Toplevel()
            self.win.wm_title("NameGiver")
            l = tk.Label(self.win, text="Enter Name:")
            l.grid(row=1, column=0)
            self.e2 = tk.Entry(self.win,text="Enter Name")
            self.e2.grid(row=1, column=1)
            b = tk.Button(self.win, text="Okay", command=self.Safe2DataBase)
            b.grid(row=2, column=0)

        def Safe2DataBase(self):
            print("ID: %s\nLast Name: %s" % (self.token, self.e2.get()))
            db.add_new_player(self.e2.get(), self.token)
            self.win.destroy()


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