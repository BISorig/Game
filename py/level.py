from py.Person import *
from py.Camera import *
from py.Map import *
from py.Portal import portal_group
from py.Button import button_group
from py.maze import *

WASD = [pygame.K_d, pygame.K_a, 1073742049]
size = w, h = 1920, 1080


class Level:

    def __init__(self, player, mp, level, maze):
        pygame.mouse.set_visible(False)
        self.maze = maze
        self.pause_rect = pygame.Surface((1920, 1080))
        self.pause_rect.fill('black')
        self.pause_rect.set_alpha(100)
        self.map = mp
        self.level = level
        self.cmr = Camera(w)
        self.run = 1
        self.motion_keydown = []
        self.attack_keydown = []
        self.mouse_down = 0
        self.PLAYER_EVENT = pygame.USEREVENT + 1
        self.PLAYER_ATTACK_EVENT = pygame.USEREVENT + 2
        self.button_event = pygame.USEREVENT + 200
        pygame.time.set_timer(self.button_event, 500)
        self.cycl(player)
        pygame.time.set_timer(self.button_event, 0)
        player.num_enem = 0

    def cycl(self, player):
        while self.run:
            mouse_down = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    if event.key in WASD:
                        num_images = 1
                        self.motion_keydown.append(event.key)
                    elif event.key == 27:
                        screen.blit(self.pause_rect, (0, 0))
                        if self.pause():
                            self.run = 0
                    elif event.key == pygame.K_e:
                        if portal_group.sprites()[0].button.draw_fl and \
                                not portal_group.sprites()[0].button.done:
                            if Maze(screen, self.maze, player):
                                portal_group.sprites()[0].button.done = 1
                                player.max_hp = int(player.max_hp)
                        elif player.rect.x > 1630 and player.num_enem == 0:
                            if self.level < 3:
                                cur.execute(f"""UPDATE Person SET level = {self.level + 1}""")
                                con.commit()
                            cur.execute(f"""UPDATE Person SET step = {int(player.step)}""")
                            cur.execute(f"""UPDATE Person SET max_hp = {int(player.max_hp)}""")
                            cur.execute(f"""UPDATE Person SET damage = {int(player.damage)}""")
                            con.commit()
                            player.num_images = 0
                            return 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down = event.button
                if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                    mouse_down = -3
                if event.type == pygame.KEYUP:
                    if event.key in WASD and event.key in self.motion_keydown:
                        self.motion_keydown.remove(event.key)
                if event.type in [self.PLAYER_EVENT, self.PLAYER_ATTACK_EVENT]:
                    player.num_images += 1
                if event.type in enemys_events:
                    for enemy in enemys:
                        if event.type in enemy[0].events:
                            enemy[0].num_images += 1
                if event.type == portal_group.sprites()[0].event:
                    portal_group.sprites()[0].update()
                if event.type == self.button_event and \
                        (portal_group.sprites()[0].button.draw_fl and
                         not portal_group.sprites()[0].button.done or
                         (player.rect.x > 1630 and player.num_enem == 0)):
                    button_group.update()

            player.update(self.motion_keydown, mouse_down, screen)
            enemys_group.update(player)
            screen.fill('black')
            all_sprites.draw(screen)
            if (v_let_sprites.sprites()[0].rect.x < -48 or player.route == 'right' and
                player.rect.x >= 828) and \
                    (v_let_sprites.sprites()[1].rect.x > 1920 + 48 or player.route == 'left' and
                     player.rect.x <= 828):
                self.cmr.update(player)
                self.cmr.apply(player)
                self.cmr.apply(self.map)
                self.cmr.apply(portal_group.sprites()[0])
                self.cmr.apply(portal_group.sprites()[0].button)
                self.cmr.apply(button_group.sprites()[1])
                for i in v_let_sprites.sprites():
                    self.cmr.apply(i)
                for i in h_let_sprites.sprites():
                    self.cmr.apply(i)
                for i in enemys_group.sprites():
                    self.cmr.apply(i)
            if portal_group.sprites()[0].button.draw_fl or (player.rect.x > 1630 and
                                                            player.num_enem == 0):
                button_group.draw(screen)
            portal_group.draw(screen)
            player_group.draw(screen)
            screen.blit(player.text, (100, 100))

            enemys_group.draw(screen)
            pygame.display.flip()

    def pause(self):
        font = pygame.font.Font(None, 100)
        text = font.render('Хотите выйти в меню? (y/n)', True, 'red')
        screen.blit(text, (525, 540))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == 27 or event.key == pygame.K_n:
                        return 0
                    elif event.key == pygame.K_y:
                        return 1
            pygame.display.flip()

