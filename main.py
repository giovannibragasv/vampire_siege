import sys
import pygame
from src.game import Game
from src.settings import TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, FPS


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    game = Game(screen, clock)
    game.run()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
