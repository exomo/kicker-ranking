# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 18:55:33 2017

@author: fschoenhut
"""

import sys
import Game

def main(argv):
    
        # example Create Game
    Game1 = Game.Game()
    Game1.build_Team()
    
       # Welches Team hat gewonnen
    Game1.result()
    

      
    
    # example: show Game
    #Game1.show_Game()
    
if __name__ == "__main__":
    main(sys.argv)
