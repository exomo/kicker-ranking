
import sqlite3
from kicker import player
from kicker import Game
import trueskill

class Database():
    def __init__(self, filename):
        self.database = sqlite3.connect(filename)
        # if the database does not exist it is created
        self.create_database()

    def __del__(self):
        self.database.close()

    def create_database(self):
        self.database.execute("CREATE TABLE IF NOT EXISTS players (name TEXT UNIQUE, token_id TEXT PRIMARY KEY, skill_mu REAL, skill_sigma REAL)")
        self.database.execute("CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, player1 TEXT, player2 TEXT, player3 TEXT, player4 TEXT, team1_score INTEGER, team2_score INTEGER)")
        self.database.commit()
        print("Created database")

    def add_new_player(self, name, token_id):
        self.database.execute("INSERT INTO players VALUES(?, ?, ?, ?)", (name, token_id, trueskill.Rating().mu, trueskill.Rating().sigma))
        self.database.commit()
        print("Added new player: " + name)

    def get_player(self, token_id):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM players WHERE token_id=?", [token_id])
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
        print("Update player:\n {0}".format(p))
        self.database.execute("UPDATE players SET skill_mu=?, skill_sigma=? WHERE token_id=?", (p.rating.mu, p.rating.sigma, p.tokenID))
        self.database.commit()

    def create_player(self, db_result):
        p = player.Player()
        p.name = db_result[0]
        p.tokenID = db_result[1]
        p.rating = trueskill.Rating(mu=db_result[2], sigma=db_result[3])
        return p

    def add_game(self, game):
        """Add a game to the games list"""
        cur = self.database.cursor()
        insert_statement = "INSERT INTO games (player1, player2, player3, player4, team1_score, team2_score) VALUES (?,?,?,?,?,?)"
        cur.execute(insert_statement, (
            game.player1.tokenID,
            game.player2.tokenID,
            game.player3.tokenID,
            game.player4.tokenID,
            game.scoreTeam1,
            game.scoreTeam2))
        self.database.commit()

    def update_game(self, game):
        print("Update game:\n {0}".format(game))
        self.database.execute("UPDATE games SET player1=?, player2=?, player3=?, player4=?, team1_score=?, team2_score=? WHERE id=?", (game.player1.tokenID, game.player2.tokenID, game.player3.tokenID, game.player4.tokenID, game.scoreTeam1, game.scoreTeam2, game.id))
        self.database.commit()

    def get_games(self, number=None):
        """Get the last number games"""
        cur = self.database.cursor()
        if number is None:
            select_statement = "SELECT timestamp, player1, player2, player3, player4, team1_score, team2_score, id FROM games ORDER BY timestamp DESC"
        else:
            select_statement = "SELECT timestamp, player1, player2, player3, player4, team1_score, team2_score, id FROM games ORDER BY timestamp DESC LIMIT {n}".format(n=number)

        cur.execute(select_statement)

        games = []
        for entry in cur:
            game = Game.Game()
            game.time = entry[0]
            try:
                game.player1 = self.get_player(entry[1])
            except:
                game.player1 = player.Player()
                game.player1.name = "Unregistered Player"
            try:
                game.player2 = self.get_player(entry[2])
            except:
                game.player2 = player.Player()
                game.player2.name = "Unregistered Player"
            try:
                game.player3 = self.get_player(entry[3])
            except:
                game.player3 = player.Player()
                game.player3.name = "Unregistered Player"
            try:
                game.player4 = self.get_player(entry[4])
            except:
                game.player4 = player.Player()
                game.player4.name = "Unregistered Player"
            game.scoreTeam1 = entry[5]
            game.scoreTeam2 = entry[6]
            game.id = entry[7]
            games.append(game)

        return games

    def get_game(self, id):
        """Get the last number games"""
        cur = self.database.cursor()
        cur.execute("SELECT timestamp, player1, player2, player3, player4, team1_score, team2_score FROM games WHERE id=?", [id])
        
        for entry in cur:
            game = Game.Game()
            game.time = entry[0]
            try:
                game.player1 = self.get_player(entry[1])
            except:
                game.player1 = player.Player()
                game.player1.name = "Unregistered Player"
            try:
                game.player2 = self.get_player(entry[2])
            except:
                game.player2 = player.Player()
                game.player2.name = "Unregistered Player"
            try:
                game.player3 = self.get_player(entry[3])
            except:
                game.player3 = player.Player()
                game.player3.name = "Unregistered Player"
            try:
                game.player4 = self.get_player(entry[4])
            except:
                game.player4 = player.Player()
                game.player4.name = "Unregistered Player"
            game.scoreTeam1 = entry[5]
            game.scoreTeam2 = entry[6]
            game.id = int(id)
            
        return game

    def rerank_games(self):
        # load players
        players = self.get_all_players()
        # reset ratings to default
        for p in players:
            p.reset_rating()
            self.update_player_skill(p)

        # load games
        games = self.get_games() #TODO: Number of games in db would be sufficient

        # rate game
        for i in range(len(games)):
            # Get game with updated player ratings
            g = self.get_game(i+1)
            if g.scoreTeam1 > g.scoreTeam2:
                winner_team = 1
            else:
                winner_team = 2
            g.save_to_database(winner_team, self, True)
