import pygame
from domain.characters.Character import Character


class CharacterDamage(Character):

    def __init__(self):
        super().__init__("Hercules", 800, 0, 10)

        self.sprites = {
            'idle': pygame.image.load(f'./assets/images/characters/damage/idle.png'),
            'attack': pygame.image.load(f'./assets/images/characters/damage/attack.png'),
            'take_hit': pygame.image.load(f'./assets/images/characters/damage/take_hit.png'),
            'death': pygame.image.load(f'./assets/images/characters/damage/death.png'),
            'ultimate': pygame.image.load(f'./assets/images/characters/damage/ultimate.png'),
            'profile': pygame.image.load(f'./assets/images/characters/damage/profile.png')
        }

        self.frame_counts = {
            'idle': 10,
            'attack': 6,
            'take_hit': 3,
            'ultimate': 9,
            'death': 11
        }

        self.nameLightAttack = 'Golpe de Leão'
        self.nameMediumAttack = 'Martelo de Hefesto'
        self.nameHeavyAttack = '13º Trabalho'
        self.nameUltimateAttack = 'Ira de Zeus'

        self.lightAttack = 30
        self.mediumAttack = 45
        self.heavyAttack = 60

        self.description = 'Hercules é o gigante da batalha, esmagando tudo em seu caminho com força devastadora. Quando a fúria atinge seu auge, ele libera a Ira de Zeus, dobrando o dano e obliterando seus adversários.'

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

    def ult_attack(self, intensity, character):
        if not self.verify_ult():
            raise ValueError("Ultimate não disponível")

        character._attack((self.heavyAttack * 2) * intensity)
        self.ult = 0
