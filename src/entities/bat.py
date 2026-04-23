import math
import pygame
from src.settings import BAT_SPEED, BAT_DAMAGE


class Bat:
    """Projectile launched by the Mirror Enemy during its bat wave attack."""

    SIZE = 14

    def __init__(self, cx, cy, target_x, target_y):
        dx, dy = target_x - cx, target_y - cy
        dist = math.hypot(dx, dy) or 1
        self.vx = (dx / dist) * BAT_SPEED
        self.vy = (dy / dist) * BAT_SPEED
        self.x  = float(cx)
        self.y  = float(cy)
        self.alive = True
        self._wing_frame = 0
        self._wing_timer = 0

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x) - self.SIZE // 2,
            int(self.y) - self.SIZE // 2,
            self.SIZE, self.SIZE,
        )

    def update(self, dt, arena_inner, player):
        self.x += self.vx * dt / 16
        self.y += self.vy * dt / 16

        self._wing_timer += dt
        if self._wing_timer >= 120:
            self._wing_timer = 0
            self._wing_frame = (self._wing_frame + 1) % 2

        if not arena_inner.colliderect(self.rect):
            self.alive = False
            return

        if self.rect.colliderect(player.rect):
            player.take_damage(BAT_DAMAGE)
            self.alive = False

    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        body_color = (50, 0, 70)
        wing_color = (80, 0, 110)

        # Body
        pygame.draw.ellipse(surface, body_color, (cx - 4, cy - 3, 8, 7))

        # Wings (flap animation)
        if self._wing_frame == 0:
            pygame.draw.ellipse(surface, wing_color, (cx - 12, cy - 7, 10, 6))
            pygame.draw.ellipse(surface, wing_color, (cx + 2,  cy - 7, 10, 6))
        else:
            pygame.draw.ellipse(surface, wing_color, (cx - 12, cy + 1, 10, 5))
            pygame.draw.ellipse(surface, wing_color, (cx + 2,  cy + 1, 10, 5))

        # Eyes
        pygame.draw.circle(surface, (220, 0, 0), (cx - 2, cy - 1), 1)
        pygame.draw.circle(surface, (220, 0, 0), (cx + 2, cy - 1), 1)
