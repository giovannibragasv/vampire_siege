import math
from pathlib import Path
import pygame
from src.settings import (
    PLAYER_SPEED, PLAYER_MAX_HP, HOLY_WATER_MAX,
    CROSS_ORBIT_RADIUS, CROSS_ORBIT_SPEED_DEG,
    CONTACT_DAMAGE_COOLDOWN_MS,
    DODGE_DURATION_MS, DODGE_COOLDOWN_MS, DODGE_SPEED_MULT,
    C_BONE, C_BLOOD_MID, C_GOLD,
)
from src.transforms.matrices import flip_surface
from src.weapons.shotgun import Shotgun
from src.weapons.holy_water import HolyWater
from src.weapons.silver_cross import SilverCross
from src.weapons.stake import Stake


class Player:
    WIDTH  = 32
    HEIGHT = 48
    IDLE_FRAME_MS = 450
    WALK_FRAME_MS = 140
    ACTION_FRAME_MS = 120
    DAMAGE_FRAME_MS = 220
    DEATH_FRAME_MS = 360

    def __init__(self, cx, cy):
        self.rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.rect.center = (cx, cy)

        self.hp     = PLAYER_MAX_HP
        self.max_hp = PLAYER_MAX_HP
        self.speed  = float(PLAYER_SPEED)
        self._facing_right = True
        self._invincible_timer = 0
        self.just_damaged = False   # read by Game to trigger shake
        self._move_dx = 0.0
        self._move_dy = 0.0
        self._idle_timer = 0
        self._idle_frame_index = 0
        self._walk_timer = 0
        self._walk_frame_index = 0
        self._action_frames = None
        self._action_timer = 0
        self._action_frame_index = 0
        self._action_frame_ms = self.ACTION_FRAME_MS
        self._dead = False
        self._death_finished = False

        # Weapons
        self._active_weapon = "shotgun"
        self.shotgun    = Shotgun()
        self.holy_water = HolyWater()
        self.stake      = Stake()

        # Orbiting crosses
        self.orbit_radius              = float(CROSS_ORBIT_RADIUS)
        self.orbit_speed_multiplier    = 1.0
        self.shotgun_damage_multiplier = 1.0
        self._crosses: list[SilverCross] = []
        self.add_orbit_slot()

        # Dodge roll
        self._dodge_active   = False
        self._dodge_timer    = 0
        self._dodge_cooldown = 0
        self._dodge_vx       = 0.0
        self._dodge_vy       = 0.0
        self._trail: list[tuple[int, int]] = []  # world positions for ghost trail
        self._cam_x = 0
        self._cam_y = 0
        self._facing_down = True

        self._idle_frames_front = self._load_frames("player_idle", 2)
        self._walk_frames_front = self._load_frames("player_walk", 4)
        self._walk_frames_back = self._load_frames("player_back_walk", 4)
        self._idle_frames_back = [self._walk_frames_back[1]]
        self._fire_frames = self._load_frames("player_fire", 2)
        self._throw_frames = self._load_frames("player_throw", 2)
        self._damaged_frames = self._load_named_frames(["player_damaged.png"])
        self._death_frames = self._load_frames("player_death", 4)
        self._surface = self._idle_frames_front[0]

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def handle_event(self, event, cam_x=0, cam_y=0):
        if self._dead:
            return
        self._cam_x = cam_x
        self._cam_y = cam_y
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self._active_weapon = "shotgun"
            elif event.key == pygame.K_2:
                self._active_weapon = "holy_water"
            elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                self._try_dodge()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            wx, wy = mx + cam_x, my + cam_y
            cx, cy = self.rect.center
            if event.button == 1:
                if self._active_weapon == "shotgun":
                    if self.shotgun.handle_fire(cx, cy, wx, wy):
                        self._play_action(self._fire_frames, self.ACTION_FRAME_MS)
                else:
                    if self.holy_water.handle_fire(cx, cy, wx, wy):
                        self._play_action(self._throw_frames, self.ACTION_FRAME_MS)
            elif event.button == 3:
                self.stake.handle_fire(cx, cy, wx, wy)

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update(self, dt, arena):
        self._invincible_timer = max(0, self._invincible_timer - dt)
        self._dodge_cooldown   = max(0, self._dodge_cooldown - dt)
        self.just_damaged = False

        if self._dead:
            self._update_animation(dt)
            return

        self._move(dt, arena)
        self._update_facing()
        self._update_animation(dt)

        if arena.try_refill_water(self.rect):
            self.holy_water.refill()
        if arena.try_collect_cross(self.rect):
            self.add_orbit_slot()
        arena.try_collect_heal(self)

        # Ghost trail update
        if self._dodge_active:
            self._trail.append(self.rect.center)
            if len(self._trail) > 3:
                self._trail.pop(0)
        else:
            self._trail.clear()

    def _move(self, dt, arena):
        if self._dodge_active:
            self._dodge_timer -= dt
            if self._dodge_timer <= 0:
                self._dodge_active = False
            self._move_dx = self._dodge_vx
            self._move_dy = self._dodge_vy
            spd = self.speed * DODGE_SPEED_MULT * dt / 16
            self.rect.x += int(self._dodge_vx * spd)
            self.rect.y += int(self._dodge_vy * spd)
        else:
            keys = pygame.key.get_pressed()
            dx = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - \
                 int(keys[pygame.K_a] or keys[pygame.K_LEFT])
            dy = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - \
                 int(keys[pygame.K_w] or keys[pygame.K_UP])
            if dx != 0 and dy != 0:
                f = 1 / math.sqrt(2)
                dx *= f; dy *= f
            self._move_dx = dx
            self._move_dy = dy
            self.rect.x += int(dx * self.speed * dt / 16)
            self.rect.y += int(dy * self.speed * dt / 16)

        arena.clamp_entity(self.rect)
        arena.push_out_tombstones(self.rect)

    def _try_dodge(self):
        if self._dodge_active or self._dodge_cooldown > 0:
            return
        keys = pygame.key.get_pressed()
        dx = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - \
             int(keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - \
             int(keys[pygame.K_w] or keys[pygame.K_UP])
        if dx == 0 and dy == 0:
            return
        dist = math.hypot(dx, dy) or 1
        self._dodge_vx     = dx / dist
        self._dodge_vy     = dy / dist
        self._dodge_active = True
        self._dodge_timer  = DODGE_DURATION_MS
        self._dodge_cooldown = DODGE_COOLDOWN_MS
        # Full invincibility during roll
        self._invincible_timer = max(self._invincible_timer, DODGE_DURATION_MS)

    def _update_facing(self):
        mx, my = pygame.mouse.get_pos()
        screen_cx = self.rect.centerx - self._cam_x
        screen_cy = self.rect.centery - self._cam_y
        self._facing_right = mx >= screen_cx
        self._facing_down  = my >= screen_cy

    def _update_animation(self, dt):
        if self._dead:
            self._update_death_animation(dt)
            return

        if self._action_frames:
            self._update_action_animation(dt)
            return

        moving = abs(self._move_dx) > 0 or abs(self._move_dy) > 0
        if not moving:
            self._walk_timer = 0
            self._walk_frame_index = 0
            idle_frames = self._current_idle_frames()
            self._idle_timer += dt
            if self._idle_timer >= self.IDLE_FRAME_MS:
                steps = self._idle_timer // self.IDLE_FRAME_MS
                self._idle_timer %= self.IDLE_FRAME_MS
                self._idle_frame_index = (self._idle_frame_index + steps) % len(idle_frames)
            self._surface = idle_frames[self._idle_frame_index % len(idle_frames)]
            return

        self._idle_timer = 0
        self._idle_frame_index = 0
        self._walk_timer += dt
        if self._walk_timer >= self.WALK_FRAME_MS:
            frames = self._current_frames()
            steps = self._walk_timer // self.WALK_FRAME_MS
            self._walk_timer %= self.WALK_FRAME_MS
            self._walk_frame_index = (self._walk_frame_index + steps) % len(frames)

        frames = self._current_frames()
        self._surface = frames[self._walk_frame_index % len(frames)]

    def _play_action(self, frames, frame_ms):
        if self._dead:
            return
        self._action_frames = frames
        self._action_timer = 0
        self._action_frame_index = 0
        self._action_frame_ms = frame_ms
        self._surface = frames[0]

    def _update_action_animation(self, dt):
        self._action_timer += dt
        if self._action_timer >= self._action_frame_ms:
            steps = self._action_timer // self._action_frame_ms
            self._action_timer %= self._action_frame_ms
            self._action_frame_index += steps

        if self._action_frame_index >= len(self._action_frames):
            self._action_frames = None
            self._action_timer = 0
            self._action_frame_index = 0
            self._update_animation(0)
            return

        self._surface = self._action_frames[self._action_frame_index]

    def start_death(self):
        if self._dead:
            return
        self._dead = True
        self._death_finished = False
        self._dodge_active = False
        self._trail.clear()
        self._move_dx = 0.0
        self._move_dy = 0.0
        self._action_frames = None
        self._action_timer = 0
        self._action_frame_index = 0
        self._surface = self._death_frames[0]

    @property
    def death_finished(self):
        return self._death_finished

    def _update_death_animation(self, dt):
        if self._death_finished:
            self._surface = self._death_frames[-1]
            return

        self._action_timer += dt
        if self._action_timer >= self.DEATH_FRAME_MS:
            steps = self._action_timer // self.DEATH_FRAME_MS
            self._action_timer %= self.DEATH_FRAME_MS
            self._action_frame_index = min(
                self._action_frame_index + steps,
                len(self._death_frames) - 1,
            )
        self._surface = self._death_frames[self._action_frame_index]
        self._death_finished = self._action_frame_index >= len(self._death_frames) - 1

    # ------------------------------------------------------------------
    # Damage
    # ------------------------------------------------------------------

    def take_damage(self, amount):
        if self._invincible_timer > 0:
            return
        self.hp = max(0, self.hp - amount)
        self._invincible_timer = CONTACT_DAMAGE_COOLDOWN_MS
        self.just_damaged = True
        if self.hp <= 0:
            self.start_death()
        else:
            self._play_action(self._damaged_frames, self.DAMAGE_FRAME_MS)

    # ------------------------------------------------------------------
    # Upgrades
    # ------------------------------------------------------------------

    def add_orbit_slot(self):
        idx = len(self._crosses)
        if idx >= 3:
            return
        self._crosses.append(
            SilverCross(idx, self.orbit_radius, self.orbit_speed_multiplier)
        )

    # ------------------------------------------------------------------
    # Weapons (called by WaveManager)
    # ------------------------------------------------------------------

    def update_weapons_with_enemies(self, dt, arena, enemies):
        cx, cy = self.rect.center
        for cross in self._crosses:
            cross.orbit_radius     = self.orbit_radius
            cross.orbit_speed_mult = self.orbit_speed_multiplier
            cross.update(dt, cx, cy)
            for e in enemies:
                cross.try_hit(e)
        self.shotgun.damage_mult = self.shotgun_damage_multiplier
        self.shotgun.update(dt, arena.inner, enemies)
        self.holy_water.update(dt, enemies)
        self.stake.update(dt, enemies, cx, cy)

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------

    def draw(self, surface):
        # Ghost trail during dodge
        if self._dodge_active and self._trail:
            for i, pos in enumerate(self._trail):
                alpha = 80 + i * 40
                ghost = self._surface.copy()
                ghost.set_alpha(alpha)
                if not self._facing_right:
                    ghost = flip_surface(ghost, flip_x=True, flip_y=False)
                r = ghost.get_rect(center=pos)
                surface.blit(ghost, r)

        img = self._surface.copy()
        if not self._facing_right:
            img = flip_surface(img, flip_x=True, flip_y=False)
        # Damage flash (invincible but not rolling)
        if self._invincible_timer > 0 and not self._dodge_active:
            if (self._invincible_timer // 80) % 2 == 0:
                img.fill((255, 80, 80, 100), special_flags=pygame.BLEND_RGBA_ADD)

        # Semi-transparent during dodge
        if self._dodge_active:
            img.set_alpha(160)

        rect = img.get_rect(center=self.rect.center)
        surface.blit(img, rect)

        for cross in self._crosses:
            cross.draw(surface)

        self.stake.draw(surface, self.rect.centerx, self.rect.centery)
        self.shotgun.draw(surface)
        self.holy_water.draw(surface)

        # Dodge cooldown ring
        if self._dodge_cooldown > 0:
            frac = 1.0 - self._dodge_cooldown / DODGE_COOLDOWN_MS
            arc_rect = pygame.Rect(0, 0, 28, 28)
            arc_rect.center = (self.rect.centerx, self.rect.bottom + 8)
            import math as _m
            end_angle = _m.pi * 2 * frac
            pygame.draw.arc(surface, C_GOLD, arc_rect,
                            _m.pi / 2, _m.pi / 2 + end_angle, 3)

    def _current_frames(self):
        return self._walk_frames_front if self._facing_down else self._walk_frames_back

    def _current_idle_frames(self):
        return self._idle_frames_front if self._facing_down else self._idle_frames_back

    def _load_frames(self, prefix, count):
        return self._load_named_frames(
            [f"{prefix}_{idx}.png" for idx in range(1, count + 1)]
        )

    def _load_named_frames(self, filenames):
        root = Path(__file__).resolve().parents[2]
        sprite_dir = root / "assets" / "sprites" / "player"
        frames = []
        for filename in filenames:
            frame = None
            for frame_path in (root / filename, sprite_dir / filename):
                try:
                    frame = pygame.image.load(frame_path.as_posix()).convert_alpha()
                    if frame.get_size() != (self.WIDTH, self.HEIGHT):
                        frame = pygame.transform.scale(frame, (self.WIDTH, self.HEIGHT))
                    break
                except (FileNotFoundError, pygame.error):
                    continue
            frames.append(frame if frame is not None else self._make_placeholder_surface())
        return frames

    def _make_placeholder_surface(self):
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (92, 51, 23),
                         (6, 12, self.WIDTH - 12, self.HEIGHT - 12), border_radius=4)
        pygame.draw.ellipse(surf, (200, 149, 130), (8, 2, 16, 14))
        pygame.draw.rect(surf, (139, 58, 26), (8, 2, 16, 6))
        pygame.draw.rect(surf, (100, 100, 100), (self.WIDTH - 10, 20, 12, 5))
        return surf
