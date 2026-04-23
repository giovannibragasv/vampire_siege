import random
import pygame


class BloodDecal:
    LIFETIME_MS = 4500

    def __init__(self, cx, cy):
        self.cx    = cx + random.randint(-10, 10)
        self.cy    = cy + random.randint(-6, 6)
        self.w     = random.randint(22, 38)
        self.h     = random.randint(10, 18)
        self._timer = 0
        # Pre-render at full opacity; alpha applied per draw
        self._surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.ellipse(self._surf, (90, 0, 0, 255),
                            (0, 0, self.w, self.h))
        # Smaller inner highlight
        if self.w > 14:
            pygame.draw.ellipse(self._surf, (120, 10, 10, 180),
                                (3, 2, self.w - 6, self.h - 4))

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
