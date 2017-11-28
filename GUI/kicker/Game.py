# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 17:53:19 2017

@author: fschoenhut
"""
from datetime import datetime
import trueskill

class Game():

    def __init__(self):
        # Variables for every Game
        self._scoreTeam1 = 0 # 0 bis 2
        self._scoreTeam2 = 0 # 0 bis 2
        self._player1 = u""
        self._player2 = u""
        self._player3 = u""
        self._player4 = u""
        self._time = 0

    # methods
    # -------------------------------------------------------------------------------------------------------------------------------------
    #
    def set_scoreTeam1(self, scoreTeam1):
        self._scoreTeam1 = scoreTeam1

    def get_scoreTeam1(self):
        return self._scoreTeam1

    def set_scoreTeam2(self, scoreTeam2):
        self._scoreTeam2 = scoreTeam2

    def get_scoreTeam2(self):
        return self._scoreTeam2

    def set_player1(self, player1):
        self._player1 = player1

    def get_player1(self):
        return self._player1

    def set_player2(self, player2):
        self._player2 = player2

    def get_player2(self):
        return self._player2

    def set_player3(self, player3):
        self._player3 = player3

    def get_player3(self):
        return self._player3

    def set_player4(self, player4):
        self._player4 = player4

    def get_player4(self):
        return self._player4

    def set_time(self, time=None):
        if time:
            self._time = time
        else:
            self._time = datetime.now()

    def get_time(self):
        return self._time

    # properties
    # ----------------------------------------------------------------------------------------------------------------------------

    scoreTeam1 = property(get_scoreTeam1, set_scoreTeam1)# 0 bis 2
    scoreTeam2 = property(get_scoreTeam2, set_scoreTeam2)

    player1 = property(get_player1, set_player1)
    player2 = property(get_player2, set_player2)
    player3 = property(get_player3, set_player3)
    player4 = property(get_player4, set_player4)

    time = property(get_time, set_time)

    def save_to_database(self, winner_team, db):
        db.add_game(self)

        # Ratings der einzelnen Spieler laden (mu und sigma können auch explizit übergeben werden)
        ratings = [player.rating for player in [self.player1, self.player2, self.player3, self.player4]]

        print("Initial player ratings:")
        for rating in ratings:
            print(rating)

        # Teams zuweisen
        # TODO: Teams variabel machen
        team1 = ratings[0:2]
        team2 = ratings[2:4]

        print('{:.1%} chance to draw'.format(trueskill.quality([team1, team2])))
        if trueskill.quality([team1, team2]) < 0.50:
            print('This match seems to be not so fair')

        # neue Bewertungen anhand des Ergebnisses berechnen
        if winner_team == 1:
            (self.player1.rating, self.player2.rating), (self.player3.rating, self.player4.rating) = trueskill.rate([team1, team2], ranks=[0, 1]) # Team1 wins (rank lower)
        elif winner_team == 2:
            (self.player1.rating, self.player2.rating), (self.player3.rating, self.player4.rating) = trueskill.rate([team1, team2], ranks=[1, 0]) # Team2 wins (rank lower)

        # save updated skills to database
        for player in [self.player1, self.player2, self.player3, self.player4]:
            db.update_player_skill(player)
 