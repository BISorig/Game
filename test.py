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
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        size_person = (150, 100)
        self.images = {"right": {'Idle': [pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Idle\\Idle{i}.png"), size_person)
                                           for i in range(8)],
                                 'Run': [pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Run\\Run{i}.png"), size_person)
                                         for i in range(10)],
                                 'Death': [pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Death\\Death{i}.png"),size_person)
                                           for i in range(10)]
                                 },


                       "left": {'Idle': [pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Idle\\Idle{i}.png"), size_person), True, False)
                                         for i in range(8)],
                                'Run': [pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Run\\Run{i}.png"), size_person), True, False)
                                        for i in range(10)],
                                'Death': [pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"data\\Hero Knight\\Sprites\\HeroKnight\\Death\\Death{i}.png"),size_person), True, False)
                                        for i in range(10)]

                                },
                       }
        self.masks = {"right": {"Idle": [pygame.mask.from_surface(self.images["right"]["Idle"][i]) for i in range(8)],
                                "Run": [pygame.mask.from_surface(self.images["right"]["Run"][i]) for i in range(10)]},

                      "left": {"Idle": [pygame.mask.from_surface(self.images["left"]["Idle"][i]) for i in range(8)],
                               "Run": [pygame.mask.from_surface(self.images["left"]["Run"][i]) for i in range(10)]
                               }}
        self.image = self.images['right']['Idle'][0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x + 200, y + 200)
        self.route = 'right'
        self.num_images = 0
        self.step = par_person['step']
        self.mode = "Idle"
        self.pr_mode = "Idle"
        self.hp = 9999999999999999999
        self.event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.event, 100)

    def update(self, motion_keydown, mouse_down, screen):
        font = pygame.font.Font(None, 36)
        self.text = font.render(str(self.hp), True, 'red')
        self.death()
        if self.mode != 'Death':
            self.motion(motion_keydown)
            self.attack(mouse_down)
            self.mask = self.masks[self.route][self.mode][self.num_images]
        if self.mode == 'Death' and self.num_images == 9:
            pygame.time.set_timer(self.event, 0)
        self.image = self.images[self.route][self.mode][self.num_images]

    def motion(self, keydown):
        if not keydown and self.mode not in ['Attack', 'Roll', 'BlockIdle', 'Hit']:
            self.mode = "Idle"
            self.num_images %= 8
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

    def death(self):
        if self.hp <= 0 and self.mode != 'Death':
            self.mode = 'Death'
            self.num_images = 0
            pygame.time.set_timer(self.event, 300)