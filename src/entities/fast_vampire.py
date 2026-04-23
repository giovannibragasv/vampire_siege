from src.settings import FAST_VAMPIRE_SPEED, FAST_VAMPIRE_HP, FAST_VAMPIRE_DAMAGE
from src.entities.enemy import Enemy


class FastVampire(Enemy):
    WIDTH  = 24
    HEIGHT = 36
    COLOR  = (40, 20, 5)

    def __init__(self, cx, cy):
        super().__init__(cx, cy, FAST_VAMPIRE_HP, FAST_VAMPIRE_SPEED,
                         FAST_VAMPIRE_DAMAGE, self.COLOR)
        import pygame
        self.rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.rect.center = (cx, cy)
        self._surface = self._make_surface()
