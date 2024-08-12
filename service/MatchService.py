import random
from domain.characters.CharacterDamage import CharacterDamage
from domain.questions.Question import Question

states = {
    'selectingDefender': 1,
    'selectingAttack': 2,
    'waitingAnswer': 3,
    'attacking': 4,
    'end': 5
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
            if not isinstance(self.getPlayer(self.getAttackerIndex()).getCharacter(), CharacterDamage) and ultimate:
                typeAttack()
            else:
                typeAttack(damage, defender.getCharacter())
            return 'true'
        else:
            self.attacker.getCharacter().punish(punish)
            return 'false'

    def attack(self, level, damage, defender, question, answer):
        try:
            if level == 'light':
                isCorrect = self.validateAnswer(question, answer, damage, defender, 3, self.attacker.getCharacter().light_attack)
            elif level == 'medium':
                isCorrect = self.validateAnswer(question, answer, damage, defender, 2, self.attacker.getCharacter().medium_attack)
            elif level == 'heavy':
                isCorrect = self.validateAnswer(question, answer, damage, defender, 1, self.attacker.getCharacter().heavy_attack)
            elif level == 'ultimate':
                isCorrect = self.validateAnswer(question, answer, damage, defender, 5,
                                        self.attacker.getCharacter().ult_attack, True)
            else:
                raise ValueError("Invalid attack type.")
            willEliminate = self.__willEliminate()
            if not willEliminate:
                self.__setNextAttacker()
            else:
                isCorrect = 'death'
            return isCorrect
        except ValueError as e:
            print(e)

    def getPlayers(self):
        return self.players

    def getPlayer(self, index):
        if len(self.players) == 1:
            return self.players[0]
        elif len(self.players) == 0:
            return self.attacker

        return self.players[index]

    def setCurrentState(self, state):
        self.currentState = state

    def getCurrentState(self):
        return self.currentState

    def getAttackerIndex(self):
        if self.attacker not in self.players and len(self.players) > 1:
            self.attacker = random.choice(self.players)
        elif len(self.players) == 1:
            return 0
        return self.players.index(self.attacker)

    def __setNextAttacker(self):
        maxIndex = len(self.players) - 1
        currentAttackerIndex = self.getAttackerIndex()
        if (maxIndex) == currentAttackerIndex:
            self.attacker = self.players[0]
        elif len(self.players) == 1:
            pass
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
        if len(self.players) == 1:
            self.currentState = states['end']
            return True
        return False

