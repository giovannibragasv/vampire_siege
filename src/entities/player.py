import pygame
from src.settings import (
    PLAYER_SPEED, PLAYER_MAX_HP, HOLY_WATER_MAX,
    CROSS_ORBIT_RADIUS, CROSS_ORBIT_SPEED_DEG,
    CONTACT_DAMAGE_COOLDOWN_MS,
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

        # Weapons
        self._active_weapon = "shotgun"  # "shotgun" | "holy_water"
        self.shotgun    = Shotgun()
        self.holy_water = HolyWater()

        # Orbiting crosses
        self.orbit_radius         = float(CROSS_ORBIT_RADIUS)
        self.orbit_speed_multiplier = 1.0
        self.shotgun_damage_multiplier = 1.0
        self._crosses: list[SilverCross] = []
        self.add_orbit_slot()   # start with 1 cross

        # Damage multiplier plumbing
        self.shotgun.damage_mult = self.shotgun_damage_multiplier

        # Placeholder surface — replaced by sprite sheet when art is ready
        self._surface = self._make_surface()

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self._active_weapon = "shotgun"
            elif event.key == pygame.K_2:
                self._active_weapon = "holy_water"

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            cx, cy = self.rect.center
            if self._active_weapon == "shotgun":
                self.shotgun.handle_fire(cx, cy, mx, my)
            else:
                self.holy_water.handle_fire(cx, cy, mx, my)

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update(self, dt, arena):
        self._move(dt, arena)
        self._update_facing()
        self._update_weapons(dt, arena)
        self._invincible_timer = max(0, self._invincible_timer - dt)

        # Fountain refill
        if arena.try_refill_water(self.rect):
            self.holy_water.refill()

        # Cross pickup
        if arena.try_collect_cross(self.rect):
            self.add_orbit_slot()

    def _move(self, dt, arena):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - \
             (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - \
             (keys[pygame.K_w] or keys[pygame.K_UP])

        if dx != 0 and dy != 0:
            import math
            factor = 1 / math.sqrt(2)
            dx *= factor
            dy *= factor

        self.rect.x += int(dx * self.speed * dt / 16)
        self.rect.y += int(dy * self.speed * dt / 16)
        arena.clamp_entity(self.rect)

    def _update_facing(self):
        mx, _ = pygame.mouse.get_pos()
        self._facing_right = mx >= self.rect.centerx

    def _update_weapons(self, dt, arena):
        enemies = arena._wave_manager_ref.enemies if hasattr(arena, "_wave_manager_ref") else []
        cx, cy  = self.rect.center
        for cross in self._crosses:
            cross.orbit_radius         = self.orbit_radius
            cross.orbit_speed_mult     = self.orbit_speed_multiplier
            cross.update(dt, cx, cy)
        self.shotgun.damage_mult = self.shotgun_damage_multiplier
        self.shotgun.update(dt, arena.inner, [])
        self.holy_water.update(dt, [])

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
    # Damage
    # ------------------------------------------------------------------

    def take_damage(self, amount):
        if self._invincible_timer > 0:
            return
        self.hp = max(0, self.hp - amount)
        self._invincible_timer = CONTACT_DAMAGE_COOLDOWN_MS

    # ------------------------------------------------------------------
    # Upgrades
    # ------------------------------------------------------------------

    def add_orbit_slot(self):
        idx = len(self._crosses)
        if idx >= 3:
            return
        c = SilverCross(idx, self.orbit_radius, self.orbit_speed_multiplier)
        self._crosses.append(c)

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------

    def draw(self, surface):
        img = self._surface
        if not self._facing_right:
            # Reflection transform: flip sprite across vertical axis
            img = flip_surface(img, flip_x=True, flip_y=False)
        rect = img.get_rect(center=self.rect.center)
        surface.blit(img, rect)

        if self._invincible_timer > 0 and (self._invincible_timer // 80) % 2 == 0:
            flash = img.copy()
            flash.fill((255, 80, 80, 100), special_flags=pygame.BLEND_RGBA_ADD)
            surface.blit(flash, rect)

        for cross in self._crosses:
            cross.draw(surface)

    def _make_surface(self):
        """Placeholder until sprite sheets are loaded."""
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        # Body
        pygame.draw.rect(surf, (92, 51, 23),
                         (6, 12, self.WIDTH - 12, self.HEIGHT - 12), border_radius=4)
        # Head
        pygame.draw.ellipse(surf, (200, 149, 130), (8, 2, 16, 14))
        # Hair
        pygame.draw.rect(surf, (139, 58, 26), (8, 2, 16, 6))
        # Gun
        pygame.draw.rect(surf, (100, 100, 100), (self.WIDTH - 10, 20, 12, 5))
        return surf
