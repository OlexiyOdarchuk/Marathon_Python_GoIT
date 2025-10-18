import pygame
from config import settings
from core.game import Game

pygame.init()
screen = pygame.display.set_mode((settings["width"], settings["height"]))
game = Game(screen, settings)
game.run()
pygame.quit()
