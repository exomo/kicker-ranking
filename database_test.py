import sys
import donglebert

def main(argv):
    player_db = donglebert.Database("kicker_scores.db")
    player_db.create_database()
    # player_db.add_new_player('thomas', "0815")

    player_db.show_players()

    p1 = player_db.get_player("9876")
    p2 = player_db.get_player("123456")

    if(p1):
        p1.show_player()
    if(p2):
        p2.show_player()

if __name__ == "__main__":
    main(sys.argv)