from abc import ABC, abstractmethod
import pygame
import sys

from view.Colors import Colors

class BaseView(ABC):

    def __init__(self):
        pygame.init()
        self._screenWidth = 1280
        self._screenHeight = 720
        self._screen = pygame.display.set_mode((self._screenWidth, self._screenHeight))
        self._font = pygame.font.Font(None, 30)
        self._running = True
        self._button_pressed = False

        pygame.display.set_caption("Ouroboros")

    def _event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == pygame.MOUSEBUTTONUP:
                self._button_pressed = False

    def _quit(self):
        pygame.quit()
        sys.exit()

    def _drawText(self, text, font, color, surface, coordinates):
        textObj = font.render(text, True, color)
        textRectangle = textObj.get_rect()
        textRectangle.topleft = coordinates
        surface.blit(textObj, textRectangle)

    def _drawButton(self, text, font, color, hoverColor, coordinates, size, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if coordinates[0] + size[0] > mouse[0] > coordinates[0] and coordinates[1] + size[1] > mouse[1] > coordinates[1]:
            pygame.draw.rect(self._screen, hoverColor, (coordinates[0], coordinates[1], size[0], size[1]))
            if click[0] == 1 and action is not None and not self._button_pressed:
                action()
                self._button_pressed = True
        else:
            pygame.draw.rect(self._screen, color, (coordinates[0], coordinates[1], size[0], size[1]))

        self._drawText(text, font, Colors.WHITE, self._screen, coordinates)

    def _drawImage(self, directory, size, coordinates):
        self._screen.blit(pygame.transform.scale(pygame.image.load(directory), size), coordinates)

    def _setCaption(self, caption):
        pygame.display.set_caption(caption)

