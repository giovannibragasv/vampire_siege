import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, C_VOID, C_BONE, C_GOLD, C_BLOOD_HIGH, C_DARK_PURPLE


class UpgradeMenu:
    CARD_W = 200
    CARD_H = 260
    PADDING = 40

    def __init__(self, upgrades: list[dict]):
        self.upgrades = upgrades
        self._hovered = -1
        self._font_title = pygame.font.SysFont("serif", 22, bold=True)
        self._font_desc  = pygame.font.SysFont("serif", 16)
        self._font_head  = pygame.font.SysFont("serif", 32, bold=True)
        self._cards: list[pygame.Rect] = []
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

        head = self._font_head.render("CHOOSE AN UPGRADE", True, C_GOLD)
        surface.blit(head, head.get_rect(centerx=SCREEN_WIDTH // 2, y=80))

        for i, (upg, rect) in enumerate(zip(self.upgrades, self._cards)):
            border_color = C_GOLD if i == self._hovered else C_BONE
            bg_color = (30, 10, 50) if i == self._hovered else C_DARK_PURPLE

            pygame.draw.rect(surface, bg_color, rect, border_radius=8)
            pygame.draw.rect(surface, border_color, rect, 2, border_radius=8)

            name  = self._font_title.render(upg["name"], True, C_GOLD)
            surface.blit(name, name.get_rect(centerx=rect.centerx, y=rect.top + 16))

            # Word-wrap description
            words  = upg["desc"].split()
            lines, line = [], []
            for w in words:
                test = " ".join(line + [w])
                if self._font_desc.size(test)[0] < self.CARD_W - 24:
                    line.append(w)
                else:
                    lines.append(" ".join(line))
                    line = [w]
            if line:
                lines.append(" ".join(line))

            for j, text in enumerate(lines):
                rendered = self._font_desc.render(text, True, C_BONE)
                surface.blit(rendered,
                             rendered.get_rect(centerx=rect.centerx,
                                               y=rect.top + 60 + j * 22))

            hint = self._font_desc.render("click to select", True, (120, 100, 140))
            surface.blit(hint, hint.get_rect(centerx=rect.centerx, bottom=rect.bottom - 12))
