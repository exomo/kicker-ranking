import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import ttk
from tkinter.messagebox import showinfo

from PIL import Image, ImageTk

import time
from database import database
from hardware import rfid
from kicker import Game

import trueskill
from trueskill import Rating
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

kickerDB = "kicker_scores.db"
db = database.Database(kickerDB)

rfidReader = rfid.rfid()

#: Default initial mean of ratings.
MU = 30.
#: Default initial standard deviation of ratings.
SIGMA = MU / 3
#: Default distance that guarantees about 76% chance of winning.
BETA = SIGMA / 2
#: Default dynamic factor.
TAU = SIGMA / 100
#: Default draw probability of the game.
DRAW_PROBABILITY = .0
#: A basis to check reliability of the result.
DELTA = 0.0001

class KickerApp(tk.Tk):
    """
    Main class of GUI, specifies basic layout.
    """
    def __init__(self, *args, **kwargs):
        """
        Init function of main class.
        """
        if 'mpmath' in trueskill.backends.available_backends():
            # mpmath can be used in the current environment
            backend = 'mpmath'
        else:
            backend = None

        # Parameter über Admin-Interface verstellbar? Ranglisten-Reset bei Parameter-Änderung notwendig?
        # Spielpaarungen und Ergebnisse mitloggen, damit hinterher Parameter appliziert werden können.
        # Wird für Anzeige der letzten Spiele eh gebraucht
        env = trueskill.setup(mu=MU, sigma=SIGMA, beta=BETA, tau=TAU, draw_probability=DRAW_PROBABILITY, backend=backend) # Es gibt kein Unentschieden

        print(env)

        tk.Tk.__init__(self, *args, **kwargs)

        self.wm_title("ITK Kicker Rangliste")
        self.change_window_mode("window") # change to "fullscreen" to start in full screen

        # exit on Esc
        self.bind('<Escape>', lambda e: self.destroy())
        # Alt + Enter changes between fullscreen and window
        self.bind('<Alt-Return>', lambda e: self.toggle_window_mode())

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.numPlayers = 0

        frame = ButtonFrame(parent=self, controller=self)
        frame.config(bg="white")
        frame.pack(side="top", fill="x", in_=self)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.config(bg="lightblue")
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

        # Startseite mit etwas verzögerung aufrufen sonst wird <<ShowFrame>> event nicht ausgelöst.
        self.after(10, lambda: self.show_frame("GamePage"))

    def change_window_mode(self, mode):
        if mode == "fullscreen":
            # go fullscreen
            self.resizable(width=False, height=False)
            self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
            self.attributes("-fullscreen", True)
            self.window_mode = mode

        if mode == "window":
            # run in a window
            self.attributes("-fullscreen", False)
            self.geometry('800x600')
            self.resizable(width=True, height=True)
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
    """
    Class to show navigation buttons
    """
    def __init__(self, parent, controller):
        """
        Init function of ButtonFrame
        """
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
    """
    Class to show a frame, where completed games are listed and new games can be started
    """
    def __init__(self, parent, controller):
        """
        Init function of GamePage
        """
        tk.Frame.__init__(self, parent)
        self.bind("<<ShowFrame>>", self.onShowFrame)
        self.controller = controller

        self.cancelNewGame = False

        label = tk.Label(self, text="Letzte Spiele:", font="Helvetica 12")
        label.pack(side="top", fill="x", pady=10)

        lists = tk.Frame(self)
        lists.pack(side="top", fill="both", expand=True)

        scrollbar = tk.Scrollbar(lists)
        scrollbar.pack(side="right", fill="y")

        self.gameList = ttk.Treeview(lists,
                                     columns=("spiel", "team1", "result", "team2", "time"),
                                     show="headings",
                                     yscrollcommand=scrollbar.set
                                    )

        self.gameList.heading("spiel", text="Spiel-ID")
        self.gameList.column("spiel", minwidth=100, width=100, stretch=False)

        self.gameList.heading("team1", text="Team 1")
        self.gameList.column("team1", minwidth=200, width=200, anchor="e")

        self.gameList.heading("result", text="Endstand")
        self.gameList.column("result", minwidth=100, width=100, anchor="s", stretch=False)

        self.gameList.heading("team2", text="Team 2")
        self.gameList.column("team2", minwidth=200, width=200)

        self.gameList.heading("time", text="Zeit")
        self.gameList.column("time", minwidth=150, width=150)

        self.gameList.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.gameList.yview)

        button1 = tk.Button(self, text="Neues Spiel", command=self.newGame)
        button1.pack(side="left", fill="x", expand=True)

    def newGame(self):
        self.Players = []
        self.numPlayers = 1

        self.win = tk.Toplevel()
        self.win.wm_title("Window")

        self.popupMsg = tk.StringVar()
        self.popupMsg.set("Bitte Token von Spieler %d scannen." % (self.numPlayers))

        l = tk.Label(self.win, textvariable=self.popupMsg)
        l.grid(row=0, column=0)

        self.after(10, self.SkanToken)

        b = tk.Button(self.win, text="Abbrechen", command=self.cancelScan)
        b.grid(row=1, column=0)

    def cancelScan(self):
        self.cancelNewGame = True
        self.win.destroy()

    def SkanToken(self):
        if self.cancelNewGame:
            return
        tokenID = rfidReader.TryGetToken()
        if tokenID != None:
            player = db.get_player(tokenID)
            if player != None:
                if not player.tokenID in [p.tokenID for p in self.Players]:
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
                    self.popupMsg.set("Spieler bereits hinzugefügt.\nBitte Token von Spieler %d scannen" % (self.numPlayers))
                    self.controller.update_idletasks()
                    self.after(100, self.SkanToken)
            else:
                self.popupMsg.set("Spieler nicht registriert!\nBitte Token von Spieler %d scannen" % (self.numPlayers))
                self.controller.update_idletasks()
                self.after(100, self.SkanToken)
        else:
            self.after(100, self.SkanToken)

    def onShowFrame(self, event):

        self.gameList.delete(*self.gameList.get_children())

        games = db.get_last_games()

        for i, game in enumerate(games):
            if i%2 == 0:
                self.gameList.insert("", tk.END,
                                     text="Spiel {game}".format(game=i+1),
                                     values=(
                                         "{game}".format(game=game.id),
                                         "{p1} und {p2}".format(p1=game.player1.name, p2=game.player2.name),
                                         "{s1} : {s2}".format(s1=game.scoreTeam1, s2=game.scoreTeam2),
                                         "{p1} und {p2}".format(p1=game.player3.name, p2=game.player4.name),
                                         game.time),
                                     tags=("oddrow",)
                                    )
            else:
                self.gameList.insert("", tk.END,
                                     text="Spiel {game}".format(game=i+1),
                                     values=(
                                         "{game}".format(game=game.id),
                                         "{p1} und {p2}".format(p1=game.player1.name, p2=game.player2.name),
                                         "{s1} : {s2}".format(s1=game.scoreTeam1, s2=game.scoreTeam2),
                                         "{p1} und {p2}".format(p1=game.player3.name, p2=game.player4.name),
                                         game.time),
                                     tags=("evenrow",)
                                    )

            self.gameList.tag_configure("oddrow", background="lightblue")


