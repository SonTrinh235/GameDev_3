import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('GameDev_3')
        self.clock = pygame.time.Clock()
        
        self.import_assets()
        
        self.current_level_index = 0
        self.level = Level(LEVEL_DATA[self.current_level_index], self.surfaces, self.next_level)
        self.status = 'menu'

    def import_assets(self):
        def get_surf(path, fallback_color):
            try:
                return pygame.image.load(path).convert_alpha()
            except:
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill(fallback_color)
                return surf

        self.surfaces = {
            'tile': get_surf('Assets/graphics/tile.png', 'grey'),
            'bg_tile': get_surf('Assets/graphics/bg_tile.png', (50, 50, 50)),
            'coin': get_surf('Assets/graphics/Coin.png', 'yellow'),
            'star': get_surf('Assets/graphics/Star.png', 'gold'),
            'enemy': get_surf('Assets/graphics/Signus.png', 'red'),
            'spike': get_surf('Assets/graphics/Spike.png', 'purple'),
            'bounce': get_surf('Assets/graphics/Bounce.png', 'orange'),
            'goal': get_surf('Assets/graphics/goal.png', 'green'),
            'key': get_surf('Assets/graphics/key.png', 'cyan'),
            'door': get_surf('Assets/graphics/key_hole.png', 'brown'),
        }

    def next_level(self):
        self.current_level_index += 1
        if self.current_level_index < len(LEVEL_DATA):
            self.level = Level(LEVEL_DATA[self.current_level_index], self.surfaces, self.next_level)
        else:
            self.status = 'menu'
            self.current_level_index = 0

    def restart_current_level(self):
        self.level = Level(LEVEL_DATA[self.current_level_index], self.surfaces, self.next_level)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.status == 'menu':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.current_level_index = 0
                            self.restart_current_level()
                            self.status = 'playing'
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                
                elif self.status == 'playing':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.restart_current_level()

            self.screen.fill(BG_COLOR)
            
            if self.status == 'menu':
                self.draw_menu()
            else:
                self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)

    def draw_menu(self):
        font = pygame.font.SysFont('Arial', 50)
        title_surf = font.render('CELESTE CLONE', True, 'gold')
        start_surf = font.render('PRESS ENTER TO START', True, 'white')
        
        title_rect = title_surf.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        start_rect = start_surf.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        
        self.screen.blit(title_surf, title_rect)
        self.screen.blit(start_surf, start_rect)

if __name__ == '__main__':
    game = Game()
    game.run()