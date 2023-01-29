import pygame
import sys
import os

FPS = 60

pygame.init()
size = w, h = 400, 300
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Перемещение героя. Новый уровень')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    print(fullname)
    if not os.path.isfile(fullname):
        print(f'Файл с рисунком "{fullname}" не найден!')
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is None:
        image.convert_alpha()
    else:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')
tile_width = tile_height = 50


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    rules = ["Перемещение героя", "", "", "Герой двигается", "Карта на месте"]
    font = pygame.font.Font(None, 30)
    text_coord = 50
    image = load_image('fon.jpg')
    image = pygame.transform.scale(image, (400, 300))
    screen.blit(image, (0, 0))
    for line in rules:
        line_rend = font.render(line, True, "black")
        line_rect = line_rend.get_rect()
        text_coord += 10
        line_rect.top = text_coord
        line_rect.x = 10
        text_coord += line_rect.height
        screen.blit(line_rend, line_rect)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as file:
        map_level = file.read().split('\n')
    max_width = max(map(len, map_level))
    return list(map(lambda x: x.ljust(max_width, '.'), map_level))


class Tile(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__(all_sprites, tiles_group)
        if type == 'wall':
            self.add(box_group)
        self.image = tile_images[type]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * x, tile_height * y)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, player_group)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * x + 15, tile_height * y + 5)


def generate(level):
    new, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new = Player(x, y)
    return new, x, y


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - w // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - h // 2)


clock = pygame.time.Clock()
run = True
start_screen()
camera = Camera()
h_borders = pygame.sprite.Group()
v_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
box_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
pl = None
pl, level_x, level_y = generate(load_level('level1.txt'))
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pl.rect.y -= 50
                if pygame.sprite.spritecollideany(pl, box_group):
                    pl.rect.y += 50
            if event.key == pygame.K_LEFT:
                pl.rect.x -= 50
                if pygame.sprite.spritecollideany(pl, box_group):
                    pl.rect.x += 50
            if event.key == pygame.K_DOWN:
                pl.rect.y += 50
                if pygame.sprite.spritecollideany(pl, box_group):
                    pl.rect.y -= 50
            if event.key == pygame.K_RIGHT:
                pl.rect.x += 50
                if pygame.sprite.spritecollideany(pl, box_group):
                    pl.rect.x -= 50
    screen.fill((0, 0, 0))
    camera.update(pl)
    for i in all_sprites:
        camera.apply(i)
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()