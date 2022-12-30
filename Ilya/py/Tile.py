import pygame

all_sprites = pygame.sprite.Group()
tile_size = 10


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_size * x, tile_size * y)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))