import random
import pygame
from src.settings import (
    FPS, SCREEN_WIDTH, SCREEN_HEIGHT, C_VOID,
    UPGRADES, UPGRADE_CHOICES, WAVE_DEFINITIONS,
)


class State:
    MENU    = "menu"
    PLAYING = "playing"
    UPGRADE = "upgrade"
    GAME_OVER = "game_over"
    WIN     = "win"
    INFINITE = "infinite"


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock  = clock
        self.state  = State.MENU
        self.running = True

        self.wave_index = 0
        self.pending_upgrades = []

        self._arena = None
        self._player = None
        self._wave_manager = None
        self._hud = None
        self._upgrade_menu = None

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

        self.wave_index = 0
        self._arena = Arena()
        self._player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self._wave_manager = WaveManager(self._player, self._arena, self.wave_index)
        self._hud = HUD(self._player)
        self.state = State.PLAYING

    def _enter_upgrade(self):
        from src.ui.upgrade_menu import UpgradeMenu
        pool = UPGRADES[:]
        chosen = random.sample(pool, min(UPGRADE_CHOICES, len(pool)))
        self._upgrade_menu = UpgradeMenu(chosen)
        self.state = State.UPGRADE

    def _apply_upgrade(self, upgrade_id):
        p = self._player
        if upgrade_id == "orbit_slot":
            p.add_orbit_slot()
        elif upgrade_id == "orbit_speed":
            p.orbit_speed_multiplier *= 1.4
        elif upgrade_id == "orbit_radius":
            p.orbit_radius += 30
        elif upgrade_id == "shotgun_damage":
            p.shotgun_damage_multiplier *= 1.5
        elif upgrade_id == "max_hp":
            p.max_hp += 30
            p.hp = p.max_hp
        elif upgrade_id == "move_speed":
            p.speed *= 1.3

    def _next_wave(self):
        self.wave_index += 1
        if self.wave_index >= len(WAVE_DEFINITIONS):
            self.state = State.WIN
            return
        from src.waves.wave_manager import WaveManager
        self._wave_manager = WaveManager(
            self._player, self._arena, self.wave_index
        )
        self.state = State.PLAYING

    def _enter_infinite(self):
        from src.waves.wave_manager import WaveManager
        self._wave_manager = WaveManager(
            self._player, self._arena, wave_index=None
        )
        self.state = State.INFINITE

    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif self.state == State.MENU:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.start_game()

            elif self.state in (State.PLAYING, State.INFINITE):
                self._player.handle_event(event)
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
        if self.state not in (State.PLAYING, State.INFINITE):
            return

        self._arena.update(dt)
        self._player.update(dt, self._arena)
        self._wave_manager.update(dt)

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
        self.screen.fill(C_VOID)

        if self.state == State.MENU:
            self._draw_menu()
        elif self.state in (State.PLAYING, State.INFINITE):
            self._arena.draw(self.screen)
            self._wave_manager.draw(self.screen)
            self._player.draw(self.screen)
            self._hud.draw(self.screen)
        elif self.state == State.UPGRADE:
            self._arena.draw(self.screen)
            self._player.draw(self.screen)
            self._upgrade_menu.draw(self.screen)
        elif self.state == State.GAME_OVER:
            self._draw_game_over()
        elif self.state == State.WIN:
            self._draw_win()

        pygame.display.flip()

    def _draw_menu(self):
        font_big   = pygame.font.SysFont("serif", 72, bold=True)
        font_small = pygame.font.SysFont("serif", 32)
        title = font_big.render("VAMPIRE SIEGE", True, (196, 30, 58))
        sub   = font_small.render("Press ENTER to hunt", True, (232, 220, 200))
        cx = SCREEN_WIDTH  // 2
        cy = SCREEN_HEIGHT // 2
        self.screen.blit(title, title.get_rect(center=(cx, cy - 60)))
        self.screen.blit(sub,   sub.get_rect(center=(cx, cy + 20)))

    def _draw_game_over(self):
        font_big   = pygame.font.SysFont("serif", 72, bold=True)
        font_small = pygame.font.SysFont("serif", 32)
        msg  = font_big.render("YOU DIED", True, (196, 30, 58))
        sub  = font_small.render("R to retry   ESC to quit", True, (232, 220, 200))
        cx = SCREEN_WIDTH  // 2
        cy = SCREEN_HEIGHT // 2
        self.screen.blit(msg, msg.get_rect(center=(cx, cy - 40)))
        self.screen.blit(sub, sub.get_rect(center=(cx, cy + 30)))

    def _draw_win(self):
        font_big   = pygame.font.SysFont("serif", 64, bold=True)
        font_small = pygame.font.SysFont("serif", 30)
        msg   = font_big.render("DRACULA SLAIN", True, (200, 168, 75))
        sub1  = font_small.render("ENTER — continue to infinite mode", True, (232, 220, 200))
        sub2  = font_small.render("R — new run   ESC — quit", True, (232, 220, 200))
        cx = SCREEN_WIDTH  // 2
        cy = SCREEN_HEIGHT // 2
        self.screen.blit(msg,  msg.get_rect(center=(cx, cy - 60)))
        self.screen.blit(sub1, sub1.get_rect(center=(cx, cy + 10)))
        self.screen.blit(sub2, sub2.get_rect(center=(cx, cy + 50)))
