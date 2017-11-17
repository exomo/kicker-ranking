

# -*- coding: utf-8 -*-


class Player():

    def __init__(self):
        # Variables for every Gamer
        self._name = u""
        self._tokenID = 0
        self._gamerScore = 0.0
        self._standardDeviation = 0.0
        
    # setter-, getter-methodes 
    # -------------------------------------------------------------------------------------------------------------------------------------
    def set_name(self, name):
        self._name = name
    
    def get_name(self):
        return self._name
    
    def set_tokenID(self, token):
        self._tokenID = token
    
    def get_tokenID(self):
        return self._tokenID
    
    def set_gamerScore(self, score):
        self._gamerScore = score
        
    def get_gamerScore(self):
        return self._gamerScore
        
    def set_standardDeviation(self, deviation):
        self._standardDeviation = deviation
    
    def get_standardDeviation(self):
        return self._standardDeviation
    
    
    
    # -------------------------------------------------------------------------------------------------------------------------------------
    
    # properties
    # -------------------------------------------------------------------------------------------------------------------------------------
    name = property(get_name, set_name)
    tokenID = property(get_tokenID, set_tokenID)
    gamerScore = property(get_gamerScore, set_gamerScore)
    standardDeviation = property(get_standardDeviation, set_standardDeviation)
    # -------------------------------------------------------------------------------------------------------------------------------------
    
    def show_player(self):
        print("name:", self.name)                       # print("name:", get_name())
        print("Token ID:", self.tokenID)
        print("Gamer Score:", self.gamerScore)
        print("Standard Deviation:", self.standardDeviation)
        print()