class Player:
    def __init__(self, playerId, character):
        self.playerId = playerId
        self.character = character
        self.score = 0

    def getCharacter(self):
        return self.character