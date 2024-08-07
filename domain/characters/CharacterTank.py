from domain.characters.Character import Character


class CharacterTank(Character):

    def __init__(self):
        super().__init__("Atlas", 1500, 0)
        self.sprite = (f'./assets/tanque.png')
        self.nameHeavyAttack = "attack 1 - tank"
        self.nameMediumAttack = "attack 2 - tank"
        self.nameHeavyAttack = "attack 3 - tank"
        self.nameUltimateAttack = "attack 4 - tank"

    shield = True

    def light_attack(self, intensity, character):
        character._attack(20 * intensity)
        return

    def medium_attack(self, intensity, character):
        character._attack(30 * intensity)
        return

    def heavy_attack(self, intensity, character):
        character._attack(40 * intensity)
        return


    def _attack(self, dmg):
        if self.shield:
            self.shield = False
            raise ValueError("Ataque bloqueado")
        self.hp -= dmg

    def ult_attack(self):
        if not self.verify_ult():
            raise ValueError("Ultimate nao disponivel")

        self.shield = True
        self.ult = 0

