import sqlite3

# This script updates the data base whenever a new version needs changes in the table layout.
# Make sure this script handles all versions, only add new conversion methods and keep the old ones available
# Don't use methods of database.py or admin_database.py here since those files only support the latest database
# layout and won't be compatible with older versions of the database (exception: create new database).

# For each new database version do the following steps:
# 1. write a function that does the actual changes in the database from the last version (e.g. update_from_1), the function must return the 
#    new (current) version of the database
# 2. Add a case for this version to the update_from_version function
# 3. Increase the value of current_version to the new version number
# 4. Make sure to also increment the current version in database.py

# database file configuration
# this should be configurable via command line arguments, but for now just use fixed file names
kickerDB = "kicker_scores.db"
adminDB = "kicker_admin.db"

# version configuration
current_version = 1

def update_from_0(db):
    """Update database from version 0 to 1"""
    
    # insert version table
    db.execute("CREATE TABLE IF NOT EXISTS version_info (version INTEGER PRIMARY KEY)")
    db.execute("INSERT INTO version_info (version) VALUES (?)", (1,))

    # rename old players and games tables
    db.execute("ALTER TABLE players RENAME TO players_old")
    db.execute("ALTER TABLE games RENAME TO games_old")

    # create new players and games tables
    db.execute("CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, token_id TEXT UNIQUE, skill_mu REAL, skill_sigma REAL)")
    db.execute("CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, player1_id INTEGER, player2_id INTEGER, player3_id INTEGER, player4_id INTEGER, team1_score INTEGER, team2_score INTEGER)")
        
    # copy and convert data from old to new tables
    db.execute("INSERT INTO players (name, token_id, skill_mu, skill_sigma) SELECT name, token_id, skill_mu, skill_sigma FROM players_old", )

    cur = db.cursor()
    games = cur.execute("SELECT id, timestamp, player1, player2, player3, player4, team1_score, team2_score FROM games_old")
    def get_player_id(token):
        player_cur = db.cursor()
        player = player_cur.execute("SELECT id FROM players WHERE token_id=?", (token,)).fetchone()
        return player[0]

    for game in games.fetchall():
        # insert the data into the new table, ids will be used instead of tokens
        player1_id = get_player_id(game[2])
        player2_id = get_player_id(game[3])
        player3_id = get_player_id(game[4])
        player4_id = get_player_id(game[5])
        updated_data = (game[0], game[1], player1_id, player2_id, player3_id, player4_id, game[6], game[7])
        db.execute("INSERT INTO games (id, timestamp, player1_id, player2_id, player3_id, player4_id, team1_score, team2_score) VALUES (?,?,?,?,?,?,?,?)", updated_data)

    # drop old tables
    db.execute("DROP TABLE players_old")
    db.execute("DROP TABLE games_old")

    db.commit()
    return 1

def get_version(db):
    version = 0

    cur = db.cursor()

    try:
        cur.execute("SELECT version FROM version_info")
        v = cur.fetchone()
        if None == v:
            version = 0
        else:
            version = v[0]
    except sqlite3.OperationalError as e:
        print(e)
        version = 0

    return version


def update_from_version(db, db_version):
    if 0 == db_version:
        return update_from_0(db)
    
    raise Exception("Error in update: No update from current version available")


def main():
    # TODO: parse kickerDB and adminDB from arguments
    
    db = sqlite3.connect(kickerDB)
    db_version = get_version(db)

    if db_version > current_version:
        raise Exception("Database version is higher than current version")
    
    if db_version == current_version:
        print("Database is up to date, skipping update")
        db.close()
        return

    # incrementally update the version
    try:
        db.commit()
        while db_version < current_version:
            db_version = update_from_version(db, db_version)
        print("Successfully updated the database to version %d" % db_version)
        
    except Exception as e:
        db.rollback()
        print("There was an error while updating the Database: %s" % e)

    finally:
        db.close()    

    

if __name__ == "__main__":
    main()
