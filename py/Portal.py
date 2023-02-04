import pygame
from py.load_image import load_image
from py.Button import *

portal_group = pygame.sprite.Group()


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__(portal_group)
        self.images = [load_image(f'data\\GameMap\\map\\portal\\portal{i}.gif', (4, 2, 4)) for i in range(9)]
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i], (self.images[i].get_width() // 2, self.images[i].get_height() // 2))
        self.image = self.images[0]
        self.masks = [pygame.mask.from_surface(self.images[i]) for i in range(9)]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.num_images = 0
        self.event = pygame.USEREVENT + 10
        pygame.time.set_timer(self.event, 100)
        self.button = Button('E')
        self.button.rect = self.button.rect.move(self.rect.x + self.image.get_width() // 2 - 30, self.rect.y - 60)
        self.player = player

    def update(self):
        print(self.button.rect)
        self.num_images += 1
        self.num_images %= 9
        self.image = self.images[self.num_images]
        if pygame.sprite.collide_mask(self.player, self):
            self.button.draw_fl = 1
        else:
            self.button.draw_fl = 0


