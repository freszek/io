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
            FOREIGN KEY (user_login) REFERENCES users(login)
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def add_board_entry(self, user_login, board_position, avatar_img):
        query = 'INSERT INTO board (user_login, board_position, avatar_img) VALUES (?, ?, ?)'
        try:
            self.conn.execute(query, (user_login, board_position, avatar_img))
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
                'avatar_img': result[3]
            }
        else:
            return None

    def update_player_position(self, user_login, new_position):
        query = 'UPDATE board SET board_position = ? WHERE user_login = ?'
        try:
            self.conn.execute(query, (new_position, user_login))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating player position: {e}")
            return False

    def close(self):
        self.conn.close()
