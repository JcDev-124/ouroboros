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
    teste = CharacterHealer()
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
            self.indexCharacter = 0

    def startMatch(self):
        try:
            self.checkSelectedPlayers()
        except ValueError as e:
            self._drawText(e, self.fontSize + 2, self._mainFont, Colors.WHITE, (640, 50))
            return

        MatchView(self.matchService).run()
        self._quit()

    def checkSelectedPlayers(self):
        if len(self.matchService.getPlayers()) != self.indexPlayer:
            message = "Aguardando Jogador " + str(self.indexPlayer + 1) + "."
            raise ValueError(message)

    def run(self):
        self._bg_frame_interval = 9
        self._ch_frame_interval = 5
        while self._running:
            clock = pygame.time.Clock()

            self._drawBackground('./assets/images/backgrounds/characterSelectionBackground.gif', (self._screenWidth, 490), (0, 0))
            self._drawImage('./assets/images/ui/gameBar.png', (self._screenWidth, 230), (0, self._screenHeight - 230))
            self._drawImage('./assets/images/ui/transition.png', (self._screenWidth, 26),
                            (0, self._screenHeight - (230 + 25)))

            if self.indexPlayer < len(self.matchService.getPlayers()):
                self.drawCharacterOption(self.indexPlayer + 1)
            else:
                self.drawStartMatchButton()

            self.drawSelectedCharacters()

            self._event()

            pygame.display.update()
            clock.tick(self._fps)

    def drawCharacterOption(self, index):
        # change if needed
        leftOffset = -30
        topGap = 20
        miniatureSize = (650, 650)

        buttonSize = (65, 45)
        buttonGap = 10
        buttonTopOffset = 425
        buttonLeftOffset = -15
        buttonImage = './assets/images/ui/button.png'

        position = (leftOffset + (self._screenWidth / 2) - ((miniatureSize[0] / 2)), topGap)
        buttonPosition = (buttonLeftOffset + (self._screenWidth / 2) - ((buttonSize[0] * 3) + (buttonGap * 2)) / 2, buttonTopOffset)

        self._drawCharacter(self.characters[self.indexCharacter], 'idle', miniatureSize, position)
        self._drawButton(u'\u2190', self._mainFont, self.fontSize, Colors.BLACK, buttonPosition, buttonSize, buttonImage, self.previousCharacter)
        buttonPosition = ((buttonPosition[0] + buttonSize[0] + buttonGap), buttonPosition[1])
        self._drawButton(str(index), self._mainFont, self.fontSize, Colors.BLACK, buttonPosition, buttonSize, buttonImage, self.selectCharacter)
        buttonPosition = ((buttonPosition[0] + buttonSize[0] + buttonGap), buttonPosition[1])
        self._drawButton(u'\u2192', self._mainFont, self.fontSize, Colors.BLACK, buttonPosition, buttonSize, buttonImage, self.nextCharacter)

    def drawSelectedCharacters(self):
        # change if needed
        gapBetween = 20
        miniatureSize = (200, 200)
        barSize = (self._screenWidth, 230)
        imageOffset = 15

        # fixed variables
        imageSize = (miniatureSize[0] - (imageOffset * 2), miniatureSize[1] - (imageOffset * 2))
        players = self.matchService.getPlayers()
        numberOfPlayers = len(players)

        totalWidth = (numberOfPlayers * miniatureSize[0]) + ((numberOfPlayers - 1) * gapBetween)
        position = ((self._screenWidth - totalWidth) / 2, (self._screenHeight - barSize[1] + ((barSize[1] - miniatureSize[1]) / 2)))
        imagePosition = (position[0] + imageOffset, position[1] + imageOffset)

        for i in range(numberOfPlayers):
            if i > self.indexPlayer:
                break

            character = players[i].getCharacter()
            if character:
                self._drawImage('./assets/images/ui/characterBackground.png', miniatureSize, position)
                self._screen.blit(pygame.transform.scale(character.getProfileImage(), imageSize), imagePosition)
                self._drawText(str(i + 1), 20, './assets/fonts/titleFont.ttf', Colors.BLACK, imagePosition, (10, 10))
                position = ((position[0] + gapBetween + miniatureSize[0]), position[1])
                imagePosition = (position[0] + imageOffset, position[1] + imageOffset)

    def drawStartMatchButton(self):
        # change if needed
        offSet = -15
        topGap = 415
        buttonSize = (180, 60)
        buttonImage = './assets/images/ui/button.png'

        # do not change
        position = ((self._screenWidth / 2) - (buttonSize[0] / 2) + offSet, topGap)

        self._drawButton('Iniciar partida', self._mainFont, self.fontSize, Colors.BLACK, position, buttonSize, buttonImage, self.startMatch)