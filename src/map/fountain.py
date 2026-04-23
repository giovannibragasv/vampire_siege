import pygame
from src.settings import FOUNTAIN_REFILL_MS, C_HOLY_BLUE, C_HOLY_LIGHT, C_SILVER


class Fountain:
    """
    Three-state interactive object: FLOWING → EMPTY → REFILLING → FLOWING.
    Drains when the player collides and has fewer than max holy water.
    """

    STATE_FLOWING   = "flowing"
    STATE_EMPTY     = "empty"
    STATE_REFILLING = "refilling"

    SIZE = 48

    def __init__(self, cx, cy):
        self.rect = pygame.Rect(0, 0, self.SIZE, self.SIZE)
        self.rect.center = (cx, cy)
        self.state = self.STATE_FLOWING
        self._refill_timer = 0

        self._frame = 0
        self._frame_timer = 0
        self._frame_interval = 180  # ms per animation frame

    # ------------------------------------------------------------------

    def try_drain(self):
        if self.state == self.STATE_FLOWING:
            self.state = self.STATE_EMPTY
            self._refill_timer = 0
            return True
        return False

    def update(self, dt):
        self._frame_timer += dt
        if self._frame_timer >= self._frame_interval:
            self._frame_timer = 0
            self._frame = (self._frame + 1) % 3

        if self.state == self.STATE_EMPTY:
            self._refill_timer += dt
            if self._refill_timer >= FOUNTAIN_REFILL_MS * 0.1:
                self.state = self.STATE_REFILLING
                self._refill_timer = 0

        elif self.state == self.STATE_REFILLING:
            self._refill_timer += dt
            if self._refill_timer >= FOUNTAIN_REFILL_MS * 0.9:
                self.state = self.STATE_FLOWING
                self._refill_timer = 0

    def draw(self, surface):
        # Placeholder geometry — replaced by sprite sheets once art is ready.
        base_color = {
            self.STATE_FLOWING:   C_HOLY_BLUE,
            self.STATE_EMPTY:     (80, 80, 100),
            self.STATE_REFILLING: C_SILVER,
        }[self.state]

        pygame.draw.rect(surface, (50, 50, 70), self.rect, border_radius=6)
        pygame.draw.rect(surface, base_color,   self.rect.inflate(-10, -10), border_radius=4)

        if self.state == self.STATE_FLOWING:
            drop_y = self.rect.top + 8 + (self._frame * 4)
            pygame.draw.circle(surface, C_HOLY_LIGHT,
                               (self.rect.centerx, drop_y), 3)
