import pygame

from domain.questions.Question import Question
from domain.questions.Questions import Questions
from view.BaseView import BaseView
from view.Colors import Colors
from service.MatchService import states

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
        self.matchService = matchService
        self.matchService.startMatch()

        gameBarSize = (self._screenWidth, 220)
        gameBarSurface = pygame.Surface(gameBarSize)

        while self._running:
            self._screen.fill(Colors.BLACK)
            gameBarSurface.fill(Colors.CYAN)
            self._screen.blit(gameBarSurface, (0, (self._screenHeight - gameBarSize[1])))

            self.drawAttackerMiniature()
            if self.matchService.getCurrentState() == states['selectingDefender']:
                self.drawDefenderOptions()
            elif self.matchService.getCurrentState() == states['selectingAttack']:
                self.drawAttackOptions()
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

            self.drawFighters()
            
            self._event()
            pygame.display.update()

        pygame.quit()

    def drawAttackOptions(self):
        attacker = self.matchService.getPlayers()[self.matchService.getAttackerIndex()].getCharacter()
        self._drawButton(attacker.getNameLightAttack(), self._font, Colors.GRAY, Colors.WHITE, (450, 500), (300, 70), self.setLevel, ('easy', 'light'))
        self._drawButton(attacker.getNameMediumAttack(), self._font, Colors.GRAY, Colors.WHITE, (760, 500), (300, 70), self.setLevel, ('normal', 'medium'))
        self._drawButton(attacker.getNameHeavyAttack(), self._font, Colors.GRAY, Colors.WHITE, (450, 580), (300, 70), self.setLevel, ('hard', 'heavy'))
        self._drawButton(attacker.getNameUltimateAttack(), self._font, Colors.GRAY, Colors.WHITE, (760, 580), (300, 70),self.setLevel, ('ultimate', 'ultimate'))

    def drawAttackerMiniature(self):
        attacker = self.matchService.getPlayers()[self.matchService.getAttackerIndex()].getCharacter()

        self._drawImage(attacker.getSprite(), (200, 200), (75, 510))

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
                    self._drawButton("", self._font, Colors.GRAY, Colors.WHITE, (x, 510),
                                     (150, 150), self.selectedDefender, i)
                    self._drawImage(player.getCharacter().getSprite(), (150, 150), (x, 510))

                    x += 160

    def drawFighters(self):
        attacker = self.matchService.getPlayers()[self.matchService.getAttackerIndex()].getCharacter()
        defender = self.matchService.getPlayers()[self.indexDefender].getCharacter()
        self._drawImage(attacker.getSprite(), (200, 200), (300, 250))
        self._drawImage(defender.getSprite(), (200, 200), (600, 250))

    def setLevel(self, level):
        print(level)
        self.questionLevel = level[0]
        self.attackLevel = level[1]
        self.matchService.setCurrentState(states['waitingAnswer'])

    def drawQuestion(self):
        if not self.questionReceived:
            question = Questions()
            self.questionReceived = question.get_question(self.questionLevel)
        self._drawText(self.questionReceived.question, self._font, Colors.WHITE, self._screen, (200, 50))

    def validateAnswer(self):
        self.matchService.setCurrentState(states['attacking'])
        return self.questionReceived.validate_answer(self._insertedText)

    def attack(self):
        defenderPlayer = self.matchService.getPlayers()[self.indexDefender]
        self.matchService.attack(self.attackLevel, self.attackIntensity, defenderPlayer)
        print(defenderPlayer.getCharacter().hp)
        self.matchService.setCurrentState(states['selectingDefender'])

