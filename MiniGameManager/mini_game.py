from Minigames.SortTrash.gierka import Game
from Minigames.WaterSafe.minigame import WaterSafeGame
from Minigames.BioFoodGame.MinigameBioFood import EkologicznySnake
from Minigames.SnakeMinigame.SnakeGame import SnakeGame
from Minigames.DoorGame.doorgame import DoorGame


class MiniGame:
    def __init__(self, minigameID, minigameName, duration, minimalNumberOfPoints):
        self.minigameID = minigameID
        self.minigameName = minigameName
        self.duration = duration
        self.minimalNumberOfPoints = minimalNumberOfPoints

    def startMinigame(self):
        game = None
        if self.minigameName == "WaterSafe":
            game = WaterSafeGame()
        elif self.minigameName == "CleanUp":
            game = Game()
        elif self.minigameName == "EkoSnake":
            game = EkologicznySnake()
        elif self.minigameName == "Snake":
            game = SnakeGame()
        elif self.minigameName == "DoorGame":
            game = DoorGame()
        return game.run_game()

