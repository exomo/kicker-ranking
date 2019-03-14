import sys
import sqlite3
from database import database

def main(argv):
    # Open the database file (creates if it doesn't exist)
    player_db = database.Database("kicker_scores.db")
    
    # Initialize database tables, does nothing if it already exists
    player_db.create_database()

    # Add a new player to the database, specify name and token id, score is set to a default
    # Throws an exception if the player already exists in the database.
    try:
        player_db.add_new_player('dilbert', "42424242424242")
    except sqlite3.IntegrityError as ex:
        print("Could not create player: %s" % ex) 
    try:
        player_db.add_new_player('donglebert', "133708154711")
    except sqlite3.IntegrityError as ex:
        print("Could not create player: %s" % ex) 
        
    # Show a list of all players in the database
    player_db.show_players()

    # Get a player with a specific token id or None if not in the database
    # p1 = player_db.get_player("133708154711")
    p1 = player_db.get_player("42424242424242")
    if(p1 == None):
        print("Player 1 not found")
    else:
        p1.show_player()

    p2 = player_db.get_player("123456")
    if(p2 == None):
        print("Player 2 not found")
    else:
        p2.show_player()

    # Store a new skill value for a player
    p1.gamerScore += 0.2
    p1.standardDeviation -= 0.1
    player_db.update_player_skill(p1)

    # Get all players ordered by skill
    rank_list = player_db.get_all_players()
    place = 1
    for p in rank_list:
        print("%3d. %-20s %f" % (place, p.name, p.gamerScore))
        place += 1

if __name__ == "__main__":
    main(sys.argv)