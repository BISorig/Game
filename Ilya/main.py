import pygame
import sys, os
from py.Map import Map
from py.Person import *
from py.Camera import *
from py.Tile import *

pygame.init()
size = w, h = 1900, 1000
screen = pygame.display.set_mode(size)
WASD = [pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a]
player = Person(50, 60)
camera = Camera(w, h)
step = 10
map = Map(467, 0)
run = True
keydown = []
num_images = 0
NUM_EVENT = pygame.USEREVENT + 1
route = 'down'
clock = pygame.time.Clock()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key in WASD:
                num_images = 1
                pygame.time.set_timer(NUM_EVENT, 100)
                keydown.append(event.key)
        if event.type == pygame.KEYUP:
            if event.key in WASD:
                keydown.remove(event.key)
                if not keydown:
                    player.image = player.images[route][0]
                    pygame.time.set_timer(NUM_EVENT, 0)
        if event.type == NUM_EVENT:
            num_images += 1
            num_images %= 10
            if num_images == 0:
                num_images = 1
    for key in keydown[:2]:
        player.image = player.images[route][num_images]
        if key == pygame.K_w:
            route = 'up'
            player.rect.y -= step
        if key == pygame.K_s:
            route = 'down'
            player.rect.y += step
        if key == pygame.K_a:
            route = 'left'
            player.rect.x -= step
        if key == pygame.K_d:
            route = 'right'
            player.rect.x += step
    print(map.rect.x, map.rect.y)
    screen.fill('black')
    camera.update(player)
    for i in all_sprites:
        camera.apply(i)
    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()