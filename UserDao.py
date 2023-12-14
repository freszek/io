import sqlite3
from typing import List

from FriendList import User


class UserDao:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
    def get_points(self, user):
        return []

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