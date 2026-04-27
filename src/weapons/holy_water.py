import math
from pathlib import Path
import pygame
from src.settings import (
    HOLY_WATER_MAX, HOLY_WATER_SPEED, HOLY_WATER_DAMAGE,
    HOLY_WATER_RADIUS, HOLY_WATER_COOLDOWN_MS,
    HOLY_WATER_PUDDLE_MS, HOLY_WATER_PUDDLE_TICK, HOLY_WATER_PUDDLE_DMG,
    C_HOLY_BLUE, C_HOLY_LIGHT,
)


_ITEM_SPRITES = Path(__file__).resolve().parents[2] / "assets" / "sprites" / "items"


def _load_item_sprite(filename, size):
    try:
        sprite = pygame.image.load((_ITEM_SPRITES / filename).as_posix()).convert_alpha()
    except (FileNotFoundError, pygame.error):
        return None
    if sprite.get_size() != size:
        sprite = pygame.transform.scale(sprite, size)
    return sprite


class WaterPuddle:
    """Glowing DoT zone left behind after a splash dissipates."""

    _sprite = None

    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.radius = HOLY_WATER_RADIUS
        self._timer = 0.0
        self._tick_timer = 0.0
        self._pulse = 0.0
        self.alive = True
        self._hit_this_tick: set[int] = set()

    def update(self, dt, enemies):
        self._timer += dt
        self._pulse = (self._pulse + dt / 380) % (2 * math.pi)
        if self._timer >= HOLY_WATER_PUDDLE_MS:
            self.alive = False
            return

        self._tick_timer += dt
        if self._tick_timer >= HOLY_WATER_PUDDLE_TICK:
            self._tick_timer = 0
            self._hit_this_tick.clear()

        for e in enemies:
            if id(e) not in self._hit_this_tick:
                ex, ey = e.rect.center
                if math.hypot(ex - self.cx, ey - self.cy) <= self.radius:
                    e.take_damage(HOLY_WATER_PUDDLE_DMG)
                    self._hit_this_tick.add(id(e))

    def draw(self, surface):
        if WaterPuddle._sprite is None:
            WaterPuddle._sprite = _load_item_sprite("puddle.png", (32, 32))

        if WaterPuddle._sprite:
            progress = self._timer / HOLY_WATER_PUDDLE_MS
            pulse = 1.0 + 0.08 * math.sin(self._pulse)
            size = max(1, int(32 * pulse))
            sprite = pygame.transform.scale(WaterPuddle._sprite, (size, size))
            sprite.set_alpha(max(0, int(190 * (1 - progress))))
            surface.blit(sprite, sprite.get_rect(center=(self.cx, self.cy)))
            return

        progress = self._timer / HOLY_WATER_PUDDLE_MS
        base_a  = int(110 * (1 - progress))
        inner_a = int(55  * (1 - progress))
        r = self.radius
        pulse_r = int(r * 0.55 + r * 0.12 * math.sin(self._pulse))

        s = pygame.Surface((r * 2 + 4, r * 2 + 4), pygame.SRCALPHA)
        # Outer transparent fill
        pygame.draw.circle(s, (*C_HOLY_BLUE, inner_a), (r + 2, r + 2), r)
        # Pulsing inner pool
        pygame.draw.circle(s, (*C_HOLY_BLUE, base_a), (r + 2, r + 2), pulse_r)
        # Outer edge ring
        pygame.draw.circle(s, (*C_HOLY_LIGHT, base_a), (r + 2, r + 2), r, 2)
        # Inner bright ring
        pygame.draw.circle(s, (*C_HOLY_LIGHT, min(255, base_a + 40)),
                           (r + 2, r + 2), pulse_r, 1)
        surface.blit(s, (self.cx - r - 2, self.cy - r - 2))


