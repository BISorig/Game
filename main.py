import os
import sys
import pygame

pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
fps = 60
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)

    return image


class FirstDungeon(pygame.sprite.Sprite):
    arena = load_image("arena.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = FirstDungeon.arena
        self.rect = self.arena.get_rect()


if __name__ == '__main__':
    pygame.display.set_caption('Первый данж')

    all_sprites = pygame.sprite.Group()

    FirstDungeon(all_sprites)
    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 255))
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()