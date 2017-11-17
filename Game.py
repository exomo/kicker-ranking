# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 17:53:19 2017

@author: fschoenhut
"""
import player

class Game():

    def __init__(self):
        # Variables for every Game
        self._scoreTeam1 = 0 # 0 bis 2
        self._scoreTeam2 = 0 # 0 bis 2
        self._player1 = u""
        self._player2 = u""
        self._player3 = u""
        self._player4 = u""
    
    # methodes 
    # -------------------------------------------------------------------------------------------------------------------------------------
        
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
   
    # properties
    # ----------------------------------------------------------------------------------------------------------------------------      
    
    scoreTeam1 = property(get_scoreTeam1, set_scoreTeam1)# 0 bis 2
    scoreTeam2 = property(get_scoreTeam2, set_scoreTeam2)
    
    player1 = property(get_player1, set_player1)
    player2 = property(get_player2, set_player2)
    player3 = property(get_player3, set_player3)
    player4 = property(get_player4, set_player4)
    
  
  
  
 