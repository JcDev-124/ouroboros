import pygame
import os
import sys
from abc import ABC, abstractmethod
from typing import Iterator, Optional
from PIL import Image

from domain.characters.CharacterTank import CharacterTank
from domain.characters.CharacterHealer import CharacterHealer
from domain.characters.CharacterDamage import CharacterDamage
from view.AudioManager import AudioManager
from view.Colors import Colors

class BaseView(ABC):

    def __init__(self):
        pygame.init()
        self._screenWidth = 1280
        self._screenHeight = 720
        self._fps = 60
        self._screen = pygame.display.set_mode((self._screenWidth, self._screenHeight))
        self._running = True
        self._button_pressed = False
        self._input_active = False
        self._input_text = ""
        self._insertedText = ""
        self._soundButton = False
        self._mainFont = './assets/fonts/mainFont.ttf'
        pygame.display.set_caption("Ouroboros")
        pygame.display.set_icon(pygame.image.load('./assets/icons/favicon.png'))
        self._character_shadow = './assets/images/characters/shadow.png'

        self._input_box = pygame.Rect(100, 100, 140, 32)  # Example position and size
        self._color_inactive = pygame.Color('lightskyblue3')
        self._color_active = pygame.Color('dodgerblue2')
        self._color = self._color_inactive

        self._gif_frame_iterator_bg = None
        self._gif_frame_iterator_char = {}
        self._frame_counter = 0
        self._bg_frame_interval = 10
        self._ch_frame_interval = 5
        self._pygame_image_bg = None
        self._pygame_images_char = {}

        # audio
        self.audio_manager = AudioManager()
        self.audio_manager.load_sound_effect('click', './assets/sounds/confirm1.ogg')
        self.audio_manager.play_background_music('./assets/sounds/background.ogg')

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

    def _drawText(self, text, size, fontDirectory, color, coordinates, offset=None):
        font = pygame.font.Font(fontDirectory, size)
        textObj = font.render(text, True, color)
        textRectangle = textObj.get_rect()
        if offset:
            textRectangle.center = (coordinates[0] + offset[0], coordinates[1] + offset[1])
        else:
            textRectangle.center = coordinates
        self._screen.blit(textObj, textRectangle)

    def _drawTextBox(self, text, size, fontDirectory, color, coordinates, boxSize):
        font = pygame.font.Font(fontDirectory, size)
        words = text.split(' ')
        lines = []
        currentLine = ""

        for word in words:
            testLine = f"{currentLine} {word}".strip()
            if font.size(testLine)[0] <= boxSize[0]:
                currentLine = testLine
            else:
                lines.append(currentLine)
                currentLine = word

        if currentLine:
            lines.append(currentLine)

        yOffset = coordinates[1]
        for line in lines:
            self._drawText(line, size, fontDirectory, color, (coordinates[0], yOffset))
            yOffset += size + (size * 0.15)


    def _drawButton(self, text, fontDirectory, fontSize, fontColor, coordinates, size, image=None, action=None,
                    parameters=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if coordinates[0] + size[0] > mouse[0] > coordinates[0] and coordinates[1] + size[1] > mouse[1] > coordinates[
            1]:
            if image is None:
                pygame.draw.rect(self._screen, Colors.LIGHT_GRAY, (coordinates[0], coordinates[1], size[0], size[1]))
            else:
                self._drawImage(image, size, coordinates)
            self.__drawButtonOverlay(size, coordinates)
            if click[0] == 1 and action is not None and not self._button_pressed:
                self.audio_manager.play_sound_effect('click')
                if parameters is None:
                    action()
                else:
                    action(parameters)
                self._button_pressed = True
        else:
            if image is None:
                pygame.draw.rect(self._screen, Colors.GRAY, (coordinates[0], coordinates[1], size[0], size[1]))
            else:
                self._drawImage(image, size, coordinates)

        self._drawText(text, fontSize, fontDirectory, fontColor,
                       (coordinates[0] + (size[0] / 2), coordinates[1] + (size[1] / 2)))

    def __drawButtonOverlay(self, size, coordinates):
        s = pygame.Surface(size)
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self._screen.blit(s, coordinates)

    def _drawImage(self, directory, size, coordinates):
        self._screen.blit(pygame.transform.scale(pygame.image.load(directory), size), coordinates)

    def _setCaption(self, caption):
        pygame.display.set_caption(caption)

    def _drawInputBox(self):

        if self._input_active:
            border_color = Colors.ATTACK_BAR
        else:
            border_color = (64,58,44)

        fill_color = Colors.BG_BAR

        self._input_box.w = 150
        self._input_box.h = 25

        input_box_x = (self._screenWidth - self._input_box.w) // 2
        input_box_y = self._screenHeight - self._input_box.h - 60

        self._input_box.topleft = (input_box_x, input_box_y)

        pygame.draw.rect(self._screen, fill_color, self._input_box)

        border_thickness = 3
        pygame.draw.rect(self._screen, border_color, self._input_box, border_thickness)

        text_surface = pygame.font.Font(self._mainFont, 14).render(self._input_text, True, Colors.WHITE)
        self._screen.blit(text_surface, (
            self._input_box.x + 5, self._input_box.y + (self._input_box.h - text_surface.get_height()) // 2))

        self._input_box.w = max(300, text_surface.get_width() + 10)

    def _drawBackground(self, directory, tam, pos):
        if self._gif_frame_iterator_bg is None:
            self._gif_frame_iterator_bg = self._gifFrameExtractor(directory)

        if self._frame_counter % self._bg_frame_interval == 0:
            frame = next(self._gif_frame_iterator_bg)
            frame = frame.convert('RGBA')
            mode = frame.mode
            size = frame.size
            data = frame.tobytes()

            self._pygame_image_bg = pygame.image.fromstring(data, size, mode)

        if self._pygame_image_bg is not None:
            self._screen.blit(pygame.transform.scale(self._pygame_image_bg, tam), pos)

        self._frame_counter += 1

    def _drawCharacter(self, character, action, tam, pos, flip=False):
        character_id = id(character)

        key = (character_id, action)

        if key not in self._pygame_images_char:
            self._pygame_images_char[key] = None

        if self._frame_counter % self._ch_frame_interval == 0:
            frame = character.getNextSprite()
            frame = frame.convert_alpha()
            self._pygame_images_char[key] = frame

        if self._pygame_images_char[key] is not None:
            image = pygame.transform.scale(self._pygame_images_char[key], tam)

            if flip:
                image = pygame.transform.flip(image, True, False)

            self._screen.blit(image, pos)

            shadow_offset = 0.0
            if isinstance(character, CharacterDamage):
                shadow_offset = 0.56
            elif isinstance(character, CharacterHealer):
                shadow_offset = 0.58
            elif isinstance(character, CharacterTank):
                shadow_offset = 0.53

            shadow_size = (int(tam[0] * 0.85), int(tam[1] * 0.2))
            shadow_pos = (pos[0] + ((tam[0] - shadow_size[0]) / 2), pos[1] + int(tam[1] * shadow_offset))
            self._screen.blit(pygame.transform.scale(pygame.image.load(self._character_shadow), shadow_size),
                              shadow_pos)

    def _gifFrameExtractor(self, gif_path: str) -> Iterator[Image.Image]:
        if not os.path.isfile(gif_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {gif_path}")

        gif = Image.open(gif_path)

        while True:
            for frame in range(gif.n_frames):
                gif.seek(frame)
                yield gif.copy()
