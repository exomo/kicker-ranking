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
from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from database import database
from hardware import rfid
from kicker import Game

# global setup of database and rfid reader
kickerDB = "kicker_scores.db"
db = database.Database(kickerDB)
db.show_players()

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
    ranking_list = ObjectProperty()

    def new_player(self):
        """show popup to create new player"""
        popup = NewPlayerPopup(ranking_list=self.ranking_list)
        popup.open()
        print("Show the 'New Player' popup")
        self.ranking_list.refresh()

class RankingList(RecycleView):
    def __init__(self, **kwargs):
        super(RankingList, self).__init__(**kwargs)
        self.refresh()

    def refresh(self):
        rank = db.get_all_players()
        self.data = [
            {
                'name' : player.name,
                'rank' : i+1,
                'score' : player.rating.mu,
                'sigma' : player.rating.sigma
            }
            for i, player in enumerate(rank)]

class NewPlayerPopup(Popup):
    enable_ok = BooleanProperty()
    player_name = ObjectProperty()
    token_id = StringProperty()

    def __init__(self, ranking_list, **kwargs):
        super(NewPlayerPopup, self).__init__(**kwargs)
        self.ranking_list = ranking_list
        self.timer = Clock.schedule_interval(self.on_interval, 0.5)

    def on_interval(self, time_elapsed):
        token = rfidReader.TryGetToken()
        if token:
            #TODO: check if token is already registered, show validation error
            self.token_id = token
            self.timer.cancel()

    def on_ok(self):
        db.add_new_player(self.player_name.text, self.token_id)
        self.ranking_list.refresh()
        self.dismiss()

    def validate_input(self):
        #TODO: Check that name is unique, show validation error
        self.enable_ok = self.player_name.text and self.token_id

    def focus_name_input(self, t):
        self.player_name.focus = True
        print(t)

    # def on_focus(self, sender, value):
    #     """Workaround for text_validate_unfocus property. When losing focus set focus back"""
    #     if not value:
    #         sender.focus = True

    def on_dismiss(self):
        self.timer.cancel()

class GamePage(BoxLayout):

    def new_game(self, text):
        print(text)

class KickerApp(App):
    """
    Main class of GUI, specifies basic layout.
    """
    def build(self):
        # Builder.load_file("GUI/KickerApp.kv", encoding='utf8')
        # with open("GUI/KickerApp.kv", encoding='utf8') as f:
        #     Builder.load_string(f.read())
        self.title = "~ ITK Kicker Rangliste ~"
        self.tab_widget = KickerWidget()
        return self.tab_widget

    def switch_tab(self, tab):
        self.tab_widget.switch_to(self.tab_widget.tab_list[tab])
        for t in self.tab_widget.tab_list:
            print(t.content)

if __name__ == "__main__":
    KickerApp().run()
