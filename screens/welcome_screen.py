import pygame
import pygame.locals

from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from .base_screen import Screen


class WelcomeScreen(Screen):
    def __init__(self, window, fps=60, bgcolor=None):
        super().__init__(window, fps, bgcolor)
        self.choice = ""
        self.mode = ""
        self.Rect_upper = pygame.locals.Rect(
            WINDOW_WIDTH / 2 - 65, WINDOW_HEIGHT * 2 / 5 - 10, 150, 50
        )
        self.Rect_lower = pygame.locals.Rect(
            WINDOW_WIDTH / 2 - 65, WINDOW_HEIGHT * 3 / 5 - 10, 150, 50
        )

    def create_text_surface(self, text, size):
        """function reused from previous lab"""
        arial = pygame.font.SysFont("arial", size)
        text_surface = arial.render(text, True, (0, 0, 0))

        return text_surface

    def process_event(self, event):
        if event.type == pygame.locals.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.Rect_upper.collidepoint(mouse_pos):
                self.mode = "practice"
                self.running = False
            if self.Rect_lower.collidepoint(mouse_pos):
                self.mode = "ranked"
                self.running = False

    def process_loop(self):
        pygame.font.init()

        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        window.fill((255, 255, 255))

        practice_text = self.create_text_surface("Free Practice", 24)
        ranked_text = self.create_text_surface("Ranked Match", 24)
        title_text = self.create_text_surface("Pong", 40)

        pygame.draw.rect(window, (255, 227, 40), self.Rect_upper)
        pygame.draw.rect(window, (255, 227, 40), self.Rect_lower)

        window.blit(ranked_text, (WINDOW_WIDTH / 2 - 55, WINDOW_HEIGHT * 3 / 5))
        window.blit(practice_text, (WINDOW_WIDTH / 2 - 55, WINDOW_HEIGHT * 2 / 5))
        window.blit(title_text, (WINDOW_WIDTH / 2 - 35, WINDOW_HEIGHT * 1 / 5))

        pygame.display.flip()
