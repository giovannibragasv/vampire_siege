import random
import pygame
from src.settings import (
    FPS, SCREEN_WIDTH, SCREEN_HEIGHT, ARENA_WIDTH, ARENA_HEIGHT,
    C_VOID, C_BONE, C_GOLD, C_BLOOD_HIGH,
    UPGRADES, UPGRADE_CHOICES, WAVE_DEFINITIONS, WAVE_BANNER_MS,
)
from src.camera import Camera


class State:
    MENU      = "menu"
    PLAYING   = "playing"
    UPGRADE   = "upgrade"
    GAME_OVER = "game_over"
    WIN       = "win"
    INFINITE  = "infinite"


class Game:
    def __init__(self, screen, clock):
        self.screen  = screen
        self.clock   = clock
        self.state   = State.MENU
        self.running = True

        self.wave_index = 0
        self._camera    = Camera()
        self._world_surface = pygame.Surface((ARENA_WIDTH, ARENA_HEIGHT))

        # Screen shake
        self._shake_timer     = 0
        self._shake_intensity = 0

        # Wave banner
        self._banner_text  = ""
        self._banner_timer = 0

        self._arena         = None
        self._player        = None
        self._wave_manager  = None
        self._hud           = None
        self._upgrade_menu  = None

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS)
            self._handle_events()
            self._update(dt)
            self._draw()

    # ------------------------------------------------------------------
    # State transitions
    # ------------------------------------------------------------------

    def start_game(self):
        from src.map.arena import Arena
        from src.entities.player import Player
        from src.waves.wave_manager import WaveManager
        from src.ui.hud import HUD

        self.wave_index    = 0
        self._arena        = Arena()
        self._player       = Player(ARENA_WIDTH // 2, ARENA_HEIGHT * 3 // 4)
        self._wave_manager = WaveManager(self._player, self._arena, self.wave_index)
        self._hud          = HUD(self._player, self._wave_manager)
        self._camera.update(self._player.rect)
        self._show_banner(f"WAVE {self.wave_index + 1}")
        self.state = State.PLAYING

    def _enter_upgrade(self):
        from src.ui.upgrade_menu import UpgradeMenu
        chosen = random.sample(UPGRADES, min(UPGRADE_CHOICES, len(UPGRADES)))
        self._upgrade_menu = UpgradeMenu(chosen)
        self.state = State.UPGRADE

    def _apply_upgrade(self, uid):
        p = self._player
        if uid == "orbit_slot":      p.add_orbit_slot()
        elif uid == "orbit_speed":   p.orbit_speed_multiplier *= 1.4
        elif uid == "orbit_radius":  p.orbit_radius += 30
        elif uid == "shotgun_damage":p.shotgun_damage_multiplier *= 1.5
        elif uid == "max_hp":
            p.max_hp += 30
            p.hp = p.max_hp
        elif uid == "move_speed":    p.speed *= 1.3

    def _next_wave(self):
        self.wave_index += 1
        if self.wave_index >= len(WAVE_DEFINITIONS):
            self.state = State.WIN
            return
        from src.waves.wave_manager import WaveManager
        self._wave_manager = WaveManager(
            self._player, self._arena, self.wave_index
        )
        self._hud._wave_manager = self._wave_manager
        self._show_banner(f"WAVE {self.wave_index + 1}")
        self.state = State.PLAYING

    def _enter_infinite(self):
        from src.waves.wave_manager import WaveManager
        self._wave_manager = WaveManager(self._player, self._arena, wave_index=None)
        self._hud._wave_manager = self._wave_manager
        self._show_banner("INFINITE MODE")
        self.state = State.INFINITE

    def _show_banner(self, text):
        self._banner_text  = text
        self._banner_timer = WAVE_BANNER_MS

    def trigger_shake(self, intensity=6, duration_ms=300):
        self._shake_timer     = max(self._shake_timer, duration_ms)
        self._shake_intensity = max(self._shake_intensity, intensity)

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------

    def _handle_events(self):
        cam_x, cam_y = self._camera.x, self._camera.y
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif self.state == State.MENU:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.start_game()

            elif self.state in (State.PLAYING, State.INFINITE):
                self._player.handle_event(event, cam_x, cam_y)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

            elif self.state == State.UPGRADE:
                result = self._upgrade_menu.handle_event(event)
                if result:
                    self._apply_upgrade(result)
                    self._next_wave()

            elif self.state in (State.GAME_OVER, State.WIN):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.start_game()
                    elif event.key == pygame.K_RETURN and self.state == State.WIN:
                        self._enter_infinite()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def _update(self, dt):
        self._shake_timer     = max(0, self._shake_timer - dt)
        self._banner_timer    = max(0, self._banner_timer - dt)
        if self._shake_timer == 0:
            self._shake_intensity = 0

        if self.state not in (State.PLAYING, State.INFINITE):
            return

        self._arena.update(dt)
        self._player._cam_x = self._camera.x
        self._player.update(dt, self._arena)
        self._wave_manager.update(dt)
        self._camera.update(self._player.rect)

        # Screen shake on player damage
        if self._player.just_damaged:
            self.trigger_shake(intensity=7, duration_ms=320)
            self._player.just_damaged = False

        if self._player.hp <= 0:
            self.state = State.GAME_OVER
            return

        if self.state == State.PLAYING and self._wave_manager.wave_cleared():
            if self.wave_index + 1 >= len(WAVE_DEFINITIONS):
                self.state = State.WIN
            else:
                self._enter_upgrade()

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------

    def _draw(self):
        if self.state == State.MENU:
            self.screen.fill(C_VOID)
            self._draw_menu()

        elif self.state in (State.PLAYING, State.INFINITE, State.UPGRADE):
            self._draw_world()

        elif self.state == State.GAME_OVER:
            self.screen.fill(C_VOID)
            self._draw_game_over()

        elif self.state == State.WIN:
            self.screen.fill(C_VOID)
            self._draw_win()

        pygame.display.flip()

    def _draw_world(self):
        # --- World surface ---
        self._world_surface.fill(C_VOID)
        self._arena.draw(self._world_surface)
        self._wave_manager.draw(self._world_surface)
        self._player.draw(self._world_surface)

        # --- Viewport blit with shake ---
        ox = oy = 0
        if self._shake_timer > 0:
            ox = random.randint(-self._shake_intensity, self._shake_intensity)
            oy = random.randint(-self._shake_intensity, self._shake_intensity)

        self.screen.fill(C_VOID)
        self.screen.blit(self._world_surface, (ox, oy), self._camera.viewport)

        # --- HUD (screen-space, no shake) ---
        if self.state in (State.PLAYING, State.INFINITE):
            self._hud.draw(self.screen)
            self._draw_wave_banner()
        elif self.state == State.UPGRADE:
            self._upgrade_menu.draw(self.screen)

    def _draw_wave_banner(self):
        if self._banner_timer <= 0:
            return
        # Fade in during first 400ms, hold, fade out during last 600ms
        ratio = self._banner_timer / WAVE_BANNER_MS
        if ratio > 0.8:
            alpha = int(255 * (1.0 - ratio) / 0.2)
        elif ratio < 0.3:
            alpha = int(255 * ratio / 0.3)
        else:
            alpha = 255

        font  = pygame.font.SysFont("serif", 72, bold=True)
        surf  = font.render(self._banner_text, True, C_GOLD)
        surf.set_alpha(alpha)
        self.screen.blit(surf, surf.get_rect(center=(SCREEN_WIDTH // 2,
                                                      SCREEN_HEIGHT // 3)))

    # ------------------------------------------------------------------
    # Screen overlays
    # ------------------------------------------------------------------

    def _draw_menu(self):
        f_big   = pygame.font.SysFont("serif", 72, bold=True)
        f_small = pygame.font.SysFont("serif", 32)
        title = f_big.render("VAMPIRE SIEGE", True, (196, 30, 58))
        sub   = f_small.render("Press ENTER to hunt", True, C_BONE)
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.screen.blit(title, title.get_rect(center=(cx, cy - 60)))
        self.screen.blit(sub,   sub.get_rect(center=(cx, cy + 20)))

    def _draw_game_over(self):
        f_big   = pygame.font.SysFont("serif", 72, bold=True)
        f_small = pygame.font.SysFont("serif", 32)
        msg  = f_big.render("YOU DIED", True, (196, 30, 58))
        score_text = f"Score: {self._wave_manager.score if self._wave_manager else 0}"
        score = f_small.render(score_text, True, C_GOLD)
        sub   = f_small.render("R — retry   ESC — quit", True, C_BONE)
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.screen.blit(msg,   msg.get_rect(center=(cx, cy - 60)))
        self.screen.blit(score, score.get_rect(center=(cx, cy)))
        self.screen.blit(sub,   sub.get_rect(center=(cx, cy + 50)))

    def _draw_win(self):
        f_big   = pygame.font.SysFont("serif", 64, bold=True)
        f_small = pygame.font.SysFont("serif", 30)
        msg    = f_big.render("DRACULA SLAIN", True, C_GOLD)
        score_text = f"Score: {self._wave_manager.score if self._wave_manager else 0}"
        score  = f_small.render(score_text, True, C_BONE)
        sub1   = f_small.render("ENTER — infinite mode", True, C_BONE)
        sub2   = f_small.render("R — new run   ESC — quit", True, C_BONE)
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.screen.blit(msg,   msg.get_rect(center=(cx, cy - 70)))
        self.screen.blit(score, score.get_rect(center=(cx, cy - 20)))
        self.screen.blit(sub1,  sub1.get_rect(center=(cx, cy + 20)))
        self.screen.blit(sub2,  sub2.get_rect(center=(cx, cy + 55)))
