from abc import ABC, abstractmethod


class Character(ABC):
    def __init__(self, name, hp, ult):
        self.name = name
        self.hp = hp
        self.ult = ult


    def attack(self, dmg):
        self.hp -= dmg
        return


    def verify_ult(self):
        return self.ult > 3


    def is_alive(self):
        return self.hp > 0


    def get_hp(self):
        return self.hp

