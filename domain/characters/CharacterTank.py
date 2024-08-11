import pygame
from domain.characters.Character import Character

class CharacterTank(Character):

    def __init__(self):
        super().__init__("Atlas", 1500, 0, 25)

        self.sprites = {
            'idle': pygame.image.load(f'./assets/images/characters/tank/idle.png'),
            'attack': pygame.image.load(f'./assets/images/characters/tank/attack.png'),
            'take_hit': pygame.image.load(f'./assets/images/characters/tank/take_hit.png'),
            'death': pygame.image.load(f'./assets/images/characters/tank/death.png'),
            'ultimate': pygame.image.load(f'./assets/images/characters/tank/ultimate.png'),
            'profile': pygame.image.load(f'./assets/images/characters/tank/profile.png')
        }

        self.frame_counts = {
            'idle': 11,
            'attack': 7,
            'take_hit': 4,
            'ultimate': 7,
            'death': 11
        }

        self.nameLightAttack = 'Muralha de Titã'
        self.nameMediumAttack = 'Apoio do Céu'
        self.nameHeavyAttack = 'Avalanche Titânica'
        self.nameUltimateAttack = 'Cúpula'

        self.lightAttack = 20
        self.mediumAttack = 30
        self.heavyAttack = 40

        self.shield = False

        self.description = 'Atlas é o pilar da defesa, suportando os golpes mais poderosos com resiliência inquebrável. Em situações extremas, ele levanta a Barreira do Firmamento, bloqueando o próximo ataque.'

    def light_attack(self, intensity, character):
        if self.hasLuck():
            intensity = intensity * 2
        character._attack(self.lightAttack * intensity)
        self.addUltPoints(1)
        return

    def medium_attack(self, intensity, character):
        if self.hasLuck():
            intensity = intensity * 2
        character._attack(self.mediumAttack * intensity)
        self.addUltPoints(2)
        return

    def heavy_attack(self, intensity, character):
        if self.hasLuck():
            intensity = intensity * 2
        character._attack(self.heavyAttack * intensity)
        self.addUltPoints(3)
        return

    def _attack(self, dmg, ult=0):
        if self.shield:
            self.shield = False
            raise ValueError("Ataque bloqueado")
        self.hp -= dmg

    def ult_attack(self):
        if not self.verify_ult():
            raise ValueError("Ultimate não disponível")
        self.shield = True
        self.ult = 0
