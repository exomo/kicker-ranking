

# -*- coding: utf-8 -*-

import trueskill

class Player():

    def __init__(self):
        # Variables for every Gamer
        self._name = u""
        self._tokenID = 0
        self._rating = trueskill.Rating()

    def __repr__(self):
        return "Player\n -Name: {0}\n -Token ID: {1}\n -Score: mu {2}, sigma {3}".format(self.name, self.tokenID, self.rating.mu, self.rating.sigma)

    # setter-, getter-methods
    # -------------------------------------------------------------------------------------------------------------------------------------
    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_tokenID(self, token):
        self._tokenID = token

    def get_tokenID(self):
        return self._tokenID

    def set_rating(self, rating):
        self._rating = rating

    def get_rating(self):
        return self._rating

    # -------------------------------------------------------------------------------------------------------------------------------------
    # properties
    # -------------------------------------------------------------------------------------------------------------------------------------
    name = property(get_name, set_name)
    tokenID = property(get_tokenID, set_tokenID)
    rating = property(get_rating, set_rating)
    # -------------------------------------------------------------------------------------------------------------------------------------

    def show_player(self):
        print(self)
        print()

    def reset_rating(self):
        self._rating = trueskill.Rating()
