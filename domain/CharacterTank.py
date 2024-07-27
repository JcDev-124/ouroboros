from domain.Character import Character


class CharacterTank(Character):

    shield = True

    def light_attack(self, dmg, character):
        character.attack(dmg)
        return

    def medium_attack(self, dmg, character):
        character.attack(dmg)
        return

    def heavy_attack(self, dmg, character):
        character.attack(dmg)
        return


    def attack(self, dmg):
        if self.shield:
            self.shield = False
            raise ValueError("Ataque bloqueado")
        self.hp -= dmg

    def ult_attack(self):
        if not self.verify_ult():
            raise ValueError("Ultimate nao disponivel")

        self.shield = True
        self.ult = 0

