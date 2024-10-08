import sys

import pygame

from domain.player.Player import Player
from service.MatchService import MatchService
from view.BaseView import BaseView
from view.Colors import Colors

modulename = 'MatchView'
if modulename not in sys.modules:
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
        self._bg_frame_interval = 9
        while self._running:
            clock = pygame.time.Clock()

            self._drawBackground('./assets/images/backgrounds/menuBackground.gif', (self._screenWidth, self._screenHeight), (0, 0))
            self._drawImage('./assets/images/backgrounds/menuBlur.png', (708, 125), (286, 53))
            self._drawText('OuroBoros', 124, './assets/fonts/titleFont.ttf', Colors.WHITE, (self._screenWidth / 2, 115))

            self.drawOptions((280, 80))

            self._event()

            pygame.display.update()
            clock.tick(self._fps)

        pygame.quit()

    def drawOptions(self, optionSize):
        font = './assets/fonts/mainFont.ttf'
        fontSize = 28
        image = './assets/images/ui/button.png'

        leftGap = 15
        betweenGap = 10
        x = (self._screenWidth - leftGap - optionSize[0])
        y = (self._screenHeight - 20 - optionSize[1])

        self._drawButton('Sair', font, fontSize, Colors.BLACK, (x, y), optionSize, image, self._quit)
        y -= (betweenGap + optionSize[1])

        self._drawButton('3 Players', font, fontSize, Colors.BLACK, (x, y), optionSize, image, self.selectThreePlayers)
        y -= (betweenGap + optionSize[1])

        self._drawButton('2 Players', font, fontSize, Colors.BLACK, (x, y), optionSize, image, self.selectTwoPlayers)




