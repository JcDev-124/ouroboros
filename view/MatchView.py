import pygame

from view.BaseView import BaseView
from view.Colors import Colors

class MatchView(BaseView):

    def __init__(self):
        super().__init__()

    def run(self):
        while self._running:
            self._screen.fill(Colors.BLACK)

            self._drawText('Bem vindo ao OuroBoros', self._font, Colors.WHITE, self._screen, (200, 50))

            self._drawButton('Teste Nova Classe', self._font, Colors.GRAY, Colors.WHITE, (150, 200), (200, 50))

            self._event()

            pygame.display.update()

        pygame.quit()