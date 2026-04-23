import math
import pygame
from src.settings import CONTACT_DAMAGE_COOLDOWN_MS


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
        self._surface = self._make_surface()

    # ------------------------------------------------------------------

    def take_damage(self, amount):
        self.hp -= amount
        self._hit_timer = 120
        if self.hp <= 0:
            self.alive = False

    def _move_toward(self, tx, ty, dt):
        dx, dy = tx - self.rect.centerx, ty - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.rect.x += int((dx / dist) * self.speed * dt / 16)
            self.rect.y += int((dy / dist) * self.speed * dt / 16)
        self._facing_right = dx >= 0

    def try_damage_player(self, player, dt):
        self._contact_cooldown = max(0, self._contact_cooldown - dt)
        if self._contact_cooldown > 0:
            return
        if self.rect.colliderect(player.rect):
            player.take_damage(self.damage)
            self._contact_cooldown = CONTACT_DAMAGE_COOLDOWN_MS

    def update(self, dt, player, arena):
        px, py = player.rect.center
        self._move_toward(px, py, dt)
        arena.clamp_entity(self.rect)
        arena.push_out_tombstones(self.rect)
        self.try_damage_player(player, dt)
        self._hit_timer = max(0, self._hit_timer - dt)

    def draw(self, surface):
        img = self._surface.copy()
        if self._hit_timer > 0:
            img.fill((255, 60, 60, 120), special_flags=pygame.BLEND_RGBA_ADD)
        if not self._facing_right:
            img = pygame.transform.flip(img, True, False)
        surface.blit(img, self.rect)
        self._draw_hp_bar(surface)

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
