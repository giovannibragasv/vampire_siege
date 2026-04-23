import pygame
from src.settings import ARENA_WIDTH, ARENA_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    """
    Tracks a viewport window into the larger world surface.
    Clamps so the viewport never shows outside the arena.
    """

    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, target_rect: pygame.Rect):
        self.x = max(0, min(target_rect.centerx - SCREEN_WIDTH  // 2,
                             ARENA_WIDTH  - SCREEN_WIDTH))
        self.y = max(0, min(target_rect.centery - SCREEN_HEIGHT // 2,
                             ARENA_HEIGHT - SCREEN_HEIGHT))

    def screen_to_world(self, sx: int, sy: int) -> tuple[int, int]:
        """Convert screen-space mouse coordinates to world-space."""
        return sx + self.x, sy + self.y

    @property
    def viewport(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, SCREEN_WIDTH, SCREEN_HEIGHT)
