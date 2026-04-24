import pygame
from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, ARENA_WIDTH, ARENA_HEIGHT,
    HOLY_WATER_MAX, SHOTGUN_MAGAZINE,
    C_BONE, C_BLOOD_HIGH, C_GOLD, C_SILVER, C_HOLY_BLUE, C_DARK_PURPLE,
)

# Panel anchor: portrait sits at (PAD, SCREEN_HEIGHT - PORTRAIT_SIZE - PAD)
_PAD           = 8
_GUN_W         = 50
_GUN_H         = 46
_AMMO_ICON_W   = 10
_AMMO_ICON_H   = 18
_AMMO_GAP      = 4
_VIAL_W        = 12
_VIAL_H        = 20
_VIAL_GAP      = 5


class HUD:
    PORTRAIT_SIZE = 72

    def __init__(self, player, wave_manager=None):
        self.player        = player
        self._wave_manager = wave_manager
        self._font         = pygame.font.SysFont("serif", 18, bold=True)
        self._font_small   = pygame.font.SysFont("serif", 14)
        self._portraits    = self._build_portraits()
        self._gun_surf     = self._build_gun_surf()

    # ------------------------------------------------------------------
    # Anchors (computed once for readability)
    # ------------------------------------------------------------------

    def _anchors(self):
        px = _PAD
        py = SCREEN_HEIGHT - self.PORTRAIT_SIZE - _PAD   # portrait top-left
        gx = px + self.PORTRAIT_SIZE + _PAD              # gun / ammo column x
        ammo_y = py                                       # ammo row aligned with portrait top
        gun_y  = ammo_y + _AMMO_ICON_H + 4
        water_x = gx + _GUN_W + _PAD
        water_y = gun_y + (_GUN_H - _VIAL_H) // 2       # vertically centre water with gun
        hp_y   = py - 18                                  # hp bar just above portrait
        indicator_y = py - 56                             # weapon label
        stake_y     = py - 38                             # stake label + bar
        return dict(
            px=px, py=py,
            gx=gx, ammo_y=ammo_y, gun_y=gun_y,
            water_x=water_x, water_y=water_y,
            hp_y=hp_y, indicator_y=indicator_y, stake_y=stake_y,
        )

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def draw(self, surface):
        a = self._anchors()
        self._draw_weapon_indicator(surface, a)
        self._draw_hp_bar(surface, a)
        self._draw_portrait(surface, a)
        self._draw_shotgun_counter(surface, a)
        self._draw_gun_sprite(surface, a)
        self._draw_water_charges(surface, a)
        if self._wave_manager:
            self._draw_wave_info(surface)
            self._draw_minimap(surface)

    # ------------------------------------------------------------------
    # Weapon indicator + stake (above portrait)
    # ------------------------------------------------------------------

    def _draw_weapon_indicator(self, surface, a):
        w   = self.player._active_weapon
        txt = "[1] Shotgun" if w == "shotgun" else "[2] Holy Water"
        col = C_SILVER if w == "shotgun" else C_HOLY_BLUE
        lbl = self._font.render(txt, True, col)
        surface.blit(lbl, (a["px"], a["indicator_y"]))

        stake     = self.player.stake
        ready_col = (210, 170, 70)
        cd_col    = (110, 85, 35)
        sy        = a["stake_y"]
        stk_lbl   = self._font_small.render("[RMB] Stake", True,
                                             ready_col if stake.ready else cd_col)
        surface.blit(stk_lbl, (a["px"], sy))
        if not stake.ready:
            bar_w = 80
            pygame.draw.rect(surface, (40, 30, 15),   (a["px"], sy + 14, bar_w, 4))
            pygame.draw.rect(surface, (200, 160, 50),
                             (a["px"], sy + 14, int(bar_w * stake.cooldown_frac), 4))

    # ------------------------------------------------------------------
    # HP bar (just above portrait)
    # ------------------------------------------------------------------

    def _draw_hp_bar(self, surface, a):
        p       = self.player
        bx, by  = a["px"], a["hp_y"]
        bw, bh  = 220, 14
        filled  = int(bw * max(0, p.hp) / p.max_hp)

        pygame.draw.rect(surface, (20, 0, 0),   (bx, by, bw, bh), border_radius=4)
        pygame.draw.rect(surface, C_BLOOD_HIGH, (bx, by, filled, bh), border_radius=4)
        pygame.draw.rect(surface, C_BONE,       (bx, by, bw, bh), 2, border_radius=4)
        label = self._font_small.render(f"{p.hp}/{p.max_hp}", True, C_BONE)
        surface.blit(label, (bx + 4, by))

    # ------------------------------------------------------------------
    # Portrait (bottom-left)
    # ------------------------------------------------------------------

    def _draw_portrait(self, surface, a):
        p     = self.player
        ratio = p.hp / p.max_hp
        if ratio >= 0.75:
            stage = 0
        elif ratio >= 0.30:
            stage = 1
        else:
            stage = 2

        portrait = self._portraits[stage]
        surface.blit(portrait, (a["px"], a["py"]))

        border_color = [C_GOLD, C_BLOOD_HIGH, (220, 50, 50)][stage]
        pygame.draw.rect(surface, border_color,
                         (a["px"], a["py"],
                          self.PORTRAIT_SIZE, self.PORTRAIT_SIZE), 2, border_radius=4)

    # ------------------------------------------------------------------
    # Ammo counter (above gun sprite)
    # ------------------------------------------------------------------

    def _draw_shotgun_counter(self, surface, a):
        sg     = self.player.shotgun
        ox, oy = a["gx"], a["ammo_y"]
        iw, ih = _AMMO_ICON_W, _AMMO_ICON_H

        for i in range(SHOTGUN_MAGAZINE):
            x = ox + i * (iw + _AMMO_GAP)
            if sg.reloading:
                color = (60, 60, 80)
            elif i < sg.ammo:
                color = C_SILVER
            else:
                color = (50, 40, 55)
            pygame.draw.rect(surface, color, (x, oy, iw, ih), border_radius=3)
            if not sg.reloading and i < sg.ammo:
                pygame.draw.rect(surface, C_BONE, (x + 2, oy + 2, 2, 5))

        if sg.reloading:
            bar_w = SHOTGUN_MAGAZINE * (iw + _AMMO_GAP) - _AMMO_GAP
            bar_y = oy + ih + 2
            pygame.draw.rect(surface, (30, 20, 40), (ox, bar_y, bar_w, 4), border_radius=2)
            filled = int(bar_w * sg.reload_progress)
            pygame.draw.rect(surface, C_GOLD, (ox, bar_y, filled, 4), border_radius=2)
            lbl = self._font_small.render("RELOAD", True, C_GOLD)
            surface.blit(lbl, (ox, bar_y + 6))

    # ------------------------------------------------------------------
    # Gun sprite (right of portrait, below ammo)
    # ------------------------------------------------------------------

    def _draw_gun_sprite(self, surface, a):
        surface.blit(self._gun_surf, (a["gx"], a["gun_y"]))

    # ------------------------------------------------------------------
    # Holy water charges (right of gun)
    # ------------------------------------------------------------------

    def _draw_water_charges(self, surface, a):
        charges = self.player.holy_water.charges
        ox, oy  = a["water_x"], a["water_y"]
        vw, vh  = _VIAL_W, _VIAL_H

        for i in range(HOLY_WATER_MAX):
            x = ox + i * (vw + _VIAL_GAP)
            if i < charges:
                body_color  = C_HOLY_BLUE
                inner_color = (176, 200, 255)
            else:
                body_color  = (30, 30, 50)
                inner_color = (50, 50, 70)

            pygame.draw.rect(surface, body_color, (x, oy + 4, vw, vh - 4), border_radius=3)
            pygame.draw.rect(surface, (92, 51, 23), (x + 3, oy, vw - 6, 5), border_radius=2)
            if i < charges:
                pygame.draw.rect(surface, inner_color, (x + 2, oy + 6, 3, 6))

    # ------------------------------------------------------------------
    # Wave info panel (top-right) — unchanged
    # ------------------------------------------------------------------

    def _draw_wave_info(self, surface):
        wm  = self._wave_manager
        from src.settings import WAVE_DEFINITIONS, SCREEN_WIDTH

        if wm.wave_index is None:
            wave_label = "INFINITE"
        else:
            total = len(WAVE_DEFINITIONS)
            wave_label = f"WAVE {wm.wave_index + 1}/{total}"

        secs       = wm.wave_time_ms // 1000
        mm, ss     = divmod(secs, 60)
        time_label = f"{mm:02d}:{ss:02d}"
        remaining  = wm.enemies_remaining()
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
    # Mini-map (bottom-right corner) — unchanged
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
            return ox + int(wx * mw / ARENA_WIDTH), oy + int(wy * mh / ARENA_HEIGHT)

        bg = pygame.Surface((mw, mh), pygame.SRCALPHA)
        bg.fill((10, 0, 20, 180))
        surface.blit(bg, (ox, oy))

        inner_scale_x = (ARENA_WIDTH  - 64) * mw / ARENA_WIDTH
        inner_scale_y = (ARENA_HEIGHT - 64) * mh / ARENA_HEIGHT
        pygame.draw.rect(surface, (30, 10, 50),
                         (ox + int(32 * mw / ARENA_WIDTH),
                          oy + int(32 * mh / ARENA_HEIGHT),
                          int(inner_scale_x), int(inner_scale_y)))

        for t in arena.tombstones:
            sx, sy = ws(*t.rect.center)
            pygame.draw.rect(surface, (90, 90, 100), (sx - 1, sy - 1, 3, 3))

        for f in arena.fountains:
            sx, sy = ws(*f.rect.center)
            pygame.draw.circle(surface, C_HOLY_BLUE, (sx, sy), 3)

        for e in wm.enemies:
            sx, sy = ws(*e.rect.center)
            if hasattr(e, '_phase'):
                pygame.draw.circle(surface, C_GOLD, (sx, sy), 4)
            else:
                pygame.draw.circle(surface, C_BLOOD_HIGH, (sx, sy), 2)

        px, py = ws(*self.player.rect.center)
        pygame.draw.circle(surface, (255, 255, 255), (px, py), 3)
        pygame.draw.line(surface, (255, 255, 255), (px - 5, py), (px + 5, py), 1)
        pygame.draw.line(surface, (255, 255, 255), (px, py - 5), (px, py + 5), 1)

        pygame.draw.rect(surface, C_GOLD, (ox, oy, mw, mh), 1)

    # ------------------------------------------------------------------
    # Asset builders
    # ------------------------------------------------------------------

    def _build_gun_surf(self):
        """Placeholder shotgun sprite — barrel + stock + guard."""
        w, h = _GUN_W, _GUN_H
        s = pygame.Surface((w, h), pygame.SRCALPHA)

        # Stock (brown, angled wedge)
        stock_pts = [(0, h - 8), (18, h - 4), (18, h), (0, h)]
        pygame.draw.polygon(s, (110, 65, 28), stock_pts)

        # Receiver body
        pygame.draw.rect(s, (80, 80, 90), (10, h // 2 - 5, 22, 14), border_radius=2)

        # Barrel (long, double-barrelled look)
        pygame.draw.rect(s, C_SILVER, (30, h // 2 - 6, w - 30, 5), border_radius=1)
        pygame.draw.rect(s, C_SILVER, (30, h // 2 + 1, w - 30, 5), border_radius=1)
        # Barrel highlight
        pygame.draw.rect(s, C_BONE,   (32, h // 2 - 5, w - 34, 2))
        pygame.draw.rect(s, C_BONE,   (32, h // 2 + 2, w - 34, 2))

        # Trigger guard (small circle outline)
        pygame.draw.circle(s, (60, 60, 70), (20, h // 2 + 8), 5, 1)

        # Muzzle cap
        pygame.draw.rect(s, (50, 50, 60), (w - 4, h // 2 - 7, 4, 14), border_radius=1)

        return s

    def _build_portraits(self):
        """Three face portraits for HP stages."""
        s = self.PORTRAIT_SIZE
        portraits = []

        # Stage 0 — healthy
        surf = pygame.Surface((s, s), pygame.SRCALPHA)
        pygame.draw.rect(surf, C_DARK_PURPLE, (0, 0, s, s), border_radius=6)
        pygame.draw.ellipse(surf, (200, 150, 120), (14, 10, s - 28, s - 20))
        pygame.draw.rect(surf, (139, 58, 26), (14, 10, s - 28, 16))
        pygame.draw.ellipse(surf, (60, 40, 20), (22, 28, 10, 8))
        pygame.draw.ellipse(surf, (60, 40, 20), (40, 28, 10, 8))
        pygame.draw.circle(surf, (20, 10, 5),   (27, 32), 3)
        pygame.draw.circle(surf, (20, 10, 5),   (45, 32), 3)
        pygame.draw.circle(surf, C_BONE, (25, 30), 1)
        pygame.draw.circle(surf, C_BONE, (43, 30), 1)
        pygame.draw.arc(surf, (140, 80, 60), pygame.Rect(26, 44, 20, 10), 3.6, 5.8, 2)
        portraits.append(surf)

        # Stage 1 — damaged
        surf = pygame.Surface((s, s), pygame.SRCALPHA)
        pygame.draw.rect(surf, C_DARK_PURPLE, (0, 0, s, s), border_radius=6)
        pygame.draw.ellipse(surf, (180, 130, 100), (14, 10, s - 28, s - 20))
        pygame.draw.rect(surf, (100, 40, 20), (14, 10, s - 28, 16))
        pygame.draw.ellipse(surf, (60, 40, 20), (22, 30, 10, 6))
        pygame.draw.ellipse(surf, (60, 40, 20), (40, 30, 10, 6))
        pygame.draw.circle(surf, (20, 10, 5),   (27, 33), 3)
        pygame.draw.circle(surf, (20, 10, 5),   (45, 33), 3)
        pygame.draw.ellipse(surf, (120, 180, 220), (50, 22, 5, 8))
        pygame.draw.arc(surf, (140, 80, 60), pygame.Rect(26, 46, 20, 10), 0.0, 3.14, 2)
        pygame.draw.line(surf, C_BLOOD_HIGH, (34, 20), (38, 28), 1)
        portraits.append(surf)

        # Stage 2 — critical
        surf = pygame.Surface((s, s), pygame.SRCALPHA)
        pygame.draw.rect(surf, (30, 0, 0), (0, 0, s, s), border_radius=6)
        pygame.draw.ellipse(surf, (150, 110, 90), (14, 10, s - 28, s - 20))
        pygame.draw.rect(surf, (80, 30, 10), (14, 10, s - 28, 16))
        pygame.draw.ellipse(surf, (60, 40, 20), (22, 31, 10, 4))
        pygame.draw.ellipse(surf, (60, 40, 20), (40, 31, 10, 4))
        pygame.draw.circle(surf, (20, 10, 5),   (27, 33), 2)
        pygame.draw.circle(surf, (20, 10, 5),   (45, 33), 2)
        pygame.draw.line(surf, C_BLOOD_HIGH, (30, 16), (34, 30), 2)
        pygame.draw.line(surf, C_BLOOD_HIGH, (46, 14), (44, 28), 1)
        pygame.draw.line(surf, (120, 60, 40), (28, 50), (44, 48), 2)
        pygame.draw.line(surf, (120, 60, 40), (28, 50), (26, 46), 1)
        pygame.draw.line(surf, (120, 60, 40), (44, 48), (46, 44), 1)
        portraits.append(surf)

        return portraits
