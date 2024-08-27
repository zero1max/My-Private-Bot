import sqlite3
from dataclasses import dataclass

@dataclass
class Database:
    connect: sqlite3.Connection = None
    cursor: sqlite3.Cursor = None

    def __post_init__(self):
        self.connect = sqlite3.connect('users.db')
        self.cursor = self.connect.cursor()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                username TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                contact TEXT NOT NULL
            )
        """)
        self.connect.commit()
        
    def add_user(self, name, contact):
        self.cursor.execute("""
            INSERT INTO users (name, contact) VALUES (?, ?)
        """, (name, contact))
        self.connect.commit()

    def select_users(self):
        self.cursor.execute("SELECT * FROM users") 
        return self.cursor.fetchall()

    def select_user(self, id):
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
        return self.cursor.fetchone()    
    
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connect:
            self.connect.close()
