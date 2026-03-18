import pygame
import math
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
        self.is_following = False
        self.target = None
        self.base_y = pos[1] 

        if self.item_type in ['coin', 'star']:
            frame_w, frame_h = (80, 80) if self.item_type == 'coin' else (50, 49)
            target_w, target_h = (24, 24) if self.item_type == 'coin' else (28, 28)

            sheet_w = surface.get_width()
            if sheet_w >= frame_w:
                for x in range(0, sheet_w, frame_w):
                    frame_surf = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
                    frame_surf.blit(surface, (0, 0), pygame.Rect(x, 0, frame_w, frame_h))
                    self.frames.append(pygame.transform.scale(frame_surf, (target_w, target_h)))
            else:
                self.frames.append(pygame.transform.scale(surface, (target_w, target_h)))
        else:
            self.frames.append(surface)

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def floating_effect(self):
        time = pygame.time.get_ticks()
        self.rect.centery = self.base_y + math.sin(time / 200) * 5

    def trailing_effect(self, player_pos):
        if self.target and player_pos:
            facing_right = getattr(self.target, 'facing_right', True)
            offset_x = -30 if facing_right else 30
            target_v = pygame.math.Vector2(player_pos[0] + offset_x, player_pos[1] - 20)
            current_v = pygame.math.Vector2(self.rect.center)
            new_pos = current_v.lerp(target_v, 0.15)
            self.rect.center = (int(new_pos.x), int(new_pos.y))

    def update(self, *args):
        player_pos = args[0] if args else None
        if self.item_type in ['coin', 'star'] and len(self.frames) > 1:
            self.animate()
        if self.item_type == 'key':
            if not self.is_following: self.floating_effect()
            else: self.trailing_effect(player_pos)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size, surface, collision_sprites):
        super().__init__()
        self.frames = []
        frame_width, frame_height = 59, 97
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
        if self.frame_index >= len(self.frames): self.frame_index = 0
        img = self.frames[int(self.frame_index)]
        self.image = pygame.transform.flip(img, True, False) if self.direction < 0 else img

    def check_collisions(self):
        self.rect.x += self.direction * self.speed
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.direction > 0: self.rect.right = sprite.rect.left
                else: self.rect.left = sprite.rect.right
                self.direction *= -1
                return 

        l_check = pygame.Rect(self.rect.centerx + (self.direction * 16), self.rect.bottom + 1, 2, 2)
        if not any(s.rect.colliderect(l_check) for s in self.collision_sprites):
            self.direction *= -1

    def update(self, *args):
        self.animate()
        self.check_collisions()

class CrumblingPlatform(pygame.sprite.Sprite):
    def __init__(self, pos, size, surface):
        super().__init__()
        if surface: self.image = surface.copy()
        else:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill('blue') 
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.math.Vector2(pos)
        self.velocity_y = 0
        self.gravity = 0.8
        self.activated = False

    def update(self, *args):
        if self.activated:
            self.velocity_y += self.gravity
            self.pos.y += self.velocity_y
            self.rect.y = int(self.pos.y)
            if self.rect.top > SCREEN_HEIGHT * 1.5: self.kill()

    def start_crumbling(self, group):
        if not self.activated:
            self.activated = True
            for sprite in group:
                if not sprite.activated:
                    distance = self.pos.distance_to(sprite.pos)
                    if distance <= TILE_SIZE + 2: 
                        sprite.start_crumbling(group)
class SurpriseBlock(pygame.sprite.Sprite):
    def __init__(self, pos, size, surface, item_surf, popped_surf):
        super().__init__()
        self.image = surface if surface else pygame.Surface((size, size))
        if not surface: self.image.fill('yellow')
            
        self.rect = self.image.get_rect(topleft=pos)
        self.item_surf = item_surf
        self.popped_image = popped_surf
        
        if not popped_surf:
            self.popped_image = pygame.Surface((size, size))
            self.popped_image.fill((100, 100, 100))
            
        self.is_empty = False

    def spawn_trap(self, trap_group, visible_group, collision_group):
        if not self.is_empty:
            spawn_pos = (self.rect.x, self.rect.y - TILE_SIZE)
            trap = Item01(spawn_pos, TILE_SIZE, self.item_surf, collision_group)
            trap_group.add(trap)
            visible_group.add(trap)
            
            self.is_empty = True
            self.image = self.popped_image

class Item01(pygame.sprite.Sprite):
    def __init__(self, pos, size, surface, collision_sprites):
        super().__init__()
        self.frames = []
        f_w, f_h = 97, 92 

        if surface and surface.get_width() >= f_w:
            num_frames = surface.get_width() // f_w
            for i in range(num_frames):
                x = i * f_w
                frame_surf = pygame.Surface((f_w, f_h), pygame.SRCALPHA)
                frame_surf.blit(surface, (0, 0), pygame.Rect(x, 0, f_w, f_h))
                self.frames.append(pygame.transform.scale(frame_surf, (size, size)))
        
        if not self.frames:
            if surface and surface.get_width() > 0:
                self.frames.append(pygame.transform.scale(surface, (size, size)))
            else:
                fallback = pygame.Surface((size, size))
                fallback.fill('green')
                self.frames.append(fallback)

        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = 1
        self.speed = 3
        self.collision_sprites = collision_sprites

    def animate(self):
        if len(self.frames) > 1:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.frames): self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]

    def update(self, *args):
        self.animate()
        self.rect.x += self.direction * self.speed
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.direction > 0: self.rect.right = sprite.rect.left
                else: self.rect.left = sprite.rect.right
                self.direction *= -1
                return 
        l_check = pygame.Rect(self.rect.centerx + (self.direction * 16), self.rect.bottom + 1, 2, 2)
        if not any(s.rect.colliderect(l_check) for s in self.collision_sprites):
            self.direction *= -1