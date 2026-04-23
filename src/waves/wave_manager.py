import random
import pygame
from src.settings import (
    WAVE_DEFINITIONS, SPAWN_MARGIN,
    ARENA_WIDTH, ARENA_HEIGHT,
    VAMPIRE_HP, FAST_VAMPIRE_HP,
)
import math as _math
from src.entities.blood_decal import BloodDecal


_SCORE_VALUES = {
    "vampire": 10,
    "fast":    15,
    "mirror":  50,
    "dracula": 200,
}


class WaveManager:
    def __init__(self, player, arena, wave_index):
        self.player     = player
        self.arena      = arena
        self.wave_index = wave_index
        self.enemies: list = []
        self._spawn_queue: list = []
        self._spawn_timer = 0
        self._spawn_interval = 1200   # ms between individual spawns
        self._cleared = False
        self._infinite_timer = 0
        self._infinite_interval = 20_000

        self.score = 0
        self.kills = 0
        self._decals: list[BloodDecal] = []
        self.wave_time_ms = 0  # elapsed time in current wave

        # Give the arena a back-reference so player weapons can reach enemies
        arena._wave_manager_ref = self

        if wave_index is None:
            self._setup_infinite()
        else:
            self._setup_wave(wave_index)

    # ------------------------------------------------------------------

    def _spawn_point(self):
        side = random.randint(0, 3)
        m = SPAWN_MARGIN
        if side == 0:
            return (random.randint(m, ARENA_WIDTH - m), m)
        elif side == 1:
            return (random.randint(m, ARENA_WIDTH - m), ARENA_HEIGHT - m)
        elif side == 2:
            return (m, random.randint(m, ARENA_HEIGHT - m))
        else:
            return (ARENA_WIDTH - m, random.randint(m, ARENA_HEIGHT - m))

    def _setup_wave(self, idx):
        defn = WAVE_DEFINITIONS[idx]

        normal = [("vampire", None)] * defn["vampires"] + \
                 [("fast",    None)] * defn["fast_vampires"]
        random.shuffle(normal)

        queue = []
        if defn.get("has_mirror"):
            queue.append(("mirror", None))
        queue.extend(normal)
        if defn.get("has_boss"):
            queue.append(("dracula", None))

        self._spawn_queue = queue

    def _setup_infinite(self):
        self._spawn_queue = []

    def _enqueue_infinite_wave(self):
        count_v = random.randint(8, 16)
        count_f = random.randint(3, 8)
        self._spawn_queue += [("vampire", None)] * count_v
        self._spawn_queue += [("fast",    None)] * count_f

    # ------------------------------------------------------------------

    def wave_cleared(self):
        return self._cleared

    def enemies_remaining(self):
        return len(self.enemies) + len(self._spawn_queue)

    def update(self, dt):
        self.wave_time_ms += dt

        # Spawn from queue
        self._spawn_timer += dt
        if self._spawn_timer >= self._spawn_interval and self._spawn_queue:
            self._spawn_timer = 0
            self._do_spawn(self._spawn_queue.pop(0))

        # Infinite mode: enqueue new wave periodically
        if self.wave_index is None:
            self._infinite_timer += dt
            if self._infinite_timer >= self._infinite_interval or not self._spawn_queue:
                self._infinite_timer = 0
                self._enqueue_infinite_wave()

        # Snapshot alive state before updates to detect deaths this frame
        alive_before = {id(e): e.alive for e in self.enemies}

        for e in self.enemies:
            e.update(dt, self.player, self.arena)

        # Weapon collision (via player method)
        self.player.update_weapons_with_enemies(dt, self.arena, self.enemies)

        # Detect deaths: spawn decals and accumulate score
        for e in self.enemies:
            if alive_before.get(id(e), True) and not e.alive:
                cx, cy = e.rect.center
                self._decals.append(BloodDecal(cx, cy))
                self.kills += 1
                self.score += getattr(e, "_score_value", 10)

        self.enemies = [e for e in self.enemies if e.alive]

        # Update and cull decals
        for d in self._decals:
            d.update(dt)
        self._decals = [d for d in self._decals if d.alive]

        # Check cleared
        if (self.wave_index is not None and
                not self._spawn_queue and
                not self.enemies and
                not self._cleared):
            self._cleared = True

    def _do_spawn(self, entry):
        from src.entities.vampire import Vampire
        from src.entities.fast_vampire import FastVampire
        from src.entities.mirror_enemy import MirrorEnemy
        from src.entities.dracula import Dracula

        kind, _ = entry
        px, py  = self.player.rect.center

        if kind == "vampire":
            cx, cy = self._spawn_point()
            e = Vampire(cx, cy)
        elif kind == "fast":
            cx, cy = self._spawn_point()
            e = FastVampire(cx, cy)
        elif kind == "mirror":
            e = MirrorEnemy(px, py)
        elif kind == "dracula":
            e = Dracula(ARENA_WIDTH // 2, ARENA_HEIGHT // 2)
        else:
            return

        e._score_value = _SCORE_VALUES.get(kind, 10)

        # HP scaling: per-wave multiplier or infinite time ramp
        if self.wave_index is not None:
            hp_mult = WAVE_DEFINITIONS[self.wave_index].get("hp_mult", 1.0)
        else:
            # Every 2 minutes in infinite mode add 15% more HP
            mins = self.wave_time_ms / 120_000
            hp_mult = 1.0 + mins * 0.15
        scaled = int(e.hp * hp_mult)
        e.hp = scaled
        e.max_hp = scaled

        self.enemies.append(e)

    def draw(self, surface):
        for d in self._decals:
            d.draw(surface)
        for e in self.enemies:
            e.draw(surface)
