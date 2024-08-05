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

        self.matchService.getPlayers()[self.indexPlayer].setCharacter(selectedCharacter)
        self.indexesSprite[self.indexPlayer] = self.indexCharacter
        self.indexPlayer += 1

    def startMatch(self):
        try:
            self.checkSelectedPlayers()
        except ValueError as e:
            print(e)
            return

        MatchView().run(self.matchService)
        self._quit()

    def checkSelectedPlayers(self):
        if len(self.matchService.getPlayers()) != self.indexPlayer:
            message = "Aguardando Jogador " + str(self.indexPlayer + 1) + "."
            raise ValueError(message)

    def run(self):
        self._setCaption("Match")

        while self._running:
            self._screen.fill(Colors.BLACK)

            self._drawText('Seleção de Jogadores', self._font, Colors.WHITE, self._screen, (200, 50))

            x = 200
            for idx, player in enumerate(self.matchService.getPlayers()):
                if idx == self.indexPlayer:
                    self._drawImage(self.characters[self.indexCharacter].getSprite(), (200, 200), (x, 300))
                    self._drawButton('<', self._font, Colors.GRAY, Colors.WHITE, (x, 510), (48, 40), self.previousCharacter)
                    x += 76
                    self._drawButton(str(player.getId() + 1), self._font, Colors.GRAY, Colors.WHITE, (x, 510), (48, 40), self.selectCharacter)
                    x += 76
                    self._drawButton('>', self._font, Colors.GRAY, Colors.WHITE, (x, 510), (48, 40), self.nextCharacter)
                    x += 210
                else:
                    self._drawImage(self.characters[self.indexesSprite[idx]].getSprite(), (200, 200),  (x, 300))
                    x += 362

            self._drawButton('Iniciar partida', self._font, Colors.GRAY, Colors.WHITE, (550, 600), (200, 50), self.startMatch)

            self._event()

            pygame.display.update()