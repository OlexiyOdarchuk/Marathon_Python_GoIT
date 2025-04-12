import pygame
import os

class Player:
    def __init__(self, x, y, size, image_path):
        self.images = [pygame.image.load(os.path.join(image_path, img)).convert_alpha()
                       for img in sorted(os.listdir(image_path))]
        self.image_index = 0
        self.rect = self.images[0].get_rect(x=x, y=y)
        self.speed = [0, 0]

    def update(self, keys, screen_width, screen_height):
        if keys[pygame.K_DOWN] and self.rect.bottom < screen_height:
            self.speed[1] = 4
        elif keys[pygame.K_UP] and self.rect.top > 0:
            self.speed[1] = -4
        else:
            self.speed[1] = 0

        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.speed[0] = 4
        elif keys[pygame.K_LEFT] and self.rect.left > 0:
            self.speed[0] = -4
        else:
            self.speed[0] = 0

        self.rect.move_ip(self.speed)

    def animate(self):
        self.image_index = (self.image_index + 1) % len(self.images)

    def draw(self, surface):
        surface.blit(self.images[self.image_index], self.rect)
