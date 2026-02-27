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
        self.image = surface
        self.rect = self.image.get_rect(center=pos)
        self.item_type = item_type # 'coin', 'star', 'upgrade'

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size, surface):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = 1
        self.speed = 2

    def reverse_image(self):
        if self.direction > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, shift):
        self.rect.x += self.direction * self.speed

class Boss(pygame.sprite.Sprite):
    def __init__(self, pos, size, surface):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.health = 10
    