import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
import random

pygame.init()

# Constants
HEIGHT = 800
WIDTH = 1200
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)
FPS = 120

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(COLOR_WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 1
        self.rect.y = 1
        self.speed = [0, 0]

    def update(self, keys):
        if keys[K_DOWN] and self.rect.bottom < HEIGHT:
            self.speed[1] = 1
        elif keys[K_UP] and self.rect.top > 0:
            self.speed[1] = -1
        else:
            self.speed[1] = 0

        if keys[K_RIGHT] and self.rect.right < WIDTH:
            self.speed[0] = 1
        elif keys[K_LEFT] and self.rect.left > 0:
            self.speed[0] = -1
        else:
            self.speed[0] = 0

        self.rect = self.rect.move(self.speed)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(COLOR_BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(0, HEIGHT)
        self.speed = [random.randint(-6, -1), 0]

    def update(self):
        self.rect = self.rect.move(self.speed)

class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(COLOR_RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = 0
        self.speed = [0, 2]

    def update(self):
        self.rect = self.rect.move(self.speed)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
        self.enemies = pygame.sprite.Group()
        self.bonuses = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

        pygame.time.set_timer(pygame.USEREVENT + 1, 1500)
        pygame.time.set_timer(pygame.USEREVENT + 2, 2000)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.render()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == pygame.USEREVENT + 1:
                self.create_enemy()
            elif event.type == pygame.USEREVENT + 2:
                self.create_bonus()

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)

        self.enemies.update()
        self.bonuses.update()

        self.check_collisions()
        self.remove_offscreen_objects()

    def render(self):
        self.screen.fill(COLOR_BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def create_enemy(self):
        enemy = Enemy()
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def create_bonus(self):
        bonus = Bonus()
        self.bonuses.add(bonus)
        self.all_sprites.add(bonus)

    def check_collisions(self):
        if pygame.sprite.spritecollide(self.player, self.bonuses, True):
            # Тут буде прописана логіка для взаємодії з бонусами
            pass
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            # Тут буде прописана логіка для взаємодії з ворогами
            pass

    def remove_offscreen_objects(self):
        for enemy in self.enemies:
            if enemy.rect.left < 0:
                enemy.kill()

        for bonus in self.bonuses:
            if bonus.rect.bottom > HEIGHT:
                bonus.kill()

if __name__ == "__main__":
    game = Game()
    game.run()
