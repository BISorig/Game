import pygame

all_sprites = pygame.sprite.Group()
let_sprites = pygame.sprite.Group()
h_let_sprites = pygame.sprite.Group()
v_let_sprites = pygame.sprite.Group()
map_sprite = pygame.sprite.Group()
tile_size = 48


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, type):
        if type == 'h_let':
            super().__init__(h_let_sprites)
        elif type == 'v_let':
            super().__init__(v_let_sprites)
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x * 48, y * 48)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))