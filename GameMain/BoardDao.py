import sqlite3


class BoardDao:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS board (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_login TEXT NOT NULL,
            board_position INTEGER,
            avatar_img TEXT,
            round_number INTEGER,
            FOREIGN KEY (user_login) REFERENCES users(login)
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def add_board_entry(self, user_login, board_position, avatar_img, round_number):
        query = 'INSERT INTO board (user_login, board_position, avatar_img, round_number) VALUES (?, ?, ?, ?)'
        try:
            self.conn.execute(query, (user_login, board_position, avatar_img, round_number))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding board entry: {e}")
            return False

    def get_board_entry_by_user_login(self, user_login):
        query = 'SELECT * FROM board WHERE user_login = ?'
        cursor = self.conn.execute(query, (user_login,))
        result = cursor.fetchone()

        if result:
            return {
                'id': result[0],
                'user_login': result[1],
                'board_position': result[2],
                'avatar_img': result[3],
                'round_number': result[4]
            }
        else:
            return None

    def get_users_with_current_round(self, round_number):
        query = 'SELECT user_login FROM board WHERE round_number = ?'
        cursor = self.conn.execute(query, (round_number,))
        results = cursor.fetchall()

        users_with_current_round = [result[0] for result in results]
        return users_with_current_round

    def update_player_position(self, user_login, new_position):
        query = 'UPDATE board SET board_position = ? WHERE user_login = ?'
        try:
            self.conn.execute(query, (new_position, user_login))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating player position: {e}")
            return False

    def update_player_round(self, user_login, new_round_number):
        query = 'UPDATE board SET round_number = ? WHERE user_login = ?'
        try:
            self.conn.execute(query, (new_round_number, user_login))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating player round: {e}")
            return False

    def get_user_count(self):
        query = 'SELECT COUNT(*) FROM board'
        cursor = self.conn.execute(query)
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return 0

    def get_all_players(self):
        query = 'SELECT * FROM board'
        cursor = self.conn.execute(query)
        results = cursor.fetchall()

        players = []
        for result in results:
            players.append({
                'id': result[0],
                'user_login': result[1],
                'board_position': result[2],
                'avatar_img': result[3],
                'round_number': result[4]
            })

        return players

    def get_all_players_avatars_except_current(self, current_user_login):
        try:
            query = 'SELECT avatar_img FROM board WHERE user_login != ?'
            cursor = self.conn.execute(query, (current_user_login,))
            results = cursor.fetchall()

            avatars = [result[0] for result in results]

            return avatars
        except Exception as e:
            print(f"Error fetching avatars: {e}")
            return []

    def update_avatar_image(self, user_login, new_avatar_img):
        query = 'UPDATE board SET avatar_img = ? WHERE user_login = ?'
        try:
            self.conn.execute(query, (new_avatar_img, user_login))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating avatar image: {e}")
            return False

    def close(self):
        self.conn.close()
