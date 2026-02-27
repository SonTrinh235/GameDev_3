import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(topleft = pos)
        
        self.obstacle_sprites = obstacle_sprites

        # Movement States
        self.direction = pygame.math.Vector2()
        self.on_ground = False
        self.on_wall = False
        self.facing_right = True

        # Dash Logic
        self.is_dashing = False
        self.can_dash = True
        self.dash_timer = 0
        self.dash_cooldown_timer = 0

        # Grab Logic
        self.is_grabbing = False

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.is_dashing:
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.facing_right = True
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.facing_right = False
            else:
                self.direction.x = 0

            if keys[K_JUMP] and self.on_ground:
                self.direction.y = JUMP_SPEED

            if keys[K_DASH] and self.can_dash:
                self.start_dash()

        self.is_grabbing = keys[K_GRAB]

    def start_dash(self):
        self.is_dashing = True
        self.can_dash = False
        self.dash_timer = pygame.time.get_ticks()
        dash_dir = self.direction.x if self.direction.x != 0 else (1 if self.facing_right else -1)
        self.direction.x = dash_dir
        self.direction.y = 0

    def check_dash_status(self):
        current_time = pygame.time.get_ticks()
        if self.is_dashing:
            if current_time - self.dash_timer >= DASH_DURATION:
                self.is_dashing = False
                self.dash_cooldown_timer = current_time
        
        if not self.can_dash and not self.is_dashing:
            if current_time - self.dash_cooldown_timer >= DASH_COOLDOWN:
                self.can_dash = True

    def apply_gravity(self):
        if self.is_grabbing and self.on_wall and self.direction.y > 0:
            self.direction.y += GRAVITY * WALL_FRICTION
            if self.direction.y > WALL_SLIDE_SPEED:
                self.direction.y = WALL_SLIDE_SPEED
        else:
            self.direction.y += GRAVITY
            if self.direction.y > TERMINAL_VELOCITY:
                self.direction.y = TERMINAL_VELOCITY
        
        self.rect.y += self.direction.y

    def horizontal_collision(self):
        self.on_wall = False
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left
                    self.on_wall = True
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                    self.on_wall = True

    def vertical_collision(self):
        self.on_ground = False
        for sprite in self.obstacle_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def update(self):
        self.check_dash_status()
        self.input()
        
        if self.is_dashing:
            self.rect.x += self.direction.x * DASH_SPEED
            self.horizontal_collision()
        else:
            self.rect.x += self.direction.x * PLAYER_SPEED
            self.horizontal_collision()
            self.apply_gravity()
            self.vertical_collision()