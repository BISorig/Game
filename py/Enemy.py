import random

import pygame.sprite
from py.Tile import h_let_sprites
from py.load_image import load_image
enemys_group = pygame.sprite.Group()
enemys_events = []


class Enemy(pygame.sprite.Sprite):
    def __init__(self, params, x, y):
        super().__init__(enemys_group)
        self.images = {"right": {'Idle': [load_image(f"data\\Enemy\\{params['Name']}\\Sprites\\Idle\\Idle{i}.png", 'white')
                                          for i in range(params['idle'])],
                                 'Run': [load_image(f"data\\Enemy\\{params['Name']}\\Sprites\\Run\\Run{i}.png", 'white')
                                         for i in range(params['run'])],
                                 'Attack': [load_image(f"data\\Enemy\\{params['Name']}\\Sprites\\Attack\\Attack{i}.png", 'white')
                                            for i in range(params['attack_pict_num'])],
                                 'Hit': [load_image(f"data\\Enemy\\{params['Name']}\\Sprites\\Hit\\Hit{i}.png", 'white')
                                            for i in range(params['hit_pict_num'])],
                                 'Death': [load_image(f"data\\Enemy\\{params['Name']}\\Sprites\\Death\\Death{i}.png", 'white')
                                            for i in range(params['death_pict_num'])]
                                 },
                       "left": {'Idle': [pygame.transform.flip(load_image(f"data\\Enemy\\{params['Name']}\\Sprites\\Idle\\Idle{i}.png", 'white'), True, False)
                                         for i in range(params['idle'])],
                                'Run': [pygame.transform.flip(load_image(f"data\\Enemy\\{params['Name']}\\Sprites\\Run\\Run{i}.png", 'white'), True, False)
                                        for i in range(params['run'])],
                                'Attack': [pygame.transform.flip(load_image(f"data\\Enemy\\{params['Name']}\\Sprites\\Attack\\Attack{i}.png", 'white'), True, False)
                                           for i in range(params['attack_pict_num'])],
                                'Hit': [pygame.transform.flip(load_image(f"data\\Enemy\\{params['Name']}\\Sprites\\Hit\\Hit{i}.png", 'white'), True, False)
                                           for i in range(params['hit_pict_num'])],
                                'Death': [pygame.transform.flip(load_image(f"data\\Enemy\\{params['Name']}\\Sprites\\Death\\Death{i}.png", 'white'), True, False)
                                        for i in range(params['death_pict_num'])]
                                }
                       }
        for route in self.images.keys():
            for mode in self.images[route].keys():
                for image in range(len(self.images[route][mode])):
                    self.images[route][mode][image] = pygame.transform.scale(self.images[route][mode][image], (self.images[route][mode][image].get_width() * 4,
                                                                                                               self.images[route][mode][image].get_height() * 4))
        self.masks = {"right": {"Idle": [pygame.mask.from_surface(self.images["right"]["Idle"][i]) for i in range(params['idle'])],
                                "Run": [pygame.mask.from_surface(self.images["right"]["Run"][i]) for i in range(params['run'])],
                                "Attack": [pygame.mask.from_surface(self.images["right"]["Attack"][i]) for i in range(params['attack_pict_num'])],
                                "Hit": [pygame.mask.from_surface(self.images["right"]["Hit"][i]) for i in range(params['hit_pict_num'])]},

                      "left": {"Idle": [pygame.mask.from_surface(self.images["left"]["Idle"][i]) for i in range(params['idle'])],
                               "Run": [pygame.mask.from_surface(self.images["left"]["Run"][i]) for i in range(params['run'])],
                               "Attack": [pygame.mask.from_surface(self.images["left"]["Attack"][i]) for i in range(params['attack_pict_num'])],
                               'Hit': [pygame.mask.from_surface(self.images["left"]["Hit"][i]) for i in range(params['hit_pict_num'])]}}
        self.image = self.images['right']['Idle'][0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.route = 'right'
        self.num_images = 0
        self.step = params['step']
        self.mode = "Idle"
        self.pr_mode = 'Idle'
        self.event = pygame.NUMEVENTS - 1 - len(enemys_events)
        enemys_events.append(self.event)
        pygame.time.set_timer(self.event, params['idle_event_time'])
        self.hp = params['hp']
        self.damage = params['damage']
        self.params = params
        self.events = [self.event]

    def update(self, player):
        self.death()
        if player.mode == 'Death':
            self.mode = 'Idle'
            self.num_images %= self.params['idle']
        elif self.mode != 'Death':
            if (player.rect.x - self.rect.x) ** 2 + (player.rect.y - self.rect.y) ** 2 > 1000000 and self.mode not in ['Idle', 'Attack', 'Hit']:
                self.pr_mode = self.mode
                self.mode = 'Idle'
                self.num_images = 0
            elif 100000 < (player.rect.x - self.rect.x) ** 2 + (player.rect.y - self.rect.y) ** 2 <= 1000000 and self.mode not in ['Run', 'Attack', 'Hit']:
                self.pr_mode = self.mode
                self.mode = 'Run'
                self.num_images = 0
            if (player.rect.x - self.rect.x) ** 2 + (player.rect.y - self.rect.y) ** 2 <= 100000 and self.mode not in ['Attack', 'Hit']:
                self.pr_mode = self.mode
                self.mode = 'Attack'
                self.fl = 0
                self.num_images = 0
            #print(self.mode, self.pr_mode)
            if self.mode == 'Idle' and self.pr_mode != 'Idle':
                self.pr_mode = self.mode
                pygame.time.set_timer(self.event, self.params['idle_event_time'])
            elif self.mode == 'Hit' and self.pr_mode != 'Hit':
                self.pr_mode = self.mode
                pygame.time.set_timer(self.event, 200)
            elif self.mode == 'Run' and self.pr_mode != 'Run':
                self.pr_mode = self.mode
                pygame.time.set_timer(self.event, self.params['run_event_time'])
            elif self.mode == 'Attack' and self.pr_mode != 'Attack':
                self.pr_mode = 'Attack'
                pygame.time.set_timer(self.event, self.params['attack_event_time'])



            self.hit(player)
            self.turn(player)

            self.motion(player)
            self.attack(player)
        elif self.mode == 'Death' and self.num_images == self.params['death_pict_num'] - 1:
            pygame.time.set_timer(self.event, 0)
            #print(self.num_images)
        self.image = self.images[self.route][self.mode][self.num_images]

    def turn(self, player):
        if self.mode not in ['Hit', 'Attack']:
            self.route = 'right'
            if (player.rect.x - (self.rect.x - 10)) ** 2 < (player.rect.x - (self.rect.x + 10)) ** 2:
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
        if self.num_images == self.params['attack_pict_num'] and self.mode == 'Attack':
            self.mode = 'Idle'
            self.fl = 0
        if self.mode == 'Attack':
            self.num_images %= self.params['attack_pict_num']
            if self.num_images == self.params['attack_motion_pict_num']:
                if self.route == 'right' and not (pygame.sprite.collide_mask(self, player) and player.mode == 'BlockIdle'):
                    self.rect.x += self.params['attack_motion']

                elif not (pygame.sprite.collide_mask(self, player) and player.mode == 'BlockIdle'):
                    self.rect.x -= self.params['attack_motion']
                elif self.route == 'right':
                    player.rect.x += player.step
                else:
                    player.rect.x -= player.step
            # if self.num_images == 0:
            #     self.a = self.rect.x
            # if self.num_images == self.params['attack_pict_num'] - 1:
            #     #print(self.rect.x - self.a)
            if player.mode != 'Roll' and pygame.sprite.collide_mask(self, player) and self.num_images not in [0, 1, 2]:
                player.hp -= self.damage
                if player.mode not in ['BlockIdle', 'Death']:
                    player.hit(self)

    def death(self):
        if self.hp <= 0 and self.mode != 'Death':
            self.mode = 'Death'
            self.num_images = 0
            pygame.time.set_timer(self.event, 300)



    def hit(self, player):
        if pygame.sprite.collide_mask(self, player) and player.mode == 'Attack' and self.mode != 'Hit' and (self.mode != 'Attack' or self.num_images in [0, 1, 2]):
            self.pr_mode = self.mode
            self.mode = 'Hit'
            self.num_images = 0
        elif self.mode == 'Hit' and self.num_images == self.params['hit_pict_num']:
            self.pr_mode = 'Hit'
            self.mode = 'Idle'
            self.num_images = 0
        if self.mode == 'Hit' and self.num_images == 0:
            self.hp -= 1
            if player.route == 'right':
                self.rect.x += 3
                self.route = 'left'
            else:
                self.rect.x -= 3
                self.route = 'right'


