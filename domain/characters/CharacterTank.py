import pygame
from domain.characters.Character import Character


class CharacterTank(Character):

    def __init__(self):
        super().__init__("Atlas", 1500, 0, 25)

        self.sprites = {
            'idle': pygame.image.load(f'./assets/images/characters/tank/idle.png'),
            'attack': pygame.image.load(f'./assets/images/characters/tank/attack1.png'),
            'take_hit': pygame.image.load(f'./assets/images/characters/tank/take_hit.png'),
            'death': pygame.image.load(f'./assets/images/characters/tank/death.png'),
            'profile': pygame.image.load(f'./assets/images/characters/tank/profile.png')
        }

        self.frame_counts = {
            'idle': 11,
            'attack': 7,
            'take_hit': 4,
            'death': 11
        }

        self.nameLightAttack = "attack 1 - tank"
        self.nameMediumAttack = "attack 2 - tank"
        self.nameHeavyAttack = "attack 3 - tank"
        self.nameUltimateAttack = "attack 4 - tank"

        self.shield = True

    def light_attack(self, intensity, character):
        if self.hasLuck():
            intensity = intensity * 2
        character._attack(20 * intensity)
        self.addUltPoints(1)
        return

    def medium_attack(self, intensity, character):
        if self.hasLuck():
            intensity = intensity * 2
        character._attack(30 * intensity)
        self.addUltPoints(2)
        return

    def heavy_attack(self, intensity, character):
        if self.hasLuck():
            intensity = intensity * 2
        character._attack(40 * intensity)
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
