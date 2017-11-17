# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 17:53:19 2017

@author: fschoenhut
"""
import player

class Game():

    def __init__(self):
        # Variables for every Game
        self._satz = 0 # Wert zwischen 0 und 2 für jeden gewonnenen Satz
        self._sieg = 0 # Wert 1 oder 2 für das Gewinner Team

    # methodes 
    # -------------------------------------------------------------------------------------------------------------------------------------
            
    # create 4 Players
    def build_Team(self):
        print("Team wird erstellt")

        p1 = player.Player()
        p2 = player.Player()
        p3 = player.Player()
        p4 = player.Player()
                
        p1.show_player()
        p2.show_player()
        p3.show_player()
        p4.show_player()
        
    def result(self):
        print("Der Gewinner ist Team")
        
        

  #p1.name = "Dieter", p1.tokenID = 12345, p1.gamerScore = 2.5,   p1.standardDeviation = 0.4
    
  
  
  
 