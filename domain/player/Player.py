class Player:
    def __init__(self, playerId):
        self.__playerId = playerId
        self.__character = None
        self.score = 0


    def getId(self):
        return self.__playerId
    def setCharacter(self, character):
        self.__character = character
    def getCharacter(self):
        return self.__character