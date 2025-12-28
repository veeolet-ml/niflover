import math
import pygame

from games.snake.score_manager import ScoreManager


class HUD:
    # Color fade settings
    FADE_SPEED = 0.001
    COLOR_MIN = 180
    COLOR_MAX = 255

    def __init__(self, screen: pygame.Surface, score_manager: ScoreManager) -> None:
        self.screen = screen
        self.font_big = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 48)
        self.font_small = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 32)
        self.score_manager = score_manager
        self.color_time = 0

        self._create_surfaces((255, 255, 255))

    def _get_fading_color(self) -> tuple:
        """Calculate the current color based on time using sine waves for smooth transitions."""
        r = int(self.COLOR_MIN + (self.COLOR_MAX - self.COLOR_MIN) * 
                (0.5 + 0.5 * math.sin(self.color_time + 1)))
        g = int(self.COLOR_MIN + (self.COLOR_MAX - self.COLOR_MIN) * 
                (0.5 + 0.5 * math.sin(self.color_time * 1.1 + 2)))
        b = int(self.COLOR_MIN + (self.COLOR_MAX - self.COLOR_MIN) * 
                (0.5 + 0.5 * math.sin(self.color_time * 1.2 + 3)))
        return (r, g, b)

    def update(self, dt: int) -> None:
        """Update the color fade - dt is in milliseconds."""
        self.color_time += dt * self.FADE_SPEED
        if self.color_time > 2 * math.pi:
            self.color_time -= 2 * math.pi
        self._create_surfaces(self._get_fading_color())

    def _create_surfaces(self, color: tuple) -> None:
        # Start screen elements
        self.title_surf = self.font_big.render("SNAKE", True, color)
        self.title_rect = self.title_surf.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 4)
        )

        self.press_to_start = self.font_small.render(
            "Press SPACE or ENTER to start", True, color
        )
        self.press_to_start_rect = self.press_to_start.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 20)
        )

        # Game over screen elements
        self.game_over_surf = self.font_big.render("GAME OVER", True, color)
        self.game_over_rect = self.game_over_surf.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 4)
        )

        self.restart_surf = self.font_small.render("Press R to restart", True, color)
        self.restart_rect = self.restart_surf.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
        )

        self.quit_surf = self.font_small.render("Press Q to quit", True, color)
        self.quit_rect = self.quit_surf.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 50)
        )

    def draw_start(self) -> None:
        self.screen.blit(self.title_surf, self.title_rect)
        self.screen.blit(self.press_to_start, self.press_to_start_rect)

    def draw_running(self) -> None:
        right = self.screen.width * 99 // 100
        height1 = self.screen.height * 13 // 15
        height2 = self.screen.height * 14 // 15
        text_surface = self.font_small.render(f"Score: {self.score_manager.score}",
                                              True, self._get_fading_color())
        text_rect = text_surface.get_rect(midright=(right, height1))
        self.screen.blit(text_surface, text_rect)
        text_surface = self.font_small.render(f"High Score: {self.score_manager.high_score}",
                                              True, self._get_fading_color())
        text_rect = text_surface.get_rect(midright=(right, height2))

        self.screen.blit(text_surface, text_rect)

    def draw_game_over(self) -> None:
        self.screen.blit(self.game_over_surf, self.game_over_rect)
        self.screen.blit(self.restart_surf, self.restart_rect)
        self.screen.blit(self.quit_surf, self.quit_rect)