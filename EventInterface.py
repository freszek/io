from abc import ABC, ABCMeta, abstractmethod


class EventInterface(ABC, metaclass=ABCMeta):

    @abstractmethod
    def start_event(self):
        pass

    @abstractmethod
    def end_event(self, player_id):
        pass

    @abstractmethod
    def can_player_join(self, player_id):
        pass

    @abstractmethod
    def calculate_score(self):
        pass
