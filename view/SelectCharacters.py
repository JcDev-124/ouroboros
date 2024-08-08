import pygame

from domain.characters.CharacterDamage import CharacterDamage
from domain.characters.CharacterHealer import CharacterHealer
from domain.characters.CharacterTank import CharacterTank
from view.BaseView import BaseView
from view.MatchView import MatchView
from view.Colors import Colors


class SelectCharacters(BaseView):
    indexPlayer = 0
    indexCharacter = 0
    indexesSprite = [0, 0, 0]
    fontSize = 16
    characters = [CharacterDamage(), CharacterHealer(), CharacterTank()]
    selectedPositions = []
    x = 250

    def __init__(self, matchService):
        self.matchService = matchService
        super().__init__()

    def previousCharacter(self):
        if self.indexCharacter == 0:
            self.indexCharacter = len(self.characters) - 1
        else:
            self.indexCharacter -= 1

    def nextCharacter(self):
        if self.indexCharacter == len(self.characters) - 1:
            self.indexCharacter = 0
        else:
            self.indexCharacter += 1

    def selectCharacter(self):

        funCharacter = {
            0: CharacterDamage(),
            1: CharacterHealer(),
            2: CharacterTank()
        }

        selectedCharacter = None
        if self.indexCharacter in funCharacter:
            selectedCharacter = funCharacter[self.indexCharacter]

        if self.indexPlayer < len(self.matchService.getPlayers()):
            self.matchService.getPlayers()[self.indexPlayer].setCharacter(selectedCharacter)
            self.indexesSprite[self.indexPlayer] = self.indexCharacter

            character = self.matchService.getPlayers()[self.indexPlayer].getCharacter()
            self._drawImage(character.getSprite(), (250, 250), (self.x, 450))
            self._drawButton(str(self.indexPlayer + 1), self._mainFont, 10, Colors.BLACK, (self.x + 100, 630), (40, 40))
            self.x += 250
            self.indexPlayer += 1

    def startMatch(self):
        try:
            self.checkSelectedPlayers()
        except ValueError as e:
            self._drawText(e, self.fontSize + 2, self._mainFont, Colors.WHITE, (640, 50))

            return

        MatchView().run(self.matchService)
        self._quit()

    def checkSelectedPlayers(self):
        if len(self.matchService.getPlayers()) != self.indexPlayer:
            message = "Aguardando Jogador " + str(self.indexPlayer + 1) + "."
            raise ValueError(message)

    def run(self):
        self._setCaption("Match")
        gameBarSize = (self._screenWidth, 220)
        gameBarSurface = pygame.Surface(gameBarSize)
        gameBarSurface.fill(Colors.CYAN)
        self._screen.blit(gameBarSurface, (0, (self._screenHeight - gameBarSize[1])))
        self._screen.fill(Colors.BLACK)
        while self._running:

            self._drawText('Seleção de Jogadores', self.fontSize + 2, self._mainFont, Colors.WHITE, (640, 50))
            self._drawCharacter('./assets/champion-selection/background.gif', (1280, 500), (0, 0))


            if self.indexPlayer < len(self.matchService.getPlayers()):
                self._drawCharacter(self.characters[self.indexCharacter].getSprite(), (350, 350), (450, 225))
                self._drawButton('<', self._mainFont, self.fontSize, Colors.LIGHT_GRAY, (525, 460), (48, 40), None,
                                 self.previousCharacter)
                self._drawButton(str(1), self._mainFont, self.fontSize, Colors.LIGHT_GRAY, (600, 460), (48, 40),
                                 None, self.selectCharacter)
                self._drawButton('>', self._mainFont, self.fontSize, Colors.LIGHT_GRAY, (675, 460), (48, 40), None,
                                 self.nextCharacter)
            else:
                self._drawButton('Iniciar partida', self._mainFont, self.fontSize, Colors.LIGHT_GRAY, (525, 675),
                                 (200, 50), None,
                                 self.startMatch)
            self._event()

            pygame.display.update()
