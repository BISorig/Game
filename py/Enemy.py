import random

import pygame.sprite
from py.Tile import h_let_sprites
from py.load_image import load_image
enemys_group = pygame.sprite.Group()
enemys_events = []


class Enemy(pygame.sprite.Sprite):
    def __init__(self, params, x, y):
        super().__init__(enemys_group)
        size_person = x, y
        self.images = {"right": {'Idle': [load_image(f"data\\Enemy\\{params['Name']}\\Sprites\\Idle\\Idle{i}.png", 'white')
                                          for i in range(params['idle'])],
                                 'Run': [load_image(f"data\\Enemy\\{params['Name']}\\Sprites\\Run\\Run{i}.png", 'white')
                                         for i in range(params['run'])],
                                 'Attack': [load_image(f"data\\Enemy\\{params['Name']}\\Sprites\\Attack\\Attack{i}.png", 'white')
                                            for i in range(params['attack'])]},
                       "left": {'Idle': [pygame.transform.flip(load_image(f"data\\Enemy\\{params['Name']}\\Sprites\\Idle\\Idle{i}.png", 'white'), True, False)
                                         for i in range(params['idle'])],
                                'Run': [pygame.transform.flip(load_image(f"data\\Enemy\\{params['Name']}\\Sprites\\Run\\Run{i}.png", 'white'), True, False)
                                        for i in range(params['run'])],
                                'Attack': [pygame.transform.flip(load_image(f"data\\Enemy\\{params['Name']}\\Sprites\\Attack\\Attack{i}.png", 'white'), True, False)
                                           for i in range(params['attack'])]
                                }
                       }
        for route in self.images.keys():
            for mode in self.images[route].keys():
                for image in range(len(self.images[route][mode])):
                    self.images[route][mode][image] = pygame.transform.scale(self.images[route][mode][image], (self.images[route][mode][image].get_width() * 4,
                                                                                                               self.images[route][mode][image].get_height() * 4))
        self.masks = {"right": {"Idle": [pygame.mask.from_surface(self.images["right"]["Idle"][i]) for i in range(params['idle'])],
                                "Run": [pygame.mask.from_surface(self.images["right"]["Run"][i]) for i in range(params['run'])],
                                "Attack": [pygame.mask.from_surface(self.images["right"]["Attack"][i]) for i in range(params['attack'])]},

                      "left": {"Idle": [pygame.mask.from_surface(self.images["left"]["Idle"][i]) for i in range(params['idle'])],
                               "Run": [pygame.mask.from_surface(self.images["left"]["Run"][i]) for i in range(params['run'])],
                               "Attack": [pygame.mask.from_surface(self.images["left"]["Attack"][i]) for i in range(params['attack'])]}}
        self.image = self.images['right']['Idle'][0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(random.randint(1000, 1600), 500)
        self.route = 'right'
        self.num_images = 0
        self.step = params['step']
        self.mode = "Idle"
        self.pr_mode = 'Idle'
        self.event_calmness = pygame.NUMEVENTS - 1 - len(enemys_events)
        enemys_events.append(self.event_calmness)
        self.event_attack = pygame.NUMEVENTS - 1 - len(enemys_events)
        enemys_events.append(self.event_attack)
        print(2)
        pygame.time.set_timer(self.event_attack, 0)
        pygame.time.set_timer(self.event_calmness, 80)
        self.hp = params['hp']
        self.damage = params['damage']
        self.params = params

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
            pygame.time.set_timer(self.event_attack, 0)
            pygame.time.set_timer(self.event_calmness, 50)
        elif self.mode == 'Attack' and self.pr_mode != 'Attack':
            self.pr_mode = 'Attack'
            pygame.time.set_timer(self.event_calmness, 0)
            pygame.time.set_timer(self.event_attack, 300)
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
            self.num_images %= self.params['idle']
        if self.mode == 'Run':
            self.num_images %= self.params['run']
            turn = 1
            if self.route == 'left':
                turn = -1
            self.rect.x += self.step * turn
        if not pygame.sprite.spritecollideany(self, h_let_sprites):
            self.rect.y += self.step

    def attack(self, player):
        if self.num_images == self.params['attack'] and self.mode == 'Attack':
            self.mode = 'Idle'
            self.fl = 0
        if self.mode == 'Attack':
            self.num_images %= self.params['attack']
            if self.num_images == 3:
                if self.route == 'right' and not (pygame.sprite.collide_mask(self, player) and player.mode == 'BlockIdle'):
                    self.rect.x += self.step * 10
                elif not (pygame.sprite.collide_mask(self, player) and player.mode == 'BlockIdle'):
                    self.rect.x -= self.step * 10
                elif self.route == 'right':
                    player.rect.x += player.step
                else:
                    player.rect.x -= player.step
            if player.mode != 'Roll' and pygame.sprite.collide_mask(self, player) and self.num_images not in [0, 1, 2]:
                player.hp -= 0.5



