import pygame
from settings import *
from player import Player
from sprites import StaticTile, Item, Enemy

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x += (player.rect.centerx - SCREEN_WIDTH // 2 - self.offset.x) * 0.1
        self.offset.y += (player.rect.centery - SCREEN_HEIGHT // 2 - self.offset.y) * 0.1

        for sprite in self.sprites():
            if isinstance(sprite, StaticTile):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

        for sprite in self.sprites():
            if not isinstance(sprite, StaticTile):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

class Level:
    def __init__(self, level_data, surface_dict, trigger_next_level): 
        self.display_surface = pygame.display.get_surface()
        self.level_data = level_data
        self.surfaces = surface_dict
        self.trigger_next_level = trigger_next_level
        
        self.visible_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.goal_sprites = pygame.sprite.Group()
        self.spike_sprites = pygame.sprite.Group()
        self.bounce_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()
        
        self.has_key = False

        self.setup_level()

    def setup_level(self):
        for row_index, row in enumerate(self.level_data):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                
                if cell == 'X':
                    tile = StaticTile((x, y), TILE_SIZE, self.surfaces['tile'])
                    self.collision_sprites.add(tile)
                    self.visible_sprites.add(tile)
                elif cell == 'B':
                    tile = StaticTile((x, y), TILE_SIZE, self.surfaces['bg_tile'])
                    self.visible_sprites.add(tile)
                elif cell == 'P':
                    self.player = Player((x, y), [self.visible_sprites], self.collision_sprites)
                elif cell == 'C':
                    item = Item((x, y), TILE_SIZE, self.surfaces['coin'], 'coin')
                    self.item_sprites.add(item)
                    self.visible_sprites.add(item)
                elif cell == 'S':
                    item = Item((x, y), TILE_SIZE, self.surfaces['star'], 'star')
                    self.item_sprites.add(item)
                    self.visible_sprites.add(item)
                elif cell == 'K':
                    item = Item((x, y), TILE_SIZE, self.surfaces['key'], 'key')
                    self.item_sprites.add(item)
                    self.visible_sprites.add(item)
                elif cell == 'E':
                    enemy = Enemy((x, y), TILE_SIZE, self.surfaces['enemy'], self.collision_sprites)
                    self.enemy_sprites.add(enemy)
                    self.visible_sprites.add(enemy)
                elif cell == '^':
                    spike = StaticTile((x, y), TILE_SIZE, self.surfaces['spike'])
                    self.spike_sprites.add(spike)
                    self.visible_sprites.add(spike)
                elif cell == 'J':
                    bounce = StaticTile((x, y), TILE_SIZE, self.surfaces['bounce'])
                    self.bounce_sprites.add(bounce)
                    self.visible_sprites.add(bounce)
                elif cell == 'D':
                    door = StaticTile((x, y), TILE_SIZE, self.surfaces['door'])
                    self.door_sprites.add(door)
                    self.collision_sprites.add(door)
                    self.visible_sprites.add(door)
                elif cell == 'G':
                    goal = StaticTile((x, y), TILE_SIZE, self.surfaces['goal'])
                    self.goal_sprites.add(goal)
                    self.visible_sprites.add(goal)

    def reset(self):
        self.visible_sprites.empty()
        self.collision_sprites.empty()
        self.item_sprites.empty()
        self.enemy_sprites.empty()
        self.goal_sprites.empty()
        self.spike_sprites.empty()
        self.bounce_sprites.empty()
        self.door_sprites.empty()
        self.has_key = False
        self.setup_level()

    def interaction(self):
        for enemy in self.enemy_sprites.sprites():
            if enemy.rect.colliderect(self.player.rect):
                if self.player.m.direction.y > 0 and self.player.rect.bottom <= enemy.rect.bottom:
                    enemy.kill()
                    self.player.m.direction.y = JUMP_SPEED * 0.8
                    self.player.m.has_dashed = False 
                else:
                    self.reset()
                    break 

        for spike in self.spike_sprites.sprites():
            if spike.rect.inflate(-12, -12).colliderect(self.player.rect):
                self.reset()
                break

        for bounce in self.bounce_sprites.sprites():
            if bounce.rect.colliderect(self.player.rect):
                self.player.m.direction.y = -16
                self.player.m.is_dashing = False
                self.player.m.has_dashed = False
                self.player.rect.bottom = bounce.rect.top

        collided_items = pygame.sprite.spritecollide(self.player, self.item_sprites, True)
        for item in collided_items:
            if item.item_type == 'key':
                self.has_key = True

        if self.has_key:
            for door in self.door_sprites.sprites():
                if self.player.rect.inflate(4, 4).colliderect(door.rect):
                    door.kill()

        if pygame.sprite.spritecollide(self.player, self.goal_sprites, False):
            self.trigger_next_level()

        if self.player.rect.top > SCREEN_HEIGHT * 2:
            self.reset()

    def run(self):
        self.visible_sprites.update()
        self.interaction()
        
        self.visible_sprites.custom_draw(self.player)
        self.player.draw_stamina(self.visible_sprites.offset)