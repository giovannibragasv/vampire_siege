import math
import random
import pygame
from src.settings import (
    ARENA_WIDTH, ARENA_HEIGHT,
    C_VOID, C_DARK_PURPLE, C_BLOOD_DARK,
    TOMBSTONE_COUNT,
)


class Arena:
    WALL_THICKNESS = 32

    def __init__(self):
        self.rect  = pygame.Rect(0, 0, ARENA_WIDTH, ARENA_HEIGHT)
        self.inner = pygame.Rect(
            self.WALL_THICKNESS,
            self.WALL_THICKNESS,
            ARENA_WIDTH  - self.WALL_THICKNESS * 2,
            ARENA_HEIGHT - self.WALL_THICKNESS * 2,
        )
        self._build_tombstones()
        self._build_fountains()
        self._build_cross_pickup()
        self._build_heal_pickup()

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    # Fountain corners (must match _build_fountains margin)
    _FOUNTAIN_MARGIN = 160
    _FOUNTAIN_CLEAR  = 110  # min distance from any fountain centre

    def _build_tombstones(self):
        from src.map.tombstone import Tombstone
        m = self._FOUNTAIN_MARGIN
        fountain_centres = [
            (m,                m),
            (ARENA_WIDTH  - m, m),
            (m,                ARENA_HEIGHT - m),
            (ARENA_WIDTH  - m, ARENA_HEIGHT - m),
        ]

        tombstones   = []
        min_wall     = 100
        min_center   = 240
        min_spawn    = 240
        min_between  = 130
        center_x     = ARENA_WIDTH  // 2
        center_y     = ARENA_HEIGHT // 2
        spawn_x      = ARENA_WIDTH  // 2
        spawn_y      = ARENA_HEIGHT * 3 // 4
        tries        = 0

        while len(tombstones) < TOMBSTONE_COUNT and tries < 600:
            tries += 1
            cx = random.randint(self.inner.left  + min_wall, self.inner.right  - min_wall)
            cy = random.randint(self.inner.top   + min_wall, self.inner.bottom - min_wall)

            if math.hypot(cx - center_x, cy - center_y) < min_center:
                continue
            if math.hypot(cx - spawn_x,  cy - spawn_y)  < min_spawn:
                continue
            if any(math.hypot(cx - t.rect.centerx, cy - t.rect.centery) < min_between
                   for t in tombstones):
                continue
            if any(math.hypot(cx - fx, cy - fy) < self._FOUNTAIN_CLEAR
                   for fx, fy in fountain_centres):
                continue
            tombstones.append(Tombstone(cx, cy))

        self.tombstones = tombstones

    def _build_fountains(self):
        from src.map.fountain import Fountain
        m = 160
        self.fountains = [
            Fountain(m,                m),
            Fountain(ARENA_WIDTH  - m, m),
            Fountain(m,                ARENA_HEIGHT - m),
            Fountain(ARENA_WIDTH  - m, ARENA_HEIGHT - m),
        ]

    def _build_cross_pickup(self):
        from src.map.cross_pickup import CrossPickup
        self.cross_pickup = CrossPickup(ARENA_WIDTH // 2, ARENA_HEIGHT // 2)

    def _build_heal_pickup(self):
        from src.map.heal_pickup import HealPickup
        self.heal_pickup = HealPickup(ARENA_WIDTH // 2, ARENA_HEIGHT // 2 - 70)

    # ------------------------------------------------------------------
    # Collision helpers
    # ------------------------------------------------------------------

    def clamp_entity(self, rect: pygame.Rect):
        rect.left   = max(rect.left,   self.inner.left)
        rect.right  = min(rect.right,  self.inner.right)
        rect.top    = max(rect.top,    self.inner.top)
        rect.bottom = min(rect.bottom, self.inner.bottom)

    def push_out_tombstones(self, rect: pygame.Rect):
        """AABB push-out so entities cannot walk through tombstones."""
        for t in self.tombstones:
            if not rect.colliderect(t.rect):
                continue
            ol = t.rect.right  - rect.left
            or_ = rect.right  - t.rect.left
            ot = t.rect.bottom - rect.top
            ob = rect.bottom  - t.rect.top
            px = ol if ol < or_ else -or_
            py = ot if ot < ob  else -ob
            if abs(px) <= abs(py):
                rect.x += px
            else:
                rect.y += py

    # ------------------------------------------------------------------
    # Pickup helpers
    # ------------------------------------------------------------------

    def try_collect_cross(self, player_rect: pygame.Rect) -> bool:
        if self.cross_pickup and not self.cross_pickup.collected:
            if self.cross_pickup.rect.colliderect(player_rect):
                self.cross_pickup.collected = True
                return True
        return False

    def try_collect_heal(self, player) -> bool:
        return self.heal_pickup.try_collect(player)

    def try_refill_water(self, player_rect: pygame.Rect) -> bool:
        for f in self.fountains:
            if f.rect.colliderect(player_rect):
                return f.try_drain()
        return False

    # ------------------------------------------------------------------
    # Update / Draw
    # ------------------------------------------------------------------

    def update(self, dt):
        for f in self.fountains:
            f.update(dt)
        if self.cross_pickup and not self.cross_pickup.collected:
            self.cross_pickup.update(dt)
        self.heal_pickup.update(dt)

    def draw(self, surface):
        surface.fill(C_VOID)
        pygame.draw.rect(surface, C_DARK_PURPLE, self.inner)

        for t in self.tombstones:
            t.draw(surface)
        for f in self.fountains:
            f.draw(surface)
        if self.cross_pickup and not self.cross_pickup.collected:
            self.cross_pickup.draw(surface)
        self.heal_pickup.draw(surface)

        # Wall border drawn last so it sits on top of edge objects
        pygame.draw.rect(surface, C_BLOOD_DARK, self.rect, self.WALL_THICKNESS)
