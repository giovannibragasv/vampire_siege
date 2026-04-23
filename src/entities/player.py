import math
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


class Player:
    WIDTH  = 32
    HEIGHT = 48

    def __init__(self, cx, cy):
        self.rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.rect.center = (cx, cy)

        self.hp     = PLAYER_MAX_HP
        self.max_hp = PLAYER_MAX_HP
        self.speed  = float(PLAYER_SPEED)
        self._facing_right = True
        self._invincible_timer = 0
        self.just_damaged = False   # read by Game to trigger shake

        # Weapons
        self._active_weapon = "shotgun"
        self.shotgun    = Shotgun()
        self.holy_water = HolyWater()

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

        self._surface = self._make_surface()

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def handle_event(self, event, cam_x=0, cam_y=0):
        self._cam_x = cam_x
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self._active_weapon = "shotgun"
            elif event.key == pygame.K_2:
                self._active_weapon = "holy_water"
            elif event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                self._try_dodge()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            wx, wy = mx + cam_x, my + cam_y
            cx, cy = self.rect.center
            if self._active_weapon == "shotgun":
                self.shotgun.handle_fire(cx, cy, wx, wy)
            else:
                self.holy_water.handle_fire(cx, cy, wx, wy)

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update(self, dt, arena):
        self._invincible_timer = max(0, self._invincible_timer - dt)
        self._dodge_cooldown   = max(0, self._dodge_cooldown - dt)
        self.just_damaged = False

        self._move(dt, arena)
        self._update_facing()

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
        mx, _ = pygame.mouse.get_pos()
        screen_cx = self.rect.centerx - self._cam_x
        self._facing_right = mx >= screen_cx

    # ------------------------------------------------------------------
    # Damage
    # ------------------------------------------------------------------

    def take_damage(self, amount):
        if self._invincible_timer > 0:
            return
        self.hp = max(0, self.hp - amount)
        self._invincible_timer = CONTACT_DAMAGE_COOLDOWN_MS
        self.just_damaged = True

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
                    ghost = flip_surface(ghost)
                r = ghost.get_rect(center=pos)
                surface.blit(ghost, r)

        img = self._surface.copy()
        if not self._facing_right:
            img = flip_surface(img)

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

        # Dodge cooldown ring
        if self._dodge_cooldown > 0:
            frac = 1.0 - self._dodge_cooldown / DODGE_COOLDOWN_MS
            arc_rect = pygame.Rect(0, 0, 28, 28)
            arc_rect.center = (self.rect.centerx, self.rect.bottom + 8)
            import math as _m
            end_angle = _m.pi * 2 * frac
            pygame.draw.arc(surface, C_GOLD, arc_rect,
                            _m.pi / 2, _m.pi / 2 + end_angle, 3)

    def _make_surface(self):
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (92, 51, 23),
                         (6, 12, self.WIDTH - 12, self.HEIGHT - 12), border_radius=4)
        pygame.draw.ellipse(surf, (200, 149, 130), (8, 2, 16, 14))
        pygame.draw.rect(surf, (139, 58, 26), (8, 2, 16, 6))
        pygame.draw.rect(surf, (100, 100, 100), (self.WIDTH - 10, 20, 12, 5))
        return surf
