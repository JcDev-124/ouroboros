from domain.characters.Character import Character


class CharacterHealer(Character):

    def __init__(self):
        super().__init__("Asclepio", 1000, 0)
        self.sprite = (f'./assets/cura.png')
        self.nameHeavyAttack = "attack 1 - healer"
        self.nameMediumAttack = "attack 2 - healer"
        self.nameHeavyAttack = "attack 3 - healer"
        self.nameUltimateAttack = "attack 4 - healer"

    def light_attack(self, intensity, character):
        character._attack(10 * intensity)
        return

    def medium_attack(self, intensity, character):
        character._attack(20 * intensity)
        return

    def heavy_attack(self, intensity, character):
        character._attack(30 * intensity)
        return

    def ult_attack(self):
        if not self.verify_ult():
            raise ValueError("Ultimate nao disponivel")
        if self.hp > (self._maxHpValue * 0.4):
            self.hp = self._maxHpValue
        else:
            self.hp += self._maxHpValue * 0.6
        self.ult = 0