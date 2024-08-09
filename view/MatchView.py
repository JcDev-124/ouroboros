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

    attackIntensity = 5

    def __init__(self):
        super().__init__()

    def run(self, matchService):
        clock = pygame.time.Clock()
        fps = 60
        self.matchService = matchService
        self.matchService.startMatch()

        gameBarSize = (self._screenWidth, 220)
        gameBarSurface = pygame.Surface(gameBarSize)

        while self._running:
            self._screen.fill(Colors.BLACK)
            gameBarSurface.fill(Colors.CYAN)
            
            self._screen.blit(gameBarSurface, (0, (self._screenHeight - gameBarSize[1])))

            self._drawCharacter(self.matchService.getPlayers()[self.matchService.getAttackerIndex()].getCharacter().getSprite(), (200, 200), (0, 510))
            self.drawHpPlayer((10, 680), (200, 20), self.matchService.getAttackerIndex())
            self.drawFighters()
            self.drawHPAllPlayers()
            if self.matchService.getCurrentState() == states['selectingDefender']:
                self.drawDefenderOptions()
            elif self.matchService.getCurrentState() == states['selectingAttack']:
                self.drawAttackOptions()
                self.drawHpPlayer((self._screenWidth - 210, 680), (200, 20), self.indexDefender)
                self._drawCharacter(self.matchService.getPlayers()[self.indexDefender].getCharacter().getSpriteRotate(), (200, 200), (self._screenWidth - 200, 510))

            elif self.matchService.getCurrentState() == states['waitingAnswer']:
                self.drawQuestion()
                self._drawInputBox()


                if self._insertedText != '':
                    print(self.validateAnswer())
                    self._insertedText = ''
                    self.questionReceived = None
                else:
                    pass

            elif self.matchService.getCurrentState() == states['attacking']:
                self.attack()



            self._event()
            pygame.display.update()
            clock.tick(fps)
        pygame.quit()

    def drawAttackOptions(self):
        fontSize = 14
        buttonWidth, buttonHeight = 300, 70
        verticalSpacing = 20
        gameBarSize = (self._screenWidth, 220)

        gameBarPosY = self._screenHeight - gameBarSize[1]

        startY = (gameBarSize[1] - (2 * buttonHeight + verticalSpacing)) // 2 + gameBarPosY

        centerX = (gameBarSize[0] - (2 * buttonWidth + 20)) // 2

        attacker = self.matchService.getPlayers()[self.matchService.getAttackerIndex()].getCharacter()
        self._drawButton(attacker.getNameLightAttack(), self._mainFont, fontSize, Colors.BLACK, (centerX, startY),(buttonWidth, buttonHeight), None, self.setLevel, ('easy', 'light'))
        self._drawButton(attacker.getNameMediumAttack(), self._mainFont, fontSize, Colors.BLACK,(centerX + buttonWidth + 20, startY), (buttonWidth, buttonHeight), None, self.setLevel,('normal', 'medium'))
        self._drawButton(attacker.getNameHeavyAttack(), self._mainFont, fontSize, Colors.BLACK, (centerX, startY + buttonHeight + verticalSpacing), (buttonWidth, buttonHeight), None, self.setLevel, ('hard', 'heavy'))
        self._drawButton(attacker.getNameUltimateAttack(), self._mainFont, fontSize, Colors.BLACK,(centerX + buttonWidth + 20, startY + buttonHeight + verticalSpacing),(buttonWidth, buttonHeight), None, self.setLevel, ('ultimate', 'ultimate'))


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
                                     (150, 150), player.getCharacter().getSprite(), self.selectedDefender, i)

                    x += 160

    def drawFighters(self):
        attacker = self.matchService.getPlayers()[self.matchService.getAttackerIndex()].getCharacter()
        defender = self.matchService.getPlayers()[self.indexDefender].getCharacter()
        self._drawCharacter(attacker.getSprite(), (200, 200), (300, 250))
        self._drawCharacter(defender.getSpriteRotate(), (200, 200), (600, 250))

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

    def validateAnswer(self):
        self.matchService.setCurrentState(states['attacking'])
        return self.questionReceived.validate_answer(self._insertedText)

    def attack(self):
        defenderPlayer = self.matchService.getPlayers()[self.indexDefender]
        self.matchService.attack(self.attackLevel, self.attackIntensity, defenderPlayer)
        self.matchService.setCurrentState(states['selectingDefender'])

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
        currentBarWidth = int((currentHp / maxHp) * size[0])

        pygame.draw.rect(self._screen, Colors.GRAY, (cord[0], cord[1], size[0], size[1]))
        pygame.draw.rect(self._screen, Colors.RED, (cord[0], cord[1], currentBarWidth, size[1]))

        text = f"{currentHp}/{maxHp}"
        textSurface = pygame.font.Font(self._mainFont, 12).render(text, True, Colors.WHITE)
        textWidth, text_height = textSurface.get_size()

        textX = cord[0] + (size[0] - textWidth) // 2
        textY = cord[1] + (size[1] - text_height) // 2

        self._screen.blit(textSurface, (textX, textY))


