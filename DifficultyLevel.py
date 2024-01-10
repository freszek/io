from enum import Enum


def to_string(level):
    if not isinstance(level, DifficultyLevel):
        raise TypeError("Level must be of type DifficultyLevel")
    return level.name.upper()


def to_int(level):
    if not isinstance(level, DifficultyLevel):
        raise TypeError("Level must be of type DifficultyLevel")
    return level.value


class DifficultyLevel(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2

    @classmethod
    def from_string(cls, level_str):
        try:
            return cls[level_str.upper()]
        except KeyError:
            raise ValueError(f"Invalid difficulty level: {level_str}")

    @classmethod
    def from_int(cls, level_int):
        try:
            return cls(level_int)
        except ValueError:
            raise ValueError(f"Invalid difficulty level integer: {level_int}")
