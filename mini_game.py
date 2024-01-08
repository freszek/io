# import gierka
from Minigames.WaterSafe.minigame import WaterSafeGame


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
        # elif self.minigameName == "CleanUp":
            # game = gierka.generate_game()
        return game.run_game()
