
import sqlite3
from kicker import player
from kicker.game import Game
from kicker.player import Player
import trueskill
import os.path

class Database():
    def get_current_version(self):
        """Returns current database version supported by this file"""
        return 1

    def __init__(self, filename):

        if not os.path.isfile(filename):
            # if the database does not exist it is created
            self.database = sqlite3.connect(filename)
            self.create_database()
        else:
            self.database = sqlite3.connect(filename)

        if self.get_version() != self.get_current_version():
            raise Exception("The version of the database file is not supported. Upgrade the database before starting.")
        # self.database = sqlite3.connect(filename)

    def __del__(self):
        self.database.close()

    def get_version(self):
        """Read the version from the database"""
        version = 0
        cur = self.database.cursor()
        try:
            cur.execute("SELECT version FROM version_info")
            v = cur.fetchone()
            if None == v:
                version = 0
            else:
                version = v[0]
        except sqlite3.OperationalError:
            version = 0
        return version

    def create_database(self):
        self.database.execute("CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, token_id TEXT UNIQUE, skill_mu REAL, skill_sigma REAL, is_admin BIT, is_hidden BIT)")
        self.database.execute("CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, player1_id INTEGER, player2_id INTEGER, player3_id INTEGER, player4_id INTEGER, team1_score INTEGER, team2_score INTEGER)")
        self.database.execute("CREATE TABLE IF NOT EXISTS version_info (version INTEGER PRIMARY KEY)")
        self.database.execute("INSERT INTO version_info (version) VALUES (?)", (self.get_current_version(),))
        self.database.commit()
        print("Created database")

    def add_new_player(self, name, token_id, is_admin, is_hidden):
        self.database.execute("INSERT INTO players (name, token_id, skill_mu, skill_sigma, is_admin, is_hidden) VALUES(?, ?, ?, ?, ?, ?)", (name, token_id, trueskill.Rating().mu, trueskill.Rating().sigma, is_admin, is_hidden))
        self.database.commit()
        print("Added new player: " + name)

    def get_player(self, player_id):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM players WHERE id=?", [player_id])
        result = cur.fetchone()
        if result != None:
            return self.create_player(result)
        else:
            return None

    def get_player_by_name(self, name):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM players WHERE name=?", [name])
        result = cur.fetchone()
        if result != None:
            return self.create_player(result)
        else:
            return None

    def get_player_by_token(self, token_id):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM players WHERE token_id=?", [token_id])
        result = cur.fetchone()
        if result != None:
            return self.create_player(result)
        else:
            return None

    def is_admin(self, token_id):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM players WHERE token_id=? AND is_admin=?", (token_id, 1))
        result = cur.fetchone()
        if result != None:
            return True
        else:
            return False

    def set_as_admin(self, p):
        """tags a player as an admin"""
        self.database.execute("UPDATE players SET is_admin=? WHERE id=?", (1, p.id))
        self.database.commit()

    def get_all_players(self):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM players ORDER BY skill_mu DESC, skill_sigma ASC")
        return [self.create_player(p) for p in cur.fetchall()]

    def get_active_players(self):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM players WHERE is_hidden=0 ORDER BY skill_mu DESC, skill_sigma ASC")
        return [self.create_player(p) for p in cur.fetchall()]

    def get_admin_players(self):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM players WHERE is_admin=1 ORDER BY skill_mu DESC, skill_sigma ASC")
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
        print("Update player:\n{0}".format(p))
        self.database.execute("UPDATE players SET skill_mu=?, skill_sigma=? WHERE id=?", (p.rating.mu, p.rating.sigma, p.id))
        self.database.commit()

    def create_player(self, db_result):
        p = Player()
        p.id = db_result[0]
        p.name = db_result[1]
        p.tokenID = db_result[2]
        p.rating = trueskill.Rating(mu=db_result[3], sigma=db_result[4])
        p.is_admin = db_result[5]
        p.is_hidden = db_result[6]
        return p

    def retire_player(self, p):
        """Players should be rather updated by status and later removed from the database based on their token and is_hidden value"""
        print("Retire player:\n{0}".format(p))
        self.database.execute("UPDATE players SET is_hidden=?, token_id=?, is_admin=? WHERE id=?", (1, None, 0, p.id))
        self.database.commit()

    def remove_retired_players(self, p):
        """Remove players with token_id=0 and is_hidden=1"""
        pass

    def add_game(self, game):
        """Add a game to the games list"""
        cur = self.database.cursor()
        insert_statement = "INSERT INTO games (player1_id, player2_id, player3_id, player4_id, team1_score, team2_score) VALUES (?,?,?,?,?,?)"
        cur.execute(insert_statement, (
            game.player1.id,
            game.player2.id,
            game.player3.id,
            game.player4.id,
            game.scoreTeam1,
            game.scoreTeam2))
        self.database.commit()

    def update_game(self, game):
        print("Update game:\n {0}".format(game))
        self.database.execute("UPDATE games SET player1_id=?, player2_id=?, player3_id=?, player4_id=?, team1_score=?, team2_score=? WHERE id=?", (game.player1.id, game.player2.id, game.player3.id, game.player4.id, game.scoreTeam1, game.scoreTeam2, game.id))
        self.database.commit()

    def get_games(self, number=None):
        """Get the last number games"""
        cur = self.database.cursor()
        if number is None:
            select_statement = "SELECT timestamp, player1_id, player2_id, player3_id, player4_id, team1_score, team2_score, id FROM games ORDER BY id DESC"
        else:
            select_statement = "SELECT timestamp, player1_id, player2_id, player3_id, player4_id, team1_score, team2_score, id FROM games ORDER BY id DESC LIMIT {n}".format(n=number)

        cur.execute(select_statement)

        games = []
        for entry in cur:
            game = Game()
            game.time = entry[0]
            try:
                game.player1 = self.get_player(entry[1])
            except:
                game.player1 = Player()
                game.player1.name = "Unregistered Player"
            try:
                game.player2 = self.get_player(entry[2])
            except:
                game.player2 = Player()
                game.player2.name = "Unregistered Player"
            try:
                game.player3 = self.get_player(entry[3])
            except:
                game.player3 = Player()
                game.player3.name = "Unregistered Player"
            try:
                game.player4 = self.get_player(entry[4])
            except:
                game.player4 = Player()
                game.player4.name = "Unregistered Player"
            game.scoreTeam1 = entry[5]
            game.scoreTeam2 = entry[6]
            game.id = entry[7]
            games.append(game)

        return games

    def get_game_ids(self):
        """"Get ids of all games"""
        cur = self.database.cursor()
        cur.execute("SELECT id FROM games ORDER BY id ASC")
        ids = []
        for entry in cur:
            ids.append(entry[0])
        return ids

    def get_game(self, game_id):
        """Get game with id"""
        cur = self.database.cursor()
        cur.execute("SELECT timestamp, player1_id, player2_id, player3_id, player4_id, team1_score, team2_score FROM games WHERE id=?", [game_id])
        result = cur.fetchone()

        if result is None:
            return None

        game = Game()
        game.time = result[0]
        try:
            game.player1 = self.get_player(result[1])
        except:
            game.player1 = Player()
            game.player1.name = "Unregistered Player"
        try:
            game.player2 = self.get_player(result[2])
        except:
            game.player2 = Player()
            game.player2.name = "Unregistered Player"
        try:
            game.player3 = self.get_player(result[3])
        except:
            game.player3 = Player()
            game.player3.name = "Unregistered Player"
        try:
            game.player4 = self.get_player(result[4])
        except:
            game.player4 = Player()
            game.player4.name = "Unregistered Player"
        game.scoreTeam1 = result[5]
        game.scoreTeam2 = result[6]
        game.id = int(game_id)

        return game

    def delete_game(self, game_id):
        print("Delete game:\n{0}".format(game_id))
        self.database.execute("DELETE FROM games WHERE id=?", [game_id])
        self.database.commit()

    def rerank_games(self):
        # load players
        players = self.get_all_players()
        # reset ratings to default
        for p in players:
            p.reset_rating()
            self.update_player_skill(p)

        # load games
        game_ids = self.get_game_ids()

        # rate game
        for gid in game_ids:
            # Get game with updated player ratings
            g = self.get_game(gid)
            if g.scoreTeam1 > g.scoreTeam2:
                winner_team = 1
            else:
                winner_team = 2
            g.save_to_database(winner_team, self, True)
