import pygame
import random

class Bonus:
    def __init__(self, image, screen_width):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(
            x=random.randint(0, screen_width - self.image.get_width()),
            y=-self.image.get_height()
        )
        self.speed = [0, random.randint(4, 8)]

    def update(self):
        self.rect.move_ip(self.speed)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
