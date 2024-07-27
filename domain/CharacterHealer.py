from domain.Character import Character


class CharacterHealer(Character):


    def light_attack(self, dmg, character):
        character.attack(dmg)
        return

    def medium_attack(self, dmg, character):
        character.attack(dmg)
        return

    def heavy_attack(self, dmg, character):
        character.attack(dmg)
        return

    def ult_attack(self):
        if not self.verify_ult():
            raise ValueError("Ultimate nao disponivel")

        self.hp += 20
        self.ult = 0