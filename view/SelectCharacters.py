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
    characters = [CharacterDamage(), CharacterHealer(), CharacterTank()]
    selectedPositions = []
    fontSize = 16

    maxStats = None

    gameBarSize = None

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
        self._bg_frame_interval = 5
        self._ch_frame_interval = 3
        self.gameBarSize = (self._screenWidth, 230)
        self.maxStats = self.getMaxStats()
        while self._running:
            clock = pygame.time.Clock()

            self._drawBackground('./assets/images/backgrounds/characterSelectionBackground.gif', (self._screenWidth, 490), (0, 0))
            self._drawImage('./assets/images/ui/gameBar.png', (self._screenWidth, self.gameBarSize[1]), (0, self._screenHeight - self.gameBarSize[1]))
            self._drawImage('./assets/images/ui/transition.png', (self._screenWidth, 26),
                            (0, self._screenHeight - (self.gameBarSize[1] + 25)))

            if self.indexPlayer < len(self.matchService.getPlayers()):
                self.drawCharacterStats()
                self.drawCharacterOption(self.indexPlayer + 1)
            else:
                self.drawStartMatchButton()

            self.drawSelectedCharacters()

            self._event()

            pygame.display.update()
            clock.tick(self._fps)

    def getMaxStats(self):
        maxStats = (0, 0, 0)
        for stat in range(3):
            for i, character in enumerate(self.characters):
                if stat == 0:
                    maxStats = (max(character.get_hp(), maxStats[stat]), maxStats[1], maxStats[2])
                elif stat == 1:
                    maxStats = (maxStats[0], max(character.getAttackMean(), maxStats[1]), maxStats[2])
                elif stat == 2:
                    maxStats = (maxStats[0], maxStats[1], max(character.getLuck(), maxStats[2]))

        return maxStats

    def drawCharacterStats(self):
        # size
        overlaySize = (350, 420)
        offset = ((self._screenHeight - self.gameBarSize[1]) - overlaySize[1]) / 2
        coordinates = (self._screenWidth - overlaySize[0] - offset, offset)
        # character name and description
        nameSize = 35
        descriptionSize = 18
        fontSpacingMultiplier = 0.85
        topMargin = 20
        sMargin = 20

        # stats bar
        barSizeMultiplier = 0.90
        # do not change
        barAspectRatio = 0.4278
        barSize = (overlaySize[0] * barSizeMultiplier, overlaySize[0] * barSizeMultiplier * barAspectRatio)
        barCoordinates = (coordinates[0] + (overlaySize[0] - barSize[0]) / 2,
                          coordinates[1] + nameSize + (nameSize * fontSpacingMultiplier))

        # do not change
        fillSize = (barSize[0] * 0.905, barSize[1] * 0.209)
        fillOffset = (barSize[0] * 0.0746, barSize[1] * 0.035)
        fillGap = barSize[1] * 0.1164
        fillCoordinates = (barCoordinates[0] + fillOffset[0], barCoordinates[1] + fillOffset[1])

        # do not change
        self._drawImage('./assets/images/ui/characterBackground.png', overlaySize, coordinates)
        self._drawText(self.characters[self.indexCharacter].name, nameSize, './assets/fonts/titleFont.ttf',
                       Colors.BLACK,
                       (coordinates[0] + overlaySize[0] / 2, coordinates[1] + (nameSize * fontSpacingMultiplier)),
                       (0, nameSize * 0.2))

        # character stats
        character = self.characters[self.indexCharacter]
        hp = character.get_hp()
        attack = character.getAttackMean()
        luck = character.getLuck()

        # fill stats bar
        # hp
        statsFill = (fillSize[0] * (hp / self.maxStats[0]))
        pygame.draw.rect(self._screen, Colors.BG_BAR,
                         (fillCoordinates[0], fillCoordinates[1], fillSize[0], fillSize[1]))
        pygame.draw.rect(self._screen, Colors.HP_BAR, (fillCoordinates[0], fillCoordinates[1], statsFill, fillSize[1]))
        fillCoordinates = (fillCoordinates[0], fillCoordinates[1] + fillSize[1] + fillGap)
        # attack
        statsFill = (fillSize[0] * (attack / self.maxStats[1]))
        pygame.draw.rect(self._screen, Colors.BG_BAR,
                         (fillCoordinates[0], fillCoordinates[1], fillSize[0], fillSize[1]))
        pygame.draw.rect(self._screen, Colors.ATTACK_BAR,
                         (fillCoordinates[0], fillCoordinates[1], statsFill, fillSize[1]))
        fillCoordinates = (fillCoordinates[0], fillCoordinates[1] + fillSize[1] + fillGap)
        # luck
        statsFill = (fillSize[0] * (luck / self.maxStats[2]))
        pygame.draw.rect(self._screen, Colors.BG_BAR,
                         (fillCoordinates[0], fillCoordinates[1], fillSize[0], fillSize[1]))
        pygame.draw.rect(self._screen, Colors.LUCK_BAR,
                         (fillCoordinates[0], fillCoordinates[1], statsFill, fillSize[1]))

        self._drawImage('./assets/images/ui/statsBar.png', barSize, barCoordinates)

        # description
        description = character.getDescription()
        descriptionBoxSize = (overlaySize[0] - sMargin * 2, overlaySize[1] - barCoordinates[1] - barSize[1] - sMargin * 2)
        descriptionCoordinates = (coordinates[0] + sMargin + descriptionBoxSize[0] / 2, barCoordinates[1] + barSize[1] + topMargin)
        self._drawTextBox(description, descriptionSize, './assets/fonts/mainFont.ttf', Colors.BLACK,
                          descriptionCoordinates, descriptionBoxSize)

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