import pygame
import sys
from py.load_image import load_image


def Menu(screen, con, cur):
    music_on_off = False
    sound_on_off = False
    pygame.mouse.set_visible(True)
    level = cur.execute("SELECT level FROM Person").fetchall()[0][0]

    def terminate():
        pygame.quit()
        sys.exit()

    def autors():
        font = pygame.font.Font(None, 25)
        line = 'by Nikita Babashev and Ilya Bikmaev'
        line_rendered = font.render(line, 1, pygame.Color('grey'))
        line_rect = line_rendered.get_rect()
        line_rect.top = 1050
        line_rect.x = 10
        screen.blit(line_rendered, line_rect)

    def checkmusicsound(text, stage):
        font = pygame.font.Font(None, 50)
        line = text
        line_rendered = font.render(line, 1, pygame.Color('blue'))
        line_rect = line_rendered.get_rect()
        line_rect.top = 300
        text_button_on_off = 'on/off'
        if stage == 'sound':
            line_rect.x = 725
        if stage == 'music':
            line_rect.x = 875
        bg = pygame.image.load('data/textures/fonmenu.jpg')
        bg = pygame.transform.scale(bg, (800, 300))
        screen.blit(bg, (560, 240))
        screen.blit(line_rendered, line_rect)
        surf = pygame.font.SysFont('Corbel', 100)
        button_on_off = surf.render(text_button_on_off, True, pygame.Color('red'))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos_m = pygame.mouse.get_pos()
                    if 830 < pos_m[0] < 1070 and 380 < pos_m[1] < 450:
                        return True
            pos_m = pygame.mouse.get_pos()

            if 830 < pos_m[0] < 1070 and 380 < pos_m[1] < 450:
                button_on_off = surf.render(text_button_on_off, True, pygame.Color('light green'))
            else:
                button_on_off = surf.render(text_button_on_off, True, pygame.Color('red'))
            screen.blit(button_on_off, (825, 375))
            pygame.display.flip()

    def yesorno(text, stage):
        font = pygame.font.Font(None, 50)
        line = text
        line_rendered = font.render(line, 1, pygame.Color('blue'))
        line_rect = line_rendered.get_rect()
        line_rect.top = 300
        text_button_yes = ''
        text_button_no = ''
        if stage == 'exit':
            text_button_yes = 'yes'
            text_button_no = 'no'
            line_rect.x = 600
        bg = pygame.image.load('data/textures/fonmenu.jpg')
        bg = pygame.transform.scale(bg, (800, 300))
        screen.blit(bg, (560, 240))
        screen.blit(line_rendered, line_rect)
        surf = pygame.font.SysFont('Corbel', 100)
        button_yes = surf.render(text_button_yes, True, pygame.Color('red'))
        button_no = surf.render(text_button_no, True, pygame.Color('red'))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if 700 < mouse[0] < 825 and 400 < mouse[1] < 450:
                        return True
                    if 1105 < mouse[0] < 1200 and 400 < mouse[1] < 450:
                        return False
            pos_m = pygame.mouse.get_pos()
            if 400 < pos_m[0] < 825 and 400 < pos_m[1] < 450:
                button_yes = surf.render(text_button_yes, True, pygame.Color('light green'))
            elif 1105 < pos_m[0] < 1200 and 400 < pos_m[1] < 450:
                button_no = surf.render(text_button_no, True, pygame.Color('light green'))
            else:
                button_no = surf.render(text_button_no, True, pygame.Color('red'))
                button_yes = surf.render(text_button_yes, True, pygame.Color('red'))
            screen.blit(button_yes, (700, 375))
            screen.blit(button_no, (1100, 375))
            pygame.display.flip()

    def createtext(text, color, x, y):
        surf = pygame.font.SysFont('Corbel', 75)
        text_button = surf.render(text, True, pygame.Color(color))
        screen.blit(text_button, (x, y))

    pygame.display.set_caption("MENU")
    bg = pygame.image.load('data/textures/fonmenuosn.png')
    bg = pygame.transform.scale(bg, (1920, 1080))
    screen.blit(bg, (0, 0))
    bg = pygame.image.load('data/GameMap/buildings/House11.png')
    bg = pygame.transform.scale(bg, (bg.get_width() * 0.3, bg.get_height() * 0.3))
    screen.blit(bg, (1420, 540))
    bg = pygame.image.load('data/textures/namegame.png')
    screen.blit(bg, (-30, 0))
    bg = pygame.image.load('data/GameMap/goose/Goose.png')
    kr = load_image('data/GameMap/goose/krest.png', 'white')
    kr = pygame.transform.scale(kr, (100, 100))
    bg = pygame.transform.scale(bg, (100, 100))
    screen.blit(bg, (1400, 30))
    screen.blit(kr, (1400, 30))
    bg = pygame.image.load('data/textures/goose.png')
    bg = pygame.transform.scale(bg, (100, 50))
    screen.blit(bg, (300, 300))
    x1, y1 = 0, 150
    while x1 < 2000:
        pygame.draw.line(screen, pygame.Color('blue'), (x1, y1), (x1 + 100, y1 + 50), 5)
        pygame.draw.line(screen, pygame.Color('blue'), (x1 + 100, y1 + 50), (x1 + 200, y1), 5)
        x1 += 200
    autors()
    check_fill = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_m = pygame.mouse.get_pos()
                if 605 < pos_m[0] < 910 and 670 < pos_m[1] < 705:
                    cur.execute("""UPDATE Person SET level = 1""")
                    con.commit()
                    cur.execute(f"""UPDATE Person SET step = {5}""")
                    con.commit()
                    cur.execute(f"""UPDATE Person SET max_hp = {100}""")
                    con.commit()
                    cur.execute(f"""UPDATE Person SET damage = {5}""")
                    con.commit()
                    return True
                if 900 < pos_m[0] < 1000 and 920 < pos_m[1] < 955:
                    if yesorno('???? ?????????????????????????? ???????????? ?????????? ???? ?????????', 'exit'):
                        terminate()
                    else:
                        screen.fill((0, 0, 0))
                        check_fill = True
                if 1055 < pos_m[0] < 1305 and 670 < pos_m[1] < 705:
                    if level:
                        return True # ???????????????????? ?????????????????????? ???????? ?? ?????????????????? ???????? ???? ??????
                if 605 < pos_m[0] < 775 and 820 < pos_m[1] < 855:
                    if checkmusicsound('?????????? ???????????????? ??????????????????', 'sound'):
                        if sound_on_off:
                            sound_on_off = False
                        else:
                            sound_on_off = True
                        screen.fill((0, 0, 0))
                        check_fill = True
                if 1050 < pos_m[0] < 1220 and 820 < pos_m[1] < 855:
                    if checkmusicsound('????????????', 'music'):
                        if music_on_off:
                            music_on_off = False
                        else:
                            music_on_off = True
                        screen.fill((0, 0, 0))
                        check_fill = True
        pos_m = pygame.mouse.get_pos()
        if check_fill:
            pygame.display.set_caption("MENU")
            bg = pygame.image.load('data/textures/fonmenuosn.png')
            bg = pygame.transform.scale(bg, (1920, 1080))
            screen.blit(bg, (0, 0))
            bg = pygame.image.load('data/GameMap/buildings/House11.png')
            bg = pygame.transform.scale(bg, (bg.get_width() * 0.3, bg.get_height() * 0.3))
            screen.blit(bg, (1420, 540))
            bg = pygame.image.load('data/textures/namegame.png')
            screen.blit(bg, (-30, 0))
            bg = pygame.image.load('data/GameMap/goose/Goose.png')
            kr = load_image('data/GameMap/goose/krest.png', 'white')
            kr = pygame.transform.scale(kr, (100, 100))
            bg = pygame.transform.scale(bg, (100, 100))
            screen.blit(bg, (1400, 30))
            screen.blit(kr, (1400, 30))
            bg = pygame.image.load('data/textures/goose.png')
            bg = pygame.transform.scale(bg, (100, 50))
            screen.blit(bg, (300, 300))
            x1, y1 = 0, 150
            while x1 < 2000:
                pygame.draw.line(screen, pygame.Color('blue'), (x1, y1), (x1 + 100, y1 + 50), 5)
                pygame.draw.line(screen, pygame.Color('blue'), (x1 + 100, y1 + 50), (x1 + 200, y1),
                                 5)
                x1 += 200
            autors()
            check_fill = False
        if 605 < pos_m[0] < 910 and 670 < pos_m[1] < 705:
            createtext('new game', 'blue', 600, 650)  # ?????????????? ???????????? ?????? ???????????? ????????
        else:
            createtext('new game', 'red', 600, 650)
        if 1055 < pos_m[0] < 1305 and 670 < pos_m[1] < 705:

            if not level:
                createtext('continue', 'light blue', 1050, 650)  # ?????????????? ???????????? ??????
            # ?????????????????????? ????????
            else:
                createtext('continue', 'blue', 1050, 650)
        else:
            if not level:
                createtext('continue', 'dark red', 1050, 650)
            # ?????????? ??????????????????, ???????? ???? ???????????????????? (???????? ?????? ????????)
            else:
                createtext('continue', 'red', 1050, 650)
        if 605 < pos_m[0] < 775 and 820 < pos_m[1] < 855:
            createtext('sound', 'blue', 600, 800)  # ?????????????? ???????????? ???????????? ?????????? ?? ??.??.
            # ?????? ????????
        else:
            createtext('sound', 'red', 600, 800)
        if 1050 < pos_m[0] < 1220 and 820 < pos_m[1] < 855:
            createtext('music', 'blue', 1050, 800)  # ?????????????? ???????????? ???????????? ??????, ????????
        else:
            createtext('music', 'red', 1050, 800)
        if 900 < pos_m[0] < 1000 and 920 < pos_m[1] < 955:
            createtext('exit', 'blue', 900, 900)  # ?????????????? ???????????? ????????????
        else:
            createtext('exit', 'red', 900, 900)
        pygame.display.flip()
