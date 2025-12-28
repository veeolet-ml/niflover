import math
import random
import pygame

from games.snake.score_manager import ScoreManager


class HUD:
    # Color fade settings
    FADE_SPEED = 0.001
    COLOR_MIN = 180
    COLOR_MAX = 255

    # Hints to display during gameplay (add your own!)
    HINTS = [
        "Tip: Press E for superfast mode",
        "Tip: Eat food to grow longer",
        "Tip: Press any key to immediately step",
    ]

    def __init__(self, screen: pygame.Surface, score_manager: ScoreManager) -> None:
        self.screen = screen
        self.font_big = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 48)
        self.font_small = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 32)
        self.score_manager = score_manager
        self.color_time = 0
        self.current_hint = random.choice(self.HINTS)

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

    def _render_wrapped_text(self, text: str, font: pygame.font.Font, color: pygame.Color | pygame.typing.SequenceLike[int] | int | str, 
                              max_width: int, line_spacing: int = 10) -> pygame.Surface:
        """
        Render text with manual word wrapping and custom line spacing.
        
        Arguments:
            text: The text to render
            font: The pygame font to use
            color: Any pygame color
            max_width: Maximum width before wrapping
            line_spacing: Extra pixels between lines (default 10)
        
        Returns:
            A surface containing the wrapped text
        """
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width = font.size(test_line)[0]
            if test_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        if not lines:
            return font.render("", True, color)
        
        # Render each line
        line_surfaces = [font.render(line, True, color) for line in lines]
        line_height = font.get_height()
        
        # Calculate total height with spacing
        total_height = len(line_surfaces) * line_height + (len(line_surfaces) - 1) * line_spacing
        max_line_width = max(surf.get_width() for surf in line_surfaces)
        
        # Create combined surface
        combined = pygame.Surface((max_line_width, total_height), pygame.SRCALPHA)
        y = 0
        for surf in line_surfaces:
            combined.blit(surf, (0, y))
            y += line_height + line_spacing
        
        return combined

    def _create_surfaces(self, color: pygame.Color | pygame.typing.SequenceLike[int] | int | str) -> None:
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

        self.you_win_surf = self.font_big.render("YOU WIN!", True, color)
        self.you_win_rect = self.you_win_surf.get_rect(
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
        color = self._get_fading_color()
        
        right = self.screen.width * 99 // 100
        height1 = self.screen.height * 13 // 15
        height2 = self.screen.height * 14 // 15
        text_surface = self.font_small.render(f"Score: {self.score_manager.score}",
                                              True, color)
        text_rect = text_surface.get_rect(midright=(right, height1))
        self.screen.blit(text_surface, text_rect)
        text_surface = self.font_small.render(f"High Score: {self.score_manager.high_score}",
                                              True, color)
        text_rect = text_surface.get_rect(midright=(right, height2))
        self.screen.blit(text_surface, text_rect)

        # Instructions
        mid_height = self.screen.height * 9 // 10
        instr_surf = self._render_wrapped_text(
            "WASD or Arrow Keys to move", self.font_small, color,
            self.screen.width * 3 // 10, line_spacing=10
        )
        instr_rect = instr_surf.get_rect(midleft=(self.screen.width * 1 // 100, mid_height))
        self.screen.blit(instr_surf, instr_rect)

        # Random hint
        hint_surf = self._render_wrapped_text(
            self.current_hint, self.font_small, color,
            self.screen.width * 35 // 100, line_spacing=10
        )
        hint_rect = hint_surf.get_rect(midleft=(self.screen.width * 35 // 100, mid_height))
        self.screen.blit(hint_surf, hint_rect)

    def draw_game_over(self) -> None:
        if self.score_manager.score >= 1000:
            self.screen.blit(self.you_win_surf, self.you_win_rect)
        else:
            self.screen.blit(self.game_over_surf, self.game_over_rect)
        self.screen.blit(self.restart_surf, self.restart_rect)
        self.screen.blit(self.quit_surf, self.quit_rect)