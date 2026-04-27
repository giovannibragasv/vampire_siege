import math
from pathlib import Path
import pygame
from src.settings import (
    CROSS_ORBIT_RADIUS, CROSS_ORBIT_SPEED_DEG,
    CROSS_SPIN_SPEED_DEG, CROSS_DAMAGE, CROSS_HIT_COOLDOWN_MS,
    C_GOLD, C_SILVER,
)
from src.transforms.matrices import orbit_position, rotate_surface


class SilverCross:
    """
    Orbiting weapon. Position computed each frame via orbit_position()
    (rotation matrix + translation). Sprite rotated via rotate_surface()
    (rotation matrix applied to surface pixels).
    """

    SIZE = 24

    def __init__(self, orbit_index, orbit_radius, orbit_speed_mult):
        self._phase_offset = orbit_index * (360 / 4)  # spread multiple crosses evenly
        self._orbit_angle  = float(self._phase_offset)
        self._spin_angle   = 0.0
        self.orbit_radius  = orbit_radius
        self.orbit_speed_mult = orbit_speed_mult
        self._hit_cooldowns: dict[int, int] = {}
        self._surface = self._load_surface()
        self.rect = pygame.Rect(0, 0, self.SIZE, self.SIZE)

    # ------------------------------------------------------------------

    def _make_surface(self):
        surf = pygame.Surface((self.SIZE, self.SIZE), pygame.SRCALPHA)
        cx, cy = self.SIZE // 2, self.SIZE // 2
        pygame.draw.rect(surf, C_GOLD,   (cx - 2, 2, 4, self.SIZE - 4))
        pygame.draw.rect(surf, C_GOLD,   (4, cy - 2, self.SIZE - 8, 4))
        pygame.draw.rect(surf, C_SILVER, (cx - 3, 2, 1, self.SIZE - 4))
        pygame.draw.rect(surf, C_SILVER, (4, cy - 3, self.SIZE - 8, 1))
        pygame.draw.circle(surf, (139, 0, 0), (cx, cy), 3)
        return surf

    def _load_surface(self):
        root = Path(__file__).resolve().parents[2]
        path = root / "assets" / "sprites" / "items" / "cross.png"
        try:
            surf = pygame.image.load(path.as_posix()).convert_alpha()
            if surf.get_size() != (self.SIZE, self.SIZE):
                surf = pygame.transform.scale(surf, (self.SIZE, self.SIZE))
            return surf
        except (FileNotFoundError, pygame.error):
            return self._make_surface()

    def update(self, dt, player_cx, player_cy):
        deg_per_sec = CROSS_ORBIT_SPEED_DEG * self.orbit_speed_mult
        self._orbit_angle = (self._orbit_angle + deg_per_sec * dt / 1000) % 360
        self._spin_angle  = (self._spin_angle  + CROSS_SPIN_SPEED_DEG * dt / 1000) % 360

        angle_rad = math.radians(self._orbit_angle)
        ox, oy = orbit_position(player_cx, player_cy, self.orbit_radius, angle_rad)
        self.rect.center = (int(ox), int(oy))

        for eid in list(self._hit_cooldowns):
            self._hit_cooldowns[eid] -= dt
            if self._hit_cooldowns[eid] <= 0:
                del self._hit_cooldowns[eid]

    def try_hit(self, enemy):
        eid = id(enemy)
        if eid not in self._hit_cooldowns:
            if self.rect.colliderect(enemy.rect):
                enemy.take_damage(CROSS_DAMAGE)
                self._hit_cooldowns[eid] = CROSS_HIT_COOLDOWN_MS
                return True
        return False

    def draw(self, surface):
        rotated = rotate_surface(self._surface, self._spin_angle)
        rect = rotated.get_rect(center=self.rect.center)
        surface.blit(rotated, rect)
