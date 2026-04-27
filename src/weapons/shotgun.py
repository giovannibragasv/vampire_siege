import math
from pathlib import Path
import pygame
from src.settings import (
    SHOTGUN_PELLETS,
    SHOTGUN_SPREAD_DEG,
    SHOTGUN_PELLET_SPEED,
    SHOTGUN_PELLET_DAMAGE,
    SHOTGUN_COOLDOWN_MS,
    SHOTGUN_MAGAZINE,
    SHOTGUN_RELOAD_MS,
    SHOTGUN_MAX_RANGE,
    C_SILVER,
    C_BONE,
)
from src.transforms.matrices import rotation_matrix, apply_transform, rotate_surface

_ITEM_SPRITES = Path(__file__).resolve().parents[2] / "assets" / "sprites" / "items"


class Pellet:
    SIZE = 8
    _BULLET_W = 14
    _BULLET_H = 6
    _sprite = None

    def __init__(self, x, y, vx, vy):
        self.rect = pygame.Rect(
            x - self.SIZE // 2, y - self.SIZE // 2, self.SIZE, self.SIZE
        )
        self.vx = vx
        self.vy = vy
        self.alive = True
        self._ox = float(x)   # spawn origin for range check
        self._oy = float(y)
        # Pre-build bullet surface aligned to travel direction
        self._surf = self._make_surf(vx, vy)

    def _make_surf(self, vx, vy):
        if Pellet._sprite is None:
            try:
                Pellet._sprite = pygame.image.load((_ITEM_SPRITES / "pellet.png").as_posix()).convert_alpha()
            except (FileNotFoundError, pygame.error):
                Pellet._sprite = False

        angle_deg = -math.degrees(math.atan2(vy, vx))
        if Pellet._sprite:
            sprite = Pellet._sprite
            if sprite.get_size() != (self.SIZE, self.SIZE):
                sprite = pygame.transform.scale(sprite, (self.SIZE, self.SIZE))
            return rotate_surface(sprite, angle_deg)

        w, h = self._BULLET_W, self._BULLET_H
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        # Silver casing
        pygame.draw.ellipse(s, C_SILVER, (0, 0, w, h))
        # Brighter tip (leading edge)
        pygame.draw.ellipse(s, C_BONE, (w // 2, 1, w // 2 - 1, h - 2))
        # Dark base rim
        pygame.draw.ellipse(s, (120, 120, 140), (0, 1, w // 3, h - 2))
        # Rotate to face velocity (R(θ) matrix via rotate_surface)
        return rotate_surface(s, angle_deg)

    def update(self, dt, arena_inner):
        self.rect.x += int(self.vx * dt / 16)
        self.rect.y += int(self.vy * dt / 16)
        dist = math.hypot(self.rect.centerx - self._ox,
                          self.rect.centery - self._oy)
        if not arena_inner.colliderect(self.rect) or dist >= SHOTGUN_MAX_RANGE:
            self.alive = False

    def draw(self, surface):
        r = self._surf.get_rect(center=self.rect.center)
        surface.blit(self._surf, r)


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
        self.ammo = SHOTGUN_MAGAZINE
        self._reloading = False
        self._reload_timer = 0

    # -- public state for HUD --
    @property
    def reloading(self):
        return self._reloading

    @property
    def reload_progress(self):
        if not self._reloading:
            return 1.0
        return min(1.0, self._reload_timer / SHOTGUN_RELOAD_MS)

    def handle_fire(self, player_cx, player_cy, target_x, target_y):
        if self._cooldown > 0 or self._reloading or self.ammo <= 0:
            return False
        self._spawn_pellets(player_cx, player_cy, target_x, target_y)
        self._cooldown = SHOTGUN_COOLDOWN_MS
        self.ammo -= 1
        if self.ammo <= 0:
            self._reloading = True
            self._reload_timer = 0
        return True

    def _spawn_pellets(self, ox, oy, tx, ty):
        dx, dy = tx - ox, ty - oy
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        base_vx = (dx / dist) * SHOTGUN_PELLET_SPEED
        base_vy = (dy / dist) * SHOTGUN_PELLET_SPEED

        half = SHOTGUN_SPREAD_DEG / 2
        step = SHOTGUN_SPREAD_DEG / max(SHOTGUN_PELLETS - 1, 1)
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
        if self._reloading:
            self._reload_timer += dt
            if self._reload_timer >= SHOTGUN_RELOAD_MS:
                self._reloading = False
                self.ammo = SHOTGUN_MAGAZINE
        for p in self.pellets:
            p.update(dt, arena_inner)
            if p.alive:
                for e in enemies:
                    if p.rect.colliderect(e.rect):
                        pmag = math.hypot(p.vx, p.vy) or 1
                        kbx = (p.vx / pmag) * 7
                        kby = (p.vy / pmag) * 7
                        e.take_damage(getattr(p, "damage", SHOTGUN_PELLET_DAMAGE), kbx, kby)
                        p.alive = False
                        break
        self.pellets = [p for p in self.pellets if p.alive]

    def draw(self, surface):
        for p in self.pellets:
            p.draw(surface)

    @property
    def ready(self):
        return self._cooldown <= 0 and not self._reloading and self.ammo > 0
