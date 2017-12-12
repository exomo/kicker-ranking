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
    hint_new_player = StringProperty()
    display_image = StringProperty('empty.png')

    def __init__(self, ranking_list, **kwargs):
        super(NewPlayerPopup, self).__init__(**kwargs)
        self.ranking_list = ranking_list
        self.timer = Clock.schedule_interval(self.on_interval, 0.5)
        self.hint_new_player = 'Bitte Token einlesen'

    def on_interval(self, time_elapsed):
        token = rfidReader.TryGetToken()
        if token:
            # Check if token is already registered
            if db.get_player(token) is None:
                self.display_image = 'check.png'
                self.hint_new_player = 'Token erfolgreich gelesen.\nBitte Namen eingeben\nund bestätigen.'
                self.token_id = token
                self.timer.cancel()
            else:
                self.display_image = 'error.png'
                self.hint_new_player = 'Spieler existiert bereits.\nBitte anderes Token scannen\noder abbrechen.'
                print("Player already exists! Please scan another token.")     

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
    game_list = ObjectProperty()

    def new_game(self, text):
        """show popup to add new game"""
        popup = NewGamePopup(self.game_list)
        popup.open()
        print("Show the 'New Game' popup")
        self.game_list.refresh()

class GameList(RecycleView):
    def __init__(self, **kwargs):
        super(GameList, self).__init__(**kwargs)
        self.refresh()

    def refresh(self):
        games = db.get_games(20)
        self.data = [
            {
                'game_id' : game.id,
                'player1' : game.player1.name,
                'player2' : game.player2.name,
                'player3' : game.player3.name,
                'player4' : game.player4.name,
                'score1'  : game.scoreTeam1,
                'score2'  : game.scoreTeam2,
                'oddline': i % 2 == 0
            }
            for i, game in enumerate(games)]

class NewGamePopup(Popup):
    """Popup to enter a new game"""
    team1 = ObjectProperty() 
    team2 = ObjectProperty() 

    def __init__(self, game_list, **kwargs):
        super(NewGamePopup, self).__init__(**kwargs)
        self.game_list = game_list
        self.players = []
        #self.timer = Clock.schedule_interval(self.on_interval, 0.1)
        #self.team1.player1 = 'Spieler 1\n[b]Bitte Token einlesen[/b]'

    def on_interval(self, time_elapsed):
        token = rfidReader.TryGetToken()
        if token is not None:
            player = db.get_player(token)
            if player is not None and not player.tokenID in [p.tokenID for p in self.players]:
                self.players.append(player)
                player_number = len(self.players)
                if player_number == 1:
                    self.team1.player1 = player.name
                    self.team1.player2 = 'Spieler 2\n[b]Bitte Token einlesen[/b]'
                elif player_number == 2:
                    self.team1.player2 = player.name
                    self.team2.player1 = 'Spieler 3\n[b]Bitte Token einlesen[/b]'
                elif player_number == 3:
                    self.team2.player1 = player.name
                    self.team2.player2 = 'Spieler 4\n[b]Bitte Token einlesen[/b]'
                elif player_number == 4:
                    self.team2.player2 = player.name
                    self.timer.cancel()

    def on_ok(self):
        print('{:d} : {:d}'.format(self.team1.score, self.team2.score))

    def on_dismiss(self):
        self.timer.cancel()

class KickerApp(App):
    """
    Main class of GUI, specifies basic layout.
    """
    def build(self):
        # Builder.load_file("GUI/KickerApp.kv", encoding='utf8')
        with open("GUI/KickerUi.kv", encoding='utf8') as f:
            Builder.load_string(f.read())
        self.title = "~ ITK Kicker Rangliste ~"
        self.tab_widget = KickerWidget()
        return self.tab_widget

    def switch_tab(self, tab):
        self.tab_widget.switch_to(self.tab_widget.tab_list[tab])
        for t in self.tab_widget.tab_list:
            print(t.content)

if __name__ == "__main__":
    KickerApp().run()
