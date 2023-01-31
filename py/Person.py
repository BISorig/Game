import pygame.sprite
from py.load_image import *
from py.Tile import all_sprites, let_sprites, h_let_sprites
player_group = pygame.sprite.Group()


class Person(pygame.sprite.Sprite):
    def __init__(self, x, y, step=0):
        super().__init__(player_group, all_sprites)
        size_person = (x, y)
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
                                            for i in range(8)]},


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
                                          for i in range(8)]
                                },
                       }
        self.masks = {"right": {"Idle": [pygame.mask.from_surface(self.images["right"]["Idle"][i]) for i in range(8)],
                                "Run": [pygame.mask.from_surface(self.images["right"]["Run"][i]) for i in range(10)],
                                "Jump": [pygame.mask.from_surface(self.images["right"]["Jump"][i]) for i in range(3)],
                                "Attack": [pygame.mask.from_surface(self.images["right"]["Attack"][i]) for i in range(20)],
                                "BlockIdle": [pygame.mask.from_surface(self.images["right"]["BlockIdle"][i]) for i in range(8)],
                                "Roll": [pygame.mask.from_surface(self.images["left"]["Roll"][i]) for i in range(9)]},

                      "left": {"Idle": [pygame.mask.from_surface(self.images["left"]["Idle"][i]) for i in range(8)],
                               "Run": [pygame.mask.from_surface(self.images["left"]["Run"][i]) for i in range(10)],
                               "Jump": [pygame.mask.from_surface(self.images["left"]["Jump"][i]) for i in range(3)],
                               "Roll": [pygame.mask.from_surface(self.images["left"]["Roll"][i]) for i in range(9)],
                               "BlockIdle": [pygame.mask.from_surface(self.images["left"]["BlockIdle"][i]) for i in range(8)],
                               "Attack": [pygame.mask.from_surface(self.images["left"]["Attack"][i]) for i in range(20)]}}
        self.image = self.images['right']['Idle'][0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(300, 300)
        self.route = 'right'
        self.num_images = 0
        self.step = 3
        self.mode = "Idle"
        self.jump_m = -1
        self.jump = 500
        self.jump_h = 5
        self.pr_mode = "Idle"
        self.attack_queue = 0
        self.hp = 100
        self.event_attack = pygame.USEREVENT + 2
        self.event_calmness = pygame.USEREVENT + 1
        pygame.time.set_timer(self.event_calmness, 100)
        self.fl_block = 0
        self.num_attack = 0

    def update(self, motion_keydown, mouse_down, screen):
        font = pygame.font.Font(None, 36)
        self.text = font.render(str(self.hp), True, 'red')

        self.motion(motion_keydown)
        self.attack(mouse_down)
        #print(self.mode, self.num_images)
        self.image = self.images[self.route][self.mode][self.num_images]
        self.mask = self.masks[self.route][self.mode][self.num_images]

    def motion(self, keydown):
        if self.mode == 'Roll':
            if self.num_images == 9:
                pygame.time.set_timer(self.event_attack, 0)
                pygame.time.set_timer(self.event_calmness, 150)
                self.num_images = 0
                self.mode = 'Idle'
            elif self.route == 'right':
                self.rect.x += self.step
            else:
                self.rect.x -= self.step
        if not keydown and self.mode not in ['Attack', 'Roll', 'BlockIdle']:
            self.mode = "Idle"
            self.num_images %= 8
        if pygame.K_w not in keydown:
            self.jump_m = -1
        for key in keydown[:2]:
            if key == pygame.K_w:
                if self.mode not in ['Jump', 'Attack', 'Roll', 'BlockIdle']:
                    self.mode = "Jump"
                    self.jump_m = 0
                if self.jump_m < self.jump and self.jump_m != -1:
                    self.jump_m += self.jump_h
                    self.rect.y -= self.jump_h
                    if self.mode not in ["Attack", 'Roll', 'BlockIdle']:
                        self.num_images = 1
                elif self.jump_m == self.jump:
                    self.jump_m = -1
                    if pygame.K_w in keydown:
                        keydown.remove(pygame.K_w)

            if key in [pygame.K_a, pygame.K_d]:
                if self.mode not in ['Run', 'Jump', 'Attack', 'Roll', 'BlockIdle']:
                    self.mode = 'Run'
                    self.num_images = 0
                else:
                    self.pr_mode = 'Run'
                if key == pygame.K_a:
                    k = -1
                    self.route = 'left'
                else:
                    k = 1
                    self.route = 'right'
                if self.mode not in ['Attack', 'Roll', 'BlockIdle']:
                    self.rect.x += self.step * k
                    self.num_images %= 10
                if pygame.sprite.spritecollideany(self, let_sprites):
                    self.rect.x -= self.step * k
            if key == 1073742049 and self.mode not in ['Attack', 'Roll', 'BlockIdle']:
                keydown.remove(1073742049)
                self.mode = 'Roll'
                self.num_images = 0
                pygame.time.set_timer(self.event_calmness, 0)
                pygame.time.set_timer(self.event_attack, 75)

        if not pygame.sprite.spritecollideany(self, h_let_sprites) and self.jump_m == -1:
            if self.mode != 'Attack':
                self.mode = "Jump"
                self.num_images = 2
            self.rect.y += self.jump_h
        elif pygame.sprite.spritecollideany(self, h_let_sprites) and self.mode == 'Jump':
            self.mode = self.pr_mode

    def attack(self, mouse_down):
        if mouse_down == 1:
            self.attack_queue += 1
            if self.mode != 'Attack':
                pygame.time.set_timer(self.event_calmness, 0)
                pygame.time.set_timer(self.event_attack, 75)
                self.mode = 'Attack'
                self.num_images = 0
                self.num_attack = 1
        elif (mouse_down == 3 or self.fl_block) and self.mode not in ['Attack', 'Jump', 'Roll']:
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
                print(self.attack_queue)
            if self.num_images in [2, 3, 8, 9, 16, 17]:
                if self.route == 'right':
                    self.rect.x += self.step
                else:
                    self.rect.x -= self.step
            if not self.attack_queue:
                self.mode = 'Idle'
                pygame.time.set_timer(self.event_attack, 0)
                pygame.time.set_timer(self.event_calmness, 150)
                self.num_images = 0



    def block(self):
        self.num_images %= 5
        self.fl_block = 1
        self.mode = 'BlockIdle'



