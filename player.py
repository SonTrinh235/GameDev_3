import pygame
from settings import *
from movement import Movement

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.base_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.base_image.fill(PLAYER_COLOR)
        self.image = self.base_image
        self.rect = self.image.get_rect(topleft = pos)
        
        self.display_width = TILE_SIZE
        self.display_height = TILE_SIZE
        self.rotation_angle = 0
        
        self.obstacle_sprites = obstacle_sprites
        self.display_surface = pygame.display.get_surface()
        self.m = Movement(self)
        
        self.on_ground = False
        self.on_wall = False
        self.facing_right = True
        self.old_on_ground = False

        self.remainder_x = 0.0
        self.remainder_y = 0.0

    def animate(self):
        if self.m.direction.y < 0 and not self.on_ground:
            self.display_width = pygame.math.lerp(self.display_width, TILE_SIZE * 0.75, 0.2)
            self.display_height = pygame.math.lerp(self.display_height, TILE_SIZE * 1.25, 0.2)
        elif self.m.direction.y > 0 and not self.on_ground:
            self.display_width = pygame.math.lerp(self.display_width, TILE_SIZE * 1.1, 0.1)
            self.display_height = pygame.math.lerp(self.display_height, TILE_SIZE * 0.9, 0.1)
        elif self.on_ground and not self.old_on_ground:
            self.display_width = TILE_SIZE * 1.5
            self.display_height = TILE_SIZE * 0.5
        else:
            self.display_width = pygame.math.lerp(self.display_width, TILE_SIZE, 0.2)
            self.display_height = pygame.math.lerp(self.display_height, TILE_SIZE, 0.2)

        target_angle = 0
        if self.on_wall and not self.on_ground:
            target_angle = 12 if self.facing_right else -12
        elif self.m.direction.x != 0 and self.on_ground:
            target_angle = -8 if self.m.direction.x > 0 else 8
        self.rotation_angle = pygame.math.lerp(self.rotation_angle, target_angle, 0.15)

        scaled = pygame.transform.scale(self.base_image, (int(self.display_width), int(self.display_height)))
        self.image = pygame.transform.rotate(scaled, self.rotation_angle)
        
        curr_bottom = self.rect.bottom
        curr_centerx = self.rect.centerx
        self.rect = self.image.get_rect(midbottom = (curr_centerx, curr_bottom))

    def horizontal_collision(self):
        self.on_wall = False
        check_rect = self.rect.inflate(4, 0)
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(check_rect):
                if sprite.rect.colliderect(self.rect):
                    if self.m.direction.x > 0: 
                        self.rect.right = sprite.rect.left
                        self.remainder_x = 0 
                    elif self.m.direction.x < 0: 
                        self.rect.left = sprite.rect.right
                        self.remainder_x = 0 
                
                if not self.on_ground:
                    if self.rect.right >= sprite.rect.left - 2:
                        self.on_wall = True
                        self.facing_right = True
                    elif self.rect.left <= sprite.rect.right + 2:
                        self.on_wall = True
                        self.facing_right = False

    def vertical_collision(self):
        if self.m.is_grabbing: return
        
        self.old_on_ground = self.on_ground
        self.on_ground = False
        
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.m.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.m.direction.y = 0
                    self.remainder_y = 0 
                    self.on_ground = True
                elif self.m.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.m.direction.y = 0
                    self.remainder_y = 0 

        # Kiểm tra dính sàn (Ground Stickiness)
        if not self.on_ground and self.old_on_ground and self.m.direction.y >= 0:
            check_rect = self.rect.move(0, 1) # Check dò xuống 1 pixel
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(check_rect):
                    self.on_ground = True
                    self.m.direction.y = 0
                    self.remainder_y = 0
                    break

    def draw_stamina(self, offset):
        if self.m.stamina < self.m.stamina_max:
            bar_width = (self.m.stamina / self.m.stamina_max) * TILE_SIZE
            bar_rect = pygame.Rect(self.rect.left - offset.x, self.rect.top - 15 - offset.y, bar_width, 5)
            color = 'red' if self.m.stamina < 100 else 'yellow' if self.m.stamina < 200 else 'green'
            pygame.draw.rect(self.display_surface, color, bar_rect)

    def update(self):
        self.m.check_dash_status()
        self.m.input(pygame.key.get_pressed())
        
        speed = DASH_SPEED if self.m.is_dashing else PLAYER_SPEED
        
        move_x = (self.m.direction.x * speed) + self.remainder_x
        move_int_x = int(move_x)
        self.remainder_x = move_x - move_int_x
        
        self.rect.x += move_int_x
        self.horizontal_collision()
        
        if self.m.is_dashing:
            move_y = (self.m.direction.y * speed) + self.remainder_y
        else:
            self.m.apply_gravity()
            move_y = self.m.direction.y + self.remainder_y
            
        move_int_y = int(move_y)
        self.remainder_y = move_y - move_int_y
        
        self.rect.y += move_int_y
        self.vertical_collision()
            
        self.animate()