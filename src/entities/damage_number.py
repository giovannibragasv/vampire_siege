import random
import pygame

_FONT: "pygame.font.Font | None" = None


def _get_font() -> pygame.font.Font:
    global _FONT
    if _FONT is None:
        _FONT = pygame.font.SysFont("serif", 15, bold=True)
    return _FONT


class DamageNumber:
    """Floating damage readout that drifts upward and fades out."""

    LIFETIME_MS = 900

    def __init__(self, x: int, y: int, amount: int):
        self.x = float(x) + random.randint(-8, 8)
        self.y = float(y) - 8
        self._timer = 0.0
        self.alive = True

        if amount < 30:
            color = (255, 220, 50)
        elif amount < 80:
            color = (255, 140, 30)
        else:
            color = (255, 55, 55)

        self._surf = _get_font().render(str(amount), True, color)

    def update(self, dt: float):
        self._timer += dt
        self.y -= 1.3 * dt / 16
        if self._timer >= self.LIFETIME_MS:
            self.alive = False

    def draw(self, surface: pygame.Surface):
        progress = self._timer / self.LIFETIME_MS
        # Hold full opacity until 55%, then fade
        alpha = 255 if progress < 0.55 else int(255 * (1 - progress) / 0.45)
        img = self._surf.copy()
        img.set_alpha(max(0, alpha))
        surface.blit(img, (int(self.x) - img.get_width() // 2, int(self.y)))
