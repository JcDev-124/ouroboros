import pygame

from domain.player.Player import Player
from service.MatchService import MatchService
from view.BaseView import BaseView
from view.Colors import Colors
from view.SelectCharacters import SelectCharacters

class MenuView(BaseView):

    def __init__(self):
        super().__init__()
        self.matchService = MatchService()

    def selectTwoPlayers(self):
        for i in range(2):
            self.matchService.addPlayer(Player(i))

        SelectCharacters(self.matchService).run()
        self._quit()

    def selectThreePlayers(self):
        for i in range(3):
            self.matchService.addPlayer(Player(i))

        SelectCharacters(self.matchService).run()
        self._quit()

    def run(self):
        while self._running:
            self._screen.fill(Colors.BLACK)

            self._drawText('Bem vindo ao OuroBoros', self._font, Colors.WHITE, self._screen, (200, 50))
            self._drawButton('2 Jogadores', self._font,Colors.GRAY, Colors.WHITE,(150, 200), (200, 50),  self.selectTwoPlayers)
            self._drawButton('3 Jogadores', self._font, Colors.GRAY, Colors.WHITE,(150, 350), (200, 50),  self.selectThreePlayers)
            self._drawButton('Sair', self._font, Colors.GRAY, Colors.WHITE,(150, 500), (200, 50),  self._quit)

            self._event()
            pygame.display.update()

        pygame.quit()
