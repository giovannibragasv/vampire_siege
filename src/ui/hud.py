import pygame
from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    HOLY_WATER_MAX, C_BONE, C_BLOOD_MID, C_BLOOD_HIGH, C_GOLD, C_HOLY_BLUE,
)


class HUD:
    def __init__(self, player):
        self.player = player
        self._font = pygame.font.SysFont("serif", 20, bold=True)

    def draw(self, surface):
        self._draw_hp_bar(surface)
        self._draw_water_charges(surface)
        self._draw_weapon_indicator(surface)

    def _draw_hp_bar(self, surface):
        p = self.player
        bar_x, bar_y = 20, 20
        bar_w, bar_h = 200, 16
        filled = int(bar_w * max(0, p.hp) / p.max_hp)

        pygame.draw.rect(surface, (20, 0, 0),    (bar_x, bar_y, bar_w, bar_h), border_radius=4)
        pygame.draw.rect(surface, C_BLOOD_HIGH,  (bar_x, bar_y, filled, bar_h), border_radius=4)
        pygame.draw.rect(surface, C_BONE,        (bar_x, bar_y, bar_w, bar_h), 2, border_radius=4)

        label = self._font.render(f"{p.hp}/{p.max_hp}", True, C_BONE)
        surface.blit(label, (bar_x + 4, bar_y))

    def _draw_water_charges(self, surface):
        charges = self.player.holy_water.charges
        for i in range(HOLY_WATER_MAX):
            x = 20 + i * 22
            y = 44
            color = C_HOLY_BLUE if i < charges else (40, 40, 60)
            pygame.draw.rect(surface, color, (x, y, 16, 20), border_radius=3)
            pygame.draw.rect(surface, C_BONE, (x, y, 16, 20), 1, border_radius=3)

    def _draw_weapon_indicator(self, surface):
        w = self.player._active_weapon
        label_text = "[1] Shotgun" if w == "shotgun" else "[2] Holy Water"
        label = self._font.render(label_text, True, C_GOLD)
        surface.blit(label, (20, 72))
