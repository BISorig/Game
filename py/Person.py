import pygame.sprite
import sqlite3
from py.load_image import *
from py.Tile import all_sprites, let_sprites, h_let_sprites, v_let_sprites
player_group = pygame.sprite.Group()

con = sqlite3.connect("data\\bd\\parameters.db")
cur = con.cursor()
res_person = cur.execute("""PRAGMA table_info(Person)""").fetchall()
res2_person = cur.execute("""SELECT * FROM Person""").fetchall()
par_person = {}
for i in range(len(res_person)):
    par_person[res_person[i][1]] = res2_person[0][i]


class Person(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(player_group, all_sprites)
        size_person = (w, h)
        self.images = {"right": {'Idle': [pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Idle\\Idle{i}.png"), size_person)
                                           for i in range(8)],
                                 'Run': [pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Run\\Run{i}.png"), size_person)
                                         for i in range(10)],
                                 'Jump': [pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Jump\\Jump{i}.png"), size_person)
                                          for i in range(3)],
                                 'Attack': [pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Attack1\\Attack{i}.png"), size_person)
                                            for i in range(20)],
                                 'Roll': [pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Roll\\Roll{i}.png"), size_person)
                                            for i in range(9)],
                                 'BlockIdle': [pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\BlockIdle\\BlockIdle{i}.png"), size_person)
                                            for i in range(8)],
                                 'Hit': [pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Hit\\Hit{i}.png"), size_person)
                                         for i in range(3)],
                                 'Death': [pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Death\\Death{i}.png"),size_person)
                                           for i in range(10)]
                                 },


                       "left": {'Idle': [pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Idle\\Idle{i}.png"), size_person), True, False)
                                         for i in range(8)],
                                'Run': [pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Run\\Run{i}.png"), size_person), True, False)
                                        for i in range(10)],
                                'Jump': [pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Jump\\Jump{i}.png"), size_person), True, False)
                                         for i in range(3)],
                                'Attack': [pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Attack1\\Attack{i}.png"), size_person), True, False)
                                           for i in range(20)],
                                'Roll': [pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Roll\\Roll{i}.png"), size_person), True, False)
                                         for i in range(9)],
                                'BlockIdle': [pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\BlockIdle\\BlockIdle{i}.png"), size_person), True, False)
                                          for i in range(8)],
                                'Hit': [pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Hit\\Hit{i}.png"),size_person), True, False)
                                              for i in range(3)],
                                'Death': [pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Death\\Death{i}.png"),size_person), True, False)
                                        for i in range(10)]

                                },
                       }
        self.masks = {"right": {"Idle": [pygame.mask.from_surface(self.images["right"]["Idle"][i]) for i in range(8)],
                                "Run": [pygame.mask.from_surface(self.images["right"]["Run"][i]) for i in range(10)],
                                "Jump": [pygame.mask.from_surface(self.images["right"]["Jump"][i]) for i in range(3)],
                                "Attack": [pygame.mask.from_surface(self.images["right"]["Attack"][i]) for i in range(20)],
                                "BlockIdle": [pygame.mask.from_surface(self.images["right"]["BlockIdle"][i]) for i in range(8)],
                                "Roll": [pygame.mask.from_surface(self.images["right"]["Roll"][i]) for i in range(9)],
                                "Hit": [pygame.mask.from_surface(self.images["right"]["Hit"][i]) for i in range(3)]},

                      "left": {"Idle": [pygame.mask.from_surface(self.images["left"]["Idle"][i]) for i in range(8)],
                               "Run": [pygame.mask.from_surface(self.images["left"]["Run"][i]) for i in range(10)],
                               "Jump": [pygame.mask.from_surface(self.images["left"]["Jump"][i]) for i in range(3)],
                               "Roll": [pygame.mask.from_surface(self.images["left"]["Roll"][i]) for i in range(9)],
                               "BlockIdle": [pygame.mask.from_surface(self.images["left"]["BlockIdle"][i]) for i in range(8)],
                               "Attack": [pygame.mask.from_surface(self.images["left"]["Attack"][i]) for i in range(20)],
                               "Hit": [pygame.mask.from_surface(self.images["left"]["Hit"][i]) for i in range(3)]
                               }}
        self.image = self.images['right']['Idle'][0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(875, 450)
        print(x, y, self.rect)
        self.route = 'right'
        self.num_images = 0
        self.step = par_person['step']
        self.mode = "Idle"
        self.jump_m = -1
        self.jump = 500
        self.jump_h = 5
        self.pr_mode = "Idle"
        self.attack_queue = 0
        self.hp = 9999999999999999999
        self.event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.event, 100)
        self.fl_block = 0
        self.num_attack = 0
        self.damage = par_person['damage']

    def update(self, motion_keydown, mouse_down, screen):

        font = pygame.font.Font(None, 36)
        self.text = font.render(str(self.hp), True, 'red')
        self.death()
        if self.mode != 'Death':
            if self.mode == 'Hit' and self.num_images == 3:
                pygame.time.set_timer(self.event, 150)
                self.mode = 'Idle'
                self.num_images = 0
            self.motion(motion_keydown)
            self.attack(mouse_down)
            self.mask = self.masks[self.route][self.mode][self.num_images]
        if self.mode == 'Death' and self.num_images == 9:
            pygame.time.set_timer(self.event, 0)
        self.image = self.images[self.route][self.mode][self.num_images]

    def motion(self, keydown):
        if self.mode == 'Roll':
            if self.num_images == 9:
                pygame.time.set_timer(self.event, 150)
                self.num_images = 0
                self.mode = 'Idle'
            elif self.route == 'right':
                self.rect.x += self.step
                if pygame.sprite.spritecollideany(self, v_let_sprites):
                    self.rect.x -= self.step
            else:
                self.rect.x -= self.step
                if pygame.sprite.spritecollideany(self, v_let_sprites):
                    self.rect.x += self.step
        if (not keydown or keydown[:2] in [[pygame.K_d, pygame.K_a], [pygame.K_a, pygame.K_d]]) and self.mode not in ['Attack', 'Roll', 'BlockIdle', 'Hit']:
            self.mode = "Idle"
            self.num_images %= 8
        if keydown[:2] not in [[pygame.K_d, pygame.K_a], [pygame.K_a, pygame.K_d]]:
            for key in keydown[:2]:
                if key in [pygame.K_a, pygame.K_d]:
                    if self.mode not in ['Run', 'Jump', 'Attack', 'Roll', 'BlockIdle', 'Hit']:
                        self.mode = 'Run'
                        self.num_images = 0
                    else:
                        self.pr_mode = 'Run'
                    if self.mode != 'Hit':
                        if key == pygame.K_a and self.mode != 'Hit':
                            k = -1
                            self.route = 'left'
                        else:
                            k = 1
                            self.route = 'right'
                        if self.mode not in ['Attack', 'Roll', 'BlockIdle']:
                            self.rect.x += self.step * k
                            self.num_images %= 10
                            if pygame.sprite.spritecollideany(self, v_let_sprites):
                                self.rect.x -= self.step * k

                if key == 1073742049 and self.mode not in ['Attack', 'Roll', 'BlockIdle', 'Hit']:
                    keydown.remove(1073742049)
                    self.mode = 'Roll'
                    self.num_images = 0
                    pygame.time.set_timer(self.event, 75)

        if not pygame.sprite.spritecollideany(self, h_let_sprites) and self.jump_m == -1:
            if self.mode != 'Attack':
                self.mode = "Jump"
                self.num_images = 2
            self.rect.y += self.jump_h
        elif pygame.sprite.spritecollideany(self, h_let_sprites) and self.mode == 'Jump':
            self.mode = self.pr_mode


    def attack(self, mouse_down):
        if mouse_down == 1 and self.mode not in ['Hit', 'BlockIdle']:
            self.attack_queue += 1
            if self.mode != 'Attack':
                pygame.time.set_timer(self.event, 75)
                self.mode = 'Attack'
                self.num_images = 0
                self.num_attack = 1
        elif (mouse_down == 3 or self.fl_block) and self.mode not in ['Attack', 'Jump', 'Roll', 'Hit']:
            self.mode = 'BlockIdle'
            self.num_images %= 8
            self.fl_block = 1
        if mouse_down == -3 and self.mode == 'BlockIdle':
            self.mode = 'Idle'
            self.num_images = 0
            self.fl_block = 0

        if self.mode == 'Attack':
            if self.num_images == 6 and self.num_attack == 1 and self.attack_queue:
                self.attack_queue -= 1
                self.num_attack = 2
            if self.num_images == 12 and self.num_attack == 2 and self.attack_queue:
                self.attack_queue -= 1
                self.num_attack = 3
            if self.num_images == 20 and self.num_attack == 3 and self.attack_queue:
                self.attack_queue = 0
            if self.num_images in [2, 3, 8, 9, 16, 17]:
                if self.route == 'right':
                    self.rect.x += self.step
                else:
                    self.rect.x -= self.step
            if not self.attack_queue:
                self.mode = 'Idle'
                pygame.time.set_timer(self.event, 150)
                self.num_images = 0

    def hit(self, enemy):
        pygame.time.set_timer(self.event, 75)
        self.mode = 'Hit'
        self.num_images = 0
        self.route = 'right'
        if enemy.route == 'right':
            self.route = 'left'

    def death(self):
        if self.hp <= 0 and self.mode != 'Death':
            self.mode = 'Death'
            self.num_images = 0
            pygame.time.set_timer(self.event, 300)



