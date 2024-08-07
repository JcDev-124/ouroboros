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
        self._bg_frame_interval = 8
        self._ch_frame_interval = 3
        while self._running:
            clock = pygame.time.Clock()
            fps = 60

            self._drawText('Seleção de Jogadores', self.fontSize + 2, self._mainFont, Colors.WHITE, (640, 50))
            self._drawBackground('./assets/images/backgrounds/characterSelectionBackground.gif', (self._screenWidth, 490), (0, 0))
            self._drawImage('./assets/images/buttons/menuButton.png', (self._screenWidth, 230), (0, self._screenHeight - 230))

            if self.indexPlayer < len(self.matchService.getPlayers()):
                self.drawCharacterOption(self.indexPlayer + 1)
            else:
                self.drawStartMatchButton()

            self.drawSelectedCharacters()
            self._event()

            pygame.display.update()
            clock.tick(fps)

    def drawCharacterOption(self, index):
        # change if needed
        topGap = 270
        miniatureSize = (200, 200)
        buttonGap = 10
        buttonCorrection = 20
        buttonImage = './assets/images/buttons/menuButton.png'

        # do not change
        dynamicButtonSize = int(((miniatureSize[0] - (buttonGap * 2)) / 3))
        buttonSize = (dynamicButtonSize, int(dynamicButtonSize) * 0.6)

        position = ((self._screenWidth / 2) - ((miniatureSize[0] / 2)), topGap)
        buttonPosition = (position[0], position[1] + miniatureSize[1] - buttonCorrection)

        self._drawCharacter(self.characters[self.indexCharacter].getSprite(), miniatureSize, position)
        self._drawButton(u'\u2190', self._mainFont, self.fontSize, Colors.BLACK, buttonPosition, buttonSize, buttonImage, self.previousCharacter)
        buttonPosition = ((buttonPosition[0] + buttonSize[0] + buttonGap), buttonPosition[1])
        self._drawButton(str(index), self._mainFont, self.fontSize, Colors.BLACK, buttonPosition, buttonSize, buttonImage, self.selectCharacter)
        buttonPosition = ((buttonPosition[0] + buttonSize[0] + buttonGap), buttonPosition[1])
        self._drawButton(u'\u2192', self._mainFont, self.fontSize, Colors.BLACK, buttonPosition, buttonSize, buttonImage, self.nextCharacter)

    def drawSelectedCharacters(self):
        # change if needed
        gapBetween = 10
        miniatureSize = (180, 180)
        barSize = (self._screenWidth, 230)

        # fixed variables
        players = self.matchService.getPlayers()
        numberOfPlayers = len(players)

        totalWidth = (numberOfPlayers * miniatureSize[0]) + ((numberOfPlayers - 1) * gapBetween)
        position = ((self._screenWidth - totalWidth) / 2, (self._screenHeight - barSize[1] + ((barSize[1] - miniatureSize[1]) / 2)))

        for i in range(numberOfPlayers):
            if i > self.indexPlayer:
                break

            character = players[i].getCharacter()
            if character:
                self._drawCharacter(character.getSprite(), miniatureSize, position)
                position = ((position[0] + gapBetween + miniatureSize[0]), position[1])

    def drawStartMatchButton(self):
        # change if needed
        offSet = -15
        topGap = 418
        buttonSize = (160, 55)
        buttonImage = './assets/images/buttons/menuButton.png'

        # do not change
        position = ((self._screenWidth / 2) - (buttonSize[0] / 2) + offSet, topGap)

        self._drawButton('Iniciar partida', self._mainFont, self.fontSize, Colors.BLACK, position, buttonSize, buttonImage, self.startMatch)