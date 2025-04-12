import pygame
from game_objects.player import Player
from game_objects.enemy import Enemy
from game_objects.bonus import Bonus
from game_objects.background import Background

class Game:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 20)
        self.bg = Background(settings["bg"], (settings["width"], settings["height"]), 3)
        self.player = Player(100, settings["height"]//2, settings["player_size"], settings["player_images"])
        self.enemies = []
        self.bonuses = []
        self.score = 0

        pygame.time.set_timer(pygame.USEREVENT + 1, 1500)
        pygame.time.set_timer(pygame.USEREVENT + 2, 2000)
        pygame.time.set_timer(pygame.USEREVENT + 3, 200)

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.USEREVENT + 1:
                    self.enemies.append(Enemy(self.settings["enemy_image"], self.settings["width"], self.settings["height"]))
                elif event.type == pygame.USEREVENT + 2:
                    self.bonuses.append(Bonus(self.settings["bonus_image"], self.settings["width"]))
                elif event.type == pygame.USEREVENT + 3:
                    self.player.animate()

            self.bg.update()
            self.bg.draw(self.screen)

            self.player.update(keys, self.settings["width"], self.settings["height"])
            self.player.draw(self.screen)

            for enemy in self.enemies[:]:
                enemy.update()
                enemy.draw(self.screen)
                if self.player.rect.colliderect(enemy.rect):
                    running = False
                elif enemy.rect.right < 0:
                    self.enemies.remove(enemy)

            for bonus in self.bonuses[:]:
                bonus.update()
                bonus.draw(self.screen)
                if self.player.rect.colliderect(bonus.rect):
                    self.bonuses.remove(bonus)
                    self.score += 1
                elif bonus.rect.top > self.settings["height"]:
                    self.bonuses.remove(bonus)

            self.screen.blit(self.font.render(f"Score: {self.score}", True, (0, 0, 0)), (10, 10))
            pygame.display.flip()
