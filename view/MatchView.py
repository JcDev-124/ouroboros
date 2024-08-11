import pygame

from domain.characters.CharacterDamage import CharacterDamage
from domain.questions.Questions import Questions
from service.MatchService import states
from view.BaseView import BaseView
from view.Colors import Colors

class MatchView(BaseView):
    matchService = None
    indexAttacker = 0
    indexDefender = 0
    questionLevel = None
    attackLevel = None
    questionReceived = None

    # design constants
    gameBarSize = None
    characterBgSize = None

    waitingState = 60
    deathCycle = False
    temporaryDefender = None

    # game constants
    attackIntensity = 5

    def __init__(self, matchService):
        self.matchService = matchService
        self.matchService.startMatch()
        super().__init__()

    def run(self):
        self._bg_frame_interval = 3
        self._ch_frame_interval = 3
        self.audio_manager.play_background_music('./assets/sounds/fight.ogg')

        # design constants
        self.gameBarSize = (self._screenWidth, 230)
        self.characterBgSize = (200, 200)

        while self._running:
            clock = pygame.time.Clock()

            self._drawBackground('./assets/images/backgrounds/matchBackground.gif',
                                 (self._screenWidth, 490), (0, 0))

            # game bar elements
            self._drawImage('./assets/images/ui/gameBar.png', (self._screenWidth, 230), (0, self._screenHeight - 230))
            self._drawImage('./assets/images/ui/transition.png', (self._screenWidth, 26),
                            (0, self._screenHeight - (230 + 25)))

            self.drawPlayersMiniature()
            self.drawPlayersStats()

            # fighters
            self.drawFighters()

            # stats overlay
            self.drawHPAllPlayers()

            # options
            if self.matchService.getCurrentState() == states['selectingDefender']:
                self.drawDefenderOptions()
            elif self.matchService.getCurrentState() == states['selectingAttack']:
                self.drawAttackOptions()
            elif self.matchService.getCurrentState() == states['waitingAnswer']:
                self.drawQuestion()
                self._drawInputBox()

                if self._insertedText != '':
                    self.matchService.setCurrentState(states['attacking'])

            elif self.matchService.getCurrentState() == states['attacking']:
                self.attack()

            if self.matchService.gameFinished() and not self.deathCycle:
                self.drawEndGame()

            self._event()

            pygame.display.update()
            clock.tick(self._fps)

    def drawPlayersMiniature(self):
        # fixed values
        bgOffset = (self.gameBarSize[1] - self.characterBgSize[1]) / 2
        chOffset = 10
        miniatureSize = (self.characterBgSize[0] - (chOffset * 2), self.characterBgSize[1] - (chOffset * 2))

        # attacker
        players = self.matchService.getPlayers()
        imageCoordinates = (bgOffset, bgOffset + (self._screenHeight - self.gameBarSize[1]))
        self._drawImage('./assets/images/ui/characterBackground.png', self.characterBgSize, imageCoordinates)
        attacker = self.matchService.getPlayer(self.matchService.getAttackerIndex()).getCharacter()
        coordinates = (chOffset + bgOffset, chOffset + bgOffset + (self._screenHeight - self.gameBarSize[1]))
        self._screen.blit(pygame.transform.scale(attacker.getProfileImage(), miniatureSize), coordinates)
        self._drawText(str(self.matchService.getAttackerIndex() + 1), 25, './assets/fonts/titleFont.ttf', Colors.BLACK, imageCoordinates, (20, 20))

        # defender
        if self.matchService.getCurrentState() == states['selectingAttack']:
            imageCoordinates = (self._screenWidth - self.characterBgSize[0] - bgOffset, bgOffset + (self._screenHeight - self.gameBarSize[1]))
            self._drawImage('./assets/images/ui/characterBackground.png', self.characterBgSize, imageCoordinates)
            defender = self.matchService.getPlayer(self.indexDefender).getCharacter()
            coordinates = (self._screenWidth - self.characterBgSize[0] - bgOffset + chOffset, chOffset + bgOffset + (self._screenHeight - self.gameBarSize[1]))
            self._screen.blit(pygame.transform.flip(pygame.transform.scale(defender.getProfileImage(), miniatureSize), 1, 0), coordinates)
            self._drawText(str(self.indexDefender + 1), 25, './assets/fonts/titleFont.ttf',
                           Colors.BLACK, imageCoordinates, (20, 20))

    def drawPlayersStats(self):
        gap = 6

        # do not change
        imageSize = (26, (self.characterBgSize[1]))
        barSize = (int(imageSize[0] * 0.775), int(imageSize[1] * 0.885))
        barTopOffset = 3
        offset = int((self.gameBarSize[1] - self.characterBgSize[1]) / 2)

        # attacker
        # ult
        attacker = self.matchService.getPlayer(self.matchService.getAttackerIndex()).getCharacter()
        maxUlt = 5
        currentUlt = attacker.getUlt()
        currentBarHeight = int((currentUlt / maxUlt) * barSize[1])

        coordinates = ((self.characterBgSize[0] + offset + gap), (offset + (self._screenHeight - self.gameBarSize[1])))
        fillCoordinates = (coordinates[0] + int((imageSize[0] - barSize[0]) / 2), (coordinates[1] + barTopOffset))
        pygame.draw.rect(self._screen, Colors.BG_BAR, (fillCoordinates[0], fillCoordinates[1], barSize[0], barSize[1]))
        pygame.draw.rect(self._screen, Colors.ULT_BAR, (fillCoordinates[0], fillCoordinates[1] + (barSize[1] - currentBarHeight), barSize[0], currentBarHeight))
        self._drawImage('./assets/images/ui/ultBar.png', imageSize, coordinates)

        # hp
        maxHp = attacker._maxHpValue
        currentHp = attacker.get_hp()
        currentBarHeight = int((currentHp / maxHp) * barSize[1])

        coordinates = (coordinates[0] + imageSize[0] + int(gap / 2), coordinates[1])
        fillCoordinates = (coordinates[0] + int((imageSize[0] - barSize[0]) / 2), (coordinates[1] + barTopOffset))
        pygame.draw.rect(self._screen, Colors.BG_BAR, (fillCoordinates[0], fillCoordinates[1], barSize[0], barSize[1]))
        pygame.draw.rect(self._screen, Colors.HP_BAR, (fillCoordinates[0], fillCoordinates[1] + (barSize[1] - currentBarHeight), barSize[0], currentBarHeight))
        self._drawImage('./assets/images/ui/hpBar.png', imageSize, coordinates)

        # defender
        if self.matchService.getCurrentState() == states['selectingAttack']:
            # ult
            defender = self.matchService.getPlayer(self.indexDefender).getCharacter()
            maxUlt = 5
            currentUlt = defender.getUlt()
            currentBarHeight = int((currentUlt / maxUlt) * barSize[1])

            coordinates = ((self._screenWidth - (self.characterBgSize[0] + offset + gap + imageSize[0])), (offset + (self._screenHeight - self.gameBarSize[1])))
            fillCoordinates = (coordinates[0] + int((imageSize[0] - barSize[0]) / 2), (coordinates[1] + barTopOffset))
            pygame.draw.rect(self._screen, Colors.BG_BAR,
                             (fillCoordinates[0], fillCoordinates[1], barSize[0], barSize[1]))
            pygame.draw.rect(self._screen, Colors.ULT_BAR, (
            fillCoordinates[0], fillCoordinates[1] + (barSize[1] - currentBarHeight), barSize[0], currentBarHeight))
            self._drawImage('./assets/images/ui/ultBar.png', imageSize, coordinates)

            maxHp = defender._maxHpValue
            currentHp = defender.get_hp()
            currentBarHeight = int((currentHp / maxHp) * barSize[1])

            coordinates = (coordinates[0] - (imageSize[0] + int(gap / 2)), coordinates[1])
            fillCoordinates = (coordinates[0] + int((imageSize[0] - barSize[0]) / 2), (coordinates[1] + barTopOffset))
            pygame.draw.rect(self._screen, Colors.BG_BAR,
                             (fillCoordinates[0], fillCoordinates[1], barSize[0], barSize[1]))
            pygame.draw.rect(self._screen, Colors.HP_BAR, (
            fillCoordinates[0], fillCoordinates[1] + (barSize[1] - currentBarHeight), barSize[0], currentBarHeight))
            self._drawImage('./assets/images/ui/hpBar.png', imageSize, coordinates)

    def drawAttackOptions(self):
        fontSize = 22
        buttonSize = (340, 80)
        gap = 10
        buttonImage = './assets/images/ui/button.png'

        totalWidth = (buttonSize[0] * 2) + gap
        totalHeight = (buttonSize[1] * 2) + gap

        position = ((self._screenWidth - totalWidth) / 2, ((self._screenHeight - self.gameBarSize[1]) + (self.gameBarSize[1] - totalHeight) / 2))

        attacker = self.matchService.getPlayer(self.matchService.getAttackerIndex()).getCharacter()
        self._drawButton(attacker.nameLightAttack, self._mainFont, fontSize, Colors.BLACK, position, buttonSize, buttonImage, self.setLevel, ('easy', 'light'))
        position = (position[0] + buttonSize[0] + gap, position[1])
        self._drawButton(attacker.nameMediumAttack, self._mainFont, fontSize, Colors.BLACK,position, buttonSize, buttonImage, self.setLevel,('normal', 'medium'))
        position = (position[0] - buttonSize[0] - gap, position[1] + buttonSize[1] + gap)
        self._drawButton(attacker.nameHeavyAttack, self._mainFont, fontSize, Colors.BLACK, position, buttonSize, buttonImage, self.setLevel, ('hard', 'heavy'))
        position = (position[0] + buttonSize[0] + gap, position[1])
        self._drawButton(attacker.nameUltimateAttack, self._mainFont, fontSize, Colors.BLACK,position,buttonSize, buttonImage, self.setLevel, ('ultimate', 'ultimate'))

    def selectedDefender(self, indexDefender):
        self.indexDefender = indexDefender
        self.matchService.setCurrentState(states['selectingAttack'])

    def drawDefenderOptions(self):
        # fixed values
        buttonSize = (180, 180)
        buttonBg = './assets/images/ui/characterBackground.png'
        offset = 7
        gap = 15

        # do not change
        imageSize = (buttonSize[0] - (offset * 2), buttonSize[1] - (offset * 2))
        buttonCoordinates = ((self._screenWidth - ((buttonSize[0] + gap) * 2)) / 2, self._screenHeight - self.gameBarSize[1] + (self.gameBarSize[1] - buttonSize[1]) / 2)
        imageCoordinates = (buttonCoordinates[0] + offset, buttonCoordinates[1] + offset)
        players = self.matchService.getPlayers()

        if len(players) == 2:
            if self.matchService.getAttackerIndex() == 0:
                self.selectedDefender(1)
            else:
                self.selectedDefender(0)
        else:
            for i, player in enumerate(players):
                if i != self.matchService.getAttackerIndex():
                    self._drawButton("", self._mainFont, 14, Colors.BLACK, buttonCoordinates,
                                     buttonSize, buttonBg, self.selectedDefender, i)
                    self._screen.blit(pygame.transform.scale(player.getCharacter().getProfileImage(), imageSize), imageCoordinates)
                    self._drawText(str(players.index(player) + 1), 20, './assets/fonts/titleFont.ttf', Colors.BLACK, imageCoordinates, (10, 10))
                    buttonCoordinates = (buttonCoordinates[0] + buttonSize[0] + gap, buttonCoordinates[1])
                    imageCoordinates = (buttonCoordinates[0] + offset, buttonCoordinates[1] + offset)

    def drawFighters(self):
        fightersSize = (680, 680)
        offSet = -120
        topGap = 0

        attacker = self.matchService.attacker.getCharacter()
        defender = self.matchService.getPlayer(self.indexDefender).getCharacter()
        self._drawCharacter(attacker, attacker.current_action, fightersSize, (offSet, topGap))
        if self.matchService.getCurrentState() != states['selectingDefender'] and len(self.matchService.players) > 1:
            self._drawCharacter(defender, defender.current_action, fightersSize, (self._screenWidth - fightersSize[0] + (-1 * offSet), topGap), True)

    def setLevel(self, level):
        self.questionLevel = level[0]
        self.attackLevel = level[1]
        self.matchService.setCurrentState(states['waitingAnswer'])

    import pygame

    def drawQuestion(self):
        if not self.questionReceived:
            question = Questions()
            self.questionReceived = question.get_question(self.questionLevel)

        image = "./assets/images/ui/questionBackground.png"
        imageSize = (550, 200)
        imageCord = ((self._screenWidth - imageSize[0]) // 2, (self._screenHeight - imageSize[1]) - 15)

        self._drawImage(image, imageSize, imageCord)

        textSize = 16
        font_path = './assets/fonts/mainFont.ttf'

        text = self.questionReceived.question
        cord = (self._screenWidth // 2, -40 + imageCord[1] + imageSize[1] // 2)
        self._drawTextBox(text, textSize, font_path, Colors.WHITE, cord, (imageSize[0] * 0.88, imageSize[1] * 0.88))

    def attack(self):
        defenderPlayer = self.matchService.getPlayer(self.indexDefender)
        attacker = self.matchService.getPlayer(self.matchService.getAttackerIndex()).getCharacter()
        if self.waitingState == 60 and not self.deathCycle:
            if self.attackLevel != 'ultimate':
                attacker.changeState('attack')
            else:
                attacker.changeState('ultimate')
                self.waitingState = self._ch_frame_interval * attacker.frame_counts['ultimate']

        defender = defenderPlayer.getCharacter()
        if self.waitingState == 60 / (defender.frame_counts['take_hit']) and not self.deathCycle:
            if isinstance(attacker, CharacterDamage) or self.attackLevel != 'ultimate':
                defender.changeState('take_hit')

        if self.waitingState > 0:
            self.waitingState -= 1
            return None

        if self.deathCycle:
            self.deathCycle = False
            self.matchService.eliminatePlayer(defenderPlayer)
            return None

        if self.matchService.attack(self.attackLevel, self.attackIntensity, defenderPlayer, self.questionReceived, self._insertedText):
            defenderPlayer.getCharacter().changeState('death')
            self.waitingState = 60
            self.deathCycle = True

        if not self.deathCycle:
            self.matchService.setCurrentState(states['selectingDefender'])
            self._insertedText = ''
            self.questionReceived = None
            self.waitingState = 60

    def drawHPAllPlayers(self):
        x = 50
        barWidth = 200
        barHeight = 20

        for idx, player in enumerate(self.matchService.getPlayers()):
            character = player.getCharacter()
            maxHp = character._maxHpValue
            currentHp = character.hp

            currentBarWidth = int((currentHp / maxHp) * barWidth)

            pygame.draw.rect(self._screen, Colors.GRAY, (900, x, barWidth, barHeight))

            pygame.draw.rect(self._screen, Colors.RED, (900, x, currentBarWidth, barHeight))

            self._drawText(f"{idx + 1}: {currentHp}/{maxHp}", 14, self._mainFont, Colors.WHITE,
                           (965 + barWidth, x + 10))

            x += barHeight + 10

    def drawEndGame(self):
        ko_image_path = './assets/images/ui/KO.png'
        imageSize = (400, 200)
        imagePosition = ( (self._screenWidth - imageSize[0]) // 2, (self._screenHeight - imageSize[1]) // 2)
        self._drawImage(ko_image_path, imageSize, imagePosition)


        buttonSize = (150, 50)
        gap = 10
        buttonImage = './assets/images/ui/button.png'

        totalWidth = (buttonSize[0] * 2) + gap
        buttonPosition = ((self._screenWidth - totalWidth) / 2, self._screenHeight // 2 + 150)

        self._drawButton("Sair", self._mainFont, 20, Colors.BLACK, buttonPosition, buttonSize, buttonImage,
                         self._quit)

        buttonPosition = (buttonPosition[0] + buttonSize[0] + gap, buttonPosition[1])

        self._drawButton("Menu", self._mainFont, 20, Colors.BLACK, buttonPosition, buttonSize, buttonImage)



