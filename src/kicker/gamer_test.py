

# -*- coding: utf-8 -*-


import sys
import player

# just for testing
def main(argv):
    # example: create p1
    p1 = player.Player()
    p1.name = "Dieter"
    p1.tokenID = 12345
    p1.gamerScore = 2.5
    p1.standardDeviation = 0.4
    
    # example: create p2
    p2 = player.Player()
    p2.name = "Achim"           # p2.set_name("Achim")
    p2.tokenID = 999999
    p2.gamerScore = 8.5
    p2.standardDeviation = 2.5    
    
    # example: show player
    p1.show_player()
    p2.show_player()
    
if __name__ == "__main__":
    main(sys.argv)