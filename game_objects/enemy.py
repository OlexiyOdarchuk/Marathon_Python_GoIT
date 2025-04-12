import pygame
import random

class Enemy:
    def __init__(self, image, screen_width, screen_height):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(
            x=screen_width,
            y=random.randint(0, screen_height - self.image.get_height())
        )
        self.speed = [random.randint(-8, -4), 0]

    def update(self):
        self.rect.move_ip(self.speed)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
