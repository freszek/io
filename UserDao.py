import hashlib
import sqlite3
from typing import List
from User import User


class UserDao:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            answer TEXT,
            question TEXT
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def get_all(self) -> List[User]:
        query = 'SELECT * FROM users'
        cursor = self.conn.execute(query)
        result = cursor.fetchall()

        users = []
        for user in result:
            users.append(User(user[0], user[1], user[2], user[3], user[4], user[5]))
        return users

    def get_by_id(self, user_id: int) -> User:
        query = 'SELECT * FROM users WHERE id = ?'
        cursor = self.conn.execute(query, (user_id,))
        result = cursor.fetchone()
        try:
            return User(result[0], result[1], result[2], result[3], result[4], result[5])
        except:
            print("User not found")

    def get_by_login(self, login) -> User:
        query = 'SELECT * FROM users WHERE login = ?'
        cursor = self.conn.execute(query, (login,))
        result = cursor.fetchone()
        try:
            return User(result[0], result[1], result[2], result[3], result[4], result[5])
        except:
            print("User not found")

    def create_user(self, user: User) -> bool:
        query = 'INSERT INTO users (login, password, email, answer, question) VALUES (?, ?, ?, ?, ?)'
        try:
            self.conn.execute(query,
                              (user.login, self.hash_password(user.password), user.email, user.answer, user.question))
            self.conn.commit()
            return True
        except:
            return False

    def update_user(self, user: User, password: str) -> bool:
        hashed_password = self.hash_password(password)
        query = 'UPDATE users SET password = ? WHERE id = ?'
        try:
            self.conn.execute(query, (hashed_password, user.id))
            self.conn.commit()
            return True
        except:
            return False

    def delete_user(self, user: User) -> bool:
        query = 'DELETE FROM users WHERE id = ?'
        try:
            self.conn.execute(query, (user.id,))
            self.conn.commit()
            return True
        except:
            return False

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def close(self):
        self.conn.close()
