import random


class MatchService:
    players = []

    def __init__(self):
        self.grantCharacter = None
        self.attacker = None

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
                self.attacker.getCharacter().ultimate_attack(damage, defender.getCharacter())
            else:
                raise ValueError("Invalid attack type.")
        except ValueError as e:
            print(e)

        self.attacker = defender
