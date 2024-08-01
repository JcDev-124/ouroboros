import pygame
import sys

class MatchView:
    def startGame(self, amountPlayers):
        self.newWindow()
        pass

    def newWindow(self):
        screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Partida")

        running = True
        while running:
            screen.fill((0, 0, 0))  # Preencher a tela com a cor preta

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.update()

        pygame.quit()
        sys.exit()