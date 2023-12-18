import sqlite3
from typing import List
from datetime import datetime

from FriendList import User


class UserDao:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
    def get_points(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM points WHERE user_id = ?', (user_id,))
        user_points = cursor.fetchall()

        self.conn.close()

        return user_points
    def create_table_friends(self):
        query = '''
        CREATE TABLE user_friends (
            user_id INTEGER,
            friend_id INTEGER,
            PRIMARY KEY (user_id, friend_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (friend_id) REFERENCES users(id)
        );
        '''
        self.conn.execute(query)
        self.conn.commit()

    def add_friend(self, user_id, new_friend_id):
        cursor = self.conn.cursor()
    
        cursor.execute(
            "SELECT COUNT(*) FROM user_friends WHERE user_id = ? AND friend_id = ?",
            (user_id, new_friend_id))
        if cursor.fetchone()[0] == 0:
            query = "INSERT INTO user_friends (user_id, friend_id) VALUES (?, ?)"
            cursor.execute(query, (user_id, new_friend_id))
            self.conn.commit()
    
        cursor.close()

    def delete_friend(self, user_id, friend_id):
        cursor = self.conn.cursor()
    
        query = "DELETE FROM user_friends WHERE user_id = ? AND friend_id = ?"
        cursor.execute(query, (user_id, friend_id))
        self.conn.commit()
    
        cursor.close()


    def get_name(self, user):
        return ""

    def create_table_points(self):
        query = '''
           CREATE TABLE IF NOT EXISTS points (
                user_id INTEGER,
                value REAL NOT NULL,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                PRIMARY KEY (user_id, value, date),
                FOREIGN KEY (user_id) REFERENCES users (user_id)
           '''
        self.conn.execute(query)
        self.conn.commit()
    def add_points(self, user_id, value, category):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = self.conn.cursor()
        cursor.execute('''
                   INSERT INTO points (user_id, value, date, category) VALUES (?, ?, ?, ?)
               ''', (user_id, value, date, category))

        self.conn.commit()
        self.conn.close()


    def get_friend_list(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
                SELECT friend_id FROM user_friends WHERE user_id = ?
            ''', user_id)

        friends = cursor.fetchall()
        self.conn.close()

        friend_ids = [friend[0] for friend in friends]
        return friend_ids

    def get_all(self) -> List[User]:
        query = 'SELECT * FROM users'
        cursor = self.conn.execute(query)
        result = cursor.fetchall()

        users = []
        for user in result:
            users.append(User(user[0], user[1]))
        return users