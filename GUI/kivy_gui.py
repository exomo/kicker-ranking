""" 
Main program for the kivy based kicker ranking gui.
"""

import time
import sys

import trueskill
from trueskill import Rating

import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.app import Builder
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.scrollview import ScrollView

from database import database
from hardware import rfid
from kicker import Game

# global setup of database and rfid reader
kickerDB = "kicker_scores.db"
db = database.Database(kickerDB)

rfidReader = rfid.rfid()

# Parameters for the trueskill ranking

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

class KickerWidget(TabbedPanel):
    """Main widget of GUI, specifies basic layout."""

    def __init__(self, **kwargs):
        super(KickerWidget, self).__init__(**kwargs)

class PlayerPage(BoxLayout):
    pass

class RankingList(GridLayout):

    def __init__(self, **kwargs):
        super(RankingList, self).__init__(**kwargs)
        for i in range(30):
            self.add_widget(RankingListItem(text="Spieler"))

    def refresh(self):
        pass

class RankingListItem(Label):
    pass
        
class GamePage(BoxLayout):
    pass

class KickerApp(App):
    """
    Main class of GUI, specifies basic layout.
    """
    def build(self):
        # Builder.load_file("GUI/KickerApp.kv", encoding='utf8')
        # with open("GUI/KickerApp.kv", encoding='utf8') as f:
        #     Builder.load_string(f.read())
        self.title = "~ ITK Kicker Rangliste ~"
        return KickerWidget()

if __name__ == "__main__":
    KickerApp().run()
