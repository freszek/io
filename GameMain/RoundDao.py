import sqlite3
from datetime import datetime

class RoundDao:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS round (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time_started TEXT NOT NULL,
            time_ended TEXT,
            round_number INTEGER
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def start_round(self, round_number):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = 'INSERT INTO round (time_started, round_number) VALUES (?, ?)'
        try:
            self.conn.execute(query, (current_time, round_number))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error starting round: {e}")
            return False

    def end_round(self, round_number):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = 'UPDATE round SET time_ended = ? WHERE round_number = ?'
        try:
            self.conn.execute(query, (current_time, round_number))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error ending round: {e}")
            return False

    def get_highest_round_number(self):
        query = 'SELECT round_number FROM round ORDER BY round_number DESC LIMIT 1'
        cursor = self.conn.execute(query)
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None
    def get_round_info(self, round_number):
        query = 'SELECT * FROM round WHERE round_number = ?'
        cursor = self.conn.execute(query, (round_number,))
        result = cursor.fetchone()

        if result:
            return {
                'id': result[0],
                'time_started': result[1],
                'time_ended': result[2],
                'round_number': result[3]
            }
        else:
            return None

    def get_all_rounds(self):
        query = 'SELECT * FROM round'
        cursor = self.conn.execute(query)
        results = cursor.fetchall()

        rounds = []
        for result in results:
            rounds.append({
                'id': result[0],
                'time_started': result[1],
                'time_ended': result[2],
                'round_number': result[3]
            })

        return rounds

    def get_round_by_number(self, round_number):
        query = 'SELECT * FROM round WHERE round_number = ?'
        cursor = self.conn.execute(query, (round_number,))
        result = cursor.fetchone()

        if result:
            return {
                'id': result[0],
                'time_started': result[1],
                'time_ended': result[2],
                'round_number': result[3]
            }
        else:
            return None

    def close(self):
        self.conn.close()
