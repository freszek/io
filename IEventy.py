from abc import ABC, ABCMeta, abstractmethod
from QuizWindow import QuizWindow


class IEventy(ABC, metaclass=ABCMeta):
    @abstractmethod
    def get_event_form(self):
        QuizWindow()
