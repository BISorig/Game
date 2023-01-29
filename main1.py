import pygame
from Person import *
from Enemy import *
from Camera import *
import csv
from Map import *

pygame.init()
pygame.mouse.set_visible(False)
size = w, h = 1900, 1000
screen = pygame.display.set_mode(size)
WASD = [pygame.K_w, pygame.K_d, pygame.K_a, 1073742049]
step = 50
player = Person(250, 165, step=step)
enemys = []
for i in range(2):
    enemys.append((Enemy(160, 180, 10), pygame.NUMEVENTS - 1 - len(enemys) * 2, pygame.NUMEVENTS - 2 - len(enemys) * 2))
print(enemys)
map = Map()
cmr = Camera(w, h)
run = True
keydown = []
mouse_down = 0
PLAYER_EVENT = pygame.USEREVENT + 1
PLAYER_ATTACK_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(PLAYER_ATTACK_EVENT, 150)
clock = pygame.time.Clock()
while run:
    mouse_down = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key in WASD:
                num_images = 1
                keydown.append(event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = event.button
        if event.type == pygame.MOUSEBUTTONUP:
            player.fl_block = 0
            player.mode = 'Idle'
        if event.type == pygame.KEYUP:
            if event.key in WASD and event.key in keydown:
                keydown.remove(event.key)
        if event.type in [PLAYER_EVENT, PLAYER_ATTACK_EVENT]:
            #print(-2)
            player.num_images += 1
        if event.type in enemys_events:
            #print(event.type)
            for enemy in enemys:
                if event.type in enemy:
                    enemy[0].num_images += 1

    player.update(keydown, mouse_down, screen)
    enemys_group.update(player)
    screen.fill('black')
    all_sprites.draw(screen)
    # cmr.update(player)
    # cmr.apply(player)
    # for i in map_sprite.sprites():
    #     cmr.apply(i)
    #     print(i.rect.x, i.rect.y)
    player_group.draw(screen)
    screen.blit(player.text, (100, 100))
    enemys_group.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()