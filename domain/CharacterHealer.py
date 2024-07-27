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
