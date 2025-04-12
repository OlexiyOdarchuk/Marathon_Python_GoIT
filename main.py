import pygame
from core.game import Game

settings = {
    "width": 1200,
    "height": 800,
    "bg": "assets/background.png",
    "player_images": "assets/Player",
    "enemy_image": "assets/enemy.png",
    "bonus_image": "assets/bonus.png",
    "player_size": (182, 76)
}

pygame.init()
screen = pygame.display.set_mode((settings["width"], settings["height"]))
game = Game(screen, settings)
game.run()
pygame.quit()
