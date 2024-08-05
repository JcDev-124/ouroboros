from domain.characters.Character import Character


class CharacterHealer(Character):

    def __init__(self):
        super().__init__("Asclepio", 300, 0)
        self.sprite = (f'./assets/cura.png')
        self.nameHeavyAttack = "attack 1 - healer"
        self.nameMediumAttack =  "attack 2 - healer"
        self.nameHeavyAttack =  "attack 3 - healer"
        self.nameUltimateAttack =  "attack 4 - healer"
    def light_attack(self, dmg, character):
        character._attack(dmg)
        return

    def medium_attack(self, dmg, character):
        character._attack(dmg)
        return

    def heavy_attack(self, dmg, character):
        character._attack(dmg)
        return

    def ult_attack(self):
        if not self.verify_ult():
            raise ValueError("Ultimate nao disponivel")

        self.hp += 20
        self.ult = 0