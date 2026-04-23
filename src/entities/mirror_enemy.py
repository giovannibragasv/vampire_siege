import math
import pygame
from src.settings import (
    MIRROR_HP, MIRROR_DAMAGE,
    MIRROR_PATROL_MS, MIRROR_CONJURE_MS,
    MIRROR_DASH_SPEED, MIRROR_DASH_DURATION_MS,
    MIRROR_BAT_COUNT,
    ARENA_CENTER_X, CONTACT_DAMAGE_COOLDOWN_MS,
)
from src.transforms.matrices import mirror_position, flip_surface, rotation_matrix, apply_transform
from src.entities.enemy import Enemy
from src.entities.bat import Bat


class _State:
    PATROL    = "patrol"
    CONJURING = "conjuring"
    SHOOTING  = "shooting"
    DASHING   = "dashing"


class MirrorEnemy(Enemy):
    """
    Mirrors the player's X across the arena centre (geometric reflection).
    Attack cycle: PATROL → CONJURING (stop + purple glow) →
                  SHOOTING (bat wave) → DASHING → PATROL.
    """

    COLOR = (200, 200, 220)

    def __init__(self, player_cx, player_cy):
        mx = int(mirror_position(player_cx, ARENA_CENTER_X))
        super().__init__(mx, player_cy, MIRROR_HP, 0, MIRROR_DAMAGE, self.COLOR)
        self._surface         = self._make_mirror_surface()
        self._conjure_surface = self._make_conjure_surface()
        self._dash_surface    = self._make_dash_surface()

        self._state           = _State.PATROL
        self._state_timer     = 0.0
        self._patrol_timer    = 0.0
        self._dash_target     = None
        self._conjure_angle   = 0.0   # orbiting particle angle
        self.bats: list[Bat]  = []

    # ------------------------------------------------------------------
    # State machine
    # ------------------------------------------------------------------

    def update(self, dt, player, arena):
        px, py = player.rect.center

        if self._state == _State.PATROL:
            # Mirror position across vertical centre
            self.rect.centerx = int(mirror_position(px, ARENA_CENTER_X))
            self.rect.centery = py
            self._patrol_timer += dt
            if self._patrol_timer >= MIRROR_PATROL_MS:
                self._patrol_timer = 0
                self._enter_conjuring()

        elif self._state == _State.CONJURING:
            # Stop in place; spin particle effect
            self._conjure_angle = (self._conjure_angle + 180 * dt / 1000) % 360
            self._state_timer += dt
            if self._state_timer >= MIRROR_CONJURE_MS:
                self._launch_bats(px, py)
                self._enter_dashing(px, py)

        elif self._state == _State.DASHING:
            self._state_timer += dt
            if self._dash_target:
                tx, ty = self._dash_target
                dx, dy = tx - self.rect.centerx, ty - self.rect.centery
                dist = math.hypot(dx, dy)
                if dist < 12 or self._state_timer >= MIRROR_DASH_DURATION_MS:
                    self._enter_patrol()
                else:
                    spd = MIRROR_DASH_SPEED * dt / 16
                    nx, ny = dx / dist, dy / dist
                    # Tombstone avoidance during dash
                    rx, ry = 0.0, 0.0
                    for t in arena.tombstones:
                        tdx = self.rect.centerx - t.rect.centerx
                        tdy = self.rect.centery - t.rect.centery
                        tdist = math.hypot(tdx, tdy) or 1
                        if tdist < 80:
                            s = (80 - tdist) / 80
                            rx += (tdx / tdist) * s * 2.5
                            ry += (tdy / tdist) * s * 2.5
                    fx, fy = nx + rx, ny + ry
                    fmag = math.hypot(fx, fy) or 1
                    self.rect.x += int((fx / fmag) * spd)
                    self.rect.y += int((fy / fmag) * spd)

        # Apply and decay knockback
        if abs(self._kbx) > 0.1 or abs(self._kby) > 0.1:
            self.rect.x += int(self._kbx * dt / 16)
            self.rect.y += int(self._kby * dt / 16)
            decay = 0.78 ** (dt / 16)
            self._kbx *= decay
            self._kby *= decay

        # Update bats
        for b in self.bats:
            b.update(dt, arena.inner, player)
        self.bats = [b for b in self.bats if b.alive]

        arena.clamp_entity(self.rect)
        arena.push_out_tombstones(self.rect)
        self.try_damage_player(player, dt)
        self._hit_timer = max(0, self._hit_timer - dt)
        self._contact_cooldown = max(0, self._contact_cooldown - dt)

    # ------------------------------------------------------------------
    # Transitions
    # ------------------------------------------------------------------

    def _enter_conjuring(self):
        self._state = _State.CONJURING
        self._state_timer = 0

    def _launch_bats(self, px, py):
        cx, cy = self.rect.center
        dx, dy = px - cx, py - cy
        dist   = math.hypot(dx, dy) or 1
        base_vx, base_vy = dx / dist, dy / dist

        spread_deg = 30
        half = spread_deg / 2
        step = spread_deg / max(MIRROR_BAT_COUNT - 1, 1)

        for i in range(MIRROR_BAT_COUNT):
            angle_rad = math.radians(-half + step * i)
            rm = rotation_matrix(angle_rad)
            rvx, rvy = apply_transform(rm, base_vx, base_vy)
            # Use a far target point so bat travels in that direction
            self.bats.append(Bat(cx, cy, cx + rvx * 500, cy + rvy * 500))

    def _enter_dashing(self, px, py):
        self._state = _State.DASHING
        self._state_timer = 0
        self._dash_target = (px, py)

    def _enter_patrol(self):
        self._state = _State.PATROL
        self._patrol_timer = 0
        self._dash_target = None

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------

    def draw(self, surface):
        # Pick sprite by state
        if self._state == _State.CONJURING:
            img = self._conjure_surface.copy()
            self._draw_conjure_particles(surface)
        elif self._state == _State.DASHING:
            img = self._dash_surface.copy()
        else:
            img = self._surface.copy()

        if self._hit_timer > 0:
            img.fill((255, 60, 60, 120), special_flags=pygame.BLEND_RGBA_ADD)

        img = flip_surface(img, flip_x=True, flip_y=False)
        surface.blit(img, self.rect)
        self._draw_hp_bar(surface)

        # Draw bats
        for b in self.bats:
            b.draw(surface)

    def _draw_conjure_particles(self, surface):
        """Orbiting purple particles to signal the charge-up."""
        cx, cy = self.rect.center
        for i in range(6):
            a = math.radians(self._conjure_angle + i * 60)
            px = cx + int(math.cos(a) * 28)
            py = cy + int(math.sin(a) * 28)
            pygame.draw.circle(surface, (155, 48, 255), (px, py), 4)
            pygame.draw.circle(surface, (200, 100, 255), (px, py), 2)

    # ------------------------------------------------------------------
    # Surfaces
    # ------------------------------------------------------------------

    def _make_mirror_surface(self):
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (200, 200, 220),
                         (4, 8, self.WIDTH - 8, self.HEIGHT - 8), border_radius=4)
        pygame.draw.ellipse(surf, (80, 40, 100), (8, 0, 16, 14))
        pygame.draw.circle(surf, (155, 48, 255), (16, 7), 3)
        return surf

    def _make_conjure_surface(self):
        """Hands raised outward, body lit purple — conjuring pose."""
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        # Body (brighter purple tint)
        pygame.draw.rect(surf, (180, 160, 220),
                         (6, 10, self.WIDTH - 12, self.HEIGHT - 12), border_radius=4)
        # Arms raised outward
        pygame.draw.rect(surf, (160, 140, 200), (0,  16, 6,  4))   # left arm
        pygame.draw.rect(surf, (160, 140, 200), (self.WIDTH - 6, 16, 6, 4))  # right arm
        # Head
        pygame.draw.ellipse(surf, (100, 60, 130), (8, 0, 16, 14))
        # Glowing eyes
        pygame.draw.circle(surf, (220, 100, 255), (14, 7), 3)
        pygame.draw.circle(surf, (220, 100, 255), (19, 7), 3)
        return surf

    def _make_dash_surface(self):
        """Horizontally elongated to suggest speed blur."""
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        # Stretched body
        pygame.draw.rect(surf, (160, 160, 210),
                         (0, 12, self.WIDTH, self.HEIGHT - 14), border_radius=6)
        # Motion streaks (dark lines behind)
        for i in range(3):
            pygame.draw.line(surf, (100, 80, 160, 80),
                             (self.WIDTH - 2 - i * 4, 14),
                             (self.WIDTH - 2 - i * 4, self.HEIGHT - 14), 2)
        # Head low / forward
        pygame.draw.ellipse(surf, (80, 40, 100), (4, 6, 14, 12))
        # Eyes determined
        pygame.draw.circle(surf, (255, 80, 255), (10, 12), 2)
        return surf
