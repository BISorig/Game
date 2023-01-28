import pygame
import os
import sys

pygame.init()
size = width, height = 1900, 1000
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Перемещение героя. Камера")
STEP = 25
fps = 60
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('textures', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    if name == 'hero.png':
        image = pygame.transform.scale(image, (24, 40))
    else:
        image = pygame.transform.scale(image, (200, 200))
    return image


tile_images = {
    'wall': load_image('wall.jpg'),
    'empty': load_image('pol.jpg')
}
player_image = load_image('hero.png')

title_width = title_height = 200


def terminate():
    pygame.quit()
    sys.exit()


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
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(title_width * pos_x, title_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(title_width * pos_x + 15, title_height * pos_y + 5)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('empty', x, y)
            if level[y][x] == '*':
                Tile('wall', x, y)
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
        print(self.dx, self.dy)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
camera = Camera()
player = None
player, level_x, level_y = generate_level(load_level('maze.txt'))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.rect.x -= STEP
                if pygame.sprite.spritecollideany(player, box_group):
                    player.rect.x += STEP
            if event.key == pygame.K_RIGHT:
                player.rect.x += STEP
                if pygame.sprite.spritecollideany(player, box_group):
                    player.rect.x -= STEP
            if event.key == pygame.K_UP:
                player.rect.y -= STEP
                if pygame.sprite.spritecollideany(player, box_group):
                    player.rect.y += STEP
            if event.key == pygame.K_DOWN:
                player.rect.y += STEP
                if pygame.sprite.spritecollideany(player, box_group):
                    player.rect.y -= STEP
    screen.fill((0, 0, 0))
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(fps)