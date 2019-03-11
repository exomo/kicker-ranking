import sqlite3

class AdminDatabase():
    def __init__(self, filename):
        self.database = sqlite3.connect(filename)
        # if the database does not exist it is created
        self.create_database()

    def __del__(self):
        self.database.close()

    def create_database(self):
        self.database.execute("CREATE TABLE IF NOT EXISTS admins (name TEXT UNIQUE, token_id TEXT PRIMARY KEY)")
        self.database.commit()
        print("Created database")

    def is_admin(self, token_id):
        cur = self.database.cursor()
        cur.execute("SELECT * FROM admins WHERE token_id=?", [token_id])
        result = cur.fetchone()
        if result != None:
            return True
        else:
            return False