import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random
import os

pygame.init()

HEIGHT = 800
WIDTH = 1200
FONT = pygame.font.SysFont("Verdana", 20)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)
PLAYER_SIZE = (182, 76)
FPS = pygame.time.Clock()
IMAGE_PATH = "img/Player"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(
    pygame.image.load("img/background.png").convert(), (WIDTH, HEIGHT)
)

bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

player = pygame.image.load("img/player.png").convert_alpha()
player_rect = player.get_rect(x=100, y=HEIGHT // 2 - PLAYER_SIZE[1] // 2)
player_speed = [1, 1]


def create_enemy():
    enemy_size = (205, 72)
    enemy = pygame.image.load("img/enemy.png").convert_alpha()
    enemy_rect = pygame.Rect(
        WIDTH,
        random.randint(enemy_size[1] // 2, HEIGHT - enemy_size[1] // 2),
        *enemy_size,
    )
    
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]


def create_bonus():
    bonus_size = (179, 298)
    bonus = pygame.image.load("img/bonus.png").convert_alpha()
    bonus_rect = pygame.Rect(
        random.randint(bonus_size[0] // 2, WIDTH // 2), -bonus_size[1], *bonus_size
    )
    
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2000)

CHANGE_PLAYER = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_PLAYER, 200)

enemies = []
bonuses = []
score = 0
image_index = 0

playing = True
while playing:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_PLAYER:
            player = pygame.image.load(
                os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index])
            )
            
            image_index = (image_index + 1) % len(PLAYER_IMAGES)

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 <= -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 <= -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_speed[1] = 4
    elif keys[K_UP] and player_rect.top > 0:
        player_speed[1] = -4
    else:
        player_speed[1] = 0

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_speed[0] = 4
    elif keys[K_LEFT] and player_rect.left > 0:
        player_speed[0] = -4
    else:
        player_speed[0] = 0

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            print("Game Over")
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            bonuses.remove(bonus)
            score += 1
            print("Bonus Collected")

    main_display.blit(FONT.render(f"Score: {score}", True, COLOR_BLACK), (10, 10))
    main_display.blit(player, player_rect)
    player_rect = player_rect.move(player_speed)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < -200:
            enemies.remove(enemy)

    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT + 290:
            bonuses.remove(bonus)
