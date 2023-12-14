import mysql.connector


class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def get_events(self):
        self.cursor.execute("SELECT * FROM events")
        return self.cursor.fetchall()

    def get_event(self, event_id):
        self.cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
        return self.cursor.fetchone()

    def get_questions(self, event_id, level):
        self.cursor.execute("SELECT * FROM questions WHERE event_id = %s AND difficulty_level = %s",
                            (event_id, level))
        return self.cursor.fetchall()

    def save_statistics(self, event_id, player_name, score, time):
        self.cursor.execute("INSERT INTO statistics (event_id, player_name, score, completion_time) "
                            "VALUES (%s, %s, %s, %s)", (event_id, player_name, score, time))
        self.connection.commit()

    def get_statistics(self, player_name):
        self.cursor.execute("SELECT * FROM statistics WHERE player_name = %s", (player_name,))
        return self.cursor.fetchall()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
