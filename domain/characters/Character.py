from abc import ABC, abstractmethod


class Character(ABC):
    def __init__(self, name, hp, ult):
        self.name = name
        self.hp = hp
        self._maxHpValue = self.hp
        self.ult = ult
        self.sprite = None
        self.spriteRotate = None
        self.nameLightAttack = None
        self.nameMediumAttack = None
        self.nameHeavyAttack = None
        self.nameUltimateAttack = None

    def _attack(self, dmg):
        self.hp -= dmg
        return

    def verify_ult(self):
        return self.ult > 3

    def is_alive(self):
        return self.hp > 0

    def get_hp(self):
        return self.hp

    def getSprite(self):
        return self.sprite

    def getSpriteRotate(self):
        return self.spriteRotate

    def getNameLightAttack(self):
        return self.nameLightAttack

    def getNameMediumAttack(self):
        return self.nameMediumAttack

    def getNameHeavyAttack(self):
        return self.nameHeavyAttack

    def getNameUltimateAttack(self):
        return self.nameUltimateAttack