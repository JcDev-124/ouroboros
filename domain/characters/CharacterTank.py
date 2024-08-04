from domain.characters.Character import Character


class CharacterTank(Character):

    def __init__(self):
        super().__init__("Atlas", 1000, 0)
        self.sprite = (f'./assets/tanque.png')

    shield = True

    def light_attack(self, dmg, character):
        character._attack(dmg)
        return

    def medium_attack(self, dmg, character):
        character._attack(dmg)
        return

    def heavy_attack(self, dmg, character):
        character._attack(dmg)
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

