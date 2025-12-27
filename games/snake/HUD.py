import pygame

from games.snake.score_manager import ScoreManager


class HUD:
    def __init__(self, screen: pygame.Surface, score_manager: ScoreManager) -> None:
        self.screen = screen
        self.font_big = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 48)
        self.font_small = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 32)
        self.score_manager = score_manager

        self.press_to_start = self.font_big.render(
            "Press SPACE or ENTER to start", True, (255, 255, 255)
        )
        self.press_to_start_rect = self.press_to_start.get_rect(
            center=(screen.get_width() // 2, screen.get_height() // 2)
        )

        self.end_surf = self.font_big.render(
            "Press Q to quit\nPress R to restart",True, (255, 255, 255))
        self.end_rect = self.end_surf.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
        )

    def draw_start(self) -> None:
        self.screen.blit(self.press_to_start, self.press_to_start_rect)

    def draw_running(self) -> None:
        right = self.screen.width * 99 // 100
        height1 = self.screen.height * 13 // 15
        height2 = self.screen.height * 14 // 15
        text_surface = self.font_small.render(f"Score: {self.score_manager.score}",
                                              True, (255, 255, 255))
        text_rect = text_surface.get_rect(midright=(right, height1))
        self.screen.blit(text_surface, text_rect)
        text_surface = self.font_small.render(f"High Score: {self.score_manager.high_score}",
                                              True, (255, 255, 255))
        text_rect = text_surface.get_rect(midright=(right, height2))

        self.screen.blit(text_surface, text_rect)

    def draw_game_over(self) -> None:
        self.screen.blit(self.end_surf, self.end_rect)