import math
from pathlib import Path
import pygame
from src.settings import C_GOLD, C_SILVER
from src.transforms.matrices import rotate_surface


class CrossPickup:
    """Silver cross lying at the arena center. Collected once on touch."""

    SIZE = 20

    def __init__(self, cx, cy):
        self.rect = pygame.Rect(0, 0, self.SIZE, self.SIZE)
        self.rect.center = (cx, cy)
        self.collected = False
        self._angle = 0.0
        self._surface = self._load_surface()

    def _make_surface(self):
        surf = pygame.Surface((self.SIZE, self.SIZE), pygame.SRCALPHA)
        cx, cy = self.SIZE // 2, self.SIZE // 2
        pygame.draw.rect(surf, C_GOLD,   (cx - 2, 2,       4, self.SIZE - 4))
        pygame.draw.rect(surf, C_GOLD,   (4,      cy - 2,  self.SIZE - 8, 4))
        pygame.draw.rect(surf, C_SILVER, (cx - 3, 2,       1, self.SIZE - 4))
        pygame.draw.rect(surf, C_SILVER, (4,      cy - 3,  self.SIZE - 8, 1))
        pygame.draw.circle(surf, (139, 0, 0), (cx, cy), 3)
        return surf

    def _load_surface(self):
        root = Path(__file__).resolve().parents[2]
        path = root / "assets" / "sprites" / "items" / "cross_pickup.png"
        try:
            surf = pygame.image.load(path.as_posix()).convert_alpha()
            if surf.get_size() != (self.SIZE, self.SIZE):
                surf = pygame.transform.scale(surf, (self.SIZE, self.SIZE))
            return surf
        except (FileNotFoundError, pygame.error):
            return self._make_surface()

    def update(self, dt):
        self._angle = (self._angle + 60 * dt / 1000) % 360

    def draw(self, surface):
        if self.collected:
            return
        rotated = rotate_surface(self._surface, self._angle)
        rect = rotated.get_rect(center=self.rect.center)
        surface.blit(rotated, rect)
