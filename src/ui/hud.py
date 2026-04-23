import pygame
from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, ARENA_WIDTH, ARENA_HEIGHT,
    HOLY_WATER_MAX, SHOTGUN_MAGAZINE,
    C_BONE, C_BLOOD_HIGH, C_GOLD, C_SILVER, C_HOLY_BLUE, C_DARK_PURPLE,
)


class HUD:
    PORTRAIT_SIZE = 72

    def __init__(self, player, wave_manager=None):
        self.player       = player
        self._wave_manager = wave_manager
        self._font       = pygame.font.SysFont("serif", 18, bold=True)
        self._font_small = pygame.font.SysFont("serif", 14)
        self._portraits  = self._build_portraits()

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def draw(self, surface):
        self._draw_hp_bar(surface)
        self._draw_shotgun_counter(surface)
        self._draw_water_charges(surface)
        self._draw_weapon_indicator(surface)
        self._draw_portrait(surface)
        if self._wave_manager:
            self._draw_wave_info(surface)
            self._draw_minimap(surface)

    # ------------------------------------------------------------------
    # HP bar
    # ------------------------------------------------------------------

    def _draw_hp_bar(self, surface):
        p = self.player
        bx, by, bw, bh = 20, 20, 220, 16
        filled = int(bw * max(0, p.hp) / p.max_hp)

        pygame.draw.rect(surface, (20, 0, 0),   (bx, by, bw, bh), border_radius=4)
        pygame.draw.rect(surface, C_BLOOD_HIGH, (bx, by, filled, bh), border_radius=4)
        pygame.draw.rect(surface, C_BONE,       (bx, by, bw, bh), 2, border_radius=4)

        label = self._font.render(f"{p.hp}/{p.max_hp}", True, C_BONE)
        surface.blit(label, (bx + 4, by))

    # ------------------------------------------------------------------
    # Shotgun ammo counter
    # ------------------------------------------------------------------

    def _draw_shotgun_counter(self, surface):
        sg = self.player.shotgun
        ox, oy = 20, 44
        icon_w, icon_h = 10, 18
        gap = 4

        for i in range(SHOTGUN_MAGAZINE):
            x = ox + i * (icon_w + gap)
            if sg.reloading:
                color = (60, 60, 80)
            elif i < sg.ammo:
                color = C_SILVER
            else:
                color = (50, 40, 55)
            # Bullet shape: rectangle with rounded top
            pygame.draw.rect(surface, color, (x, oy, icon_w, icon_h), border_radius=3)
            if not sg.reloading and i < sg.ammo:
                # Shine
                pygame.draw.rect(surface, C_BONE, (x + 2, oy + 2, 2, 5))

        # Reload bar below the bullets
        if sg.reloading:
            bar_w = SHOTGUN_MAGAZINE * (icon_w + gap) - gap
            bar_h = 4
            bar_y = oy + icon_h + 3
            pygame.draw.rect(surface, (30, 20, 40), (ox, bar_y, bar_w, bar_h), border_radius=2)
            filled = int(bar_w * sg.reload_progress)
            pygame.draw.rect(surface, C_GOLD, (ox, bar_y, filled, bar_h), border_radius=2)
            lbl = self._font_small.render("RELOADING", True, C_GOLD)
            surface.blit(lbl, (ox, bar_y + 6))

    # ------------------------------------------------------------------
    # Holy water charges
    # ------------------------------------------------------------------

    def _draw_water_charges(self, surface):
        charges = self.player.holy_water.charges
        ox, oy  = 20, 72
        vial_w, vial_h = 12, 20
        gap = 6

        for i in range(HOLY_WATER_MAX):
            x = ox + i * (vial_w + gap)
            if i < charges:
                body_color  = C_HOLY_BLUE
                inner_color = (176, 200, 255)
            else:
                body_color  = (30, 30, 50)
                inner_color = (50, 50, 70)

            # Vial body
            pygame.draw.rect(surface, body_color, (x, oy + 4, vial_w, vial_h - 4), border_radius=3)
            # Vial neck/cork
            pygame.draw.rect(surface, (92, 51, 23), (x + 3, oy, vial_w - 6, 5), border_radius=2)
            # Shine
            if i < charges:
                pygame.draw.rect(surface, inner_color, (x + 2, oy + 6, 3, 6))

    # ------------------------------------------------------------------
    # Active weapon label
    # ------------------------------------------------------------------

    def _draw_weapon_indicator(self, surface):
        w   = self.player._active_weapon
        txt = "[1] Shotgun" if w == "shotgun" else "[2] Holy Water"
        col = C_SILVER if w == "shotgun" else C_HOLY_BLUE
        lbl = self._font.render(txt, True, col)
        surface.blit(lbl, (20, 100))

        # Stake indicator (right-click, always available)
        stake = self.player.stake
        ready_col = (210, 170, 70)
        cd_col    = (110, 85, 35)
        stk_lbl = self._font_small.render("[RMB] Stake", True,
                                          ready_col if stake.ready else cd_col)
        surface.blit(stk_lbl, (20, 120))
        if not stake.ready:
            bar_w = 80
            pygame.draw.rect(surface, (40, 30, 15), (20, 134, bar_w, 4))
            pygame.draw.rect(surface, (200, 160, 50),
                             (20, 134, int(bar_w * stake.cooldown_frac), 4))

    # ------------------------------------------------------------------
    # Face portrait
    # ------------------------------------------------------------------

    def _draw_portrait(self, surface):
        p     = self.player
        ratio = p.hp / p.max_hp

        if ratio >= 0.75:
            stage = 0
        elif ratio >= 0.30:
            stage = 1
        else:
            stage = 2

        portrait = self._portraits[stage]
        px = SCREEN_WIDTH  // 2 - self.PORTRAIT_SIZE // 2
        py = SCREEN_HEIGHT - self.PORTRAIT_SIZE - 10
        surface.blit(portrait, (px, py))

        # Frame border
        border_color = [C_GOLD, C_BLOOD_HIGH, (220, 50, 50)][stage]
        pygame.draw.rect(surface, border_color,
                         (px, py, self.PORTRAIT_SIZE, self.PORTRAIT_SIZE), 2, border_radius=4)

    # ------------------------------------------------------------------
    # Wave info panel (top-right)
    # ------------------------------------------------------------------

    def _draw_wave_info(self, surface):
        wm  = self._wave_manager
        from src.settings import WAVE_DEFINITIONS, SCREEN_WIDTH

        # Wave label
        if wm.wave_index is None:
            wave_label = "INFINITE"
        else:
            total = len(WAVE_DEFINITIONS)
            wave_label = f"WAVE {wm.wave_index + 1}/{total}"

        # Elapsed time MM:SS
        secs  = wm.wave_time_ms // 1000
        mm, ss = divmod(secs, 60)
        time_label = f"{mm:02d}:{ss:02d}"

        remaining = wm.enemies_remaining()
        kill_label = f"Kills: {wm.kills}   Score: {wm.score}"

        x = SCREEN_WIDTH - 200
        y = 20
        for text, color in [
            (wave_label,          C_GOLD),
            (time_label,          C_BONE),
            (f"Left: {remaining}", C_BONE),
            (kill_label,          C_GOLD),
        ]:
            lbl = self._font.render(text, True, color)
            surface.blit(lbl, (x, y))
            y += 22

    # ------------------------------------------------------------------
    # Mini-map (bottom-right corner)
    # ------------------------------------------------------------------

    _MAP_W = 160
    _MAP_H = 90
    _MAP_PAD = 10

    def _draw_minimap(self, surface):
        wm    = self._wave_manager
        arena = wm.arena
        mw, mh = self._MAP_W, self._MAP_H
        ox = SCREEN_WIDTH  - mw - self._MAP_PAD
        oy = SCREEN_HEIGHT - mh - self._MAP_PAD

        def ws(wx, wy):
            """World → minimap screen coords."""
            return ox + int(wx * mw / ARENA_WIDTH), oy + int(wy * mh / ARENA_HEIGHT)

        # Background panel
        bg = pygame.Surface((mw, mh), pygame.SRCALPHA)
        bg.fill((10, 0, 20, 180))
        surface.blit(bg, (ox, oy))

        # Inner arena tint
        inner_scale_x = (ARENA_WIDTH  - 64) * mw / ARENA_WIDTH
        inner_scale_y = (ARENA_HEIGHT - 64) * mh / ARENA_HEIGHT
        pygame.draw.rect(surface, (30, 10, 50),
                         (ox + int(32 * mw / ARENA_WIDTH),
                          oy + int(32 * mh / ARENA_HEIGHT),
                          int(inner_scale_x), int(inner_scale_y)))

        # Tombstones — grey dots
        for t in arena.tombstones:
            sx, sy = ws(*t.rect.center)
            pygame.draw.rect(surface, (90, 90, 100), (sx - 1, sy - 1, 3, 3))

        # Fountains — blue dots
        for f in arena.fountains:
            sx, sy = ws(*f.rect.center)
            pygame.draw.circle(surface, C_HOLY_BLUE, (sx, sy), 3)

        # Enemies
        for e in wm.enemies:
            sx, sy = ws(*e.rect.center)
            if hasattr(e, '_phase'):  # Dracula
                pygame.draw.circle(surface, C_GOLD, (sx, sy), 4)
            else:
                pygame.draw.circle(surface, C_BLOOD_HIGH, (sx, sy), 2)

        # Player — white dot with crosshair mark
        px, py = ws(*self.player.rect.center)
        pygame.draw.circle(surface, (255, 255, 255), (px, py), 3)
        pygame.draw.line(surface, (255, 255, 255), (px - 5, py), (px + 5, py), 1)
        pygame.draw.line(surface, (255, 255, 255), (px, py - 5), (px, py + 5), 1)

        # Border
        pygame.draw.rect(surface, C_GOLD, (ox, oy, mw, mh), 1)

    def _build_portraits(self):
        """Build three placeholder face portraits for the three HP stages."""
        s = self.PORTRAIT_SIZE
        portraits = []

        # Stage 0 — healthy
        surf = pygame.Surface((s, s), pygame.SRCALPHA)
        pygame.draw.rect(surf, C_DARK_PURPLE, (0, 0, s, s), border_radius=6)
        # Face
        pygame.draw.ellipse(surf, (200, 150, 120), (14, 10, s - 28, s - 20))
        # Hair
        pygame.draw.rect(surf, (139, 58, 26), (14, 10, s - 28, 16))
        # Eyes — open, determined
        pygame.draw.ellipse(surf, (60, 40, 20), (22, 28, 10, 8))
        pygame.draw.ellipse(surf, (60, 40, 20), (40, 28, 10, 8))
        pygame.draw.circle(surf, (20, 10, 5),   (27, 32), 3)
        pygame.draw.circle(surf, (20, 10, 5),   (45, 32), 3)
        # Glints
        pygame.draw.circle(surf, C_BONE, (25, 30), 1)
        pygame.draw.circle(surf, C_BONE, (43, 30), 1)
        # Mouth — confident smirk
        pygame.draw.arc(surf, (140, 80, 60),
                        pygame.Rect(26, 44, 20, 10), 3.6, 5.8, 2)
        portraits.append(surf)

        # Stage 1 — damaged
        surf = pygame.Surface((s, s), pygame.SRCALPHA)
        pygame.draw.rect(surf, C_DARK_PURPLE, (0, 0, s, s), border_radius=6)
        pygame.draw.ellipse(surf, (180, 130, 100), (14, 10, s - 28, s - 20))
        pygame.draw.rect(surf, (100, 40, 20), (14, 10, s - 28, 16))
        # Eyes — narrowed, worried
        pygame.draw.ellipse(surf, (60, 40, 20), (22, 30, 10, 6))
        pygame.draw.ellipse(surf, (60, 40, 20), (40, 30, 10, 6))
        pygame.draw.circle(surf, (20, 10, 5),   (27, 33), 3)
        pygame.draw.circle(surf, (20, 10, 5),   (45, 33), 3)
        # Sweat drop
        pygame.draw.ellipse(surf, (120, 180, 220), (50, 22, 5, 8))
        # Mouth — tense frown
        pygame.draw.arc(surf, (140, 80, 60),
                        pygame.Rect(26, 46, 20, 10), 0.0, 3.14, 2)
        # Small scratch mark
        pygame.draw.line(surf, C_BLOOD_HIGH, (34, 20), (38, 28), 1)
        portraits.append(surf)

        # Stage 2 — critical
        surf = pygame.Surface((s, s), pygame.SRCALPHA)
        pygame.draw.rect(surf, (30, 0, 0), (0, 0, s, s), border_radius=6)
        pygame.draw.ellipse(surf, (150, 110, 90), (14, 10, s - 28, s - 20))
        pygame.draw.rect(surf, (80, 30, 10), (14, 10, s - 28, 16))
        # Eyes — barely open, desperate
        pygame.draw.ellipse(surf, (60, 40, 20), (22, 31, 10, 4))
        pygame.draw.ellipse(surf, (60, 40, 20), (40, 31, 10, 4))
        pygame.draw.circle(surf, (20, 10, 5),   (27, 33), 2)
        pygame.draw.circle(surf, (20, 10, 5),   (45, 33), 2)
        # Blood streaks
        pygame.draw.line(surf, C_BLOOD_HIGH, (30, 16), (34, 30), 2)
        pygame.draw.line(surf, C_BLOOD_HIGH, (46, 14), (44, 28), 1)
        # Mouth — grimace
        pygame.draw.line(surf, (120, 60, 40), (28, 50), (44, 48), 2)
        pygame.draw.line(surf, (120, 60, 40), (28, 50), (26, 46), 1)
        pygame.draw.line(surf, (120, 60, 40), (44, 48), (46, 44), 1)
        portraits.append(surf)

        return portraits
