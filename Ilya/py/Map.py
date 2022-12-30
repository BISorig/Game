import pygame
import pytmx
from py.Tile import *


class Map(pygame.sprite.Sprite):
    def __init__(self, free_tiles, finish_tiles):
        super().__init__(all_sprites)
        self.image = pygame.Surface((19200, 10800))
        self.map = pytmx.load_pygame('tiles/map.tmx')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                self.image.blit(image, (x * self.tile_size, y * self.tile_size))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(0, 0)

    def get_tile_id(self, position):
        return self.map.tiledgidmap(self.map.get_tile_gid(*position, 0))