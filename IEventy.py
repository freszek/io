from abc import ABC, ABCMeta, abstractmethod
from QuizForm import QuizForm


class IEventy(ABC, metaclass=ABCMeta):
    @abstractmethod
    def get_event_form(self):
        QuizForm()
