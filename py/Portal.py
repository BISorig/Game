import pygame
from py.load_image import load_image

portal_group = pygame.sprite.Group()

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(portal_group)
        self.image = load_image('data\\GameMap\\map\\portal\\portal0.gif', (4, 2, 4))
        self.rect = self.image.get_rect()
        self.rect.move(1000, 1000)