import hashlib
import sqlite3
from datetime import datetime, timedelta
from typing import List
from User.Userr import Userr as User


class Points:
    def __init__(self, value, date, category):
        self.value = value
        self.date = date
        self.category = category

    def get_value(self):
        return self.value

    def get_date(self):
        return self.date

    def get_category(self):
        return self.category

    def set_value(self, value):
        self.value = value

    def set_date(self, date):
        self.date = date

    def set_category(self, category):
        self.category = category


class UserDao:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_table()
        self.create_points_table()

    def get_ranking_data(self, user_list, period='daily'):
        ranking = {}

        # Ustalenie zakresu dat dla okresu
        current_date = datetime.now()
        if period == 'daily':
            start_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'weekly':
            start_date = current_date - timedelta(days=current_date.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

        for user in user_list:
            user_points = self.get_user_points(user.id)
            for point in user_points:
                point_date = datetime.strptime(point.date, '%Y-%m-%d')
                if start_date <= point_date < current_date:
                    if user.login not in ranking:
                        ranking[user.login] = 0
                    ranking[user.login] += point.value

        # Sortowanie wyników w celu utworzenia rankingu
        sorted_ranking = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
        return sorted_ranking

    def get_friends_ranking_data(self, user_id: int, period='daily'):
        ranking = {}

        # Ustalenie zakresu dat dla okresu
        current_date = datetime.now()
        if period == 'daily':
            start_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'weekly':
            start_date = current_date - timedelta(days=current_date.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

        # Pobranie listy ID znajomych
        friend_ids = self.get_friend_list(user_id)

        # Pobranie punktów dla każdego znajomego
        for friend_id in friend_ids:
            friend_points = self.get_user_points(friend_id)
            for point in friend_points:
                point_date = datetime.strptime(point.date, '%Y-%m-%d')
                if start_date <= point_date < current_date:
                    friend = self.get_by_id(friend_id)
                    if friend.login not in ranking:
                        ranking[friend.login] = 0
                    ranking[friend.login] += point.value

        # Sortowanie wyników
        sorted_ranking = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
        return sorted_ranking

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            answer TEXT,
            question TEXT
        )
        '''
        query1 = '''
        CREATE TABLE IF NOT EXISTS user_friends (
            user_id INTEGER,
            friend_id INTEGER,
            PRIMARY KEY (user_id, friend_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (friend_id) REFERENCES users(id)
        );
        '''
        self.conn.execute(query)
        self.conn.commit()
        self.conn.execute(query1)
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

    def get_friend_list(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
                SELECT friend_id FROM user_friends WHERE user_id = ?
            ''', (user_id,))  # Zauważ użycie przecinka, aby utworzyć krotkę jednoelementową

        friends = cursor.fetchall()

        friend_ids = [friend[0] for friend in friends]
        return friend_ids

    def delete_friend(self, user_id, friend_id):
        cursor = self.conn.cursor()

        query = "DELETE FROM user_friends WHERE user_id = ? AND friend_id = ?"
        cursor.execute(query, (user_id, friend_id))
        self.conn.commit()

        cursor.close()

    def add_friend(self, user_id, new_friend_id):
        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM user_friends WHERE user_id = ? AND friend_id = ?",
            (user_id, new_friend_id))
        if cursor.fetchone()[0] == 0:
            query = "INSERT INTO user_friends (user_id, friend_id) VALUES (?, ?)"
            cursor.execute(query, (user_id, new_friend_id))
            self.conn.commit()
        print("xd")

        cursor.close()

    def create_points_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category_name TEXT NOT NULL,
            round_number INTEGER NOT NULL,
            points INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def get_user_points(self, user_id: int):
        query = 'SELECT points, date, category_name FROM points WHERE user_id = ?'
        cursor = self.conn.execute(query, (user_id,))
        results = cursor.fetchall()

        points_list = []
        for result in results:
            points = Points(result[0], result[1], result[2])
            points_list.append(points)

        return points_list

    def add_points(self, user_id: int, points: int, date: str, category_name: str, round_number: int) -> bool:
        query = 'INSERT INTO points (user_id, points, date, category_name, round_number) VALUES (?, ?, ?, ?, ?)'
        try:
            self.conn.execute(query, (user_id, points, date, category_name, round_number))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def close(self):
        self.conn.close()
