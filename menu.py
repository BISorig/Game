import sqlite3

import pygame
import os
import sys
from py.Person import *


pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption("MENU")
bg = pygame.image.load('textures/fonmenuosn.png')
bg = pygame.transform.scale(bg, (1920, 1080))
screen.blit(bg, (0, 0))


def terminate():
    pygame.quit()
    sys.exit()


def applyexit():
    font = pygame.font.Font(None, 50)
    line = 'Вы действительно хотите выйти из игры?'
    line_rendered = font.render(line, 1, pygame.Color('blue'))
    line_rect = line_rendered.get_rect()
    line_rect.top = 300
    line_rect.x = 50
    bg = pygame.image.load('textures/fonmenu.png')
    bg = pygame.transform.scale(bg, (800, 300))
    screen.blit(bg, (0, 250))
    screen.blit(line_rendered, line_rect)
    surf = pygame.font.SysFont('Corbel', 100)
    button_yes = surf.render('yes', True, pygame.Color('red'))
    button_no = surf.render('no', True, pygame.Color('red'))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.blit(button_yes, (150, 375))
        screen.blit(button_no, (500, 375))
        pygame.display.flip()


def createtext(text, color, x, y):
    surf = pygame.font.SysFont('Corbel', 75)
    text_button = surf.render(text, True, pygame.Color(color))
    screen.blit(text_button, (x, y))


x1, y1 = 0, 100
while x1 != width:
    pygame.draw.line(screen, pygame.Color('blue'), (x1, y1), (x1 + 100, y1 + 50), 5)
    pygame.draw.line(screen, pygame.Color('blue'), (x1 + 100, y1 + 50), (x1 + 200, y1), 5)
    x1 += 200
running = True
createtext('play', 'red', 100, 300) # создаём кнопку для начала игры
# if _():  здесь нужно проверить на продолжение игры
# pass
createtext('continue', 'dark red', 500, 300) # создаём кнопку для продолжения игры
createtext('sound', 'red', 100, 450) # громкость / включить / выключить
createtext('music', 'red', 500, 450) # выбрать музыку
createtext('exit', 'red', 350, 600)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_m = pygame.mouse.get_pos()
            print(pos_m)
            if 100 < pos_m[0] < 220 and 300 < pos_m[1] < 375:
                pass  # запускать основной класс (начало игры)
            if 350 < pos_m[0] < 650 and 610 < pos_m[1] < 660:
                print('exit')
                if applyexit():
                    print('true')
                    terminate()
                print('false')
            if 500 < pos_m[0] < 750 and 310 < pos_m[1] < 360:
                pass  # продолжить сохранённую игру
            if 100 < pos_m[0] < 270 and 450 < pos_m[1] < 505:
                pass  # громкость / включить / выключить
            if 505 < pos_m[0] < 670 and 460 < pos_m[1] < 500:
                pass  # выбрать мелодию
    pygame.display.flip()