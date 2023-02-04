from py.Person import *
from py.Camera import *
from py.Map import *
from py.Portal import portal_group
from py.Button import button_group, button_events
from maze import *


pygame.init()
pygame.mouse.set_visible(False)
size = w, h = 1900, 1000
screen = pygame.display.set_mode(size)
WASD = [pygame.K_w, pygame.K_d, pygame.K_a, 1073742049]
player = Person(100, 100, 250, 165)
map = Map(player)
cmr = Camera(w, h)
run = 1
motion_keydown = []
attack_keydown = []
mouse_down = 0
PLAYER_EVENT = pygame.USEREVENT + 1
PLAYER_ATTACK_EVENT = pygame.USEREVENT + 2
clock = pygame.time.Clock()
while run:
    mouse_down = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key in WASD:
                num_images = 1
                motion_keydown.append(event.key)
            elif event.key == pygame.K_e and portal_group.sprites()[0].button.draw_fl:
                Maze(screen)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = event.button
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            mouse_down = -3
        if event.type == pygame.KEYUP:
            if event.key in WASD and event.key in motion_keydown:
                motion_keydown.remove(event.key)
        if event.type in [PLAYER_EVENT, PLAYER_ATTACK_EVENT]:
            player.num_images += 1
        if event.type in enemys_events:
            for enemy in enemys:
                if event.type in enemy[0].events:
                    enemy[0].num_images += 1
        if event.type == portal_group.sprites()[0].event:
            portal_group.sprites()[0].update()
        if event.type in button_events and portal_group.sprites()[0].button.draw_fl:
            portal_group.sprites()[0].button.update()


    player.update(motion_keydown, mouse_down, screen)
    enemys_group.update(player)
    screen.fill('black')
    all_sprites.draw(screen)
    if (v_let_sprites.sprites()[0].rect.x < -48 or player.route == 'right' and player.rect.x >= 828) and \
            (v_let_sprites.sprites()[1].rect.x > 1920 + 48 or player.route == 'left' and player.rect.x <= 828):
        cmr.update(player)
        cmr.apply(player)
        cmr.apply(map)
        cmr.apply(portal_group.sprites()[0])
        cmr.apply(portal_group.sprites()[0].button)
        for i in v_let_sprites.sprites():
            cmr.apply(i)
        for i in h_let_sprites.sprites():
            cmr.apply(i)
        for i in enemys_group.sprites():
            cmr.apply(i)
    if portal_group.sprites()[0].button.draw_fl:
        button_group.draw(screen)
        print(1)
    portal_group.draw(screen)
    player_group.draw(screen)
    screen.blit(player.text, (100, 100))
    enemys_group.draw(screen)
    pygame.display.flip()
pygame.quit()