import pygame
import pygame.locals
from constants import WINDOW_WIDTH, WINDOW_HEIGHT
from .base_screen import Screen


class PostGameScreen(Screen):
    def __init__(self, window, fps=60, bgcolor=None):
        super().__init__(window, fps, bgcolor)
        self.choice = ""
        self.mode = ""
        self.ball_side = ""
        self.p1_score = 0
        self.p2_score = 0
        self.Rect_upper = pygame.locals.Rect(
            WINDOW_WIDTH / 2 - 30, WINDOW_HEIGHT * 2 / 5 - 10, 100, 50
        )
        self.Rect_lower = pygame.locals.Rect(
            WINDOW_WIDTH / 2 - 30, WINDOW_HEIGHT * 3 / 5 - 10, 100, 50
        )

    def create_text_surface(self, text, size):
        """Function reused from previous lab"""
        arial = pygame.font.SysFont("arial", size)
        text_surface = arial.render(text, True, (0, 0, 0))

        return text_surface

    def process_event(self, event):
        if event.type == pygame.locals.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.Rect_upper.collidepoint(mouse_pos):
                self.mode = "welcome"
                self.running = False
            if self.Rect_lower.collidepoint(mouse_pos):
                self.mode = "quit"
                self.running = False

    def process_loop(self):
        pygame.font.init()

        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        window.fill((255, 255, 255))

        replay_text = self.create_text_surface("Replay", 24)
        quit_text = self.create_text_surface("Quit", 24)
        p1_score_text = self.create_text_surface(
            "P1 Score: {score}".format(score=self.p1_score), 24
        )
        p2_score_text = self.create_text_surface(
            "P2 Score: {score}".format(score=self.p2_score), 24
        )

        # draw rectangles for buttons
        pygame.draw.rect(window, (255, 227, 40), self.Rect_upper)
        pygame.draw.rect(window, (255, 227, 40), self.Rect_lower)

        window.blit(replay_text, (WINDOW_WIDTH / 2 - 15, WINDOW_HEIGHT * 2 / 5))
        window.blit(quit_text, (WINDOW_WIDTH / 2 - 15, WINDOW_HEIGHT * 3 / 5))
        window.blit(p1_score_text, (WINDOW_WIDTH * 2 / 5 - 40, WINDOW_HEIGHT * 1 / 5))
        window.blit(p2_score_text, (WINDOW_WIDTH * 3 / 5 - 35, WINDOW_HEIGHT * 1 / 5))

        pygame.display.flip()
