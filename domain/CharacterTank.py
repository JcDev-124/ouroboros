from domain.Character import Character


class CharacterTank(Character):

    def light_attack(self, character):
        character.hp -= 100
        return

    def medium_attack(self, character):
        character.hp -= 100
        return

    def heavy_attack(self, character):
        character.hp -= 100
        return
