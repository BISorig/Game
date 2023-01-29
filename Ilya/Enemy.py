import random

import pygame.sprite
from Tile import h_let_sprites
from load_image import load_image
enemys_group = pygame.sprite.Group()
enemys_events = []


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, step=0):
        super().__init__(enemys_group)
        size_person = x, y
        self.images = {"right": {'Idle': [load_image(f"data\\Enemy\\Fantasy Warrior\\Sprites\\Idle\\Idle{i}.png", 'white') for i in range(10)],
                                 'Run': [load_image(f"data\\Enemy\\Fantasy Warrior\\Sprites\\Run\\Run{i}.png", 'white')
                                           for i in range(8)],
                                 'Attack': [load_image(f"data\\Enemy\\Fantasy Warrior\\Sprites\\Attack\\Attack{i}.png", 'white')
                                           for i in range(7)]},
                       "left": {'Idle': [pygame.transform.flip(load_image(f"data\\Enemy\\Fantasy Warrior\\Sprites\\Idle\\Idle{i}.png", 'white'), True, False)
                                          for i in range(10)],
                                'Run': [pygame.transform.flip(load_image(f"data\\Enemy\\Fantasy Warrior\\Sprites\\Run\\Run{i}.png", 'white'), True, False)
                                        for i in range(8)],
                                'Attack': [pygame.transform.flip(load_image(f"data\\Enemy\\Fantasy Warrior\\Sprites\\Attack\\Attack{i}.png", 'white'), True, False)
                                           for i in range(7)]
                                }
                       }
        for route in self.images.keys():
            for mode in self.images[route].keys():
                for image in range(len(self.images[route][mode])):
                    self.images[route][mode][image] = pygame.transform.scale(self.images[route][mode][image], (self.images[route][mode][image].get_width() * 4,
                                                                                                               self.images[route][mode][image].get_height() * 4))
        self.masks = {"right": {"Idle": [pygame.mask.from_surface(self.images["right"]["Idle"][i]) for i in range(10)],
                                "Run": [pygame.mask.from_surface(self.images["right"]["Run"][i]) for i in range(8)],
                                "Attack": [pygame.mask.from_surface(self.images["right"]["Attack"][i]) for i in range(7)]},

                      "left": {"Idle": [pygame.mask.from_surface(self.images["left"]["Idle"][i]) for i in range(10)],
                               "Run": [pygame.mask.from_surface(self.images["left"]["Run"][i]) for i in range(8)],
                               "Attack": [pygame.mask.from_surface(self.images["left"]["Attack"][i]) for i in range(7)]}}
        self.image = self.images['right']['Idle'][0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(random.randint(1000, 1600), 500)
        self.route = 'right'
        self.num_images = 0
        self.step = 4
        self.mode = "Idle"
        self.pr_mode = 'Idle'
        self.event_calmness = pygame.NUMEVENTS - 1 - len(enemys_events)
        enemys_events.append(self.event_calmness)
        self.event_attack = pygame.NUMEVENTS - 1 - len(enemys_events)
        enemys_events.append(self.event_attack)
        print(2)
        pygame.time.set_timer(self.event_attack, 0)
        pygame.time.set_timer(self.event_calmness, 100)
        self.hp = 100
        self.damage = 1

    def update(self, player):
        if pygame.sprite.collide_mask(self, player) and player.mode == 'Attack':
            self.hp -= 10
        if self.hp <= 0:
            self.kill()
        if self.mode != 'Attack':
            self.turn(player)
        if (player.rect.x - self.rect.x) ** 2 + (player.rect.y - self.rect.y) ** 2 > 1000000 and self.mode not in ['Idle', 'Attack']:
            self.pr_mode = self.mode
            self.mode = 'Idle'
            self.num_images = 0
        elif 100000 < (player.rect.x - self.rect.x) ** 2 + (player.rect.y - self.rect.y) ** 2 <= 1000000 and self.mode not in ['Run', 'Attack']:
            self.pr_mode = self.mode
            self.mode = 'Run'
            self.num_images = 0
        if (player.rect.x - self.rect.x) ** 2 + (player.rect.y - self.rect.y) ** 2 <= 100000 and self.mode != 'Attack':
            self.pr_mode = self.mode
            self.mode = 'Attack'
            self.fl = 0
            self.num_images = 0
        if self.mode in ['Idle', 'Run'] and self.pr_mode not in ['Idle', 'Run']:
            self.pr_mode = self.mode
            print(1)
            pygame.time.set_timer(self.event_attack, 0)
            print(self.event_attack)
            pygame.time.set_timer(self.event_calmness, 100)
            print(self.event_calmness)
        elif self.mode == 'Attack' and self.pr_mode != 'Attack':
            print(3)
            self.pr_mode = 'Attack'
            pygame.time.set_timer(self.event_calmness, 0)
            print(self.event_calmness)
            pygame.time.set_timer(self.event_attack, 300)
            print(self.event_attack)
            #pygame.time.set_timer(self.event_attack, 300)
        self.motion(player)
        self.attack(player)
        self.image = self.images[self.route][self.mode][self.num_images]

    def turn(self, player):
        self.route = 'right'
        if (player.rect.x - (self.rect.x - self.step)) ** 2 < (player.rect.x - (self.rect.x + self.step)) ** 2:
            self.route = 'left'

    def motion(self, player):
        if self.mode == 'Idle':
            self.num_images %= 10
        if self.mode == 'Run':
            self.num_images %= 8
            turn = 1
            if self.route == 'left':
                turn = -1
            self.rect.x += self.step * turn
        if not pygame.sprite.spritecollideany(self, h_let_sprites):
            self.rect.y += self.step

    def attack(self, player):
        if self.mode == 'Attack':
            self.num_images %= 7
            if self.num_images == 3:
                if self.route == 'right' and not (pygame.sprite.collide_mask(self, player) and player.mode == 'Block'):
                    self.rect.x += self.step * 10
                elif not (pygame.sprite.collide_mask(self, player) and player.mode == 'Block'):
                    self.rect.x -= self.step * 10
                elif self.route == 'right':
                    player.rect.x += player.step
                else:
                    player.rect.x -= player.step
            if player.mode != 'Roll' and pygame.sprite.collide_mask(self, player):
                player.hp -= 0.5
            if self.num_images == 6:
                self.mode = 'Idle'
                self.fl = 0
            if self.num_images == 1 and self.route == 'right' and self.mode == 'Attack' and not self.fl:
                self.rect.x -= self.step * 40
                self.fl = 1


