

# -*- coding: utf-8 -*-

import trueskill

class Player():

    def __init__(self):
        # Variables for every Gamer
        self._id = 0
        self._name = u""
        self._tokenID = 0
        self._rating = trueskill.Rating()
        self._isAdmin = 0
        self._isHidden = 0

    def __repr__(self):
        return "Player\n -Name: {0}\n -Token ID: {1}\n -Score: mu {2}, sigma {3}\n -Admin: {4}\n -Pensioniert: {5}\n".format(self.name, self.tokenID, self.rating.mu, self.rating.sigma, self.isAdmin, self.isHidden)

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

    def set_isAdmin(self, isAdmin):
        self._isAdmin = isAdmin

    def get_isAdmin(self):
        return self._isAdmin

    def set_isHidden(self, isHidden):
        self._isHidden = isHidden

    def get_isHidden(self):
        return self._isHidden

    # -------------------------------------------------------------------------------------------------------------------------------------
    # properties
    # -------------------------------------------------------------------------------------------------------------------------------------
    id = property(get_id, set_id)
    name = property(get_name, set_name)
    tokenID = property(get_tokenID, set_tokenID)
    rating = property(get_rating, set_rating)
    isAdmin = property(get_isAdmin, set_isAdmin)
    isHidden = property(get_isHidden, set_isHidden)
    # -------------------------------------------------------------------------------------------------------------------------------------

    def show_player(self):
        print(self)
        print()

    def reset_rating(self):
        self._rating = trueskill.Rating()
