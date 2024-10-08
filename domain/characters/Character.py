import random
from abc import ABC, abstractmethod
import pygame


class Character(ABC):
    def __init__(self, name, hp, ult, luck):
        self.name = name
        self.hp = hp
        self._maxHpValue = self.hp
        self.ult = ult
        self.luck = luck

        # sprites
        self.sprites = {
            'idle': None,
            'attack': None,
            'take_hit': None,
            'death': None,
            'ultimate': None,
            'profile': None
        }

        self.frame_counts = {
            'idle': 0,
            'attack': 0,
            'take_hit': 0,
            'ultimate': 0,
            'death': 0
        }

        self.current_frame = 0
        self.current_action = 'idle'

        self.lightAttack = 0
        self.mediumAttack = 0
        self.heavyAttack = 0

        self.description = ''

    def _attack(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return

    def verify_ult(self):
        return self.ult == 5

    def getUlt(self):
        return self.ult

    def is_alive(self):
        return self.hp > 0

    def get_hp(self):
        return self.hp

    def punish(self, value):
        if value > self.ult:
            self.ult = 0
        else:
            self.ult -= value

    def addUltPoints(self, value):
        if self.ult + value > 5:
            self.ult = 5
        else:
            self.ult += value

    def hasLuck(self):
        chance = random.randint(0, 100)
        return chance <= self.luck

    def changeState(self, new_action):
        if new_action in self.sprites:
            self.current_action = new_action
            self.current_frame = 0

    def getNextSprite(self):
        sheet = self.sprites[self.current_action]
        num_frames = self.frame_counts[self.current_action]

        frame_width = sheet.get_width() // num_frames
        frame_height = sheet.get_height()

        frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        frame_surface.blit(sheet, (0, 0), (self.current_frame * frame_width, 0, frame_width, frame_height))

        self.current_frame += 1

        if self.current_frame >= num_frames:
            if self.current_action != 'death':
                self.current_action = 'idle'
                self.current_frame = 0
            else:
                self.current_frame -= 1

        return frame_surface

    def getProfileImage(self):
        sheet = self.sprites['profile']

        if not sheet:
            return None

        return sheet

    def getAttackMean(self):
        return (self.lightAttack + self.mediumAttack + self.heavyAttack) / 3

    def getLuck(self):
        return self.luck

    def getDescription(self):
        return self.description
