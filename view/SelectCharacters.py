import pygame
import sys

from domain.characters.CharacterDamage import CharacterDamage
from domain.characters.CharacterHealer import CharacterHealer
from domain.characters.CharacterTank import CharacterTank
from service.MatchService import MatchService

# Inicialização do Pygame
pygame.init()

# Configurações da janela
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ouroboros")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)


# Configurações de fonte
font = pygame.font.Font(None, 30)
class SelectCharacters:
    indexPlayer = 0
    indexCharacter = 0
    indexesSprite = [0,0,0]
    characters = [CharacterDamage(), CharacterHealer(), CharacterTank()]

    def startGame(self, matchService):
        self.matchService = matchService
        self.newWindow()
        pass

        # Função para desenhar texto
    def drawText(self, text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_obj, text_rect)

    # Função para desenhar botões
    def drawButton(self, text, x, y, w, h, color, hover_color, action=None):
        global button_pressed

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, hover_color, (x, y, w, h))
            if click[0] == 1 and action is not None and not button_pressed:
                action()
                button_pressed = True
        else:
            pygame.draw.rect(screen, color, (x, y, w, h))

        self.drawText(text, font, WHITE, screen, x + 20, y + 10)

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
            0 : CharacterDamage,
            1 : CharacterHealer,
            2 : CharacterTank
        }

        if self.indexCharacter in funCharacter:
            selectedCharacter = funCharacter[self.indexCharacter]

        self.matchService.getPlayers()[self.indexPlayer].setCharacter(selectedCharacter)
        self.indexesSprite[self.indexPlayer] = self.indexCharacter
        self.indexPlayer += 1


    def printPlayer(self):
        for i, player in enumerate(self.matchService.getPlayers()):
            print(player.getCharacter())

    def newWindow(self):
        global button_pressed
        global offset
        button_pressed = False
        offset = 0
        screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Partida")

        running = True

        while running:
            screen.fill((0, 0, 0))  # Preencher a tela com a cor preta

            self.drawText('Seleção de Jogadores', font, WHITE, screen, 200, 50)

            x = 200
            for idx, player in enumerate(self.matchService.getPlayers()):

                if idx == self.indexPlayer:
                    screen.blit(
                        pygame.transform.scale(pygame.image.load(self.characters[self.indexCharacter].getSprite()),
                                               (200, 200)), (x, 300))
                    self.drawButton('<', x, 510, 48, 40, GRAY, WHITE, self.previousCharacter)
                    x += 76
                    self.drawButton(str(player.getId() + 1), x, 510, 48, 40, GRAY, WHITE, self.selectCharacter)
                    x += 76
                    self.drawButton('>', x, 510, 48, 40, GRAY, WHITE, self.nextCharacter)
                    x += 210
                else:
                    screen.blit(
                        pygame.transform.scale(pygame.image.load(self.characters[self.indexesSprite[idx]].getSprite()),
                                               (200, 200)), (x, 300))
                    x += 362

            self.drawButton('Iniciar partida', 550, 600, 200, 50, GRAY, WHITE, self.printPlayer)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    button_pressed = False

            pygame.display.update()

        pygame.quit()
        sys.exit()
