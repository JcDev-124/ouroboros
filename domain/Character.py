from abc import ABC, abstractmethod


class Character(ABC):
    def __init__(self, name, hp, ult):
        self.name = name
        self.hp = hp
        self.ult = ult

    @abstractmethod
    def light_attack(self, character):
        pass

    @abstractmethod
    def medium_attack(self, character):
        pass

    @abstractmethod
    def heavy_attack(self, character):
        pass

    @abstractmethod
    def verify_ult(self):
        return self.ult > 3

    @abstractmethod
    def is_alive(self):
        return self.hp > 0