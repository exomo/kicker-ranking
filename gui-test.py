import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2

class KickerApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

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
            controller.show_frame("NewGamePage")
            # read first token

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
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("GamePage"))
        button.pack()

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