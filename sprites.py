import pygame
from settings import *

class StaticTile(pygame.sprite.Sprite):
    def __init__(self, pos, size, surface):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, size, surface, item_type):
        super().__init__()
        self.item_type = item_type
        self.frames = []
        self.frame_index = 0
        self.animation_speed = 0.15

        if self.item_type in ['coin', 'star']:
            if self.item_type == 'coin':
                frame_w = 80
                frame_h = 80
                target_w = 24
                target_h = 24
            else:
                frame_w = 50
                frame_h = 49
                target_w = 28
                target_h = 28

            sheet_w = surface.get_width()

            if sheet_w >= frame_w:
                for x in range(0, sheet_w, frame_w):
                    frame_surf = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
                    frame_surf.blit(surface, (0, 0), pygame.Rect(x, 0, frame_w, frame_h))
                    scaled_frame = pygame.transform.scale(frame_surf, (target_w, target_h))
                    self.frames.append(scaled_frame)
            else:
                self.frames.append(pygame.transform.scale(surface, (target_w, target_h)))
        else:
            self.frames.append(surface)

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        if self.item_type in ['coin', 'star'] and len(self.frames) > 0:
            self.animate()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size, surface, collision_sprites):
        super().__init__()
        
        self.frames = []
        frame_width = 59
        frame_height = 97
        sheet_width = surface.get_width()
        
        if sheet_width >= frame_width:
            for x in range(0, sheet_width, frame_width):
                frame_surf = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                frame_surf.blit(surface, (0, 0), pygame.Rect(x, 0, frame_width, frame_height))
                self.frames.append(frame_surf)
        else:
            self.frames.append(surface)
            
        self.frame_index = 0
        self.animation_speed = 0.15
        
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(bottomleft=(pos[0], pos[1] + size)) 
        
        self.direction = 1
        self.speed = 2
        self.collision_sprites = collision_sprites

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
            
        original_image = self.frames[int(self.frame_index)]
        
        if self.direction < 0:
            self.image = pygame.transform.flip(original_image, True, False)
        else:
            self.image = original_image

    def check_collisions(self):
        self.rect.x += self.direction * self.speed
        
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction > 0:
                    self.rect.right = sprite.rect.left
                elif self.direction < 0:
                    self.rect.left = sprite.rect.right
                self.direction *= -1
                return 

        ledge_check_rect = pygame.Rect(self.rect.centerx + (self.direction * TILE_SIZE // 2), self.rect.bottom + 1, 2, 2)
        is_on_ledge = False
        
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(ledge_check_rect):
                is_on_ledge = True
                break
                
        if not is_on_ledge:
            self.direction *= -1

    def update(self):
        self.animate()
        self.check_collisions()