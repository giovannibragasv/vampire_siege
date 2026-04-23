import pygame
from src.settings import (
    DRACULA_HP, DRACULA_SPEED, DRACULA_DAMAGE,
    DRACULA_P2_HP_BONUS, DRACULA_P2_SCALE, DRACULA_P2_SPEED,
    C_BLOOD_MID, C_BLOOD_HIGH, C_BONE,
)
from src.transforms.matrices import scale_surface
from src.entities.enemy import Enemy


class Dracula(Enemy):
    """
    Boss with two phases.
    Phase 2 triggered at 50% HP: full HP restored + bonus, speed increases,
    sprite scaled 1.5× via scale_surface() (scale matrix).
    """

    WIDTH  = 48
    HEIGHT = 64

    COLOR_P1 = (5,  0, 20)
    COLOR_P2 = (20, 0, 40)

    def __init__(self, cx, cy):
        super().__init__(cx, cy, DRACULA_HP, DRACULA_SPEED, DRACULA_DAMAGE, self.COLOR_P1)
        self.rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.rect.center = (cx, cy)
        self._phase = 1
        self._surface = self._make_p1_surface()
        self._p2_triggered = False

    # ------------------------------------------------------------------

    def take_damage(self, amount):
        self.hp -= amount
        self._hit_timer = 120
        if self._phase == 1 and not self._p2_triggered:
            if self.hp <= self.max_hp * 0.5:
                self._enter_phase2()
                return
        if self.hp <= 0:
            self.alive = False

    def _enter_phase2(self):
        self._phase = 2
        self._p2_triggered = True
        bonus_hp = DRACULA_P2_HP_BONUS
        self.max_hp += bonus_hp
        self.hp = self.max_hp
        self.speed = DRACULA_P2_SPEED
        self.damage = int(self.damage * 1.3)
        self._surface = self._make_p2_surface()
        # Scale the hitbox to match the visual growth
        cx, cy = self.rect.center
        self.WIDTH  = int(48 * DRACULA_P2_SCALE)
        self.HEIGHT = int(64 * DRACULA_P2_SCALE)
        self.rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.rect.center = (cx, cy)

    # ------------------------------------------------------------------

    def draw(self, surface):
        img = self._surface.copy()
        if self._hit_timer > 0:
            img.fill((255, 60, 60, 120), special_flags=pygame.BLEND_RGBA_ADD)
        if not self._facing_right:
            img = pygame.transform.flip(img, True, False)
        # Scale transform applied at draw time for phase 2
        if self._phase == 2:
            img = scale_surface(img, DRACULA_P2_SCALE, DRACULA_P2_SCALE)
        draw_rect = img.get_rect(center=self.rect.center)
        surface.blit(img, draw_rect)
        self._draw_hp_bar(surface)

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

    def _make_p1_surface(self):
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        # Cape
        pygame.draw.rect(surf, (5, 0, 20),
                         (2, 6, self.WIDTH - 4, self.HEIGHT - 6), border_radius=6)
        # Crimson lining glimpse
        pygame.draw.rect(surf, C_BLOOD_MID,
                         (10, 20, self.WIDTH - 20, self.HEIGHT - 30))
        # Head
        pygame.draw.ellipse(surf, (140, 130, 128), (12, 0, 24, 20))
        # Eyes
        pygame.draw.circle(surf, (255, 32, 32), (18, 8), 3)
        pygame.draw.circle(surf, (255, 32, 32), (30, 8), 3)
        # Ascot
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
        # Cracks
        pygame.draw.line(surf, (60, 20, 20), (14, 4), (20, 14), 1)
        pygame.draw.line(surf, (60, 20, 20), (30, 2), (34, 12), 1)
        return surf
