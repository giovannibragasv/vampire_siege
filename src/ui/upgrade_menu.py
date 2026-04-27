from pathlib import Path
import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, C_VOID, C_BONE, C_GOLD, C_BLOOD_HIGH, C_DARK_PURPLE

_UI_SPRITES = Path(__file__).resolve().parents[2] / "assets" / "sprites" / "ui"


class UpgradeMenu:
    CARD_W = 200
    CARD_H = 260
    PADDING = 40

    def __init__(self, upgrades: list[dict]):
        self.upgrades = upgrades
        self._hovered = -1
        self._font_title = pygame.font.SysFont("serif", 18, bold=True)
        self._font_desc  = pygame.font.SysFont("serif", 15)
        self._font_hint  = pygame.font.SysFont("serif", 14)
        self._font_head  = pygame.font.SysFont("serif", 32, bold=True)
        self._cards: list[pygame.Rect] = []
        self._card_frame = self._load_card_frame()
        self._build_cards()

    def _build_cards(self):
        n     = len(self.upgrades)
        total = n * self.CARD_W + (n - 1) * self.PADDING
        start = (SCREEN_WIDTH - total) // 2
        cy    = SCREEN_HEIGHT // 2 - self.CARD_H // 2
        self._cards = [
            pygame.Rect(start + i * (self.CARD_W + self.PADDING), cy,
                        self.CARD_W, self.CARD_H)
            for i in range(n)
        ]

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            self._hovered = next(
                (i for i, r in enumerate(self._cards) if r.collidepoint(mx, my)), -1
            )
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for i, r in enumerate(self._cards):
                if r.collidepoint(mx, my):
                    return self.upgrades[i]["id"]
        return None

    def draw(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        head = self._render_text(self._font_head, "CHOOSE AN UPGRADE", C_GOLD)
        surface.blit(head, head.get_rect(centerx=SCREEN_WIDTH // 2, y=80))

        for i, (upg, rect) in enumerate(zip(self.upgrades, self._cards)):
            border_color = C_GOLD if i == self._hovered else C_BONE
            bg_color = (30, 10, 50) if i == self._hovered else C_DARK_PURPLE

            if self._card_frame:
                card = pygame.transform.scale(self._card_frame, rect.size)
                surface.blit(card, rect)
                if i == self._hovered:
                    glow = pygame.Surface(rect.size, pygame.SRCALPHA)
                    pygame.draw.rect(glow, (*C_GOLD, 70), glow.get_rect(), 3, border_radius=8)
                    surface.blit(glow, rect)
            else:
                pygame.draw.rect(surface, bg_color, rect, border_radius=8)
                pygame.draw.rect(surface, border_color, rect, 2, border_radius=8)

            title_zone = pygame.Rect(rect.left + 24, rect.top + 42, rect.width - 48, 50)
            desc_zone = pygame.Rect(rect.left + 24, rect.top + 112, rect.width - 48, 92)
            self._draw_centered_lines(
                surface,
                self._wrap_text(upg["name"], self._font_title, title_zone.width),
                self._font_title,
                C_GOLD,
                title_zone,
                20,
            )
            self._draw_centered_lines(
                surface,
                self._wrap_text(upg["desc"], self._font_desc, desc_zone.width),
                self._font_desc,
                C_BONE,
                desc_zone,
                22,
            )

            hint = self._render_text(self._font_hint, "click to select", (150, 130, 165))
            surface.blit(hint, hint.get_rect(centerx=rect.centerx, bottom=rect.bottom - 38))

    def _draw_centered_lines(self, surface, lines, font, color, zone, line_h):
        old_clip = surface.get_clip()
        surface.set_clip(zone)
        total_h = min(len(lines) * line_h, zone.height)
        y = zone.top + max(0, (zone.height - total_h) // 2)
        max_lines = max(1, zone.height // line_h)
        for text in lines[:max_lines]:
            rendered = self._render_text(font, text, color)
            surface.blit(rendered, rendered.get_rect(centerx=zone.centerx, y=y))
            y += line_h
        surface.set_clip(old_clip)

    def _render_text(self, font, text, color):
        return font.render(text, True, color).convert_alpha()

    def _wrap_text(self, text, font, max_width):
        words = text.split()
        lines, line = [], []
        for word in words:
            test = " ".join(line + [word])
            if not line or font.size(test)[0] <= max_width:
                line.append(word)
            else:
                lines.append(" ".join(line))
                line = [word]
        if line:
            lines.append(" ".join(line))
        return lines

    def _load_card_frame(self):
        try:
            return pygame.image.load((_UI_SPRITES / "upgrade_card.png").as_posix()).convert_alpha()
        except (FileNotFoundError, pygame.error):
            return None
