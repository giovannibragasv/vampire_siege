import random
import pygame
from src.settings import (
    WAVE_DEFINITIONS, SPAWN_MARGIN,
    ARENA_WIDTH, ARENA_HEIGHT,
    VAMPIRE_HP, FAST_VAMPIRE_HP,
)


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
        from src.entities.vampire import Vampire
        from src.entities.fast_vampire import FastVampire
        from src.entities.mirror_enemy import MirrorEnemy
        from src.entities.dracula import Dracula

        defn = WAVE_DEFINITIONS[idx]
        queue = []

        for _ in range(defn["vampires"]):
            queue.append(("vampire", None))
        for _ in range(defn["fast_vampires"]):
            queue.append(("fast", None))
        if defn.get("has_mirror"):
            queue.insert(0, ("mirror", None))
        if defn.get("has_boss"):
            queue.append(("dracula", None))

        random.shuffle([q for q in queue if q[0] not in ("mirror", "dracula")])
        self._spawn_queue = queue

    def _setup_infinite(self):
        self._spawn_queue = []

    def _enqueue_infinite_wave(self):
        from src.entities.vampire import Vampire
        from src.entities.fast_vampire import FastVampire
        count_v = random.randint(8, 16)
        count_f = random.randint(3, 8)
        self._spawn_queue += [("vampire", None)] * count_v
        self._spawn_queue += [("fast",    None)] * count_f

    # ------------------------------------------------------------------

    def wave_cleared(self):
        return self._cleared

    def update(self, dt):
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

        # Update all enemies
        for e in self.enemies:
            e.update(dt, self.player, self.arena)

        # Weapon collision (via player method)
        self.player.update_weapons_with_enemies(dt, self.arena, self.enemies)

        self.enemies = [e for e in self.enemies if e.alive]

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
            self.enemies.append(Vampire(cx, cy))
        elif kind == "fast":
            cx, cy = self._spawn_point()
            self.enemies.append(FastVampire(cx, cy))
        elif kind == "mirror":
            self.enemies.append(MirrorEnemy(px, py))
        elif kind == "dracula":
            self.enemies.append(Dracula(ARENA_WIDTH // 2, ARENA_HEIGHT // 2))

    def draw(self, surface):
        for e in self.enemies:
            e.draw(surface)
