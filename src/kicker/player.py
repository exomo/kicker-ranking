

# -*- coding: utf-8 -*-

import trueskill

class Player():

    def __init__(self):
        # Variables for every Gamer
        self._id = 0
        self._name = u""
        self._tokenID = 0
        self._rating = trueskill.Rating()
        self._is_admin = 0
        self._is_hidden = 0

    def __repr__(self):
        return " -Name: {0}\n -Token ID: {1}\n -Score: mu {2}, sigma {3}\n -Admin: {4}\n -Pensioniert: {5}\n".format(self.name, self.tokenID, self.rating.mu, self.rating.sigma, self.is_admin, self.is_hidden)

    # setter-, getter-methods
    # -------------------------------------------------------------------------------------------------------------------------------------
    def set_id(self, id):
        self._id = id

    def get_id(self):
        return self._id

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

    def set_is_admin(self, is_admin):
        self._is_admin = is_admin

    def get_is_admin(self):
        return self._is_admin

    def set_is_hidden(self, is_hidden):
        self._is_hidden = is_hidden

    def get_is_hidden(self):
        return self._is_hidden

    # -------------------------------------------------------------------------------------------------------------------------------------
    # properties
    # -------------------------------------------------------------------------------------------------------------------------------------
    id = property(get_id, set_id)
    name = property(get_name, set_name)
    tokenID = property(get_tokenID, set_tokenID)
    rating = property(get_rating, set_rating)
    is_admin = property(get_is_admin, set_is_admin)
    is_hidden = property(get_is_hidden, set_is_hidden)
    # -------------------------------------------------------------------------------------------------------------------------------------

    def show_player(self):
        print(self)
        print()

    def reset_rating(self):
        self._rating = trueskill.Rating()
