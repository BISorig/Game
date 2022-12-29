import pygame
import pytmx

size = width, height = 512, 512
fps = 15
MAPS_DIR = "maps"
size_tile = 16


class Maze(pygame.sprite.Sprite):
    def __init__(self, filename, free_tiles):
        super().__init__(all_sprites)
        self.map = pytmx.load_pygame(f"{MAPS_DIR}/{filename}")
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = free_tiles

    def render(self, screen):
        world_map =
    def get_tile_id(self, position):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]

    def is_free(self, position):
        return True

    def find_path_step(self, start, target):
        inf = 1000
        x, y = start
        distance = [[inf] * self.width for i in range(self.height)]
        distance[y][x] = 0
        prev = [[None] * self.width for i in range(self.height)]
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                next_x, next_y = x + dx, y + dx
                if 0 <= next_x < self.width and 0 < next_y < self.height and \
                    self.is_free((next_x, next_y)) and distance[next_y][next_x] == inf:
                    distance[next_y][next_x] = distance[y][x] + 1
                    prev[next_y][next_x] = (x, y)
                    queue.append((next_x, next_y))
        x, y = target
        if distance[y][x] == inf or start == target:
            return start
        while prev[y][x] != start:
            x, y = prev[y][x]
        return x, y


class Hero(pygame.sprite.Sprite):
    def __init__(self, pic, position):
        super().__init__(all_sprites)
        self.x, self.y = position
        self.image = pygame.image.load(f"data/{pic}")
        self.image = pygame.transform.scale(self.image, (16, 16))

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        delta = (self.image.get_width() - size_tile) // 2
        screen.blit(self.image, (self.x * size_tile - delta, self.y * size_tile - delta))


class Game(pygame.sprite.Sprite):
    def __init__(self, maze, hero):
        super().__init__(all_sprites)
        self.maze = maze
        self.hero = hero

    def render(self, screen):
        self.maze.render(screen)
        self.hero.render(screen)

    def update_hero(self):
        next_x, next_y = self.hero.get_position()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            next_x -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            next_x += 1
        if pygame.key.get_pressed()[pygame.K_UP]:
            next_y -= 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            next_y += 1
        if self.maze.is_free((next_x, next_y)):
            self.hero.set_position((next_x, next_y))

    def check_win(self):
        if self.hero.get_position() == (31, 14):
            return True


def show_message(screen, message):
    font = pygame.font.Font(None, 50)
    text = font.render(message, 1, (50, 70, 0))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (200, 150, 50), (text_x - 10, text_y - 10,
                                              text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Лабиринт')
all_sprites = pygame.sprite.Group()
wall_sprites = pygame.sprite.Group()
hero_sprites = pygame.sprite.Group()
traps_sprites = pygame.sprite.Group()

maze = Maze("maze.tmx", [129])
hero = Hero("hero.png", (17, 31))
game = Game(maze, hero)

clock = pygame.time.Clock()
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if not game_over:
        game.update_hero()
    screen.fill((0, 0, 0))
    game.render(screen)
    if game.check_win():
        game_over = True
        show_message(screen, "You win")
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()