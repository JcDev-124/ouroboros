import pygame
import sys

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
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, hover_color, (x, y, w, h))
            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(screen, color, (x, y, w, h))

        self.drawText(text, font, WHITE, screen, x + 20, y + 10)

    def newWindow(self):
        screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Partida")

        image = pygame.image.load(f'./assets/character.png')

        running = True
        while running:
            screen.fill((0, 0, 0))  # Preencher a tela com a cor preta

            self.drawText('Seleção de Jogadores', font, WHITE, screen, 200, 50)

            x = 200
            for idx, player in enumerate(self.matchService.getPlayers()):
                screen.blit(pygame.transform.scale(image, (100, 100)), (x, 300))
                self.drawButton(str(player.getId() + 1), x, 410, 100, 40, GRAY, WHITE)
                x += 110

            self.drawButton('Iniciar partida', 550, 600, 200, 50, GRAY, WHITE, self.matchService.startMatch())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.update()

        pygame.quit()
        sys.exit()