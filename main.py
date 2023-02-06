from py.level import *
from py.Map import Map
from py.Button import button_group
from py.Portal import portal_group
from py.Tile import all_sprites, v_let_sprites, h_let_sprites, map_sprite
from py.Enemy import enemys_group
from py.menu import *


con = sqlite3.connect("data\\bd\\parameters.db")
cur = con.cursor()
pygame.init()
pygame.mouse.set_visible(True)
size = w, h = 1920, 1080
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
while Menu(screen, con, cur):
    level = cur.execute("""SELECT level FROM Person""").fetchall()[0][0]
    button_group.empty()
    portal_group.empty()
    all_sprites.empty()
    v_let_sprites.empty()
    h_let_sprites.empty()
    map_sprite.empty()
    player_group.empty()
    enemys_group.empty()
    player = Person(100, 100, 250, 165)
    if level == 1:
        level1 = {'size': (535 * 48, 1080), 'map': 'data\\GameMap\\map\\tiled\\Level_0.tmx',
                  'sky': 'data\\GameMap\\background\\Forest.png', 'sky_size': 800,
                  'layer_draw': (2, 8, 9, 12, 14), 'layer_h': 0, 'layer_portal': 19, 'layer_v': 18,
                  'layer_enemy': 17, 'cnt_layers': 20, 'skeleton': 577, 'goblin': 576,
                  'huntress': 574, 'Martial Hero 3': 575}
        mp = Map(player, level1, level)
        Level(player, mp, 1, 'eazy')
    level = cur.execute("""SELECT level FROM Person""").fetchall()[0][0]
    if level == 2:
        button_group.empty()
        portal_group.empty()
        all_sprites.empty()
        v_let_sprites.empty()
        h_let_sprites.empty()
        map_sprite.empty()
        player.rect.x = 100
        player.rect.y = 100
        level2 = {'size': (445 * 48, 1080), 'map': 'data\\GameMap\\map2\\tiled\\Level_0.tmx',
                  'sky': 'data\\GameMap\\background\\Sky3.png', 'sky_size': 1024, 'layer_draw': (2, 8, 3),
                  'layer_h': 0, 'layer_portal': 15, 'layer_v': 14, 'layer_enemy': 13, 'cnt_layers': 16, 'skeleton': 18}
        mp = Map(player, level2, level)
        print(mp.rect)
        Level(player, mp, 2)
    level = cur.execute("""SELECT level FROM Person""").fetchall()[0][0]
    if level == 3:
        button_group.empty()
        portal_group.empty()
        all_sprites.empty()
        v_let_sprites.empty()
        h_let_sprites.empty()
        map_sprite.empty()
        player.rect.x = 100
        player.rect.y = 100
        level2 = {'size': (445 * 48, 1080), 'map': 'data\\GameMap\\map3\\tiled\\Level_0.tmx',
                  'sky': 'data\\GameMap\\background\\Sky3.png', 'sky_size': 1024, 'layer_draw': (2, 8, 3),
                  'layer_h': 0, 'layer_portal': 15, 'layer_v': 14, 'layer_enemy': 13, 'cnt_layers': 16, 'skeleton': 18}
        mp = Map(player, level2, level)
        print(mp.rect)
        Level(player, mp, 2)
