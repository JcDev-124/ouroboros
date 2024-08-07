import random

from domain.characters.CharacterDamage import CharacterDamage

states = {
    'selectingDefender': 1,
    'selectingAttack': 2,
    'waitingAnswer': 3,
    'attacking': 4,
}

class MatchService:
    players = []

    currentState = states['selectingDefender']

    def __init__(self):
        self.grantCharacter = None
        self.attacker = None
        self.state = []

    def addPlayer(self, player):
        try:
            if len(self.players) >= 3:
                raise ValueError("Unable to add more than 3 players.")
        except ValueError as e:
            print(e)

        self.players.append(player)

    def startMatch(self):
        try:
            if len(self.players) <= 1:
                raise ValueError("Unable to start match with less than 2 players.")
        except ValueError as e:
            print(e)

        self.attacker = random.choice(self.players)

    def attack(self, level, damage, defender):
        try:
            if level == 'light':
                self.attacker.getCharacter().light_attack(damage, defender.getCharacter())
            elif level == 'medium':
                self.attacker.getCharacter().medium_attack(damage, defender.getCharacter())
            elif level == 'heavy':
                self.attacker.getCharacter().heavy_attack(damage, defender.getCharacter())
            elif level == 'ultimate':
                if type(self.attacker.getCharacter()) is CharacterDamage:
                    self.attacker.getCharacter().ult_attack(damage, defender.getCharacter())
                else:
                    self.attacker.getCharacter().ult_attack()
            else:
                raise ValueError("Invalid attack type.")
            self.__eliminatePlayer()
            self.__setNextAttacker()
        except ValueError as e:
            print(e)

        self.attacker = defender

    def getPlayers(self):
        return self.players

    def setCurrentState(self, state):
        self.currentState = state

    def getCurrentState(self):
        return self.currentState

    def getAttackerIndex(self):
        return self.players.index(self.attacker)

    def __setNextAttacker(self):
        maxIndex = len(self.players) - 1
        currentAttackerIndex = self.getAttackerIndex()
        if (maxIndex) == currentAttackerIndex:
            self.attacker = self.players[0]
        else:
            self.attacker = self.players[currentAttackerIndex + 1]

    def __eliminatePlayer(self):
        for player in self.players:
            if player.getCharacter().get_hp() <= 0:
                self.players.remove(player)
