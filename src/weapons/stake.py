import math
import pygame
from src.settings import (
    STAKE_RANGE, STAKE_DAMAGE, STAKE_ARC_DEG,
    STAKE_DURATION_MS, STAKE_COOLDOWN_MS,
)
from src.transforms.matrices import rotation_matrix, apply_transform


class Stake:
    """
    Melee sweep weapon triggered by right-click.
    Hits all enemies within STAKE_RANGE px inside a STAKE_ARC_DEG wedge.
    Arc polygon built with rotation_matrix to rotate the base vector.
    """

    def __init__(self):
        self._cooldown    = 0.0
        self._active      = False
        self._active_timer = 0.0
        self._aim_angle   = 0.0   # radians toward cursor at fire time
        self._hit: set[int] = set()

    # -- public state for HUD --
    @property
    def cooldown_frac(self) -> float:
        """0 = on cooldown, 1 = ready."""
        return min(1.0, 1.0 - self._cooldown / STAKE_COOLDOWN_MS)

    @property
    def ready(self) -> bool:
        return self._cooldown <= 0

    # ------------------------------------------------------------------

    def handle_fire(self, player_cx, player_cy, target_x, target_y):
        if self._cooldown > 0:
            return
        dx, dy = target_x - player_cx, target_y - player_cy
        self._aim_angle   = math.atan2(dy, dx)
        self._active      = True
        self._active_timer = 0.0
        self._cooldown    = STAKE_COOLDOWN_MS
        self._hit.clear()

    def update(self, dt, enemies, player_cx, player_cy):
        self._cooldown = max(0, self._cooldown - dt)

        if not self._active:
            return

        self._active_timer += dt
        progress = self._active_timer / STAKE_DURATION_MS
        half_rad = math.radians(STAKE_ARC_DEG / 2)

        for e in enemies:
            if id(e) in self._hit:
                continue
            ex, ey = e.rect.center
            dx, dy = ex - player_cx, ey - player_cy
            if math.hypot(dx, dy) > STAKE_RANGE:
                continue
            angle = math.atan2(dy, dx)
            diff = (angle - self._aim_angle + math.pi) % (2 * math.pi) - math.pi
            if abs(diff) <= half_rad * progress:   # sweep grows with progress
                e.take_damage(STAKE_DAMAGE)
                self._hit.add(id(e))

        if self._active_timer >= STAKE_DURATION_MS:
            self._active = False

    def draw(self, surface, cx, cy):
        if not self._active:
            return

        progress = min(1.0, self._active_timer / STAKE_DURATION_MS)
        r = STAKE_RANGE
        half_rad = math.radians(STAKE_ARC_DEG / 2)
        start_a = self._aim_angle - half_rad
        swept   = math.radians(STAKE_ARC_DEG * progress)
        fade    = max(0.0, 1.0 - progress ** 0.55)

        # Build arc polygon with rotation_matrix for each point
        STEPS = 16
        points: list[tuple[float, float]] = [(float(cx), float(cy))]
        for i in range(STEPS + 1):
            angle = start_a + swept * i / STEPS
            rm = rotation_matrix(angle)
            dx, dy = apply_transform(rm, float(r), 0.0)
            points.append((cx + dx, cy + dy))

        # Draw on SRCALPHA surface to support per-pixel alpha
        off = r + 4
        sz  = off * 2
        s   = pygame.Surface((sz, sz), pygame.SRCALPHA)
        sp  = [(x - cx + off, y - cy + off) for x, y in points]
        pygame.draw.polygon(s, (200, 150, 30, int(88 * fade)), sp)
        pygame.draw.polygon(s, (255, 200, 70, int(200 * fade)), sp, 2)

        # Stake shaft line at aim direction + bright tip
        tip_x = cx + r * math.cos(self._aim_angle)
        tip_y = cy + r * math.sin(self._aim_angle)
        lx, ly = int(tip_x - cx + off), int(tip_y - cy + off)
        pygame.draw.line(s, (190, 140, 60, int(230 * fade)), (off, off), (lx, ly), 3)
        pygame.draw.circle(s, (255, 215, 90, int(255 * fade)), (lx, ly), 4)

        surface.blit(s, (cx - off, cy - off))
