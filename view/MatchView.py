import pygame

from view.BaseView import BaseView
from view.Colors import Colors
from service.MatchService import states
class MatchView(BaseView):
    matchService = None
    indexAttacker = 0
    indexDefender = 0
    def __init__(self):
        super().__init__()

    def run(self, matchService):
        self.matchService = matchService
        gameBarSize = (self._screenWidth, 220)
        gameBarSurface = pygame.Surface(gameBarSize)
        while self._running:
            self._screen.fill(Colors.BLACK)
            gameBarSurface.fill(Colors.WHITE)
            self._screen.blit(gameBarSurface, (0, (self._screenHeight - gameBarSize[1])))

            self.drawAttackerMiniature()

            if self.matchService.getCurrentState() == states['selectingDefender']:
                self.drawDefenderOptions()
            elif self.matchService.getCurrentState() == states['selectingAttacker']:
                self.drawAttackOptions()

            self.drawFighters()


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

    def selectedDefender(self, indexDefender):
        self.indexDefender = indexDefender
        self.matchService.setCurrentState(states['selectingAttack'])



    def drawDefenderOptions(self):
        players = self.matchService.getPlayers()
        x = 350
        for i, player in enumerate(players):
            if i != self.indexAttacker:
                self._drawButton("", self._font, Colors.GRAY, Colors.WHITE, (x, 510),
                                 (150, 150), self.selectedDefender, i)
                self._drawImage(player.getCharacter().getSprite(), (150, 150), (x, 510))

                x += 160

    def drawFighters(self):
        attacker = self.matchService.getPlayers()[self.indexAttacker].getCharacter()
        defender = self.matchService.getPlayers()[self.indexDefender].getCharacter()
        self._drawImage(attacker.getSprite(), (200, 200), (300, 250))
        self._drawImage(defender.getSprite(), (200, 200), (600, 250))
