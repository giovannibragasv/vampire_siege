import random
from pathlib import Path
import pygame

_EFFECT_SPRITES = Path(__file__).resolve().parents[2] / "assets" / "sprites" / "effects"


class BloodDecal:
    LIFETIME_MS = 4500
    _sprite = None

    def __init__(self, cx, cy):
        self.cx    = cx + random.randint(-10, 10)
        self.cy    = cy + random.randint(-6, 6)
        self.w     = random.randint(22, 38)
        self.h     = random.randint(10, 18)
        self._timer = 0
        # Pre-render at full opacity; alpha applied per draw
        self._surf = self._make_surf()

    @property
    def alive(self):
        return self._timer < self.LIFETIME_MS

    def update(self, dt):
        self._timer += dt

    def draw(self, surface):
        alpha = max(0, int(200 * (1.0 - self._timer / self.LIFETIME_MS)))
        img = self._surf.copy()
        img.set_alpha(alpha)
        surface.blit(img, (self.cx - self.w // 2, self.cy - self.h // 2))

    def _make_surf(self):
        if BloodDecal._sprite is None:
            try:
                BloodDecal._sprite = pygame.image.load((_EFFECT_SPRITES / "blood_decal.png").as_posix()).convert_alpha()
            except (FileNotFoundError, pygame.error):
                BloodDecal._sprite = False

        if BloodDecal._sprite:
            return pygame.transform.scale(BloodDecal._sprite, (self.w, self.h))

        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (90, 0, 0, 255), (0, 0, self.w, self.h))
        if self.w > 14:
            pygame.draw.ellipse(surf, (120, 10, 10, 180),
                                (3, 2, self.w - 6, self.h - 4))
        return surf
