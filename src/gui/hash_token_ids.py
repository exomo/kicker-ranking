# Update the database from unhashed token ids to hashed token ids
# Execute this script only once for the database file when it contains unhashed token ids.

from GUI.database import database
from GUI.hardware import rfid

kickerDB = "kicker_scores.db"
db = database.Database(kickerDB)
reader = rfid.rfid()

for player in db.get_all_players():
    digest = reader.Hash(player.tokenID)
    if len(player.tokenID) == len(digest):
        print("The database is already hashed - aborting")
        exit()
    db.database.execute("UPDATE players SET token_id=? WHERE token_id=?", (digest, player.tokenID))
    db.database.execute("UPDATE games SET player1=? WHERE player1=?", (digest, player.tokenID))
    db.database.execute("UPDATE games SET player2=? WHERE player2=?", (digest, player.tokenID))
    db.database.execute("UPDATE games SET player3=? WHERE player3=?", (digest, player.tokenID))
    db.database.execute("UPDATE games SET player4=? WHERE player4=?", (digest, player.tokenID))

db.database.commit()
print("Hashes updated in database")
db.show_players()