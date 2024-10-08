import pygame

from domain.characters.CharacterDamage import CharacterDamage
from domain.characters.CharacterTank import CharacterTank
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
    playerToEliminate = None

    # game constants
    attackIntensity = 5

    koPlayed = False

    def __init__(self, matchService):
        self.matchService = matchService
        self.matchService.startMatch()
        super().__init__()

    def run(self):
        self._bg_frame_interval = 3
        self._ch_frame_interval = 3
        self.audio_manager.play_background_music('./assets/sounds/fight.ogg')

        self.audio_manager.load_sound_effect('correct', './assets/sounds/correct.mp3')
        self.audio_manager.load_sound_effect('wrong', './assets/sounds/wrong.mp3')
        self.audio_manager.load_sound_effect('ko', './assets/sounds/ko.mp3')

        # design constants
        self.gameBarSize = (self._screenWidth, 230)
        self.characterBgSize = (200, 200)

        self.timeStartTime = None
        self.timerDuration = 20
        self.timerRunning = False

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
            # stats overlay
            self.drawPlayersOverlay()

            # fighters
            self.drawFighters()

            # options
            current_state = self.matchService.getCurrentState()
            if current_state == states['selectingDefender']:
                self.timerRunning = False
                self.drawDefenderOptions()
            elif current_state == states['selectingAttack']:
                self.drawAttackOptions()
            elif current_state == states['waitingAnswer']:
                if not self.timerRunning:
                    self.startTimer()
                if self.timerRunning:
                    self.updateTimer()
                self.drawQuestion()
                self._drawInputBox()

                if self._insertedText != '':
                    self.matchService.setCurrentState(states['attacking'])

            elif current_state == states['attacking']:
                self.attack()

            if self.matchService.gameFinished() and not self.deathCycle:
                self.drawEndGame()

            self._event()

            pygame.display.update()
            clock.tick(self._fps)

    def drawPlayersOverlay(self):
        offset = -20
        barSize = (218, 26)
        miniatureSize = (barSize[1], barSize[1])
        numPlayers = len(self.matchService.getPlayers())
        XGap = 8
        YGap = 5
        correction = barSize[1] * 0.5
        markerSize = 3

        size = (barSize[0] + miniatureSize[0] + (XGap * 3), (barSize[1] * numPlayers) + (YGap * numPlayers + 1) + correction)
        position = (self._screenWidth - size[0] + offset, (offset * -1))
        miniaturePosition = (position[0] + XGap, position[1] + YGap + correction / 2)
        barPosition = (miniaturePosition[0] + XGap + miniatureSize[0], miniaturePosition[1])
        fillSize = (barSize[0] * 0.955, barSize[1] * 0.695)
        fillPosition = (barPosition[0] + barSize[0] * 0.0248, barPosition[1] + barSize[1] * 0.16)
        self._drawImage('./assets/images/ui/overlay.png', size, position)
        for i, player in enumerate(self.matchService.getPlayers()):
            character = player.getCharacter()
            hp = character.get_hp()
            maxHp = character._maxHpValue
            pygame.draw.rect(self._screen, Colors.BG_BAR,
                             (fillPosition[0], fillPosition[1], fillSize[0], fillSize[1]))
            pygame.draw.rect(self._screen, Colors.HP_BAR,
                             (fillPosition[0], fillPosition[1], (fillSize[0] * (hp / maxHp)), fillSize[1]))
            self._screen.blit(pygame.transform.scale(character.getProfileImage(), miniatureSize), miniaturePosition)
            self._drawImage('./assets/images/ui/emptyBar.png', barSize, barPosition)
            if i == self.matchService.getAttackerIndex():
                self.drawMarker(Colors.LUCK_BAR, (miniaturePosition[0] + markerSize, miniaturePosition[1] + markerSize), markerSize, True)
            elif i == self.indexDefender:
                self.drawMarker(Colors.HP_BAR, (miniaturePosition[0] + markerSize, miniaturePosition[1] + markerSize), markerSize, True)
            else:
                self.drawMarker(Colors.ATTACK_BAR, (miniaturePosition[0] + markerSize, miniaturePosition[1] + markerSize), markerSize, True)

            miniaturePosition = (miniaturePosition[0], miniaturePosition[1] + YGap + miniatureSize[1])
            barPosition = (barPosition[0], barPosition[1] + YGap + barSize[1])
            fillPosition = (fillPosition[0], fillPosition[1] + YGap + barSize[1])

    def drawMarker(self, color, position, size, outline=False):
        if outline:
            pygame.draw.circle(self._screen, Colors.BLACK, (position[0], position[1]), size + 2)
        pygame.draw.circle(self._screen, color, position, size)

    def drawPlayersMiniature(self):
        # fixed values
        bgOffset = (self.gameBarSize[1] - self.characterBgSize[1]) / 2
        chOffset = 10
        miniatureSize = (self.characterBgSize[0] - (chOffset * 2), self.characterBgSize[1] - (chOffset * 2))

        # attacker
        imageCoordinates = (bgOffset, bgOffset + (self._screenHeight - self.gameBarSize[1]))
        self._drawImage('./assets/images/ui/characterBackground.png', self.characterBgSize, imageCoordinates)
        attacker = self.matchService.getPlayer(self.matchService.getAttackerIndex()).getCharacter()
        coordinates = (chOffset + bgOffset, chOffset + bgOffset + (self._screenHeight - self.gameBarSize[1]))
        self._screen.blit(pygame.transform.scale(attacker.getProfileImage(), miniatureSize), coordinates)
        if isinstance(attacker, CharacterTank) and attacker.verify_ult():
            self._drawImage('./assets/images/characters/tank/shield.png', (24, 24), (coordinates[0] + miniatureSize[0] - 30, coordinates[1]))
        self._drawText(str(self.matchService.getAttackerIndex() + 1), 25, './assets/fonts/titleFont.ttf', Colors.BLACK, imageCoordinates, (20, 20))

        # defender
        if self.matchService.getCurrentState() == states['selectingAttack']:
            imageCoordinates = (self._screenWidth - self.characterBgSize[0] - bgOffset, bgOffset + (self._screenHeight - self.gameBarSize[1]))
            self._drawImage('./assets/images/ui/characterBackground.png', self.characterBgSize, imageCoordinates)
            defender = self.matchService.getPlayer(self.indexDefender).getCharacter()
            coordinates = (self._screenWidth - self.characterBgSize[0] - bgOffset + chOffset, chOffset + bgOffset + (self._screenHeight - self.gameBarSize[1]))
            self._screen.blit(pygame.transform.flip(pygame.transform.scale(defender.getProfileImage(), miniatureSize), 1, 0), coordinates)
            if isinstance(defender, CharacterTank) and defender.verify_ult():
                self._drawImage('./assets/images/characters/tank/shield.png', (24, 24),
                                (coordinates[0] + miniatureSize[0] - 30, coordinates[1]))
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
            self.matchService.eliminatePlayer(self.playerToEliminate)
            if len(self.matchService.getPlayers()) == 2:
                if self.matchService.getAttackerIndex() == 0:
                    self.selectedDefender(1)
                else:
                    self.selectedDefender(0)
            self.matchService.setCurrentState(states['selectingDefender'])
            self._insertedText = ''
            self.questionReceived = None
            self.waitingState = 60
            return None

        isCorrect = self.matchService.attack(self.attackLevel, self.attackIntensity, defenderPlayer, self.questionReceived,
                                 self._insertedText)

        if isCorrect == 'true':
            self.audio_manager.play_sound_effect('correct')
        if isCorrect == 'false':
            self.audio_manager.play_sound_effect('wrong')
        if isCorrect == 'death':
            self.playerToEliminate = defenderPlayer
            defenderPlayer.getCharacter().changeState('death')
            self.waitingState = 60
            self.deathCycle = True

        if not self.deathCycle:
            self.matchService.setCurrentState(states['selectingDefender'])
            self._insertedText = ''
            self.questionReceived = None
            self.waitingState = 60

    def drawEndGame(self):
        ko_image_path = './assets/images/ui/KO.png'
        imageSize = (500, 237)
        imagePosition = ( (self._screenWidth - imageSize[0]) // 2, (self._screenHeight - imageSize[1]) // 2)
        self._drawImage(ko_image_path, imageSize, imagePosition)
        if not self.koPlayed:
            self.audio_manager.play_sound_effect('ko')
            self.koPlayed = True

        buttonSize = (150, 50)
        gap = 10
        buttonImage = './assets/images/ui/button.png'

        totalWidth = (buttonSize[0] * 2) + gap
        buttonPosition = ((self._screenWidth - buttonSize[0]) / 2, self._screenHeight // 2 + 150)

        self._drawButton("Sair", self._mainFont, 20, Colors.BLACK, buttonPosition, buttonSize, buttonImage,
                         self._quit)




    def startTimer(self):
        if not self.timerRunning or pygame.time.get_ticks() - self.timeStartTime >= self.timerDuration * 1000:
            self.timeStartTime = pygame.time.get_ticks()
            self.timerRunning = True
    def updateTimer(self):
        if self.timerRunning:
            elapsedTime = pygame.time.get_ticks() - self.timeStartTime
            if elapsedTime >= self.timerDuration * 1000:
                self.timerRunning = False

            else:
                remainingTime = self.timerDuration - (elapsedTime / 1000)
                self.drawTimer(remainingTime)

    def drawTimer(self, remaining_time):
        font = pygame.font.Font('./assets/fonts/mainFont.ttf', 48)
        timerText = f"{int(remaining_time)}"
        timerSurface = font.render(timerText, True, Colors.WHITE)
        timerRect = timerSurface .get_rect(center=(self._screenWidth / 2, 50))
        self._screen.blit(timerSurface , timerRect)

    def startTimer(self):
        self.timeStartTime = pygame.time.get_ticks()
        self.timerRunning = True
        self.timeUpCallback = self.timerUp

    def updateTimer(self):
        if self.timerRunning:
            elapsedTime = (pygame.time.get_ticks() - self.timeStartTime) / 1000
            remainingTime = self.timerDuration - elapsedTime

            if remainingTime <= 0:
                self.timerRunning = False
                remainingTime = 0
                if self.timeUpCallback:
                    self.timeUpCallback()


            self.drawTimer(remainingTime)



    def timerUp(self):
        self.matchService.setCurrentState(states['selectingDefender'])
        self.matchService.attacker = self.matchService.getPlayer(self.indexDefender)
        self.timerRunning = False