import pygame

from view.BaseView import BaseView
from view.Colors import Colors

class MatchView(BaseView):

    matchService = None
    indexAttacker = 0
    def __init__(self):
        super().__init__()

    def run(self, matchService):
        self.matchService = matchService
        while self._running:
            self._screen.fill(Colors.BLACK)
            self.drawDefenderOptions()
            self.drawAttackerMiniature()

            self._event()

            pygame.display.update()

        pygame.quit()

    def drawAttackOptions(self):
        attacker = self.matchService.getPlayers()[self.indexAttacker].getCharacter()

        self._drawButton(attacker.getNameLightAttack(), self._font, Colors.GRAY, Colors.WHITE, (450, 500), (300, 70))
        self._drawButton(attacker.getNameMediumAttack(), self._font, Colors.GRAY, Colors.WHITE, (760, 500), (300, 70))
        self._drawButton(attacker.getNameHeavyAttack(), self._font, Colors.GRAY, Colors.WHITE, (450, 580), (300, 70))
        self._drawButton(attacker.getNameUltimateAttack(), self._font, Colors.GRAY, Colors.WHITE, (760, 580), (300, 70))

    def drawAttackerMiniature(self):
        attacker = self.matchService.getPlayers()[self.indexAttacker].getCharacter()

        self._drawImage(attacker.getSprite(), (200, 200), (75, 510))

    def printA(self, A):
        print(A)

    def drawDefenderOptions(self):
        players = self.matchService.getPlayers()
        x = 350
        for i, player in enumerate(players):
            if i != self.indexAttacker:
                self._drawButton("", self._font, Colors.GRAY, Colors.WHITE, (x, 510),
                                 (150, 150), self.printA, i)
                self._drawImage(player.getCharacter().getSprite(), (150, 150), (x, 510))

                x += 160