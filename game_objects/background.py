import pygame

class Background:
    def __init__(self, image_path, screen_size, speed):
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert(), screen_size)
        self.x1 = 0
        self.x2 = self.image.get_width()
        self.speed = speed

    def update(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

        if self.x1 <= -self.image.get_width():
            self.x1 = self.image.get_width()

        if self.x2 <= -self.image.get_width():
            self.x2 = self.image.get_width()

    def draw(self, surface):
        surface.blit(self.image, (self.x1, 0))
        surface.blit(self.image, (self.x2, 0))
