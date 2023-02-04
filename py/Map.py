import pytmx
from py.Tile import Tile
from py.Person import all_sprites
from py.Enemy import *
import pygame
import  sqlite3
from py.Portal import  *

enemys = []
con = sqlite3.connect("data\\bd\\parameters.db")
cur = con.cursor()
res = cur.execute("""PRAGMA table_info(Enemys)""").fetchall()
res2 = cur.execute("""SELECT * FROM Enemys""").fetchall()
print(res2)



class Map(pygame.sprite.Sprite):
    def __init__(self, player):
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
                            portal = Portal(x * self.tile_size, y * self.tile_size, player)
                        elif i == 16:
                            Tile(image, x - 1, y - 1, 'v_let')
                        elif i == 15:
                            print(gid)
                            par = {}
                            if gid == 574:
                                enemy = 9    # skel
                            elif gid == 575:
                                enemy = 2    # gob
                            elif gid == 576:
                                enemy = 4  # hunt
                            elif gid == 577:
                                enemy = 7  # med war 3
                            for j in range(16):
                                par[res[j][1]] = res2[enemy][j]
                            enemys.append((Enemy(par, x * self.tile_size, y * self.tile_size), pygame.NUMEVENTS - 1 - len(enemys) * 2, pygame.NUMEVENTS - 2 - len(enemys) * 2))
                        elif i in [2, 6, 7, 10, 12, 14]:
                            self.image.blit(image, (x * self.tile_size, y * self.tile_size))


                #print()


        self.rect = self.image.get_rect()
        self.rect = self.rect.move(0, 0)
        instructions = [pygame.transform.scale(pygame.image.load(f"data\\GameMap\\map\\instructions\\{i}.png"), (128, 128)) for i in ['left_mouse', 'right_mouse']]
        keys = [pygame.transform.scale(pygame.image.load(f"data\\Keys\\{i}-Key.png").subsurface((0, 0, 32, 32)), (64, 64)) for i in ['A', 'D']]
        shift = pygame.transform.scale(pygame.image.load(f"data\\Keys\\Shift-Key.png").subsurface((0, 0, 48, 32)), (96, 64))
        self.image.blit(instructions[0], (1400, 300))
        font = pygame.font.Font(None, 36)
        self.text_attack = font.render('Attack', True, 'red')
        self.image.blit(self.text_attack, (1428, 450))

        self.image.blit(instructions[1], (1550, 300))
        font = pygame.font.Font(None, 36)
        self.text_attack = font.render('Block', True, 'red')
        self.image.blit(self.text_attack, (1582, 450))

        self.image.blit(keys[0], (1700, 370))
        self.image.blit(keys[1], (1764, 370))
        font = pygame.font.Font(None, 36)
        self.text_attack = font.render('Motion', True, 'red')
        self.image.blit(self.text_attack, (1725, 450))

        self.image.blit(shift, (1864, 370))
        font = pygame.font.Font(None, 36)
        self.text_attack = font.render('Dodge', True, 'red')
        self.image.blit(self.text_attack, (1876, 450))

        button_end = Button('E')
        button_end.rect = button_end.rect.move(535 * 48 - 500, 400)

    def get_tile_id(self, position):
        return self.map.tiledgidmap(self.map.get_tile_gid(*position, 0))