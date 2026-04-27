import math
import random
from pathlib import Path
import pygame
from src.settings import (
    MIRROR_HP, MIRROR_DAMAGE,
    MIRROR_PATROL_MS, MIRROR_CONJURE_MS,
    MIRROR_DASH_SPEED, MIRROR_DASH_DURATION_MS,
    MIRROR_BAT_COUNT,
    ARENA_CENTER_X, CONTACT_DAMAGE_COOLDOWN_MS,
)
from src.transforms.matrices import mirror_position, rotation_matrix, apply_transform
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
    IDLE_FRAME_MS = 450
    WALK_FRAME_MS = 130
    DAMAGE_FRAME_MS = 220
    DEATH_FRAME_MS = 360

    def __init__(self, player_cx, player_cy):
        mx = int(mirror_position(player_cx, ARENA_CENTER_X))
        super().__init__(mx, player_cy, MIRROR_HP, 0, MIRROR_DAMAGE, self.COLOR)
        self.remove_ready = False
        self._idle_frames     = self._load_frames("mirror_idle", 2)
        self._walk_frames     = self._load_frames("mirror_walk", 4)
        self._damaged_frame   = self._load_named_frame("mirror_damaged.png")
        self._death_frames    = self._load_frames("mirror_death", 4)
        self._surface         = self._idle_frames[0]
        self._conjure_surface = self._make_conjure_surface()
        self._dash_surface    = self._make_dash_surface()

        self._state           = _State.PATROL
        self._state_timer     = 0.0
        self._patrol_timer    = 0.0
        self._dash_target     = None
        self._conjure_angle   = 0.0   # orbiting particle angle
        self.bats: list[Bat]  = []

        # Patrol jitter — smooth random offset applied on top of mirrored pos
        self._jx = 0.0
        self._jy = 0.0
        self._jtx = 0.0   # jitter target x
        self._jty = 0.0   # jitter target y
        self._jitter_timer    = 0.0
        self._jitter_interval = 160  # ms between new random targets
        self._anim_timer      = 0
        self._anim_index      = 0
        self._damage_anim_timer = 0
        self._dying = False

    def take_damage(self, amount, kbx=0.0, kby=0.0):
        if self._dying:
            return
        super().take_damage(amount, kbx, kby)
        if not self.alive:
            self._start_death()
        else:
            self._damage_anim_timer = self.DAMAGE_FRAME_MS
            self._surface = self._damaged_frame

    # ------------------------------------------------------------------
    # State machine
    # ------------------------------------------------------------------

    def update(self, dt, player, arena):
        if self._dying:
            self._update_death(dt)
            for b in self.bats:
                b.update(dt, arena.inner, player)
            self.bats = [b for b in self.bats if b.alive]
            self._hit_timer = max(0, self._hit_timer - dt)
            for dn in self._damage_numbers:
                dn.update(dt)
            self._damage_numbers = [dn for dn in self._damage_numbers if dn.alive]
            return

        px, py = player.rect.center

        if self._state == _State.PATROL:
            # Update jitter offset
            self._jitter_timer += dt
            if self._jitter_timer >= self._jitter_interval:
                self._jitter_timer = 0
                self._jtx = random.uniform(-28, 28)
                self._jty = random.uniform(-28, 28)
            lerp = min(1.0, dt / 70)
            self._jx += (self._jtx - self._jx) * lerp
            self._jy += (self._jty - self._jy) * lerp

            # Mirror position across vertical centre + jitter offset
            self.rect.centerx = int(mirror_position(px, ARENA_CENTER_X) + self._jx)
            self.rect.centery = int(py + self._jy)
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
        self._update_animation(dt)

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
        img = self._surface.copy()
        if self._state == _State.CONJURING and not self._dying:
            self._draw_conjure_particles(surface)

        if self._hit_timer > 0 and not self._dying:
            img.fill((255, 60, 60, 120), special_flags=pygame.BLEND_RGBA_ADD)

        surface.blit(img, self.rect)
        if self.alive:
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

    def _update_animation(self, dt):
        if self._damage_anim_timer > 0:
            self._damage_anim_timer = max(0, self._damage_anim_timer - dt)
            self._surface = self._damaged_frame
            return

        if self._state == _State.CONJURING:
            self._surface = self._conjure_surface
            return
        if self._state == _State.DASHING:
            self._surface = self._dash_surface
            return

        self._anim_timer += dt
        if self._anim_timer >= self.WALK_FRAME_MS:
            steps = self._anim_timer // self.WALK_FRAME_MS
            self._anim_timer %= self.WALK_FRAME_MS
            self._anim_index = (self._anim_index + steps) % len(self._walk_frames)
        self._surface = self._walk_frames[self._anim_index]

    def _start_death(self):
        self._dying = True
        self.remove_ready = False
        self._anim_timer = 0
        self._anim_index = 0
        self._damage_anim_timer = 0
        self._kbx = 0.0
        self._kby = 0.0
        self._surface = self._death_frames[0]

    def _update_death(self, dt):
        self._anim_timer += dt
        if self._anim_index < len(self._death_frames) - 1 and self._anim_timer >= self.DEATH_FRAME_MS:
            steps = self._anim_timer // self.DEATH_FRAME_MS
            self._anim_timer %= self.DEATH_FRAME_MS
            self._anim_index = min(self._anim_index + steps, len(self._death_frames) - 1)
        self._surface = self._death_frames[self._anim_index]
        self.remove_ready = self._anim_index >= len(self._death_frames) - 1 and self._anim_timer > self.DEATH_FRAME_MS * 0.75

    def _load_frames(self, prefix, count):
        return [
            self._load_named_frame(f"{prefix}_{idx}.png")
            for idx in range(1, count + 1)
        ]

    def _load_named_frame(self, filename):
        root = Path(__file__).resolve().parents[2]
        frame_path = root / "assets" / "sprites" / "enemies" / "mirror_enemy" / filename
        try:
            frame = pygame.image.load(frame_path.as_posix()).convert_alpha()
            if frame.get_size() != (self.WIDTH, self.HEIGHT):
                frame = pygame.transform.scale(frame, (self.WIDTH, self.HEIGHT))
            return frame
        except (FileNotFoundError, pygame.error):
            return self._make_mirror_surface()

    def _make_mirror_surface(self):
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (200, 200, 220),
                         (4, 8, self.WIDTH - 8, self.HEIGHT - 8), border_radius=4)
        pygame.draw.ellipse(surf, (80, 40, 100), (8, 0, 16, 14))
        pygame.draw.circle(surf, (155, 48, 255), (16, 7), 3)
        return surf

    def _make_conjure_surface(self):
        """Asset-based conjuring pose with a purple charge tint."""
        surf = self._damaged_frame.copy()
        surf.fill((95, 32, 180, 90), special_flags=pygame.BLEND_RGBA_ADD)
        return surf

    def _make_dash_surface(self):
        """Asset-based dash pose with subtle speed streaks."""
        surf = self._walk_frames[0].copy()
        for i in range(3):
            x = self.WIDTH - 2 - i * 4
            pygame.draw.line(surf, (155, 48, 255, 85), (x, 10), (x, self.HEIGHT - 8), 1)
        return surf
