import math
import pygame
from src.settings import CONTACT_DAMAGE_COOLDOWN_MS
from src.entities.damage_number import DamageNumber


class Enemy:
    """Base class for all enemies."""

    WIDTH  = 32
    HEIGHT = 48

    def __init__(self, cx, cy, hp, speed, damage, color):
        self.rect   = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.rect.center = (cx, cy)
        self.hp     = hp
        self.max_hp = hp
        self.speed  = speed
        self.damage = damage
        self._color = color
        self.alive  = True
        self._hit_timer    = 0
        self._contact_cooldown = 0
        self._facing_right = True
        self._kbx = 0.0  # knockback velocity x
        self._kby = 0.0  # knockback velocity y
        self._damage_numbers: list[DamageNumber] = []
        self._surface = self._make_surface()

    # ------------------------------------------------------------------

    def take_damage(self, amount, kbx=0.0, kby=0.0):
        self.hp -= amount
        self._hit_timer = 250
        self._kbx = kbx
        self._kby = kby
        self._damage_numbers.append(DamageNumber(*self.rect.center, amount))
        if self.hp <= 0:
            self.alive = False

    def _move_toward(self, tx, ty, dt, tombstones=None):
        dx, dy = tx - self.rect.centerx, ty - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist == 0:
            return

        # Attraction toward target (normalized)
        ax, ay = dx / dist, dy / dist

        # Repulsion from nearby tombstones (potential field)
        rx, ry = 0.0, 0.0
        if tombstones:
            AVOID_R = 80
            for t in tombstones:
                tdx = self.rect.centerx - t.rect.centerx
                tdy = self.rect.centery - t.rect.centery
                tdist = math.hypot(tdx, tdy) or 1
                if tdist < AVOID_R:
                    s = (AVOID_R - tdist) / AVOID_R
                    rx += (tdx / tdist) * s * 2.5
                    ry += (tdy / tdist) * s * 2.5

        fx, fy = ax + rx, ay + ry
        fmag = math.hypot(fx, fy) or 1
        fx, fy = fx / fmag, fy / fmag

        self.rect.x += int(fx * self.speed * dt / 16)
        self.rect.y += int(fy * self.speed * dt / 16)
        self._facing_right = fx >= 0

    def try_damage_player(self, player, dt):
        self._contact_cooldown = max(0, self._contact_cooldown - dt)
        if self._contact_cooldown > 0:
            return
        if self.rect.colliderect(player.rect):
            player.take_damage(self.damage)
            self._contact_cooldown = CONTACT_DAMAGE_COOLDOWN_MS

    def update(self, dt, player, arena):
        px, py = player.rect.center
        self._move_toward(px, py, dt, arena.tombstones)

        # Apply and decay knockback
        if abs(self._kbx) > 0.1 or abs(self._kby) > 0.1:
            self.rect.x += int(self._kbx * dt / 16)
            self.rect.y += int(self._kby * dt / 16)
            decay = 0.78 ** (dt / 16)
            self._kbx *= decay
            self._kby *= decay

        arena.clamp_entity(self.rect)
        arena.push_out_tombstones(self.rect)
        self.try_damage_player(player, dt)
        self._hit_timer = max(0, self._hit_timer - dt)
        for dn in self._damage_numbers:
            dn.update(dt)
        self._damage_numbers = [dn for dn in self._damage_numbers if dn.alive]

    def draw(self, surface):
        img = self._surface.copy()
        if self._hit_timer > 0:
            img.fill((255, 60, 60, 120), special_flags=pygame.BLEND_RGBA_ADD)
        if not self._facing_right:
            img = pygame.transform.flip(img, True, False)
        surface.blit(img, self.rect)
        self._draw_hp_bar(surface)
        for dn in self._damage_numbers:
            dn.draw(surface)

    def _draw_hp_bar(self, surface):
        bar_w = self.WIDTH
        bar_h = 4
        x = self.rect.left
        y = self.rect.top - 6
        pygame.draw.rect(surface, (40, 0, 0),   (x, y, bar_w, bar_h))
        filled = int(bar_w * max(0, self.hp) / self.max_hp)
        pygame.draw.rect(surface, (180, 0, 0),  (x, y, filled, bar_h))

    def _make_surface(self):
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, self._color,
                         (4, 8, self.WIDTH - 8, self.HEIGHT - 8), border_radius=4)
        pygame.draw.ellipse(surf, (180, 160, 155), (8, 0, 16, 14))
        return surf
