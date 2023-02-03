import pygame
import os
import sys
import pygame_gui

pygame.init()
size = width, height = 1900, 1000
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MAZE")
STEP = 50
fps = 300
clock = pygame.time.Clock()


def visibility():
    value_visibility = 25
    circle = pygame.Surface((1900, 1000), pygame.SRCALPHA)
    pygame.draw.circle(circle, (0, 0, 0, value_visibility), (950, 500), 300, 300)
    value_visibility = 250
    pygame.draw.circle(circle, (0, 0, 0, value_visibility), (950, 500), 1500, 1200)
    screen.blit(circle, (0, 0))


def fon():
    bg = pygame.image.load('textures/wall.jpg')
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
    'leave': load_image('door_leave.png'),
    'exit': load_image('door_exit.png')
}
player_image = load_image('hero.png')

title_width = title_height = 200


def terminate():
    pygame.quit()
    sys.exit()


def you_really_want_leave():
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
        clock.tick(fps)


def you_passed_maze():
    rules = ['ВЫ ПРОШЛИ ЛАБИРИНТ,', 'МОЖЕТЕ ВЫБРАТЬ ОДНУ ИЗ НАГРАД ']
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
    text_true_button = surf.render('hp', True, pygame.Color('dark red'))
    text_false_button = surf.render('damage', True, pygame.Color('dark red'))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 650 < mouse[0] < 750 and 800 < mouse[1] < 900:
                    return 'hp'
                if 1150 < mouse[0] < 1300 and 800 < mouse[1] < 900:
                    return 'damage'
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
        clock.tick(fps)


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
        self.rect = self.rect.move(title_width * pos_x, title_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(title_width * pos_x + 50, title_height * pos_y + 50)


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
player = None
player, level_x, level_y = generate_level(load_level('maze.txt'))
running = True
true_button = [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP,
               pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s]
check_button = []
copy_button = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key in true_button:
                check_button.append(event.key)
        if event.type == pygame.KEYUP:
            if event.key in true_button and event.key in check_button:
                check_button.remove(event.key)
    for button in check_button:
        if button == pygame.K_LEFT or button == pygame.K_a:
            player.rect.x -= STEP
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.x += STEP
        if button == pygame.K_RIGHT or button == pygame.K_d:
            player.rect.x += STEP
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.x -= STEP
        if button == pygame.K_UP or button == pygame.K_w:
            player.rect.y -= STEP
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.y += STEP
        if button == pygame.K_DOWN or button == pygame.K_s:
            player.rect.y += STEP
            if pygame.sprite.spritecollideany(player, box_group):
                player.rect.y -= STEP
    if pygame.sprite.spritecollideany(player, leave_sprite):
        if you_really_want_leave():
            print('продолжаем проходить лабиринт')
            player.rect.y -= STEP * 2
        else:
            print('возвращаемся на основную карту')
    if pygame.sprite.spritecollideany(player, exit_sprite):
        if you_passed_maze() == 'hp':
            print('получаем хп')
        if you_passed_maze() == 'damage':
            print('получаем урон')
        if you_passed_maze() == 'speed':
            print('получаем скорость')
    screen.fill((0, 0, 0))
    fon()
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    tiles_group.draw(screen)
    player_group.draw(screen)
    visibility()
    pygame.display.flip()
    clock.tick(fps)
