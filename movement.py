import pygame
from settings import *

class Movement:
    def __init__(self, player):
        self.p = player
        self.direction = pygame.math.Vector2()
        
        self.is_dashing = False
        self.can_dash = True
        self.has_dashed = False
        self.dash_timer = 0
        self.dash_cooldown_timer = 0
        
        # Thêm biến khóa phím Dash để chống Auto-fire
        self.dash_locked = False 

        self.stamina_max = 300
        self.stamina = self.stamina_max
        self.is_grabbing = False
        self.climb_speed = 4

        self.wall_jump_timer = 0
        self.wall_jump_duration = 150 
        self.jump_locked = False

    def input(self, keys):
        current_time = pygame.time.get_ticks()

        # 1. KIỂM TRA PHÍM DASH CÓ KHÓA (LOCK)
        if keys[K_DASH]:
            if not self.dash_locked and self.can_dash and not self.has_dashed:
                self.start_dash(keys)
            self.dash_locked = True
        else:
            self.dash_locked = False

        # 2. DI CHUYỂN NGANG
        if not self.is_dashing:
            if current_time - self.wall_jump_timer > self.wall_jump_duration:
                if not self.is_grabbing or self.p.on_ground:
                    target_x = 0
                    if keys[pygame.K_RIGHT]:
                        target_x = 1
                        self.p.facing_right = True
                    elif keys[pygame.K_LEFT]:
                        target_x = -1
                        self.p.facing_right = False
                    
                    if target_x != 0:
                        if abs(self.direction.x) > 1 and (self.direction.x > 0) == (target_x > 0):
                            fric = 0.05 if self.p.on_ground else 0.02
                            self.direction.x = pygame.math.lerp(self.direction.x, target_x, fric)
                        else:
                            self.direction.x = target_x
                    else:
                        if abs(self.direction.x) > 1:
                            fric = 0.15 if self.p.on_ground else 0.04
                            self.direction.x = pygame.math.lerp(self.direction.x, 0, fric)
                        else:
                            self.direction.x = pygame.math.lerp(self.direction.x, 0, 0.2)

        # 3. NHẢY & SUPER JUMP
        if keys[K_JUMP]:
            if not self.jump_locked:
                if self.is_dashing:
                    self.is_dashing = False
                    self.dash_cooldown_timer = current_time 
                    
                    if self.p.on_wall:
                        self.direction.y = JUMP_SPEED * 1.15
                        self.direction.x = -3.0 if self.p.facing_right else 3.0
                        self.stamina -= 10
                        self.wall_jump_timer = current_time
                    else:
                        self.direction.y = -8.0 
                        momentum = 3.2
                        if self.direction.x != 0:
                            self.direction.x = momentum if self.direction.x > 0 else -momentum
                        else:
                            self.direction.x = momentum if self.p.facing_right else -momentum
                else:
                    if self.p.on_ground:
                        self.direction.y = JUMP_SPEED
                        self.is_grabbing = False
                        self.p.on_wall = False
                    elif self.p.on_wall and self.stamina > 0:
                        is_pressing_into_wall = (self.p.facing_right and keys[pygame.K_RIGHT]) or \
                                                (not self.p.facing_right and keys[pygame.K_LEFT])
                        
                        self.direction.y = 0 
                        self.direction.x = 0

                        if is_pressing_into_wall:
                            self.p.rect.x += -8 if self.p.facing_right else 8
                            self.direction.y = JUMP_SPEED 
                            self.stamina -= 15
                            self.wall_jump_timer = current_time 
                        else:
                            self.direction.y = JUMP_SPEED * 0.8
                            self.direction.x = -1.2 if self.p.facing_right else 1.2
                            self.stamina -= 10
                            self.wall_jump_timer = current_time
                        
                        self.is_grabbing = False
                        self.p.on_wall = False
                
                self.jump_locked = True
        else:
            if self.jump_locked:
                if self.direction.y < -3:
                    if abs(self.direction.x) > 2.0:
                        self.direction.y *= 0.7
                    else:
                        self.direction.y *= 0.5
                self.jump_locked = False

        # 4. BÁM TƯỜNG
        if not self.is_dashing:
            can_grab = current_time - self.wall_jump_timer > 100 
            if keys[K_GRAB] and self.p.on_wall and not self.p.on_ground and self.stamina > 0 and can_grab:
                self.is_grabbing = True
                
                if current_time - self.dash_timer > 1000:
                    self.has_dashed = False 
                
                self.direction.x = 0
                if keys[pygame.K_UP]:
                    self.direction.y = -self.climb_speed
                    self.stamina -= 0.8
                elif keys[pygame.K_DOWN]:
                    self.direction.y = self.climb_speed
                    self.stamina -= 0.2
                else:
                    self.direction.y = 0
                    self.stamina -= 0.3
            else:
                self.is_grabbing = False
        else:
            self.is_grabbing = False

    # def apply_gravity(self):
    #     if self.is_grabbing: return 
        
    #     self.direction.y += GRAVITY
    #     if self.direction.y > 12: self.direction.y = 12

    #     if self.p.on_ground:
    #         self.stamina = self.stamina_max
    #         self.has_dashed = False
    def apply_gravity(self):
        if self.is_grabbing: return 
        self.direction.y += GRAVITY
        if self.direction.y > 12: self.direction.y = 12
        if self.p.on_ground:
            self.stamina = self.stamina_max
            self.has_dashed = False
            self.can_dash = True 

    def start_dash(self, keys):
        self.is_grabbing = False
        self.p.on_wall = False
        self.direction.x = 0
        self.direction.y = 0

        self.is_dashing = True
        self.can_dash = False
        self.has_dashed = True
        self.dash_timer = pygame.time.get_ticks()
        
        move_x = 0
        move_y = 0
        if keys[pygame.K_RIGHT]: move_x = 1
        elif keys[pygame.K_LEFT]: move_x = -1
        if keys[pygame.K_UP]: move_y = -1
        elif keys[pygame.K_DOWN]: move_y = 1
            
        if move_x == 0 and move_y == 0:
            move_x = 1 if self.p.facing_right else -1
            
        self.direction.x = move_x
        self.direction.y = move_y
        
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

    def check_dash_status(self):
        current_time = pygame.time.get_ticks()
        if self.is_dashing and current_time - self.dash_timer >= DASH_DURATION:
            self.is_dashing = False
            self.dash_cooldown_timer = current_time
            
            if self.direction.x > 0: self.direction.x = 1.0
            elif self.direction.x < 0: self.direction.x = -1.0
            
            self.direction.y = 0 
                
        if not self.can_dash and not self.is_dashing and current_time - self.dash_cooldown_timer >= DASH_COOLDOWN:
            self.can_dash = True