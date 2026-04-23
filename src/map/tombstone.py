import pygame


class Tombstone:
    """Impassable map obstacle. Blocks player, enemies, and pellets."""

    WIDTH  = 36
    HEIGHT = 52

    _STONE    = (72,  72,  84)
    _STONE_HI = (105, 105, 118)
    _SHADOW   = (44,  44,  52)
    _MOSS     = (50,  72,  50)

    def __init__(self, cx, cy):
        self.rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.rect.center = (cx, cy)

    def draw(self, surface):
        r = self.rect
        cx = r.centerx

        # Shadow behind
        shadow = r.move(3, 4)
        pygame.draw.rect(surface, self._SHADOW, shadow, border_radius=8)

        # Stone body
        pygame.draw.rect(surface, self._STONE, r, border_radius=8)
        # Highlight edge (left + top)
        pygame.draw.rect(surface, self._STONE_HI, r, 2, border_radius=8)

        # Carved cross
        cross_top = r.top + 8
        cross_mid = r.top + 18
        pygame.draw.line(surface, self._SHADOW,
                         (cx, cross_top), (cx, r.centery - 2), 3)
        pygame.draw.line(surface, self._SHADOW,
                         (cx - 9, cross_mid), (cx + 9, cross_mid), 3)

        # Moss patch at base
        pygame.draw.rect(surface, self._MOSS,
                         (r.left + 4, r.bottom - 10, r.width - 8, 6),
                         border_radius=3)
