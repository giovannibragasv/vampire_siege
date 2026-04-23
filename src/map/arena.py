import pygame
from src.settings import ARENA_WIDTH, ARENA_HEIGHT, C_VOID, C_DARK_PURPLE, C_BLOOD_DARK


class Arena:
    """Bounded play field. Provides wall-clamping and fountain management."""

    WALL_THICKNESS = 24

    def __init__(self):
        self.rect = pygame.Rect(0, 0, ARENA_WIDTH, ARENA_HEIGHT)
        self.inner = pygame.Rect(
            self.WALL_THICKNESS,
            self.WALL_THICKNESS,
            ARENA_WIDTH  - self.WALL_THICKNESS * 2,
            ARENA_HEIGHT - self.WALL_THICKNESS * 2,
        )
        self._build_fountains()
        self._build_cross_pickup()
        self._build_heal_pickup()

    # ------------------------------------------------------------------

    def _build_fountains(self):
        from src.map.fountain import Fountain
        margin = 120
        self.fountains = [
            Fountain(margin,               margin),
            Fountain(ARENA_WIDTH - margin, margin),
            Fountain(margin,               ARENA_HEIGHT - margin),
            Fountain(ARENA_WIDTH - margin, ARENA_HEIGHT - margin),
        ]

    def _build_cross_pickup(self):
        from src.map.cross_pickup import CrossPickup
        self.cross_pickup = CrossPickup(ARENA_WIDTH // 2, ARENA_HEIGHT // 2)

    def _build_heal_pickup(self):
        from src.map.heal_pickup import HealPickup
        # Offset slightly from cross so both are reachable
        self.heal_pickup = HealPickup(ARENA_WIDTH // 2, ARENA_HEIGHT // 2 - 60)

    # ------------------------------------------------------------------

    def clamp_entity(self, rect):
        """Clamp entity rect inside the inner play area."""
        rect.left   = max(rect.left,   self.inner.left)
        rect.right  = min(rect.right,  self.inner.right)
        rect.top    = max(rect.top,    self.inner.top)
        rect.bottom = min(rect.bottom, self.inner.bottom)

    def update(self, dt):
        for f in self.fountains:
            f.update(dt)
        if self.cross_pickup and not self.cross_pickup.collected:
            self.cross_pickup.update(dt)
        self.heal_pickup.update(dt)

    def draw(self, surface):
        # Background
        surface.fill(C_VOID)
        # Inner floor
        pygame.draw.rect(surface, C_DARK_PURPLE, self.inner)
        # Wall border
        pygame.draw.rect(surface, C_BLOOD_DARK, self.rect, self.WALL_THICKNESS)

        for f in self.fountains:
            f.draw(surface)

        if self.cross_pickup and not self.cross_pickup.collected:
            self.cross_pickup.draw(surface)
        self.heal_pickup.draw(surface)

    def try_collect_cross(self, player_rect):
        if self.cross_pickup and not self.cross_pickup.collected:
            if self.cross_pickup.rect.colliderect(player_rect):
                self.cross_pickup.collected = True
                return True
        return False

    def try_collect_heal(self, player):
        return self.heal_pickup.try_collect(player)

    def try_refill_water(self, player_rect):
        for f in self.fountains:
            if f.rect.colliderect(player_rect):
                return f.try_drain()
        return False
