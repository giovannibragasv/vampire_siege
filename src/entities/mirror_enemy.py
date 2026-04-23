import pygame
from src.settings import (
    MIRROR_HP, MIRROR_SPEED, MIRROR_DAMAGE,
    ARENA_CENTER_X, CONTACT_DAMAGE_COOLDOWN_MS,
)
from src.transforms.matrices import mirror_position, flip_surface
from src.entities.enemy import Enemy


class MirrorEnemy(Enemy):
    """
    Position is always the geometric reflection of the player across
    the arena vertical center (x = ARENA_CENTER_X).

    mirror_position() applies: T(-cx) · Ry · T(cx)
    Sprite is rendered with a horizontal flip via flip_surface().
    """

    COLOR = (200, 200, 220)

    def __init__(self, player_cx, player_cy):
        mx = int(mirror_position(player_cx, ARENA_CENTER_X))
        super().__init__(mx, player_cy, MIRROR_HP, MIRROR_SPEED, MIRROR_DAMAGE, self.COLOR)
        self._surface = self._make_mirror_surface()

    def _make_mirror_surface(self):
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        # Inverted palette: silver-white coat, purple-toned skin
        pygame.draw.rect(surf, (200, 200, 220),
                         (4, 8, self.WIDTH - 8, self.HEIGHT - 8), border_radius=4)
        pygame.draw.ellipse(surf, (80, 40, 100), (8, 0, 16, 14))
        pygame.draw.circle(surf, (155, 48, 255), (16, 7), 3)
        return surf

    def update(self, dt, player, arena):
        # Reflection: recompute position from player each frame
        new_x = int(mirror_position(player.rect.centerx, ARENA_CENTER_X))
        self.rect.centerx = new_x
        self.rect.centery = player.rect.centery
        arena.clamp_entity(self.rect)
        self.try_damage_player(player, dt)
        self._hit_timer = max(0, self._hit_timer - dt)
        self._contact_cooldown = max(0, self._contact_cooldown - dt)

    def draw(self, surface):
        img = self._surface.copy()
        if self._hit_timer > 0:
            img.fill((255, 60, 60, 120), special_flags=pygame.BLEND_RGBA_ADD)
        # Always rendered flipped — it's a mirror image
        img = flip_surface(img, flip_x=True, flip_y=False)
        surface.blit(img, self.rect)
        self._draw_hp_bar(surface)
