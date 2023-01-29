import pygame.sprite
from py.load_image import load_image
from py.Tile import all_sprites
player_group = pygame.sprite.Group()


class Person(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        size_person = (x, y)
        self.images = {'up': [pygame.transform.scale(load_image(f'person\\up\\up{i}.png', 'white'), size_person)
                              for i in range(11)],
                       'right': [pygame.transform.scale(load_image(f'person\\right\\right{i}.png', 'white'), size_person)
                                 for i in range(11)],
                       'down': [pygame.transform.scale(load_image(f'person\\down\\down{i}.png', 'white'), size_person)
                                for i in range(11)],
                       'left': [pygame.transform.scale(load_image(f'person\\left\\left{i}.png', 'white'), size_person)
                                for i in range(11)]}
        self.image = self.images['down'][0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(925, 470)

