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