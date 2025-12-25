import pygame

class HUD:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font_big = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 48)
        self.font_small = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 32)

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

    def draw_game_over(self) -> None:
        self.screen.blit(self.end_surf, self.end_rect)