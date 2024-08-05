from domain.characters.Character import Character


class CharacterDamage(Character):

    def __init__(self):
        super().__init__("Hercules", 500, 0)
        self.sprite = (f'./assets/dano.png')
        self.nameLightAttack = "attack 1 - dano"
        self.nameMediumAttack = "attack 2 - dano"
        self.nameHeavyAttack =  "attack 3 - dano"
        self.nameUltimateAttack = "attack 4 - dano"

    def light_attack(self, dmg, character):
        character._attack(dmg)
        return

    def medium_attack(self, dmg, character):
        character._attack(dmg)
        return

    def heavy_attack(self, dmg, character):
        character._attack(dmg)
        return

    def ult_attack(self, dmg, character):
        if not self.verify_ult():
            raise ValueError("Ultimate nao disponivel")

        character._attack(dmg * 2)
        self.ult = 0