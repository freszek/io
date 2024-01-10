from DifficultyLevel import DifficultyLevel
from EventInterface import EventInterface
from DifficultyLevel import to_string
from database_setup import db
import time


class Event(EventInterface):
    def __init__(self, event_id, name):
        self.__event_id = event_id
        self.__name = name
        self.__level = DifficultyLevel.EASY
        self.__questions = []
        self.__score = 0
        self.__time = 0

    def __str__(self):
        return "Event ID: " + str(self.__event_id) + "\n" + \
            "Name: " + self.__name + "\n" + \
            "Level: " + str(self.__level) + "\n"

    def get_score(self):
        return self.__score

    def get_event_id(self):
        return self.__event_id

    def get_name(self):
        return self.__name

    def get_level(self):
        return self.__level

    def set_level(self, level):
        if not isinstance(level, DifficultyLevel):
            raise TypeError("Level must be of type DifficultyLevel")
        self.__level = level

    def get_questions(self):
        return self.__questions

    def start_event(self):
        self.__time = time.perf_counter()
        qu = db.get_questions(self.__event_id, to_string(self.__level))
        self.__questions = qu

    def end_event(self):  # TODO: wziąć id gracza zamiast 0, ale to scenariusz ma dac metode
        # TODO: zapis punktów do rankingu
        db.save_statistics(self.__event_id, 0, self.__score,
                           round(time.perf_counter() - self.__time, 3), to_string(self.__level))
        db.set_achievements(0)
        self.__time = 0
        self.__questions = []
        self.__score = 0

    def can_player_join(self):  # TODO: wziąć liczbę dotychczasowych punktów gracza od scenariusza metoda
        return True

    def calculate_score(self):
        if self.__level == DifficultyLevel.EASY:
            self.__score += 1
        elif self.__level == DifficultyLevel.MEDIUM:
            self.__score += 2
        elif self.__level == DifficultyLevel.HARD:
            self.__score += 3
