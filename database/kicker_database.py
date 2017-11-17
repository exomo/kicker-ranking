import sqlite3

class KickerDb:
    def __init__(self, filename):
        self.database = sqlite3.connect(filename)

    def __del__(self):
        self.database.close()

    def create_database(self):
        self.database.execute("CREATE TABLE IF NOT EXISTS players (name TEXT PRIMARY KEY, token_id TEXT, skill_mu REAL, skill_sigma REAL)")
        self.database.commit()
        print("Created database")

    def add_new_player(self, name, token_id):
        self.database.execute("INSERT INTO players VALUES(?, ?, 25, 3)", (name, token_id))
        self.database.commit()
        print("Added new player: " + name)

    def get_player(self, id):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM players WHERE token_id=?", [id])
        result = cur.fetchone()
        if result != None:
            return Player(result[0], result[1], result[2], result[3])
        else:
            return None

    def get_all_players(self):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM players")
        return cur.fetchall().apply(lambda p: Player(result[0], result[1], result[2], result[3]))

    def show_players(self):
        print("List of all players")
        print("="*30)
        cur = self.database.cursor()
        cur.execute("SELECT * FROM players")
        for player in cur.fetchall():
            print(player)


def main():
    player_db = KickerDb("kicker_scores.db")
    # player_db.add_new_player('thomas', "0815")

    player_db.show_players()

    p1 = player_db.get_player("0815")
    p2 = player_db.get_player("0817")

    if(p1):
        p1.show_player()
    if(p2):
        p2.show_player()

main()
