import sqlite3

class DB:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                tgId INTEGER NOT NULL,
                name TEXT NOT NULL,
                tgName TEXT NOT NULL,
                count INTEGER NOT NULL
            )
        ''')
        self.connection.commit()

    def add_user(self, tgId, name, tgName, count):
        self.cursor.execute('INSERT INTO users (tgId, name, tgName, count) VALUES (?, ?, ?, ?)', (tgId, name, tgName, count))
        self.connection.commit()

    def get_user(self, tgId):
        self.cursor.execute('SELECT * FROM users WHERE tgId = ?', (tgId,))
        return self.cursor.fetchone()

    def addCount(self, tgId):
        user = self.get_user(tgId)
        self.cursor.execute('UPDATE users SET count = ? WHERE tgId = ?', (user[3]+1, tgId))
        self.connection.commit()

    def get_top_five(self):
        self.cursor.execute('SELECT * FROM users ORDER BY count DESC LIMIT 5;')
        return self.cursor.fetchall()
    
    def close(self):
        self.connection.close()

