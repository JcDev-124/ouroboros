import pygame

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

    # game constants
    attackIntensity = 5

    def __init__(self, matchService):
        self.matchService = matchService
        self.matchService.startMatch()
        super().__init__()

    def run(self):
        self._bg_frame_interval = 4
        self._ch_frame_interval = 5
        self.audio_manager.play_background_music('./assets/sounds/fight.ogg')

        # design constants
        self.gameBarSize = (self._screenWidth, 230)
        self.characterBgSize = (200, 200)

        while self._running:
            clock = pygame.time.Clock()

            self._drawBackground('./assets/images/backgrounds/matchBackground.gif',
                                 (self._screenWidth, 490), (0, 0))
            self._drawImage('./assets/images/buttons/menuButton.png', (self._screenWidth, 230),
                            (0, self._screenHeight - 230))

            self.drawPlayersMiniature()

            self.drawHpPlayer((230, 520), (20, 170), self.matchService.getAttackerIndex())
            self.drawUltPlayer((210, 520), (20, 170), self.matchService.getAttackerIndex())
            self.drawFighters()
            self.drawHPAllPlayers()

            if self.matchService.getCurrentState() == states['selectingDefender']:
                self.drawDefenderOptions()
            elif self.matchService.getCurrentState() == states['selectingAttack']:
                self.drawAttackOptions()
                self.drawHpPlayer((self._screenWidth - 230, 520), (20, 170), self.indexDefender)
                self.drawUltPlayer((self._screenWidth - 210, 520), (20, 170), self.indexDefender)

            elif self.matchService.getCurrentState() == states['waitingAnswer']:
                self.drawQuestion()
                self._drawInputBox()

                if self._insertedText != '':
                    self.matchService.setCurrentState(states['attacking'])

            elif self.matchService.getCurrentState() == states['attacking']:
                self.attack()

            if self.matchService.gameFinished():
                self._quit()

            self._event()

            pygame.display.update()
            clock.tick(self._fps)

    def drawPlayersMiniature(self):
        # fixed values
        bgOffset = (self.gameBarSize[1] - self.characterBgSize[1]) / 2
        chOffset = 10
        miniatureSize = (self.characterBgSize[0] - (chOffset * 2), self.characterBgSize[1] - (chOffset * 2))

        # attacker
        self._drawImage('./assets/images/backgrounds/characterBackground.png', self.characterBgSize, (bgOffset, bgOffset + (self._screenHeight - self.gameBarSize[1])))
        attacker = self.matchService.getPlayers()[self.matchService.getAttackerIndex()].getCharacter()
        coordinates = (chOffset + bgOffset, chOffset + bgOffset + (self._screenHeight - self.gameBarSize[1]))
        self._screen.blit(pygame.transform.scale(attacker.getProfileImage(), miniatureSize), coordinates)

        # defender
        if self.matchService.getCurrentState() == states['selectingAttack']:
            self._drawImage('./assets/images/backgrounds/characterBackground.png', self.characterBgSize, (self._screenWidth - self.characterBgSize[0] - bgOffset, bgOffset + (self._screenHeight - self.gameBarSize[1])))
            defender = self.matchService.getPlayers()[self.indexDefender].getCharacter()
            coordinates = (self._screenWidth - self.characterBgSize[0] - bgOffset + chOffset, chOffset + bgOffset + (self._screenHeight - self.gameBarSize[1]))
            self._screen.blit(pygame.transform.scale(defender.getProfileImage(), miniatureSize), coordinates)

    def drawAttackOptions(self):
        fontSize = 14
        buttonWidth, buttonHeight = 300, 70
        verticalSpacing = 20
        gameBarSize = (self._screenWidth, 220)

        gameBarPosY = self._screenHeight - gameBarSize[1]

        startY = (gameBarSize[1] - (2 * buttonHeight + verticalSpacing)) // 2 + gameBarPosY

        centerX = (gameBarSize[0] - (2 * buttonWidth + 20)) // 2

        attacker = self.matchService.getPlayers()[self.matchService.getAttackerIndex()].getCharacter()
        self._drawButton(attacker.nameLightAttack, self._mainFont, fontSize, Colors.BLACK, (centerX, startY),(buttonWidth, buttonHeight), None, self.setLevel, ('easy', 'light'))
        self._drawButton(attacker.nameMediumAttack, self._mainFont, fontSize, Colors.BLACK,(centerX + buttonWidth + 20, startY), (buttonWidth, buttonHeight), None, self.setLevel,('normal', 'medium'))
        self._drawButton(attacker.nameHeavyAttack, self._mainFont, fontSize, Colors.BLACK, (centerX, startY + buttonHeight + verticalSpacing), (buttonWidth, buttonHeight), None, self.setLevel, ('hard', 'heavy'))
        self._drawButton(attacker.nameUltimateAttack, self._mainFont, fontSize, Colors.BLACK,(centerX + buttonWidth + 20, startY + buttonHeight + verticalSpacing),(buttonWidth, buttonHeight), None, self.setLevel, ('ultimate', 'ultimate'))


    def selectedDefender(self, indexDefender):
        self.indexDefender = indexDefender
        self.matchService.setCurrentState(states['selectingAttack'])

    def drawDefenderOptions(self):
        players = self.matchService.getPlayers()

        if len(players) == 2:
            if self.matchService.getAttackerIndex() == 0:
                self.selectedDefender(1)
            else:
                self.selectedDefender(0)
        else:
            x = 350
            for i, player in enumerate(players):
                if i != self.matchService.getAttackerIndex():
                    self._drawButton("", self._mainFont, 14, Colors.BLACK, (x, 510),
                                     (150, 150), None, self.selectedDefender, i)

                    x += 160

    def drawFighters(self):
        fightersSize = (680, 680)
        offSet = -120
        topGap = 0

        attacker = self.matchService.getPlayers()[self.matchService.getAttackerIndex()].getCharacter()
        defender = self.matchService.getPlayers()[self.indexDefender].getCharacter()
        self._drawCharacter(attacker, 'idle', fightersSize, (offSet, topGap))
        self._drawCharacter(defender, 'idle', fightersSize, (self._screenWidth - fightersSize[0] + (-1 * offSet), topGap), True)

    def setLevel(self, level):
        print(level)
        self.questionLevel = level[0]
        self.attackLevel = level[1]
        self.matchService.setCurrentState(states['waitingAnswer'])

    def drawQuestion(self):
        if not self.questionReceived:
            question = Questions()
            self.questionReceived = question.get_question(self.questionLevel)
        self._drawText(self.questionReceived.question, 14, self._mainFont, Colors.WHITE, (200, 50))



    def attack(self):
        defenderPlayer = self.matchService.getPlayers()[self.indexDefender]
        self.matchService.attack(self.attackLevel, self.attackIntensity, defenderPlayer, self.questionReceived, self._insertedText)
        self.matchService.setCurrentState(states['selectingDefender'])
        self._insertedText = ''
        self.questionReceived = None
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

    def drawHpPlayer(self, cord, size, player):
        character = self.matchService.getPlayers()[player].getCharacter()
        maxHp = character._maxHpValue
        currentHp = character.hp

        currentBarHeight = int((currentHp / maxHp) * size[1])

        pygame.draw.rect(self._screen, Colors.GRAY, (cord[0], cord[1], size[0], size[1]))

        pygame.draw.rect(self._screen, Colors.RED,
                         (cord[0], cord[1] + (size[1] - currentBarHeight), size[0], currentBarHeight))

    def drawUltPlayer(self, cord, size, player):
        maxUlt = 5
        currentUlt = self.matchService.getPlayers()[player].getCharacter().getUlt()

        currentBarHeight = int((currentUlt / maxUlt) * size[1])

        pygame.draw.rect(self._screen, Colors.GRAY, (cord[0], cord[1], size[0], size[1]))

        pygame.draw.rect(self._screen, Colors.YELLOW,
                         (cord[0], cord[1] + (size[1] - currentBarHeight), size[0], currentBarHeight))
