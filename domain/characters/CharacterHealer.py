import pygame
from domain.characters.Character import Character

class CharacterHealer(Character):

    def __init__(self):
        super().__init__("Asclepio", 1000, 0)

        self.sprites = {
            'idle': pygame.image.load(f'./assets/images/characters/healer/idle.png'),
            'attack': pygame.image.load(f'./assets/images/characters/healer/attack1.png'),
            'take_hit': pygame.image.load(f'./assets/images/characters/healer/take_hit.png'),
            'death': pygame.image.load(f'./assets/images/characters/healer/death.png'),
            'profile': pygame.image.load(f'./assets/images/characters/healer/profile.png')
        }

        self.frame_counts = {
            'idle': 10,
            'attack': 13,
            'take_hit': 3,
            'death': 18
        }

        self.nameLightAttack = "attack 1 - healer"
        self.nameMediumAttack = "attack 2 - healer"
        self.nameHeavyAttack = "attack 3 - healer"
        self.nameUltimateAttack = "attack 4 - healer"

    def light_attack(self, intensity, character):
        character._attack(10 * intensity)
        self.addUltPoints(1)
        return

    def medium_attack(self, intensity, character):
        character._attack(20 * intensity)
        self.addUltPoints(2)
        return

    def heavy_attack(self, intensity, character):
        character._attack(30 * intensity)
        self.addUltPoints(3)
        return

    def ult_attack(self):
        if not self.verify_ult():
            raise ValueError("Ultimate não disponível")
        if self.hp > (self._maxHpValue * 0.4):
            self.hp = self._maxHpValue
        else:
            self.hp += self._maxHpValue * 0.6
        self.ult = 0
