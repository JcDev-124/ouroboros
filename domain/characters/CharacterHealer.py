import pygame
from domain.characters.Character import Character

class CharacterHealer(Character):

    def __init__(self):
        super().__init__("Asclepio", 1000, 0, 50)

        self.sprites = {
            'idle': pygame.image.load(f'./assets/images/characters/healer/idle.png'),
            'attack': pygame.image.load(f'./assets/images/characters/healer/attack.png'),
            'take_hit': pygame.image.load(f'./assets/images/characters/healer/take_hit.png'),
            'death': pygame.image.load(f'./assets/images/characters/healer/death.png'),
            'ultimate': pygame.image.load(f'./assets/images/characters/healer/ultimate.png'),
            'profile': pygame.image.load(f'./assets/images/characters/healer/profile.png')
        }

        self.frame_counts = {
            'idle': 10,
            'attack': 13,
            'take_hit': 3,
            'ultimate': 8,
            'death': 18
        }

        self.nameLightAttack = 'Toque de Serpente'
        self.nameMediumAttack = 'Incisão'
        self.nameHeavyAttack = 'Lash'
        self.nameUltimateAttack = 'Milagre de Epidauro'

        self.lightAttack = 10
        self.mediumAttack = 20
        self.heavyAttack = 30

        self.description = 'Asclepio combina sabedoria e precisão, capaz de ferir e curar com igual habilidade. Em momentos críticos, ele invoca o Milagre de Epidauro, restaurando sua vitalidade.'

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

    def ult_attack(self):
        if not self.verify_ult():
            raise ValueError("Ultimate não disponível")
        if self.hp > (self._maxHpValue * 0.4):
            self.hp = self._maxHpValue
        else:
            self.hp += self._maxHpValue * 0.6
        self.hp = int(self.hp)
        self.ult = 0
