from domain.characters.Character import Character


class CharacterDamage(Character):

    def __init__(self):
        super().__init__("Hercules", 800, 0)
        self.sprite = (f'./assets/champion-selection/damage.gif')
        self.spriteRotate = (f'./assets/champion-selection/damageRotate.gif')
        self.nameLightAttack = "attack 1 - dano"
        self.nameMediumAttack = "attack 2 - dano"
        self.nameHeavyAttack = "attack 3 - dano"
        self.nameUltimateAttack = "attack 4 - dano"

    def light_attack(self, intensity, character):
        character._attack(30 * intensity)
        return

    def medium_attack(self, intensity, character):
        character._attack(45 * intensity)
        return

    def heavy_attack(self, intensity, character):
        character._attack(60 * intensity)
        return

    def ult_attack(self, intensity, character):
        if not self.verify_ult():
            raise ValueError("Ultimate nao disponivel")

        character._attack((120) * intensity)
        self.ult = 0