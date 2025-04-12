import pygame
import random
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

HEIGHT = 800
WIDTH = 1200
PLAYER_SIZE = (182, 76)
FPS = 60
FONT = pygame.font.SysFont('Verdana', 20)

COLOR_BLACK = (0, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(x=100, y=HEIGHT // 2 - PLAYER_SIZE[1] // 2)
        self.speed = [0, 0]

    def update(self, keys):
        if keys[K_DOWN] and self.rect.bottom < HEIGHT:
            self.speed[1] = 4
        elif keys[K_UP] and self.rect.top > 0:
            self.speed[1] = -4
        else:
            self.speed[1] = 0

        if keys[K_RIGHT] and self.rect.right < WIDTH:
            self.speed[0] = 4
        elif keys[K_LEFT] and self.rect.left > 0:
            self.speed[0] = -4
        else:
            self.speed[0] = 0

        self.rect.move_ip(*self.speed)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(
            x=WIDTH,
            y=random.randint(36, HEIGHT - 36)
        )
        self.speed = [random.randint(-8, -4), 0]

    def update(self):
        self.rect.move_ip(*self.speed)
        if self.rect.right < -100:
            self.kill()


class Bonus(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(
            x=random.randint(89, WIDTH // 2),
            y=-298
        )
        self.speed = [0, random.randint(4, 8)]

    def update(self):
        self.rect.move_ip(*self.speed)
        if self.rect.top > HEIGHT + 300:
            self.kill()


class Game:
    def __init__(self):
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("OOP Game")

        self.bg = pygame.transform.scale(pygame.image.load('img/background.png').convert(), (WIDTH, HEIGHT))
        self.player_image = pygame.image.load('img/player.png').convert_alpha()
        self.enemy_image = pygame.image.load('img/enemy.png').convert_alpha()
        self.bonus_image = pygame.image.load('img/bonus.png').convert_alpha()

        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0

        self.bg = self.bg
        self.bg_x1 = 0
        self.bg_x2 = self.bg.get_width()
        self.bg_speed = 3

        self.player = Player(self.player_image)

        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bonuses = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        pygame.time.set_timer(pygame.USEREVENT + 1, 1500)
        pygame.time.set_timer(pygame.USEREVENT + 2, 2000)

    def spawn_enemy(self):
        enemy = Enemy(self.enemy_image)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def spawn_bonus(self):
        bonus = Bonus(self.bonus_image)
        self.bonuses.add(bonus)
        self.all_sprites.add(bonus)

    def scroll_background(self):
        self.bg_x1 -= self.bg_speed
        self.bg_x2 -= self.bg_speed
        if self.bg_x1 <= -self.bg.get_width():
            self.bg_x1 = self.bg.get_width()
        if self.bg_x2 <= -self.bg.get_width():
            self.bg_x2 = self.bg.get_width()
        self.display.blit(self.bg, (self.bg_x1, 0))
        self.display.blit(self.bg, (self.bg_x2, 0))

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == pygame.USEREVENT + 1:
                self.spawn_enemy()
            elif event.type == pygame.USEREVENT + 2:
                self.spawn_bonus()

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        self.enemies.update()
        self.bonuses.update()

        collected = pygame.sprite.spritecollide(self.player, self.bonuses, True)
        if collected:
            self.score += len(collected)
            print("Bonus collected!")

        if pygame.sprite.spritecollideany(self.player, self.enemies):
            print("Game Over!")
            self.running = False

    def draw(self):
        self.scroll_background()
        self.all_sprites.draw(self.display)
        score_text = FONT.render(f"Score: {self.score}", True, COLOR_BLACK)
        self.display.blit(score_text, (10, 10))
        pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run()
