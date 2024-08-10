import pygame
from domain.characters.Character import Character

class CharacterDamage(Character):

    def __init__(self):
        super().__init__("Hercules", 1000, 0)

        self.sprites = {
            'idle': pygame.image.load(f'./assets/images/characters/damage/idle.png'),
            'attack': pygame.image.load(f'./assets/images/characters/damage/attack1.png'),
            'take_hit': pygame.image.load(f'./assets/images/characters/damage/take_hit.png'),
            'death': pygame.image.load(f'./assets/images/characters/damage/death.png')
        }

        self.frame_counts = {
            'idle': 10,
            'attack': 7,
            'take_hit': 3,
            'death': 11
        }

        self.nameLightAttack = "attack 1 - dano"
        self.nameMediumAttack = "attack 2 - dano"
        self.nameHeavyAttack = "attack 3 - dano"
        self.nameUltimateAttack = "attack 4 - dano"

    def light_attack(self, intensity, character):
        character._attack(30 * intensity)
        self.setUlt(1)
        return

    def medium_attack(self, intensity, character):
        character._attack(45 * intensity)
        self.setUlt(2)
        return

    def heavy_attack(self, intensity, character):
        character._attack(60 * intensity)
        self.setUlt(3)
        return

    def ult_attack(self, intensity, character):
        if not self.verify_ult():
            raise ValueError("Ultimate não disponível")

        character._attack((120) * intensity)
        self.ult = 0