class WaterSplash:
    """3-frame expanding AoE — scale transform applied to radius each frame."""

    FRAME_DURATION_MS = 120
    MAX_FRAMES = 3
    _frames = None

    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self._frame = 0
        self._timer = 0
        self.alive  = True
        self._hit: set[int] = set()

    @property
    def current_radius(self):
        return int(HOLY_WATER_RADIUS * (self._frame + 1) / self.MAX_FRAMES)

    def update(self, dt, enemies):
        self._timer += dt
        if self._timer >= self.FRAME_DURATION_MS:
            self._timer = 0
            self._frame += 1
            if self._frame >= self.MAX_FRAMES:
                self.alive = False
                return

        r = self.current_radius
        for e in enemies:
            if id(e) not in self._hit:
                ex, ey = e.rect.center
                if math.hypot(ex - self.cx, ey - self.cy) <= r:
                    e.take_damage(HOLY_WATER_DAMAGE)
                    self._hit.add(id(e))

    def draw(self, surface):
        if WaterSplash._frames is None:
            WaterSplash._frames = [
                _load_item_sprite(f"splash_{i}.png", (48, 32))
                for i in range(1, self.MAX_FRAMES + 1)
            ]

        sprite = WaterSplash._frames[min(self._frame, self.MAX_FRAMES - 1)]
        if sprite:
            surface.blit(sprite, sprite.get_rect(center=(self.cx, self.cy)))
            return

        alpha = max(0, 180 - self._frame * 60)
        r = self.current_radius
        splash_surf = pygame.Surface((r * 2 + 4, r * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(splash_surf, (*C_HOLY_BLUE, alpha),
                           (r + 2, r + 2), r)
        pygame.draw.circle(splash_surf, (*C_HOLY_LIGHT, min(255, alpha + 40)),
                           (r + 2, r + 2), r, 2)
        surface.blit(splash_surf, (self.cx - r - 2, self.cy - r - 2))


class HolyWaterThrow:
    """Projectile in flight — translates toward target, spawns WaterSplash on arrival."""

    SIZE = 10
    _sprite = None

    def __init__(self, ox, oy, tx, ty):
        dx, dy = tx - ox, ty - oy
        dist = math.hypot(dx, dy) or 1
        self.vx = (dx / dist) * HOLY_WATER_SPEED
        self.vy = (dy / dist) * HOLY_WATER_SPEED
        self.x  = float(ox)
        self.y  = float(oy)
        self.tx = tx
        self.ty = ty
        self.alive = True
        self.splash: WaterSplash | None = None

    def update(self, dt):
        if not self.alive:
            return
        self.x += self.vx * dt / 16
        self.y += self.vy * dt / 16
        if math.hypot(self.tx - self.x, self.ty - self.y) < 8:
            self.alive = False
            self.splash = WaterSplash(int(self.x), int(self.y))

    def draw(self, surface):
        if not self.alive:
            return
        if HolyWaterThrow._sprite is None:
            HolyWaterThrow._sprite = _load_item_sprite("water_full.png", (16, 20))

        if HolyWaterThrow._sprite:
            angle = -math.degrees(math.atan2(self.vy, self.vx)) - 90
            sprite = pygame.transform.rotate(HolyWaterThrow._sprite, angle)
            surface.blit(sprite, sprite.get_rect(center=(int(self.x), int(self.y))))
            return

        pygame.draw.circle(surface, C_HOLY_BLUE,
                           (int(self.x), int(self.y)), self.SIZE // 2)
        pygame.draw.circle(surface, C_HOLY_LIGHT,
                           (int(self.x), int(self.y)), self.SIZE // 2, 1)


class HolyWater:
    """Manages the player's holy water supply, throws, splashes, and puddles."""

    def __init__(self):
        self.charges  = HOLY_WATER_MAX
        self._cooldown = 0
        self._throws:  list[HolyWaterThrow] = []
        self._splashes: list[WaterSplash]   = []
        self._puddles:  list[WaterPuddle]   = []

    def refill(self):
        self.charges = HOLY_WATER_MAX

    def handle_fire(self, player_cx, player_cy, target_x, target_y):
        if self._cooldown > 0 or self.charges <= 0:
            return False
        self.charges -= 1
        self._cooldown = HOLY_WATER_COOLDOWN_MS
        self._throws.append(
            HolyWaterThrow(player_cx, player_cy, target_x, target_y)
        )
        return True

    def update(self, dt, enemies):
        self._cooldown = max(0, self._cooldown - dt)

        for t in self._throws:
            t.update(dt)
            if t.splash:
                self._splashes.append(t.splash)
                t.splash = None
        self._throws = [t for t in self._throws if t.alive]

        for s in self._splashes:
            was_alive = s.alive
            s.update(dt, enemies)
            # When splash finishes it leaves a puddle
            if was_alive and not s.alive:
                self._puddles.append(WaterPuddle(s.cx, s.cy))
        self._splashes = [s for s in self._splashes if s.alive]

        for p in self._puddles:
            p.update(dt, enemies)
        self._puddles = [p for p in self._puddles if p.alive]

    def draw(self, surface):
        for p in self._puddles:
            p.draw(surface)
        for s in self._splashes:
            s.draw(surface)
        for t in self._throws:
            t.draw(surface)

    @property
    def ready(self):
        return self._cooldown <= 0 and self.charges > 0
