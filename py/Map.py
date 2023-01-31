import pytmx
from py.Tile import Tile
from py.Person import all_sprites
from py.load_image import load_image
import pygame


class Map(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((1920, 1110))
        self.map = pytmx.load_pygame('data\\map\\level1\\tiled\\Level_0.tmx')
        sky = pygame.transform.scale(pygame.image.load("data\\map\\Magic-Cliffs-Gamekit\\Environment\\PNG\\sky.png"), (1920, 1110))
        self.image.blit(sky, (0, 0))
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = 48
        for i in range(5):
            for y in range(self.height):
                for x in range(self.width):
                    image = self.map.get_tile_image(x, y, i)
                    if image:
                        image = pygame.transform.scale(image, (48, 48))
                    gid = self.map.get_tile_gid(x, y, i)
                    #print(gid, end=' ')
                    if image:
                        if i == 1:
                            Tile(image, x, y, 'h_let')
                        else:
                            self.image.blit(image, (x * self.tile_size, y * self.tile_size))


                #print()


        self.rect = self.image.get_rect()
        self.rect = self.rect.move(0, 0)

    def get_tile_id(self, position):
        return self.map.tiledgidmap(self.map.get_tile_gid(*position, 0))