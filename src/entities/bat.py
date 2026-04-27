import math
from pathlib import Path
import pygame
from src.settings import BAT_SPEED, BAT_DAMAGE


class Bat:
    """Projectile launched by the Mirror Enemy during its bat wave attack."""

    SIZE = 16
    _FRAMES = None

    def __init__(self, cx, cy, target_x, target_y):
        dx, dy = target_x - cx, target_y - cy
        dist = math.hypot(dx, dy) or 1
        self.vx = (dx / dist) * BAT_SPEED
        self.vy = (dy / dist) * BAT_SPEED
        self.x  = float(cx)
        self.y  = float(cy)
        self.alive = True
        self._wing_frame = 0
        self._wing_timer = 0
        self._frames = self._load_frames()

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x) - self.SIZE // 2,
            int(self.y) - self.SIZE // 2,
            self.SIZE, self.SIZE,
        )

    def update(self, dt, arena_inner, player):
        self.x += self.vx * dt / 16
        self.y += self.vy * dt / 16

        self._wing_timer += dt
        if self._wing_timer >= 120:
            self._wing_timer = 0
            self._wing_frame = (self._wing_frame + 1) % 2

        if not arena_inner.colliderect(self.rect):
            self.alive = False
            return

        if self.rect.colliderect(player.rect):
            player.take_damage(BAT_DAMAGE)
            self.alive = False

    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        img = self._frames[self._wing_frame].copy()
        angle = -math.degrees(math.atan2(self.vy, self.vx))
        img = pygame.transform.rotate(img, angle)
        surface.blit(img, img.get_rect(center=(cx, cy)))

    @classmethod
    def _load_frames(cls):
        if cls._FRAMES is not None:
            return cls._FRAMES

        root = Path(__file__).resolve().parents[2]
        sprite_dir = root / "assets" / "sprites" / "enemies" / "bat"
        frames = []
        for idx in range(1, 3):
            path = sprite_dir / f"bat_{idx}.png"
            try:
                frame = pygame.image.load(path.as_posix()).convert_alpha()
                if frame.get_size() != (cls.SIZE, cls.SIZE):
                    frame = pygame.transform.scale(frame, (cls.SIZE, cls.SIZE))
            except (FileNotFoundError, pygame.error):
                frame = cls._make_placeholder_frame(idx)
            frames.append(frame)
        cls._FRAMES = frames
        return frames

    @classmethod
    def _make_placeholder_frame(cls, idx):
        surf = pygame.Surface((cls.SIZE, cls.SIZE), pygame.SRCALPHA)
        body_color = (50, 0, 70)
        wing_color = (80, 0, 110)
        pygame.draw.ellipse(surf, body_color, (5, 6, 6, 5))
        if idx == 1:
            pygame.draw.ellipse(surf, wing_color, (0, 4, 7, 5))
            pygame.draw.ellipse(surf, wing_color, (9, 4, 7, 5))
        else:
            pygame.draw.ellipse(surf, wing_color, (1, 8, 6, 4))
            pygame.draw.ellipse(surf, wing_color, (9, 8, 6, 4))
        pygame.draw.circle(surf, (220, 0, 0), (6, 7), 1)
        pygame.draw.circle(surf, (220, 0, 0), (10, 7), 1)
        return surf
