import sqlite3
from typing import List

from FriendList import User


class UserDao:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
    def get_points(self, user):
        return []
    def create_table_friends(self):
        query = '''
        CREATE TABLE user_friends (
            user_id INTEGER PRIMARY KEY,
            friend_1 INTEGER DEFAULT NULL,
            friend_2 INTEGER DEFAULT NULL,
            friend_3 INTEGER DEFAULT NULL,
            friend_4 INTEGER DEFAULT NULL,
            friend_5 INTEGER DEFAULT NULL,
            friend_6 INTEGER DEFAULT NULL,
            friend_7 INTEGER DEFAULT NULL,
            friend_8 INTEGER DEFAULT NULL,
            friend_9 INTEGER DEFAULT NULL,
            friend_10 INTEGER DEFAULT NULL,
            friend_11 INTEGER DEFAULT NULL,
            friend_12 INTEGER DEFAULT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (friend_1) REFERENCES users(id),
            FOREIGN KEY (friend_2) REFERENCES users(id),
            FOREIGN KEY (friend_3) REFERENCES users(id),
            FOREIGN KEY (friend_4) REFERENCES users(id),
            FOREIGN KEY (friend_5) REFERENCES users(id),
            FOREIGN KEY (friend_6) REFERENCES users(id),
            FOREIGN KEY (friend_7) REFERENCES users(id),
            FOREIGN KEY (friend_8) REFERENCES users(id),
            FOREIGN KEY (friend_9) REFERENCES users(id),
            FOREIGN KEY (friend_10) REFERENCES users(id),
            FOREIGN KEY (friend_11) REFERENCES users(id),
            FOREIGN KEY (friend_12) REFERENCES users(id),
    
);
        '''
        self.conn.execute(query)
        self.conn.commit()

    def add_friend(user_id, new_friend_id):
        conn = sqlite3.connect('twoja_baza_danych.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT friend_1, friend_2, friend_3, friend_4, friend_5, friend_6, friend_7, friend_8, friend_9, friend_10, friend_11, friend_12 FROM user_friends WHERE user_id = ?",
            (user_id,))
        friends = cursor.fetchone()

        column_to_update = None
        for i in range(12):
            if friends[i] is None:
                column_to_update = f"friend_{i + 1}"
                break

        if column_to_update:
            query = f"UPDATE user_friends SET {column_to_update} = ? WHERE user_id = ?"
            cursor.execute(query, (new_friend_id, user_id))
            conn.commit()

        cursor.close()
        conn.close()

    def get_name(self, user):
        return ""

    def add_points(self, value):
        pass

    def get_friend_list(self, user):
        return []

    def get_all(self) -> List[User]:
        query = 'SELECT * FROM users'
        cursor = self.conn.execute(query)
        result = cursor.fetchall()

        users = []
        for user in result:
            users.append(User(user[0], user[1]))
        return users