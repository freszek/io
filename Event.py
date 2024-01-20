from DifficultyLevel import DifficultyLevel
from EventInterface import EventInterface
from DifficultyLevel import to_string
from database_setup import db
import time


class Event(EventInterface):
    def __init__(self, event_id, name):
        self.event_id = event_id
        self.name = name
        self.level = DifficultyLevel.EASY
        self.questions = []
        self.score = 0
        self.start_time = 0

    def __str__(self):
        return "Event ID: " + str(self.event_id) + "\n" + \
            "Name: " + self.name + "\n" + \
            "Level: " + str(self.level) + "\n"

    def get_score(self):
        return self.score

    def get_event_id(self):
        return self.event_id

    def get_name(self):
        return self.name

    def get_level(self):
        return self.level

    def set_level(self, level):
        if not isinstance(level, DifficultyLevel):
            raise TypeError("Level must be of type DifficultyLevel")
        self.level = level

    def get_questions(self):
        return self.questions

    def start_event(self):
        qu = db.get_questions(self.event_id, to_string(self.level))
        self.questions = qu

    def end_event(self, player_id, time_elapsed=None):
        if time_elapsed is not None:
            db.save_statistics(self.event_id, player_id, self.score, time_elapsed, to_string(self.level))
        else:
            db.save_statistics(self.event_id, player_id, self.score,
                               round(time.perf_counter() - self.start_time, 3), to_string(self.level))
        stats = [[self.event_id, player_id, self.score, round(time.perf_counter() - self.start_time, 3),
                 to_string(self.level)]]
        achievements = db.get_session_achievements(player_id)
        db.set_achievements(player_id)
        self.start_time = 0
        self.questions = []
        self.score = 0
        return player_id, stats, achievements

    def can_player_join(self, player_id):
        if db.is_legend(player_id):
            return -2
        proportion = db.check_points(player_id, self.event_id)
        for row in proportion:
            if row[0] >= 0.9:
                return -1
        return 0

    def calculate_score(self):
        if self.level == DifficultyLevel.EASY:
            self.score += 1
        elif self.level == DifficultyLevel.MEDIUM:
            self.score += 2
        elif self.level == DifficultyLevel.HARD:
            self.score += 3
