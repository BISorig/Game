import pygame

button_events = []
button_group = pygame.sprite.Group()


class Button(pygame.sprite.Sprite):
    def __init__(self, key):
        super().__init__(button_group)
        self.image = pygame.transform.scale(pygame.image.load(f'data\\Keys\\{key}-Key.png'), (128, 64))
        self.images = [self.image.subsurface((0, 0, 64, 64)), self.image.subsurface((64, 0, 64, 64))]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.num_images = 0
        self.event = pygame.USEREVENT + 20 + len(button_events)
        pygame.time.set_timer(self.event, 500)
        button_events.append(self.event)
        self.draw_fl = 0

    def update(self):
        self.num_images += 1
        self.num_images %= 2
        self.image = self.images[self.num_images]
