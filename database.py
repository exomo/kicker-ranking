
import sqlite3
import player

class Database():
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
            return self.create_player(result)
        else:
            return None

    def get_all_players(self):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM players ORDER BY skill_mu DESC, skill_sigma ASC")
        return [self.create_player(p) for p in cur.fetchall()]

    def show_players(self):
        print("List of all players")
        print("="*30)
        cur = self.database.cursor()
        cur.execute("SELECT * FROM players")
        for player in cur.fetchall():
            print(player)
        print("="*30+"\n")

    def update_player_skill(self, p):
        self.database.execute("UPDATE players SET skill_mu=?, skill_sigma=? WHERE token_id=?", (p.gamerScore, p.standardDeviation, p.tokenID))
        self.database.commit()

    def create_player(self, db_result):
        p = player.Player()
        p.name = db_result[0]
        p.tokenID = db_result[1]
        p.gamerScore = db_result[2]
        p.standardDeviation = db_result[3]
        return p
