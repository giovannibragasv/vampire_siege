import math
import pygame
from src.settings import HEAL_PICKUP_AMOUNT, HEAL_PICKUP_RESPAWN_MS, C_BLOOD_HIGH, C_BONE


class HealPickup:
    SIZE = 22

    def __init__(self, cx, cy):
        self.rect = pygame.Rect(0, 0, self.SIZE, self.SIZE)
        self.rect.center = (cx, cy)
        self.available = True
        self._respawn_timer = 0
        self._pulse = 0.0

    def try_collect(self, player):
        if not self.available:
            return False
        if self.rect.colliderect(player.rect):
            player.hp = min(player.max_hp, player.hp + HEAL_PICKUP_AMOUNT)
            self.available = False
            self._respawn_timer = 0
            return True
        return False

    def update(self, dt):
        self._pulse = (self._pulse + dt * 0.004) % (2 * math.pi)
        if not self.available:
            self._respawn_timer += dt
            if self._respawn_timer >= HEAL_PICKUP_RESPAWN_MS:
                self.available = True

    def draw(self, surface):
        if not self.available:
            return
        scale = 1.0 + math.sin(self._pulse) * 0.12
        s = int(self.SIZE * scale)
        r = pygame.Rect(0, 0, s, s)
        r.center = self.rect.center
        cx, cy = r.center

        # Glow halo
        halo = pygame.Surface((s + 16, s + 16), pygame.SRCALPHA)
        alpha = int(60 + math.sin(self._pulse) * 40)
        pygame.draw.ellipse(halo, (*C_BLOOD_HIGH, alpha),
                            (0, 0, s + 16, s + 16))
        surface.blit(halo, (cx - (s + 16) // 2, cy - (s + 16) // 2))

        # Chalice body
        pygame.draw.rect(surface, (100, 10, 10), r, border_radius=4)
        # Cross symbol
        pygame.draw.rect(surface, C_BLOOD_HIGH,
                         (cx - 2, r.top + 3, 4, s - 6))
        pygame.draw.rect(surface, C_BLOOD_HIGH,
                         (r.left + 3, cy - 2, s - 6, 4))
        # Inner shine
        pygame.draw.rect(surface, C_BONE, (cx - 1, r.top + 4, 2, 4))
