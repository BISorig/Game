import sqlite3

import pygame
import os
import sys

pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption("HARD MAZE")


def Maze(screen, level, main_player):
    STEP = 25

    def visibility():
        value_visibility = 25
        circle = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        pygame.draw.circle(circle, (0, 0, 0, value_visibility), (950, 500), 300, 300)
        value_visibility = 250
        pygame.draw.circle(circle, (0, 0, 0, value_visibility), (950, 500), 1700, 1400)
        screen.blit(circle, (0, 0))

    def fon():
        bg = pygame.image.load('textures/pol.jpg')
        bg = pygame.transform.scale(bg, (1900, 1000))
        screen.blit(bg, (0, 0))

    def load_image(name):
        fullname = os.path.join('textures', name)
        image = pygame.image.load(fullname)
        if name == 'hero.png':
            image = pygame.transform.scale(image, (150, 100))
        else:
            image = pygame.transform.scale(image, (200, 200))
        return image

    tile_images = {
        'wall': load_image('wall.jpg'),
        'empty': load_image('pol.jpg'),
        'leave': load_image('door_leave.jpg'),
        'exit': load_image('door_exit.jpg')
    }

    tile_width = tile_height = 200

    def terminate():
        pygame.quit()
        sys.exit()

    def you_really_want_leave():
        pygame.mouse.set_visible(True)
        rules = ['ВЫ ТОЧНО ХОТИТЕ ВЕРНУТЬСЯ', ' БЕЗ НАГРАДЫ?']
        font = pygame.font.Font(None, 50)
        bg = pygame.image.load('textures/true_leave.png')
        bg = pygame.transform.scale(bg, (1000, 200))
        screen.blit(bg, (450, 0))
        text_coord = 50
        for line in rules:
            line_rendered = font.render(line, 1, pygame.Color("dark red"))
            line_rect = line_rendered.get_rect()
            text_coord += 10
            line_rect.top = text_coord
            line_rect.x = 650
            text_coord += line_rect.height
            screen.blit(line_rendered, line_rect)
        surf = pygame.font.SysFont('Corbel', 100)
        text_true_button = surf.render('yes', True, pygame.Color('dark red'))
        text_false_button = surf.render('no', True, pygame.Color('dark red'))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if 650 < mouse[0] < 750 and 800 < mouse[1] < 900:
                        return True
                    if 1150 < mouse[0] < 1300 and 800 < mouse[1] < 900:
                        return False

            pos_m = pygame.mouse.get_pos()
            if 650 < pos_m[0] < 750 and 800 < pos_m[1] < 900:
                pygame.draw.circle(screen, pygame.Color('white'), (700, 850), 75, 5)
            elif 1150 < pos_m[0] < 1300 and 800 < pos_m[1] < 900:
                pygame.draw.circle(screen, pygame.Color('white'), (1210, 850), 75, 5)
            else:
                pygame.draw.circle(screen, pygame.Color('black'), (700, 850), 75, 5)
                pygame.draw.circle(screen, pygame.Color('black'), (1210, 850), 75, 5)
            screen.blit(text_false_button, (650, 800))
            screen.blit(text_true_button, (1150, 800))
            pygame.display.flip()

    def you_passed_maze():
        pygame.mouse.set_visible(True)
        rules = ['ВЫ ПРОШЛИ ЛАБИРИНТ,', 'МОЖЕТЕ ВЫБРАТЬ ОДНУ ИЗ НАГРАД']
        font = pygame.font.Font(None, 50)
        bg = pygame.image.load('textures/true_leave.png')
        bg = pygame.transform.scale(bg, (1000, 200))
        screen.blit(bg, (450, 0))
        text_coord = 50
        for line in rules:
            line_rendered = font.render(line, 1, pygame.Color("dark red"))
            line_rect = line_rendered.get_rect()
            text_coord += 10
            line_rect.top = text_coord
            line_rect.x = 650
            text_coord += line_rect.height
            screen.blit(line_rendered, line_rect)
        surf = pygame.font.SysFont('Corbel', 100)
        text_hp = surf.render('hp', True, pygame.Color('dark red'))
        text_damage = surf.render('damage', True, pygame.Color('dark red'))
        text_speed = surf.render('speed', True, pygame.Color('dark red'))
        text_okay = surf.render('confirm', True, pygame.Color('dark red'))
        rules_prise = ['hp: +0%', 'damage: +0%', 'speed: +0%']
        if level == 'hard':
            rules_prise = ['hp: +20%', 'damage: +20%', 'speed: +20%']
        if level == 'medium':
            rules_prise = ['hp: +15%', 'damage: +15%', 'speed: +15%']
        if level == 'eazy':
            rules_prise = ['hp: +10%', 'damage: +10%', 'speed: +10%']
        font = pygame.font.Font(None, 50)
        pygame.draw.rect(screen, pygame.Color('black'), ((100, 440), (250, 230)))
        text_coord = 400
        for line in rules_prise:
            line_rendered = font.render(line, 1, pygame.Color("dark red"))
            line_rect = line_rendered.get_rect()
            text_coord += 50
            line_rect.top = text_coord
            line_rect.x = 100
            text_coord += line_rect.height
            screen.blit(line_rendered, line_rect)
        prise = ''
        pygame.draw.rect(screen, (0, 0, 0, 2), ((302, 840), (120, 120)))
        pygame.draw.rect(screen, (0, 0, 0, 2), ((714, 840), (350, 120)))
        pygame.draw.rect(screen, (0, 0, 0, 2), ((1326, 840), (260, 120)))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    pygame.draw.rect(screen, (0, 0, 0, 2), ((302, 840), (120, 120)))
                    pygame.draw.rect(screen, (0, 0, 0, 2), ((714, 840), (350, 120)))
                    pygame.draw.rect(screen, (0, 0, 0, 2), ((1326, 840), (260, 120)))
                    if 312 < mouse[0] < 412 and 850 < mouse[1] < 950:
                        prise = 'hp'
                        pygame.draw.rect(screen, (100, 100, 100), ((302, 840), (120, 120)))
                    if 724 < mouse[0] < 1024 and 850 < mouse[1] < 950:
                        prise = 'damage'
                        pygame.draw.rect(screen, (100, 100, 100), ((714, 840), (350, 120)))
                    if 1336 < mouse[0] < 1585 and 850 < mouse[1] < 950:
                        prise = 'speed'
                        pygame.draw.rect(screen, (100, 100, 100), ((1326, 840), (260, 120)))
                    if 1400 < mouse[0] < 1750 and 500 < mouse[1] < 600:
                        pygame.draw.rect(screen, pygame.Color('white'), ((1390, 490), (330, 110)),
                                         5)
                        if prise != '':
                            return prise
            pos_m = pygame.mouse.get_pos()
            if 312 < pos_m[0] < 412 and 850 < pos_m[1] < 950:
                pygame.draw.rect(screen, pygame.Color('white'), ((302, 840), (120, 120)), 5)
            elif 724 < pos_m[0] < 1024 and 850 < pos_m[1] < 950:
                pygame.draw.rect(screen, pygame.Color('white'), ((714, 840), (350, 120)), 5)
            elif 1336 < pos_m[0] < 1586 and 850 < pos_m[1] < 950:
                pygame.draw.rect(screen, pygame.Color('white'), ((1326, 840), (260, 120)), 5)
            elif 1400 < pos_m[0] < 1750 and 500 < pos_m[1] < 600:
                pygame.draw.rect(screen, pygame.Color('white'), ((1390, 490), (330, 110)), 5)
                text_okay = surf.render('confirm', True, pygame.Color('light green'))
            else:
                pygame.draw.rect(screen, pygame.Color('black'), ((1390, 490), (330, 110)))
                text_okay = surf.render('confirm', True, pygame.Color('dark red'))
                pygame.draw.rect(screen, (0, 0, 0, 2), ((302, 840), (120, 120)), 5)
                pygame.draw.rect(screen, (0, 0, 0, 2), ((714, 840), (350, 120)), 5)
                pygame.draw.rect(screen, (0, 0, 0, 2), ((1326, 840), (260, 120)), 5)
            screen.blit(text_okay, (1400, 500))
            screen.blit(text_hp, (312, 850))
            screen.blit(text_damage, (724, 850))
            screen.blit(text_speed, (1336, 850))
            pygame.display.flip()

    def load_level(filename):
        filename = 'maps/' + filename
        with open(filename, 'r') as file:
            map_level = list(map(str.strip, file.readlines()))
        max_width = max(map(len, map_level))
        return list(map(lambda x: x.ljust(max_width, '.'), map_level))

    class Tile(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(tiles_group, all_sprites)
            if tile_type == 'wall':
                self.add(box_group)
            if tile_type == 'leave':
                self.add(leave_sprite)
            if tile_type == 'exit':
                self.add(exit_sprite)
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)

    class Player(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(player_group, all_sprites)
            size_person = (150, 100)
            self.images = {"right": {'Idle': [pygame.transform.scale(
                pygame.image.load(f"data\\Hero Knight\\Sprites\\"
                                  f"HeroKnight\\Idle\\Idle{i}.png"),
                size_person) for i in range(8)],
                                     'Run': [pygame.transform.scale(pygame.image.load(
                                         f"data\\Hero Knight\\Sprites\\"
                                         f"HeroKnight\\Run\\Run{i}.png"),
                                                                    size_person)
                                             for i in range(10)],
                                     'Death': [pygame.transform.scale(pygame.image.load(
                                         f"data\\Hero Knight\\Sprites\\"
                                         f"HeroKnight\\Death\\Death{i}.png"),
                                         size_person)
                                         for i in range(10)]
                                     },

                           "left": {'Idle': [pygame.transform.flip(pygame.transform.scale(
                               pygame.image.load(
                                   f"data\\Hero Knight\\Sprites\\"
                                   f"HeroKnight\\Idle\\Idle{i}.png"),
                               size_person), True, False)
                               for i in range(8)],
                               'Run': [pygame.transform.flip(pygame.transform.scale(
                                   pygame.image.load(
                                       f"data\\Hero Knight\\Sprites\\"
                                       f"HeroKnight\\Run\\Run{i}.png"),
                                   size_person), True, False)
                                   for i in range(10)],
                               'Death': [
                                   pygame.transform.flip(pygame.transform.scale(pygame.image.load(
                                       f"data\\Hero Knight\\Sprites\\"
                                       f"HeroKnight\\Death\\Death{i}.png"),
                                       size_person),
                                       True, False)
                                   for i in range(10)]

                           }
                           }
            self.image = self.images['right']['Idle'][0]
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(tile_width * pos_x + 50, tile_height * pos_y + 50)
            self.num_images = 0
            self.event = pygame.USEREVENT + 100
            self.mode = 'Idle'
            pygame.time.set_timer(self.event, 100)
            self.route = 'right'

    def generate_level(level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '#':
                    Tile('empty', x, y)
                if level[y][x] == '*':
                    Tile('wall', x, y)
                if level[y][x] == 'l':
                    Tile('leave', x, y)
                if level[y][x] == 'e':
                    Tile('exit', x, y)
                if level[y][x] == '.':
                    Tile('empty', x, y)
                    new_player = Player(x, y)
        return new_player, x, y

    class Camera:
        def __init__(self):
            self.dx = 0
            self.dy = 0

        def apply(self, obj):
            obj.rect.x += self.dx
            obj.rect.y += self.dy

        def update(self, target):
            self.dx = width // 2 - (target.rect.x + target.rect.w // 2)
            self.dy = height // 2 - (target.rect.y + target.rect.h // 2)

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    leave_sprite = pygame.sprite.Group()
    exit_sprite = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    box_group = pygame.sprite.Group()
    camera = Camera()
    level_txt = f"maze_{level}.txt"
    player, level_x, level_y = generate_level(load_level(level_txt))
    running = True
    true_button = [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP,
                   pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s]
    check_button = []
    while running:
        player.mode = 'Idle'
        player.route = 'right'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key in true_button:
                    check_button.append(event.key)
            if event.type == pygame.KEYUP:
                if event.key in true_button and event.key in check_button:
                    check_button.remove(event.key)
            if event.type == player.event:
                player.num_images += 1
                player.num_images %= 8
        for button in check_button:
            player.mode = 'Run'
            if button == pygame.K_LEFT or button == pygame.K_a:
                player.rect.x -= STEP
                player.route = 'left'
                if pygame.sprite.spritecollideany(player, box_group):
                    player.rect.x += STEP
            elif button == pygame.K_RIGHT or button == pygame.K_d:
                player.rect.x += STEP
                if pygame.sprite.spritecollideany(player, box_group):
                    player.rect.x -= STEP
            elif button == pygame.K_UP or button == pygame.K_w:
                player.rect.y -= STEP
                if pygame.sprite.spritecollideany(player, box_group):
                    player.rect.y += STEP
            elif button == pygame.K_DOWN or button == pygame.K_s:
                player.rect.y += STEP
                if pygame.sprite.spritecollideany(player, box_group):
                    player.rect.y -= STEP
        player.image = player.images[player.route][player.mode][player.num_images]
        if pygame.sprite.spritecollideany(player, leave_sprite):
            check_button = []
            if you_really_want_leave():
                pygame.mouse.set_visible(False)
                if level == 'hard' or level == 'medium':
                    player.rect.y -= STEP
                if level == 'eazy':
                    player.rect.x += STEP
            else:
                running = False
                return False
        if pygame.sprite.spritecollideany(player, exit_sprite):
            prise = you_passed_maze()
            if prise == 'hp':
                if level == 'hard':
                    main_player.max_hp *= 1.2
                if level == 'medium':
                    main_player.max_hp *= 1.15
                if level == 'eazy':
                    main_player.max_hp *= 1.1
            elif prise == 'damage':
                if level == 'hard':
                    main_player.damage *= 1.2
                if level == 'medium':
                    main_player.damage *= 1.15
                if level == 'eazy':
                    main_player.damage *= 1.1
            elif prise == 'speed':
                if level == 'hard':
                    main_player.step *= 1.2
                if level == 'medium':
                    main_player.step *= 1.15
                if level == 'eazy':
                    main_player.step *= 1.1
            running = False
            return True

        screen.fill((0, 0, 0))
        fon()
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        tiles_group.draw(screen)
        player_group.draw(screen)
        if level != 'eazy':
            visibility()
        pygame.display.flip()
