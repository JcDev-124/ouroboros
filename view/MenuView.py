from view.SelectCharacters import SelectCharacters
import pygame
import sys

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

selectCharacters = SelectCharacters()

# Configurações de fonte
font = pygame.font.Font(None, 30)
class MenuView:


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

    # Ações dos botões
    def startGameWithTwoPlayers(self):
        selectCharacters.startGame(2)
        self.quitGame()

    def startGameWithThreePlayers(self):
        selectCharacters.startGame(3)
        self.quitGame()


    def quitGame(self):
        pygame.quit()
        sys.exit()

    # Loop principal
    def mainMenu(self):
        running = True
        while running:
            screen.fill(BLACK)
    
            self.drawText('Bem vindo ao OuroBoros', font, WHITE, screen, 200, 50)
    
            self.drawButton('2 Jogadores', 150, 200, 200, 50, GRAY, WHITE, self.startGameWithTwoPlayers)
            self.drawButton('3 Jogadores', 150, 350, 200, 50, GRAY, WHITE, self.startGameWithThreePlayers)
            self.drawButton('Sair', 150, 500, 200, 50, GRAY, WHITE, self.quitGame)
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
    
            pygame.display.update()
    
        pygame.quit()
