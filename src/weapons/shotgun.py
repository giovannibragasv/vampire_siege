import math
import pygame
from src.settings import (
    SHOTGUN_PELLETS, SHOTGUN_SPREAD_DEG, SHOTGUN_PELLET_SPEED,
    SHOTGUN_PELLET_DAMAGE, SHOTGUN_COOLDOWN_MS, C_SILVER, C_BONE,
)
from src.transforms.matrices import rotation_matrix, apply_transform


class Pellet:
    SIZE = 8

    def __init__(self, x, y, vx, vy):
        self.rect = pygame.Rect(x - self.SIZE // 2, y - self.SIZE // 2,
                                self.SIZE, self.SIZE)
        self.vx = vx
        self.vy = vy
        self.alive = True
        self._angle = 0.0

    def update(self, dt, arena_inner):
        # Translation: move pellet each frame
        self.rect.x += int(self.vx * dt / 16)
        self.rect.y += int(self.vy * dt / 16)
        self._angle = (self._angle + 720 * dt / 1000) % 360
        if not arena_inner.colliderect(self.rect):
            self.alive = False

    def draw(self, surface):
        pygame.draw.ellipse(surface, C_SILVER, self.rect)
        pygame.draw.circle(surface, C_BONE,
                           self.rect.center, max(1, self.SIZE // 4))


class Shotgun:
    """
    Fires a spread of Pellets toward the cursor.
    Each pellet's velocity computed by rotating the base direction vector
    via an explicit rotation matrix (one per spread step).
    """

    def __init__(self):
        self._cooldown = 0
        self.pellets: list[Pellet] = []
        self.damage_mult = 1.0

    def handle_fire(self, player_cx, player_cy, target_x, target_y):
        if self._cooldown > 0:
            return
        self._spawn_pellets(player_cx, player_cy, target_x, target_y)
        self._cooldown = SHOTGUN_COOLDOWN_MS

    def _spawn_pellets(self, ox, oy, tx, ty):
        dx, dy = tx - ox, ty - oy
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        base_vx = (dx / dist) * SHOTGUN_PELLET_SPEED
        base_vy = (dy / dist) * SHOTGUN_PELLET_SPEED

        half   = SHOTGUN_SPREAD_DEG / 2
        step   = SHOTGUN_SPREAD_DEG / max(SHOTGUN_PELLETS - 1, 1)
        damage = int(SHOTGUN_PELLET_DAMAGE * self.damage_mult)

        for i in range(SHOTGUN_PELLETS):
            angle_deg = -half + step * i
            angle_rad = math.radians(angle_deg)
            rm = rotation_matrix(angle_rad)
            rvx, rvy = apply_transform(rm, base_vx, base_vy)
            p = Pellet(ox, oy, rvx, rvy)
            p.damage = damage
            self.pellets.append(p)

    def update(self, dt, arena_inner, enemies):
        self._cooldown = max(0, self._cooldown - dt)
        for p in self.pellets:
            p.update(dt, arena_inner)
            if p.alive:
                for e in enemies:
                    if p.rect.colliderect(e.rect):
                        e.take_damage(getattr(p, "damage", SHOTGUN_PELLET_DAMAGE))
                        p.alive = False
                        break
        self.pellets = [p for p in self.pellets if p.alive]

    def draw(self, surface):
        for p in self.pellets:
            p.draw(surface)

    @property
    def ready(self):
        return self._cooldown <= 0
