import pygame
import sys
from abc import ABC, abstractmethod
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
        self._input_active = False
        self._input_text = ""
        self._insertedText = ""
        pygame.display.set_caption("Ouroboros")

        # Initialize input box attributes
        self._input_box = pygame.Rect(100, 100, 140, 32)  # Example position and size
        self._color_inactive = pygame.Color('lightskyblue3')
        self._color_active = pygame.Color('dodgerblue2')
        self._color = self._color_inactive

    def _event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == pygame.MOUSEBUTTONUP:
                self._button_pressed = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self._input_box.collidepoint(event.pos):
                    self._input_active = not self._input_active
                else:
                    self._input_active = False
                self._color = self._color_active if self._input_active else self._color_inactive
            if event.type == pygame.KEYDOWN:
                if self._input_active:
                    if event.key == pygame.K_RETURN:
                        self._insertedText = self._input_text
                        self._input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self._input_text = self._input_text[:-1]
                    else:
                        self._input_text += event.unicode

    def _quit(self):
        pygame.quit()
        sys.exit()

    def _drawText(self, text, font, color, surface, coordinates):
        textObj = font.render(text, True, color)
        textRectangle = textObj.get_rect()
        textRectangle.topleft = coordinates
        surface.blit(textObj, textRectangle)

    def _drawButton(self, text, font, color, hoverColor, coordinates, size, action=None, parameters=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if coordinates[0] + size[0] > mouse[0] > coordinates[0] and coordinates[1] + size[1] > mouse[1] > coordinates[1]:
            pygame.draw.rect(self._screen, hoverColor, (coordinates[0], coordinates[1], size[0], size[1]))
            if click[0] == 1 and action is not None and not self._button_pressed:
                if parameters is None:
                    action()
                else:
                    action(parameters)
                self._button_pressed = True
        else:
            pygame.draw.rect(self._screen, color, (coordinates[0], coordinates[1], size[0], size[1]))

        self._drawText(text, font, Colors.WHITE, self._screen, coordinates)

    def _drawImage(self, directory, size, coordinates):
        self._screen.blit(pygame.transform.scale(pygame.image.load(directory), size), coordinates)

    def _setCaption(self, caption):
        pygame.display.set_caption(caption)

    def _drawInputBox(self):
        if self._input_active:
            color = self._color_active
        else:
            color = self._color_inactive

        pygame.draw.rect(self._screen, color, self._input_box, 2)

        text_surface = self._font.render(self._input_text, True, Colors.WHITE)
        self._screen.blit(text_surface, (self._input_box.x + 5, self._input_box.y + 5))
        self._input_box.w = max(200, text_surface.get_width() + 10)
