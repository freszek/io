import sqlite3


class DatabaseManager:
    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()

    def check_points(self, player_id, event_id):
        self.cursor.execute("SELECT COALESCE(SUM(score) / (SUM(score) * COUNT(level)), 0) AS proportion, level "
                            "FROM statistics WHERE player_id = ? AND event_id = ? GROUP BY level",
                            (player_id, event_id))
        return self.cursor.fetchall()

    def count_achievements(self, aid):
        self.cursor.execute("SELECT COUNT(*) FROM users_achievements WHERE achievement_id = ?", (aid,))
        try:
            return self.cursor.fetchone()[0]
        except TypeError:
            return 0

    def get_player_name(self, player_id):
        self.cursor.execute("SELECT login FROM users WHERE id = ?", (player_id,))
        try:
            return self.cursor.fetchone()[0]
        except TypeError:
            return -1

    def get_all_player_names(self):
        self.cursor.execute("SELECT login FROM users")
        return self.cursor.fetchall()

    def get_player_id(self, login):
        self.cursor.execute("SELECT id FROM users WHERE login = ?", (login,))
        try:
            return self.cursor.fetchone()[0]
        except TypeError:
            return -1

    def get_events(self):
        self.cursor.execute("SELECT * FROM events")
        return self.cursor.fetchall()

    def get_event(self, event_id):
        self.cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
        return self.cursor.fetchone()

    def get_achievement(self, achievement_id):
        self.cursor.execute("SELECT * FROM achievements WHERE id = ?", (achievement_id,))
        return self.cursor.fetchone()

    def get_questions(self, event_id, level):
        self.cursor.execute("SELECT * FROM questions WHERE event_id = ? AND difficulty_level = ?",
                            (event_id, level))
        return self.cursor.fetchall()

    def save_statistics(self, event_id, player_name, score, time, level):
        self.cursor.execute("INSERT INTO statistics (event_id, player_id, score, completion_time, level) "
                            "VALUES (?, ?, ?, ?, ?)", (event_id, player_name, score, time, level))
        self.connection.commit()

    def get_statistics(self, player_id):
        self.cursor.execute("SELECT * FROM statistics WHERE player_id = ?", (player_id,))
        return self.cursor.fetchall()

    def get_player_achievements(self, player_id):
        self.cursor.execute("SELECT a.id, a.name, a.description FROM achievements a "
                            "INNER JOIN main.users_achievements ua on a.id = ua.achievement_id"
                            " WHERE user_id = ?", (player_id,))
        return self.cursor.fetchall()

    def get_session_achievements(self, player_id):
        session_ids = []
        all_achievements = self.get_player_achievements(player_id)
        if 10 in all_achievements:
            return session_ids
        how_many_events = self.count_player_events(player_id)
        if how_many_events == 5:
            session_ids.append(1)
        if how_many_events == 10:
            session_ids.append(2)
        if how_many_events == 15:
            session_ids.append(3)
        if how_many_events == 20:
            session_ids.append(4)
        if self.event_under_5(player_id):
            session_ids.append(5)
        if self.all_correct(player_id):
            session_ids.append(6)
        levels = ("EASY", "MEDIUM", "HARD")
        for i, level in enumerate(levels):
            if self.completed_event(player_id, level):
                session_ids.append(7 + i)
        if self.is_legend(player_id):
            session_ids.append(10)
        all_ids = [row[0] for row in all_achievements]
        session_ids = [id_ for id_ in session_ids if id_ not in all_ids]
        return session_ids

    def set_achievements(self, player_id):
        session_achievements = self.get_session_achievements(player_id)
        all_achievements = self.get_player_achievements(player_id)
        if len(all_achievements) == 0:
            for achievement in session_achievements:
                self.cursor.execute("INSERT INTO users_achievements (user_id, achievement_id) VALUES (?, ?)",
                                    (player_id, achievement))
                self.connection.commit()
        else:
            for achievement in session_achievements:
                if achievement not in [row[0] for row in all_achievements]:
                    self.cursor.execute("INSERT INTO users_achievements (user_id, achievement_id) VALUES (?, ?)",
                                        (player_id, achievement))
                    self.connection.commit()

    def count_player_events(self, player_id):
        self.cursor.execute("SELECT DISTINCT COUNT(*) FROM statistics WHERE player_id = ?", (player_id,))
        return self.cursor.fetchone()[0]

    def event_under_5(self, player_id):
        self.cursor.execute("SELECT COUNT(*) FROM statistics WHERE player_id = ? AND completion_time < 5", (player_id,))
        if self.cursor.fetchone()[0] > 0:
            return True
        return False

    def completed_event(self, player_id, level):
        self.cursor.execute("SELECT COUNT(*) FROM statistics WHERE player_id = ? AND level = ?", (player_id, level))
        if self.cursor.fetchone()[0] > 0:
            return True
        return False

    def all_correct(self, player_id):
        arr = self.get_statistics(player_id)
        for row in arr:
            if (row[3] == 6.0 and row[-1] == "HARD" or
                    row[3] == 4.0 and row[-1] == "MEDIUM" or
                    row[3] == 2.0 and row[-1] == "EASY"):
                return True
        return False

    def is_legend(self, player_id):
        if len(self.get_player_achievements(player_id)) == 10:
            return True
        return False

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
