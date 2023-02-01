import pytmx
from py.Tile import Tile
from py.Person import all_sprites
from py.load_image import load_image
from py.Enemy import *
import pygame
import  sqlite3

enemys = []
con = sqlite3.connect("data\\bd\\parameters.db")
cur = con.cursor()
res = cur.execute("""PRAGMA table_info(Enemys)""").fetchall()
res2 = cur.execute("""SELECT * FROM Enemys""").fetchall()
print(res2)



class Map(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((535 * 48, 1080))
        self.map = pytmx.load_pygame('data\\GameMap\\map\\tiled\\Level_0.tmx')
        sky = pygame.transform.scale(pygame.image.load("data\\GameMap\\map\\background\\Forest.png"), (1920, 1080))
        for i in range(535 * 48 // 800):
            self.image.blit(sky, (800 * i, 0))
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = 48
        for i in range(18):
            for y in range(self.height):
                for x in range(self.width):
                    image = self.map.get_tile_image(x, y, i)
                    if image:
                        image = pygame.transform.scale(image, (48, 48))
                    gid = self.map.get_tile_gid(x, y, i)
                    #print(gid, end=' ')
                    if image:
                        if i == 0:
                            Tile(image, x, y, 'h_let')
                        elif i == 17:
                            Tile(image, x - 1, y - 1, 'v_let')
                        elif i == 16:
                            print(gid)
                            par = {}
                            if gid == 574:
                                a = 0
                            else:
                                a = 2
                            for j in range(16):
                                par[res[j][1]] = res2[a][j]
                            enemys.append((Enemy(par, x * self.tile_size, y * self.tile_size), pygame.NUMEVENTS - 1 - len(enemys) * 2, pygame.NUMEVENTS - 2 - len(enemys) * 2))
                        elif i in [2, 6, 8, 11, 13, 15]:
                            self.image.blit(image, (x * self.tile_size, y * self.tile_size))


                #print()


        self.rect = self.image.get_rect()
        self.rect = self.rect.move(0, 0)

    def get_tile_id(self, position):
        return self.map.tiledgidmap(self.map.get_tile_gid(*position, 0))