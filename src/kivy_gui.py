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
        rank = db.get_active_players()
        self.data = [
            {
                'name' : player.name,
                'rank' : i+1,
                'score' : player.rating.mu,
                'sigma' : player.rating.sigma
            }
            for i, player in enumerate(rank)]

class AdminList(RecycleView):
    def __init__(self, **kwargs):
        super(AdminList, self).__init__(**kwargs)
        self.refresh()

    def refresh(self):
        rank = db.get_admin_players()
        self.data = [
            {
                'name' : player.name,
                'rank' : i+1,
            }
            for i, player in enumerate(rank)]

class NewPlayerPopup(Popup):
    enable_ok = BooleanProperty()
    player_name = ObjectProperty()
    token_id = StringProperty()
    scan_token_label_text = StringProperty()
    scan_token_label_error_text = StringProperty()
    scan_token_label_success_text = StringProperty()
    display_image = StringProperty('gui/empty.png')

    def __init__(self, ranking_list, **kwargs):
        super(NewPlayerPopup, self).__init__(**kwargs)
        self.ranking_list = ranking_list
        self.timer = Clock.schedule_interval(self.on_interval, 0.1)

    def on_interval(self, time_elapsed):
        token = rfidReader.TryGetToken()
        if token:
            # Check if token is already registered
            if db.get_player_by_token(token) is None:
                self.display_image = 'gui/check.png'
                self.scan_token_label_text = self.scan_token_label_success_text
                self.token_id = token
                self.timer.cancel() 
                self.player_name.disabled = False
                self.player_name.focus = True
                self.validate_input()
            else:
                self.display_image = 'gui/error.png'
                self.scan_token_label_text = self.scan_token_label_error_text
                print("Player already exists! Please scan another token.")     

    def on_ok(self):
        db.add_new_player(self.player_name.text, self.token_id, 0, 0)
        self.ranking_list.refresh()
        self.dismiss()

    def validate_input(self):
        if self.player_name.text:
            player = db.get_player_by_name(self.player_name.text)
            if player is None:
                self.enable_ok = bool(self.token_id)
                self.scan_token_label_text = self.scan_token_label_success_text
            else:
                # todo: Show an error message if gthe player name is already used by someone else
                self.scan_token_label_text = self.name_error_text
                self.enable_ok = False
        else:
            self.enable_ok = False

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
    player_list = ObjectProperty()

    def new_game(self, text):
        """show popup to add new game"""
        popup = NewGamePopup(self.game_list, self.player_list)
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

    def __init__(self, game_list, player_list, **kwargs):
        super(NewGamePopup, self).__init__(**kwargs)
        self.game_list = game_list
        self.player_list = player_list
        self.players = []
        self.timer = Clock.schedule_interval(self.on_interval, 0.1)
        self.team1.player1 = 'Spieler 1\n[b]Bitte Token einlesen[/b]'

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
                    self.enable_ok = True
                    self.timer.cancel()

    def on_ok(self):
        result1 = self.team1.score
        result2 = self.team2.score
        if (result1 == 2 or result2 == 2) and \
            (result1 >= 0 and result2 >= 0) and \
            (result1 <= 2 and result2 <= 2) and \
            (result1 != result2):

            popup = ConfirmNewGamePopup(
                team1_score=result1, 
                team2_score=result2,
                player1=self.team1.player1,
                player2=self.team1.player2,
                player3=self.team2.player1,
                player4=self.team2.player2)
            popup.bind(on_confirm=self.on_confirm)
            popup.open()
            print('{:d} : {:d}'.format(self.team1.score, self.team2.score))
        else:
            popup = GameUnplausiblePopup()
            popup.open()

    def on_dismiss(self):
        self.timer.cancel()
    
    def on_confirm(self, sender):
        """bound to the on_confirm event of the confirmation dialog,
           stores the game into the database"""
        if self.team1.score > self.team2.score:
            winner_team = 1
        else:
            winner_team = 2
        game = Game.Game()
        game.player1 = self.players[0]
        game.player2 = self.players[1]
        game.player3 = self.players[2]
        game.player4 = self.players[3]
        game.scoreTeam1 = self.team1.score
        game.scoreTeam2 = self.team2.score
        print("Team {0} wins!".format(winner_team))
        game.save_to_database(winner_team, db)

        self.game_list.refresh()
        self.player_list.refresh()
        self.dismiss()

class ConfirmNewGamePopup(Popup):
    team1_score = NumericProperty(0)
    team2_score = NumericProperty(0)
    player1 = StringProperty()
    player2 = StringProperty()
    player3 = StringProperty()
    player4 = StringProperty()

    def __init__(self, **kwargs):
        self.register_event_type('on_confirm')
        super(ConfirmNewGamePopup, self).__init__(**kwargs)

    def confirm(self):
        """Dispatch the on_confirm event"""
        self.dispatch('on_confirm')
        self.dismiss()

    def on_confirm(self, *args):
        """Default event handler is required but does nothing"""
        pass

