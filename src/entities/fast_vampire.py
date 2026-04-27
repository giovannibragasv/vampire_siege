from src.settings import FAST_VAMPIRE_SPEED, FAST_VAMPIRE_HP, FAST_VAMPIRE_DAMAGE
from src.entities.enemy import Enemy
import pygame
from pathlib import Path


class FastVampire(Enemy):
    WIDTH  = 32
    HEIGHT = 48
    COLOR  = (40, 20, 5)
    IDLE_FRAME_MS = 220
    WALK_FRAME_MS = 90
    DAMAGE_FRAME_MS = 180
    DEATH_FRAME_MS = 160

    def __init__(self, cx, cy):
        super().__init__(cx, cy, FAST_VAMPIRE_HP, FAST_VAMPIRE_SPEED,
                         FAST_VAMPIRE_DAMAGE, self.COLOR)
        self.remove_ready = False
        self._idle_frames = self._load_frames("fast_idle", 2)
        self._walk_frames = self._load_frames("fast_walk", 4)
        self._damaged_frame = self._load_named_frame("fast_damaged.png")
        self._death_frames = self._load_frames("fast_death", 3)
        self._anim_timer = 0
        self._anim_index = 0
        self._damage_anim_timer = 0
        self._dying = False
        self._surface = self._idle_frames[0]

    def take_damage(self, amount, kbx=0.0, kby=0.0):
        if self._dying:
            return
        super().take_damage(amount, kbx, kby)
        if not self.alive:
            self._start_death()
        else:
            self._damage_anim_timer = self.DAMAGE_FRAME_MS
            self._surface = self._damaged_frame

    def update(self, dt, player, arena):
        if self._dying:
            self._update_death(dt)
            self._hit_timer = max(0, self._hit_timer - dt)
            for dn in self._damage_numbers:
                dn.update(dt)
            self._damage_numbers = [dn for dn in self._damage_numbers if dn.alive]
            return

        super().update(dt, player, arena)
        self._update_animation(dt)

    def draw(self, surface):
        img = self._surface.copy()
        if self._hit_timer > 0 and not self._dying:
            img.fill((255, 60, 60, 120), special_flags=pygame.BLEND_RGBA_ADD)
        if not self._facing_right:
            img = pygame.transform.flip(img, True, False)
        surface.blit(img, self.rect)
        if self.alive:
            self._draw_hp_bar(surface)
        for dn in self._damage_numbers:
            dn.draw(surface)

    def _update_animation(self, dt):
        if self._damage_anim_timer > 0:
            self._damage_anim_timer = max(0, self._damage_anim_timer - dt)
            self._surface = self._damaged_frame
            return

        moving = abs(self._kbx) > 0.1 or abs(self._kby) > 0.1
        frame_ms = self.WALK_FRAME_MS if moving else self.IDLE_FRAME_MS
        frames = self._walk_frames
        self._anim_timer += dt
        if self._anim_timer >= frame_ms:
            steps = self._anim_timer // frame_ms
            self._anim_timer %= frame_ms
            self._anim_index = (self._anim_index + steps) % len(frames)
        self._surface = frames[self._anim_index]

    def _start_death(self):
        self._dying = True
        self.remove_ready = False
        self._anim_timer = 0
        self._anim_index = 0
        self._damage_anim_timer = 0
        self._kbx = 0.0
        self._kby = 0.0
        self._surface = self._death_frames[0]

    def _update_death(self, dt):
        self._anim_timer += dt
        if self._anim_index < len(self._death_frames) - 1 and self._anim_timer >= self.DEATH_FRAME_MS:
            steps = self._anim_timer // self.DEATH_FRAME_MS
            self._anim_timer %= self.DEATH_FRAME_MS
            self._anim_index = min(self._anim_index + steps, len(self._death_frames) - 1)
        self._surface = self._death_frames[self._anim_index]
        self.remove_ready = self._anim_index >= len(self._death_frames) - 1 and self._anim_timer > self.DEATH_FRAME_MS * 0.75

    def _load_frames(self, prefix, count):
        return [
            self._load_named_frame(f"{prefix}_{idx}.png")
            for idx in range(1, count + 1)
        ]

    def _load_named_frame(self, filename):
        root = Path(__file__).resolve().parents[2]
        frame_path = root / "assets" / "sprites" / "enemies" / "vampire_fast" / filename
        try:
            frame = pygame.image.load(frame_path.as_posix()).convert_alpha()
            if frame.get_size() != (self.WIDTH, self.HEIGHT):
                frame = pygame.transform.scale(frame, (self.WIDTH, self.HEIGHT))
            return frame
        except (FileNotFoundError, pygame.error):
            return self._make_surface()
