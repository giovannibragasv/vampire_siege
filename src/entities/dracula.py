import pygame
import math
from src.settings import (
    DRACULA_HP, DRACULA_SPEED, DRACULA_DAMAGE,
    DRACULA_P2_HP_BONUS, DRACULA_P2_SCALE, DRACULA_P2_SPEED,
    DRACULA_P2_TRANSFORM_MS, DRACULA_P2_BAT_COUNT, DRACULA_P2_BAT_INTERVAL,
    C_BLOOD_MID, C_BLOOD_HIGH, C_BONE, C_GOLD,
)
from src.transforms.matrices import scale_surface, rotation_matrix, apply_transform
from src.entities.enemy import Enemy
from src.entities.bat import Bat


class Dracula(Enemy):
    """
    Boss with two phases.
    Phase 2 triggered at 50% HP: plays a 2.8-second transformation animation
    (immortal, stopped, flashing) then finalises stats via scale_surface().
    """

    WIDTH  = 48
    HEIGHT = 64

    COLOR_P1 = (5,  0, 20)
    COLOR_P2 = (20, 0, 40)

    def __init__(self, cx, cy):
        super().__init__(cx, cy, DRACULA_HP, DRACULA_SPEED, DRACULA_DAMAGE, self.COLOR_P1)
        self.rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.rect.center = (cx, cy)
        self._phase        = 1
        self._surface      = self._make_p1_surface()
        self._p2_surface   = self._make_p2_surface()
        self._p2_triggered = False
        self._transforming = False
        self._transform_timer = 0.0
        self._transform_scale = 1.0   # animated from 1.0 → DRACULA_P2_SCALE

        # Phase-2 bat summons
        self.bats: list[Bat] = []
        self._bat_timer = 0.0

    # ------------------------------------------------------------------
    # Damage / immortality
    # ------------------------------------------------------------------

    def take_damage(self, amount, kbx=0.0, kby=0.0):
        if self._transforming:
            return  # immortal during animation
        self.hp -= amount
        self._hit_timer = 250
        self._kbx = kbx * 0.4
        self._kby = kby * 0.4
        if self._phase == 1 and not self._p2_triggered:
            if self.hp <= self.max_hp * 0.5:
                self._begin_transform()
                return
        if self.hp <= 0:
            self.alive = False

    # ------------------------------------------------------------------
    # Transformation
    # ------------------------------------------------------------------

    def _begin_transform(self):
        self._p2_triggered = True   # block re-entry immediately
        self._transforming = True
        self._transform_timer = 0.0
        self._transform_scale = 1.0
        self._hit_timer = 0         # clear damage flash; use our own animation

    def _finish_transform(self):
        self._transforming = False
        self._phase = 2
        self.max_hp += DRACULA_P2_HP_BONUS
        self.hp = self.max_hp
        self.speed = DRACULA_P2_SPEED
        self.damage = int(self.damage * 1.3)
        cx, cy = self.rect.center
        self.WIDTH  = int(48 * DRACULA_P2_SCALE)
        self.HEIGHT = int(64 * DRACULA_P2_SCALE)
        self.rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.rect.center = (cx, cy)
        self._transform_scale = DRACULA_P2_SCALE

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def update(self, dt, player, arena):
        if self._transforming:
            self._transform_timer += dt
            progress = min(1.0, self._transform_timer / DRACULA_P2_TRANSFORM_MS)
            self._transform_scale = 1.0 + (DRACULA_P2_SCALE - 1.0) * (progress ** 2)
            if progress >= 1.0:
                self._finish_transform()
            arena.clamp_entity(self.rect)
            return

        super().update(dt, player, arena)

        if self._phase == 2:
            self._update_bats(dt, player, arena)

    def _update_bats(self, dt, player, arena):
        self._bat_timer += dt
        if self._bat_timer >= DRACULA_P2_BAT_INTERVAL:
            self._bat_timer = 0
            self._summon_bats(player)

        for b in self.bats:
            b.update(dt, arena.inner, player)
        self.bats = [b for b in self.bats if b.alive]

    def _summon_bats(self, player):
        cx, cy = self.rect.center
        px, py = player.rect.center
        dx, dy = px - cx, py - cy
        dist = math.hypot(dx, dy) or 1
        base_vx, base_vy = dx / dist, dy / dist

        spread_deg = 40
        half = spread_deg / 2
        step = spread_deg / max(DRACULA_P2_BAT_COUNT - 1, 1)

        for i in range(DRACULA_P2_BAT_COUNT):
            angle_rad = math.radians(-half + step * i)
            rm = rotation_matrix(angle_rad)
            rvx, rvy = apply_transform(rm, base_vx, base_vy)
            self.bats.append(Bat(cx, cy, cx + rvx * 500, cy + rvy * 500))

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------

    def draw(self, surface):
        if self._transforming:
            self._draw_transform(surface)
            return

        img = self._surface.copy()
        if self._hit_timer > 0:
            img.fill((255, 60, 60, 120), special_flags=pygame.BLEND_RGBA_ADD)
        if not self._facing_right:
            img = pygame.transform.flip(img, True, False)
        if self._phase == 2:
            img = scale_surface(img, DRACULA_P2_SCALE, DRACULA_P2_SCALE)
        draw_rect = img.get_rect(center=self.rect.center)
        surface.blit(img, draw_rect)
        self._draw_hp_bar(surface)

        for b in self.bats:
            b.draw(surface)

    def _draw_transform(self, surface):
        progress = self._transform_timer / DRACULA_P2_TRANSFORM_MS

        # Cross-fade between P1 and P2 surfaces
        p1 = self._make_p1_surface()
        p2 = self._make_p2_surface()
        p1.set_alpha(int(255 * (1.0 - progress)))
        p2.set_alpha(int(255 * progress))

        img = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        img.blit(p1, (0, 0))
        img.blit(p2, (0, 0))

        # Gold flash pulses — rapid early, slow late
        pulse_rate = 80 + int(progress * 200)
        if (self._transform_timer // pulse_rate) % 2 == 0:
            img.fill((200, 160, 0, 120), special_flags=pygame.BLEND_RGBA_ADD)

        img = scale_surface(img, self._transform_scale, self._transform_scale)
        draw_rect = img.get_rect(center=self.rect.center)
        surface.blit(img, draw_rect)
        self._draw_hp_bar(surface)

        # "TRANSFORMING" warning label
        if (self._transform_timer // 400) % 2 == 0:
            font = pygame.font.SysFont("serif", 16, bold=True)
            lbl  = font.render("TRANSFORMING…", True, C_GOLD)
            surface.blit(lbl, lbl.get_rect(centerx=self.rect.centerx,
                                           bottom=self.rect.top - 14))

    # ------------------------------------------------------------------
    # HP bar (wider for boss)
    # ------------------------------------------------------------------

    def _draw_hp_bar(self, surface):
        bar_w = self.WIDTH + 20
        bar_h = 6
        x = self.rect.centerx - bar_w // 2
        y = self.rect.top - 12
        pygame.draw.rect(surface, (40, 0, 0),  (x, y, bar_w, bar_h))
        filled = int(bar_w * max(0, self.hp) / self.max_hp)
        pygame.draw.rect(surface, C_BLOOD_HIGH, (x, y, filled, bar_h))
        font = pygame.font.SysFont("serif", 14)
        label = font.render("DRACULA", True, C_BONE)
        surface.blit(label, label.get_rect(centerx=self.rect.centerx, bottom=y - 2))

    # ------------------------------------------------------------------
    # Surfaces
    # ------------------------------------------------------------------

    def _make_p1_surface(self):
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (5, 0, 20),
                         (2, 6, self.WIDTH - 4, self.HEIGHT - 6), border_radius=6)
        pygame.draw.rect(surf, C_BLOOD_MID,
                         (10, 20, self.WIDTH - 20, self.HEIGHT - 30))
        pygame.draw.ellipse(surf, (140, 130, 128), (12, 0, 24, 20))
        pygame.draw.circle(surf, (255, 32, 32), (18, 8), 3)
        pygame.draw.circle(surf, (255, 32, 32), (30, 8), 3)
        pygame.draw.rect(surf, C_BONE, (18, 18, 12, 6))
        return surf

    def _make_p2_surface(self):
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, (20, 0, 40),
                         (2, 6, self.WIDTH - 4, self.HEIGHT - 6), border_radius=6)
        pygame.draw.rect(surf, C_BLOOD_HIGH,
                         (8, 20, self.WIDTH - 16, self.HEIGHT - 30))
        pygame.draw.ellipse(surf, (120, 110, 110), (10, 0, 28, 22))
        pygame.draw.circle(surf, (255, 48, 48), (17, 9), 4)
        pygame.draw.circle(surf, (255, 48, 48), (31, 9), 4)
        pygame.draw.rect(surf, C_BONE, (16, 20, 16, 6))
        pygame.draw.line(surf, (60, 20, 20), (14, 4), (20, 14), 1)
        pygame.draw.line(surf, (60, 20, 20), (30, 2), (34, 12), 1)
        return surf
