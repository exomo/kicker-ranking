import sqlite3

kickerDB = "kicker_scores.db"
adminDB = "kicker_admin.db"

adminbase = sqlite3.connect(adminDB)

adminbase.execute("CREATE TABLE IF NOT EXISTS admins (name TEXT UNIQUE, token_id TEXT PRIMARY KEY)")

database = sqlite3.connect(kickerDB)

database.execute("ATTACH DATABASE 'kicker_admin.db' AS admin")
database.execute("INSERT INTO admin.admins SELECT name, token_id FROM players WHERE players.name IN ('Kai', 'Thomas P.')")

database.commit()

database.execute("DETACH admin")

cur = adminbase.cursor()
cur.execute("SELECT * FROM admins")
for a in cur.fetchall():
    print(a)

database.close()
adminbase.close()
