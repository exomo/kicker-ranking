import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import ttk
from tkinter.messagebox import showinfo

import time
import database
import rfid
import Game

import trueskill
from trueskill import Rating
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2

LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)

kickerDB = "kicker_scores.db"
db = database.Database(kickerDB)

class KickerApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.change_window_mode("window") # change to "fullscreen" to start in full screen

        # exit on Esc
        self.bind('<Escape>', lambda e: self.destroy())
        # Ctrl + Enter changes between fullscreen and window
        self.bind('<Command-Return>', lambda e: self.toggle_window_mode())

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.numPlayers = 0

        frame = ButtonFrame(parent=self, controller=self)
        frame.config(bg="white")
        frame.pack(side="top", fill="x", in_=self)
        
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.config(bg="blue")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.pack(side="top", fill="both", expand=True, in_=self)

        self.frames = {}
        for F in (GamePage, NewGamePage, PlayerPage, AdminPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

            self.frames[page_name] = frame

        self.show_frame("GamePage")

    def change_window_mode(self, mode):
        if mode == "fullscreen":
            # go fullscreen
            self.resizable(width=False, height=False)
            self.overrideredirect(True)
            self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
            self.window_mode = mode

        if mode == "window":
            # run in a window
            self.geometry('800x600')
            self.resizable(width=True, height=True)
            self.overrideredirect(False)
            self.window_mode = mode
        
    def toggle_window_mode(self):
        if self.window_mode == "fullscreen":
            self.change_window_mode("window")
        else:
            self.change_window_mode("fullscreen")

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

        self.after(10, self.SkanToken)

        b = tk.Button(self.win, text="Abbrechen", command=self.win.destroy)
        b.grid(row=1, column=0)

    def SkanToken(self):
        reader = rfid.rfid()
        tokenID = reader.TryGetToken()
        if(tokenID != None):
            player = db.get_player(tokenID)
            if(player != None):
                self.Players.append(player)
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
                self.popupMsg.set("Spieler nicht registriert!\nBitte Token von Spieler %d scannen" % (self.numPlayers))
                self.controller.update_idletasks()
                self.after(100, self.SkanToken)
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

        button1 = tk.Button(self, text="Sieg Team 1", command=lambda: self.winner(1))
        button1.grid(row=3, column=0)

        button2 = tk.Button(self, text="Sieg Team 2", command=lambda: self.winner(2))
        button2.grid(row=3, column=1)

    def winner(self, team):
        print("Team {0} wins!".format(team))
        game = self.game
        # TODO: Use the real TrueSkill algorithm here, this is just a dummy implementation to see some change in the scores
        
        self.getGameRatings(game, team)
        
        db.update_player_skill(game.player1)
        db.update_player_skill(game.player2)
        db.update_player_skill(game.player3)
        db.update_player_skill(game.player4)
        self.controller.show_frame("GamePage")

    def getGameRatings(self, game, team):
        # Parameter über Admin-Interface verstellbar? Ranglisten-Reset bei Parameter-Änderung notwendig?
        # Spielpaarungen und Ergebnisse mitloggen, damit hinterher Parameter appliziert werden können.
        # Wird für Anzeige der letzten Spiele eh gebraucht
        env = trueskill.TrueSkill(mu=30.0, sigma=10.0, beta=5.0, tau=0.1, draw_probability=0.0) # Es gibt kein Unentschieden

        if 'mpmath' in trueskill.backends.available_backends():
            # mpmath can be used in the current environment
            env.backend = 'mpmath'
            
        print(env)
            
        # Ratings der einzelnen Spieler laden (mu und sigma können auch explizit übergeben werden)
        # TODO: Das geht mit Sicherheit auch mit so ner tollen Python-Schleife, alternativ könnte man im Player direkt das Rating-Objekt von trueskill verwenden
        p1 = env.create_rating(mu=game.player1.gamerScore, sigma=game.player1.standardDeviation) # 1P's skill, create_rating verwendet die als default die Werte die im environment festgelegt werden
        p2 = env.create_rating(mu=game.player2.gamerScore, sigma=game.player2.standardDeviation)
        p3 = env.create_rating(mu=game.player3.gamerScore, sigma=game.player3.standardDeviation)
        p4 = env.create_rating(mu=game.player4.gamerScore, sigma=game.player4.standardDeviation)

        print(p1)
        print(p2)
        print(p3)
        print(p4)

        # Teams zuweisen
        # TODO: Teams variabel machen
        Team1 = [p1, p2]
        Team2 = [p3, p4]

        print('{:.1%} chance to draw'.format(env.quality([Team1, Team2])))
        if env.quality([Team1, Team2]) < 0.50:
            print('This match seems to be not so fair')

        # neue Bewertungen anhand des Ergebnisses berechnen
        if team == 1:
            (p1, p2), (p3, p4) = env.rate([Team1, Team2], ranks=[0, 1]) # Team1 wins (rank lower)
        elif team == 2:
            (p1, p2), (p3, p4) = env.rate([Team1, Team2], ranks=[1, 0]) # Team1 wins (rank lower)

        # Neue Wertung ausgeben
        print(p1)
        print(p2)
        print(p3)
        print(p4)

        # TODO: Das geht mit Sicherheit auch mit so ner tollen Python-Schleife, alternativ könnte man im Player direkt das Rating-Objekt von trueskill verwenden
        game.player1.gamerScore = p1.mu
        game.player1.standardDeviation = p1.sigma
        game.player2.gamerScore = p1.mu
        game.player2.standardDeviation = p1.sigma
        game.player3.gamerScore = p1.mu
        game.player3.standardDeviation = p1.sigma
        game.player4.gamerScore = p1.mu
        game.player4.standardDeviation = p1.sigma

        # TODO: Neue Bewertung zurückgeben, oder gleich hier in DB speichern.
    
    def onShowFrame(self, event):
        if(NewGamePage.game != None):
            self.player1Name.set(NewGamePage.game.player1.name)
            self.player2Name.set(NewGamePage.game.player2.name)
            self.player3Name.set(NewGamePage.game.player3.name)
            self.player4Name.set(NewGamePage.game.player4.name)

class PlayerPage(tk.Frame):
 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg="blue")
        self.bind("<<ShowFrame>>", self.onShowFrame)

        label = tk.Label(self, text="Rangliste:", font="Helvetica 12")
        label.pack(side="top", fill="x", pady=10)
        self.listMsg = tk.StringVar()
        rankList = tk.Label(self, textvariable=self.listMsg)
        rankList.pack(side="top", fill="both", expand=True)
        button = tk.Button(self, text="Neuer Spieler",command=self.popup_bonus)
        button.pack(side="top", fill="x", expand=True)

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
        self.onShowFrame(None)
        
    def onShowFrame(self, event):
        rank = db.get_all_players()
        self.listMsg.set("\n".join(["{name} - {score}".format(name=p.name, score=p.gamerScore) for p in rank]))
        self.controller.update_idletasks()

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