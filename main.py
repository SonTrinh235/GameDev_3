import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Celeste - Project Mario')
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.status = 'menu'

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.status == 'menu':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.status = 'playing'
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

            self.screen.fill(BG_COLOR)
            
            if self.status == 'menu':
                self.draw_menu()
            else:
                self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)

    def draw_menu(self):
        font = pygame.font.SysFont('Arial', 50)
        text = font.render('PRESS ENTER TO START', True, 'white')
        rect = text.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, rect)

if __name__ == '__main__':
    game = Game()
    game.run()