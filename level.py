import pygame
from settings import *
from player import Player
from sprites import StaticTile, Item, Enemy

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        
        self.visible_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group() 
        self.item_sprites = pygame.sprite.Group()

        self.setup_level()

    def setup_level(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                
                if cell == 'X': # Tạo gạch/sàn
                    tile_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    tile_surf.fill('gray') # PISKEL ART LATER
                    tile = StaticTile((x, y), TILE_SIZE, tile_surf)
                    self.collision_sprites.add(tile)
                    self.visible_sprites.add(tile)
                
                if cell == 'P': # PLAYER
                    self.player = Player((x, y), [self.visible_sprites], self.collision_sprites)
                
                if cell == 'C': # COIN
                    coin = Item((x, y), TILE_SIZE, pygame.Surface((16,16)), 'coin')
                    self.item_sprites.add(coin)
                    self.visible_sprites.add(coin)
                
                if cell == 'S': #STAR
                    star = Item((x, y), TILE_SIZE, pygame.Surface((20,20)), 'star')
                    self.item_sprites.add(star)
                    self.visible_sprites.add(star)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()