class NewGamePage(tk.Frame):
    """
    Class to handle the creation of new games
    """

    game = None

    def __init__(self, parent, controller):
        """
        Init function of NewGamePage
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.onShowFrame)

        label = tk.Label(self, text="Neues Spiel:", font="Helvetica 12")
        #label.pack(side="top", fill="x", pady=10)
        label.grid(row=0, column=0, columnspan=9)

        self.player1Name = tk.StringVar()
        self.player1Name.set("Player 1")
        labelPlayer1 = tk.Label(self, textvariable=self.player1Name)
        labelPlayer1.grid(row=2, column=0, columnspan=3)

        self.player2Name = tk.StringVar()
        self.player2Name.set("Player 2")
        labelPlayer2 = tk.Label(self, textvariable=self.player2Name)
        labelPlayer2.grid(row=4, column=0, columnspan=3)

        image = Image.open("Kicker_top.jpg")
        photo = ImageTk.PhotoImage(image)

        topview = tk.Label(self, image=photo)
        topview.image = photo # keep a reference!
        topview.grid(row=1, column=3, rowspan=5, columnspan=3)

        self.player3Name = tk.StringVar()
        self.player3Name.set("Player 3")
        labelPlayer3 = tk.Label(self, textvariable=self.player3Name)
        labelPlayer3.grid(row=2, column=6, columnspan=3)

        self.player4Name = tk.StringVar()
        self.player4Name.set("Player 4")
        labelPlayer4 = tk.Label(self, textvariable=self.player4Name)
        labelPlayer4.grid(row=4, column=6, columnspan=3)

        r1minus = tk.Button(self, text="-", command=lambda: decrease(self.result1))
        r1minus.grid(row=7, column=0)

        self.result1 = tk.Entry(self, text="Result Team 1")
        self.result1.grid(row=7, column=1)

        r1plus = tk.Button(self, text="+", command=lambda: increase(self.result1))
        r1plus.grid(row=7, column=2)

        r2minus = tk.Button(self, text="-", command=lambda: decrease(self.result2))
        r2minus.grid(row=7, column=6)

        self.result2 = tk.Entry(self, text="Result Team 2")
        self.result2.grid(row=7, column=7)

        r2plus = tk.Button(self, text="+", command=lambda: increase(self.result2))
        r2plus.grid(row=7, column=8)

        auswerten = tk.Button(self, text="Spiel werten", command=lambda: self.confirm_result(int(self.result1.get()), int(self.result2.get())))
        auswerten.grid(row=8, column=0, columnspan=9)

        def increase(Entry):
            cur = int(Entry.get())
            Entry.delete(0, tk.END)
            Entry.insert(0, str(min(2, cur+1)))

        def decrease(Entry):
            cur = int(Entry.get())
            Entry.delete(0, tk.END)
            Entry.insert(0, str(max(0, cur-1)))

    def confirm_result(self, result1, result2):
        
        self.win = tk.Toplevel()
        self.win.wm_title("Bestätigung")

        question = tk.Label(self.win, text="Soll das Spiel mit folgendem Ergebnis gewertet werden?")
        question.pack(side="top")

        team1 = tk.Label(self.win, text="%s/%s" % (self.game.player1.name, self.game.player2.name))
        team1.pack(side="top")

        result = tk.Label(self.win, text="%d:%d" % (result1, result2))
        result.pack(side="top")

        team2 = tk.Label(self.win, text="%s/%s" % (self.game.player3.name, self.game.player4.name))
        team2.pack(side="top")

        b = tk.Button(self.win, text="Abbrechen", command=self.win.destroy)
        b.pack(side="left")

        auswerten = tk.Button(self.win, text="Werten", command=lambda: self.winner(result1, result2))
        auswerten.pack(side="right")

    def winner(self, result1, result2):
        self.win.destroy()

        if (result1 == 2 or result2 == 2) and (result1 >= 0 and result2 >= 0) and (result1 <= 2 and result2 <= 2) and (result1 != result2):
            if result1 > result2:
                winner_team = 1
            else:
                winner_team = 2
        else:
            print("Ergebnis unplausibel!")
            return
        self.game.scoreTeam1 = result1
        self.game.scoreTeam2 = result2
        print("Team {0} wins!".format(winner_team))
        self.game.save_to_database(winner_team, db)

        self.controller.show_frame("GamePage")

    def onShowFrame(self, event):
        if NewGamePage.game != None:
            self.player1Name.set(NewGamePage.game.player1.name)
            self.player2Name.set(NewGamePage.game.player2.name)
            self.player3Name.set(NewGamePage.game.player3.name)
            self.player4Name.set(NewGamePage.game.player4.name)

        self.result1.delete(0, tk.END)
        self.result1.insert(0, "0")

        self.result2.delete(0, tk.END)
        self.result2.insert(0, "0")

        self.controller.update_idletasks()

class PlayerPage(tk.Frame):
    """
    Class to show a frame, where the ranking is displayed and new players can be added
    """
    def __init__(self, parent, controller):
        """
        Init function of PlayerPage
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg="lightblue")
        self.bind("<<ShowFrame>>", self.onShowFrame)

        label = tk.Label(self, text="Rangliste:", font="Helvetica 12")
        label.pack(side="top", fill="x", pady=10)

        lists = tk.Frame(self)
        lists.pack(side="top", fill="both", expand=True)

        scrollbar = tk.Scrollbar(lists)
        scrollbar.pack(side="right", fill="y")

        self.rankList = ttk.Treeview(lists,
                                     columns=("rank", "player", "mu", "sigma"),
                                     show="headings",
                                     yscrollcommand=scrollbar.set
                                    )

        self.rankList.heading("rank", text="#")
        self.rankList.column("rank", minwidth=50, width=50, anchor="e", stretch=False)

        self.rankList.heading("player", text="Name")
        self.rankList.column("player", minwidth=200, width=100)

        self.rankList.heading("mu", text="Bewertung")
        self.rankList.column("mu", minwidth=100, width=100, anchor="s")

        self.rankList.heading("sigma", text="Standardabweichung")
        self.rankList.column("sigma", minwidth=100, width=100, anchor="s")

        self.rankList.pack(side="left", fill="both", expand=True)

        scrollbar.config(command=self.rankList.yview)

        button = tk.Button(self, text="Neuer Spieler", command=self.popup_bonus)
        button.pack(side="top", fill="x")

    def popup_bonus(self):
        self.win = tk.Toplevel()
        self.win.wm_title("Neuer Spieler")

        self.PopupMsg = tk.StringVar()
        self.PopupMsg.set("Bitte Token an den Scanner halten")
        l = tk.Label(self.win, textvariable=self.PopupMsg)
        l.grid(row=0, column=0)
        self.cancelNewPlayer = False

        self.after(100, self.SkanToken)

        b = tk.Button(self.win, text="Abbrechen", command=self.cancelScan)
        b.grid(row=1, column=0)

    def cancelScan(self):
        self.cancelNewPlayer = True
        self.win.destroy()

    def SkanToken(self):
        if self.cancelNewPlayer:
            return
        self.token = rfidReader.TryGetToken()
        if self.token != None:
            # Check if token is already registered
            if db.get_player(self.token) is None:
                self.NewGamePlayer()
            else:
                self.PopupMsg.set("Token bereits registriert\n"
                                  "Bitte Token an den Scanner halten")
                print("Player already exists! Please scan another token.")
                self.after(100, self.SkanToken)
        else:
            self.after(100, self.SkanToken)

    def NewGamePlayer(self):
        self.win.destroy()
        self.win = tk.Toplevel()
        self.win.wm_title("Neuer Spieler")
        l = tk.Label(self.win, text="Name:")
        l.grid(row=1, column=0)
        self.e2 = tk.Entry(self.win, text="Enter Name")
        self.e2.delete(0, tk.END)
        self.controller.update_idletasks()
        self.e2.grid(row=1, column=1)
        self.e2.focus_set()
        self.e2.bind("<Return>", lambda e: self.Safe2DataBase())
        b = tk.Button(self.win, text="Okay", command=self.Safe2DataBase)
        b.grid(row=2, column=0)

    def Safe2DataBase(self):
        print("Token ID: %s\nName: %s" % (self.token, self.e2.get()))
        db.add_new_player(self.e2.get(), self.token)
        self.win.destroy()
        self.onShowFrame(None)

    def onShowFrame(self, event):
        self.rankList.delete(*self.rankList.get_children())

        rank = db.get_all_players()

        for i, player in enumerate(rank):
            if i%2 == 0:
                self.rankList.insert("", tk.END,
                                     text="{rank}.".format(rank=i),
                                     values=("{rank}.".format(rank=i+1),
                                             player.name,
                                             '{:4.2f}'.format(player.rating.mu),
                                             '{:4.2f}'.format(player.rating.sigma)
                                            ),
                                     tags=("oddrow",)
                                    )
            else:
                self.rankList.insert("", tk.END,
                                     text="{rank}.".format(rank=i),
                                     values=("{rank}.".format(rank=i+1),
                                             player.name,
                                             '{:4.2f}'.format(player.rating.mu),
                                             '{:4.2f}'.format(player.rating.sigma)
                                            ),
                                     tags=("evenrow",)
                                    )
            self.rankList.tag_configure("oddrow", background="lightblue")

class AdminPage(tk.Frame):
    """
    Class to show a frame with an administration interface
    """
    def __init__(self, parent, controller):
        """
        Init function of AdminPage
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the administration interface", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the game page",
                           command=lambda: controller.show_frame("GamePage"))
        button.pack()


if __name__ == "__main__":
    app = KickerApp()
    app.mainloop()
