import random
from domain.characters.CharacterDamage import CharacterDamage
from domain.questions.Question import Question

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

    def validateAnswer(self, question, answer, damage, defender, punish, typeAttack, ultimate=False):
        if question.validate_answer(answer):
            if not isinstance(self.players[self.getAttackerIndex()].getCharacter(), CharacterDamage) and ultimate:
                typeAttack()
            else:
                typeAttack(damage, defender.getCharacter())
        else:
            self.attacker.getCharacter().punish(punish)

    def attack(self, level, damage, defender, question, answer):
        try:
            if level == 'light':
                self.validateAnswer(question, answer, damage, defender, 3, self.attacker.getCharacter().light_attack)
            elif level == 'medium':
                self.validateAnswer(question, answer, damage, defender, 2, self.attacker.getCharacter().medium_attack)
            elif level == 'heavy':
                self.validateAnswer(question, answer, damage, defender, 1, self.attacker.getCharacter().heavy_attack)
            elif level == 'ultimate':
                self.validateAnswer(question, answer, damage, defender, 5,
                                        self.attacker.getCharacter().ult_attack, True)
            else:
                raise ValueError("Invalid attack type.")
            willEliminate = self.__willEliminate()
            if not willEliminate:
                self.__setNextAttacker()
            return willEliminate
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
        if self.attacker not in self.players:
            self.attacker = random.choice(self.players)
        return self.players.index(self.attacker)

    def __setNextAttacker(self):
        maxIndex = len(self.players) - 1
        currentAttackerIndex = self.getAttackerIndex()
        if (maxIndex) == currentAttackerIndex:
            self.attacker = self.players[0]
        else:
            self.attacker = self.players[currentAttackerIndex + 1]

    def __willEliminate(self):
        for player in self.players:
            if player.getCharacter().get_hp() <= 0:
                return True

        return False

    def eliminatePlayer(self, player):
        self.players.remove(player)
        self.__setNextAttacker()

    def gameFinished(self):
        return len(self.players) == 1
