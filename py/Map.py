import pytmx
from py.Tile import Tile
from py.Person import all_sprites
from py.Enemy import *
import pygame
import sqlite3
from py.Portal import  *

enemys = []
con = sqlite3.connect("data\\bd\\parameters.db")
cur = con.cursor()
res = cur.execute("""PRAGMA table_info(Enemys)""").fetchall()
res2 = cur.execute("""SELECT * FROM Enemys""").fetchall()
print(res2)


class Map(pygame.sprite.Sprite):
    def __init__(self, player, level):
        super().__init__(all_sprites)

        self.image = pygame.Surface(level['size'])
        self.map = pytmx.load_pygame(level['map'])
        sky = pygame.image.load(level['sky'])
        if sky.get_height() < 768:
            sky = pygame.transform.scale(sky, (sky.get_width(), 768))
        for i in range(level['size'][0] // level['sky_size'] + 1):
            self.image.blit(sky, (level['sky_size'] * i, 0))
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = 48
        for i in range(level['cnt_layers']):
            for y in range(self.height):
                for x in range(self.width):
                    image = self.map.get_tile_image(x, y, i)
                    if image:
                        image = pygame.transform.scale(image, (48, 48))
                    gid = self.map.get_tile_gid(x, y, i)
                    #print(gid, end=' ')
                    if image:
                        if i == level['layer_h']:
                            Tile(image, x, y, 'h_let')
                        elif i == level['layer_portal']:
                            print(21)
                            portal = Portal(x * self.tile_size, y * self.tile_size, player)
                        elif i == level['layer_v']:
                            Tile(image, x - 1, y - 1, 'v_let')
                        elif i == level['layer_enemy']:
                            print(gid)
                            par = {}
                            if gid == level['skeleton']:
                                enemy = 9    # skel
                            for j in range(16):
                                par[res[j][1]] = res2[enemy][j]
                            enemys.append((Enemy(par, x * self.tile_size, y * self.tile_size), pygame.NUMEVENTS - 1 - len(enemys) * 2, pygame.NUMEVENTS - 2 - len(enemys) * 2))
                        elif i in level['layer_draw']:
                            self.image.blit(image, (x * self.tile_size, y * self.tile_size))


                #print()


        self.rect = self.image.get_rect()
        self.rect = self.rect.move(0, 0)
        instructions = [pygame.transform.scale(pygame.image.load(f"data\\GameMap\\instructions\\{i}.png"), (128, 128)) for i in ['left_mouse', 'right_mouse']]
        keys = [pygame.transform.scale(pygame.image.load(f"data\\Keys\\{i}-Key.png").subsurface((0, 0, 32, 32)), (64, 64)) for i in ['A', 'D']]
        shift = pygame.transform.scale(pygame.image.load(f"data\\Keys\\Shift-Key.png").subsurface((0, 0, 48, 32)), (96, 64))
        self.image.blit(instructions[0], (1000, 300))
        font = pygame.font.Font(None, 36)
        self.text_attack = font.render('Attack', True, 'red')
        self.image.blit(self.text_attack, (1028, 450))

        self.image.blit(instructions[1], (1150, 300))
        font = pygame.font.Font(None, 36)
        self.text_attack = font.render('Block', True, 'red')
        self.image.blit(self.text_attack, (1182, 450))

        self.image.blit(keys[0], (1300, 370))
        self.image.blit(keys[1], (1364, 370))
        font = pygame.font.Font(None, 36)
        self.text_attack = font.render('Motion', True, 'red')
        self.image.blit(self.text_attack, (1325, 450))

        self.image.blit(shift, (1464, 370))
        font = pygame.font.Font(None, 36)
        self.text_attack = font.render('Dodge', True, 'red')
        self.image.blit(self.text_attack, (1476, 450))

        button_end = Button('E')
        button_end.rect = button_end.rect.move(535 * 48 - 220, 520)

        images = [7, 9, 8]
        rast = [(5000, 240, 1.5, True), (10000, -25, 1, False), (20000, 435, 2, False)]
        for i in range(3):
            house = pygame.image.load(f'data\\GameMap\\buildings\\House{images[i]}.png')
            if rast[i][3]:
                house = pygame.transform.flip(house, True, False)
            house = pygame.transform.scale(house, (house.get_width() * rast[i][2], house.get_height() * rast[i][2]))
            self.image.blit(house, rast[i][:2])

    def get_tile_id(self, position):
        return self.map.tiledgidmap(self.map.get_tile_gid(*position, 0))