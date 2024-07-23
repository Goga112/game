import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('TETRIS')
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

bg = pygame.image.load('images/icon2.png').convert_alpha()
walk_left = [
    pygame.image.load('images/left/icon4.png').convert_alpha(),
    pygame.image.load('images/left/icon5.png').convert_alpha(),
    pygame.image.load('images/left/icon6.png').convert_alpha(),
    pygame.image.load('images/left/icon7.png').convert_alpha(),
]
walk_right = [
    pygame.image.load('images/right/icon8.png').convert_alpha(),git remote -v
    pygame.image.load('images/right/icon9.png').convert_alpha(),
    pygame.image.load('images/right/icon10.png').convert_alpha(),
    pygame.image.load('images/right/icon11.png').convert_alpha(),
]

ghost = pygame.image.load('images/ghost.png').convert_alpha()
ghost_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speed = 15
player_x = 150
player_y = 430

is_jump = False

jump_count = 8

bg_sound = pygame.mixer.Sound('sounds/bg.mp3')
bg_sound.play()

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 4500)

label = pygame.font.Font('fonts/Robot.ttf', 90)
lose_label = label.render('YOU LOSE!', False, (193, 196, 199))
restart_label = label.render('restart?', False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft = (500, 430))

gameplay = True

running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 1280, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10

                if el.x < -10:
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False


        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_speed > 10:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 1200:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_count  == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 5
        if bg_x == -1280:
            bg_x = 0
    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (470, 310))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(1282, 500)))

    clock.tick(10)