class GameUnplausiblePopup(Popup):
    pass

class AdminPage(BoxLayout):
    player_list = ObjectProperty()
    admin_list = ObjectProperty()

    def hide_player(self):
        """show popup to hide a player"""
        popup = HidePlayerPopup(player_list=self.player_list)
        popup.open()
        self.player_list.refresh()

    def admin_player(self):
        """show popup to set a player as an admin"""
        popup = AdminPlayerPopup(admin_list=self.admin_list)
        popup.open()
        self.admin_list.refresh()

class HidePlayerPopup(Popup):
    enable_ok = BooleanProperty()
    player_name = ObjectProperty()
    scan_token_label_text = StringProperty()
    scan_token_label_error_text = StringProperty()
    scan_token_label_success_text = StringProperty()
    display_image = StringProperty('gui/empty.png')

    def __init__(self, player_list, **kwargs):
        super(HidePlayerPopup, self).__init__(**kwargs)
        self.player_list = player_list
        self.timer = Clock.schedule_interval(self.on_interval, 0.1)

    def on_interval(self, time_elapsed):
        token = rfidReader.getAdminToken()
        if token is not None:
            if db.is_admin(token):
                #print("You are an admin.")
                self.display_image = 'gui/check.png'
                self.scan_token_label_text = self.scan_token_label_success_text
                self.timer.cancel()
                self.player_name.disabled = False
                self.player_name.focus = True
                self.validate_input()
            else:
                self.scan_token_label_text = self.scan_token_label_error_text
                #print("You are not an admin!")

    def on_ok(self):
        db.retire_player(db.get_player_by_name(self.player_name.text))
        self.player_list.refresh()
        self.dismiss()

    def on_dismiss(self):
        self.timer.cancel()

    def validate_input(self):
        #print(self.player_name.text)
        if self.player_name.text:
            player = db.get_player_by_name(self.player_name.text)
            if player is None:
                self.enable_ok = False
            else:
                self.enable_ok = True
        else:
            self.enable_ok = False

class AdminPlayerPopup(Popup):
    enable_ok = BooleanProperty()
    player_name = ObjectProperty()
    scan_token_label_text = StringProperty()
    scan_token_label_error_text = StringProperty()
    scan_token_label_success_text = StringProperty()
    display_image = StringProperty('gui/empty.png')

    def __init__(self, admin_list, **kwargs):
        super(AdminPlayerPopup, self).__init__(**kwargs)
        self.admin_list = admin_list
        self.timer = Clock.schedule_interval(self.on_interval, 0.1)

    def on_interval(self, time_elapsed):
        token = rfidReader.getAdminToken()
        if token is not None:
            if db.is_admin(token):
                #print("You are an admin.")
                self.display_image = 'gui/check.png'
                self.scan_token_label_text = self.scan_token_label_success_text
                self.timer.cancel()
                self.player_name.disabled = False
                self.player_name.focus = True
                self.validate_input()
            else:
                self.scan_token_label_text = self.scan_token_label_error_text
                #print("You are not an admin!")

    def on_ok(self):
        db.set_as_admin(db.get_player_by_name(self.player_name.text))
        self.admin_list.refresh()
        self.dismiss()

    def on_dismiss(self):
        self.timer.cancel()

    def validate_input(self):
        #print(self.player_name.text)
        if self.player_name.text:
            player = db.get_player_by_name(self.player_name.text)
            if player is None:
                self.enable_ok = False
            else:
                self.enable_ok = True
        else:
            self.enable_ok = False


class KickerApp(App):
    """
    Main class of GUI, specifies basic layout.
    """
    def build(self):
        # workaround for some issues with auto loading the kv file
        # - on windows, the file is read with wrong encoding, this is solved by loading the file
        #   explicitly and passing the correctly read file contents to the builder instead of 
        #   relying on the automatic loading of kv files
        # - on linux the kv file is only auto-loaded if it is in the current directory, which would
        #   be the directory above GUI, but we want the kv to be inside GUI
        # - in windows the automatic load would also happen from inside GUI if the kv file name was
        #   like the App (Kicker.kv), the file must have a different name to prevent the auto load
        with open("src/gui/KickerUi.kv", encoding='utf8') as kvFile:
            Builder.load_string(kvFile.read())
        self.title = "~ ITK Kicker Rangliste ~"
        self.tab_widget = KickerWidget()
        return self.tab_widget

    def switch_tab(self, tab):
        self.tab_widget.switch_to(self.tab_widget.tab_list[tab])
        for t in self.tab_widget.tab_list:
            print(t.content)

if __name__ == "__main__":
    if 'mpmath' in trueskill.backends.available_backends():
        # mpmath can be used in the current environment
        backend = 'mpmath'
    else:
        backend = None
    trueskill.setup(mu=MU, sigma=SIGMA, beta=BETA, tau=TAU, draw_probability=DRAW_PROBABILITY, backend=backend) # Es gibt kein Unentschieden
    KickerApp().run()
