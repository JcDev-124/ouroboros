from abc import ABC, abstractmethod
import pygame


class Character(ABC):
    def __init__(self, name, hp, ult):
        self.name = name
        self.hp = hp
        self._maxHpValue = self.hp
        self.ult = ult

        # Sprites and frame counts for different actions
        self.sprites = {
            'idle': None,
            'attack': None,
            'take_hit': None,
            'death': None
        }

        self.frame_counts = {
            'idle': 0,
            'attack': 0,
            'take_hit': 0,
            'death': 0
        }

        self.current_frame = 0
        self.current_action = 'idle'

    def _attack(self, dmg):
        self.hp -= dmg
        return

    def verify_ult(self):
        return self.ult > 3

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
    def setUlt(self, value):
        if self.ult + value > 5:
            self.ult = 5
        else:
            self.ult += value
    def getNextSprite(self, action):
        # Se a ação mudar, resete a contagem de frames para essa nova ação
        if action != self.current_action:
            self.current_action = action
            self.current_frame = 0

        # Pegue a folha de sprites e o número de frames para a ação atual
        sheet = self.sprites[self.current_action]
        num_frames = self.frame_counts[self.current_action]

        # Calcule a largura e altura de cada frame
        frame_width = sheet.get_width() // num_frames
        frame_height = sheet.get_height()

        # Crie uma superfície para o frame atual
        frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)

        # Copie o frame correspondente da folha de sprites para a superfície
        frame_surface.blit(sheet, (0, 0), (self.current_frame * frame_width, 0, frame_width, frame_height))

        # Atualize o contador de frames
        self.current_frame += 1

        # Se o contador de frames ultrapassar o número de frames disponíveis, volte ao início
        if self.current_frame >= num_frames:
            self.current_frame = 0

        # Retorne o sprite correspondente à ação atual
        return frame_surface


