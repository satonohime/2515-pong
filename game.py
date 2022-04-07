import pygame

from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from screens.post_game_screen import PostGameScreen
from screens.game_screen import GameScreen
from screens.welcome_screen import WelcomeScreen
import os


class ScreenSwitcher:
    def __init__(self):
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.next = "welcome"
        self.p1_score = 0
        self.p2_score = 0
        self.quit = False
        self.num_rounds = 10

    def welcome(self):
        """
        Initialize welcome screen and play music
        """
        self.screen = WelcomeScreen(self.window)
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join("sound", "welcome_screen.mp3"))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
        self.screen.loop()
        self.next = self.screen.mode
        self.next_screen()

    def ranked(self):
        """
        Display ranked game mode with scores
        """
        self.screen = GameScreen(self.window)
        self.screen.p1_score = self.p1_score
        self.screen.p2_score = self.p2_score
        self.screen.ranked = True
        self.screen.loop()
        if self.screen.ball.off_limits:
            if self.screen.ball_side == "right":
                self.p1_score += 1
            elif self.screen.ball_side == "left":
                self.p2_score += 1
        if self.p1_score >= self.num_rounds or self.p2_score >= self.num_rounds:
            self.next = "post_game"
        self.next_screen()

    def practice(self):
        """
        Display practice game mode with scores
        """
        self.screen = GameScreen(self.window)
        self.screen.loop()
        if not self.screen.auto_close:
            self.next = "quit"
        else:
            self.next = "practice"
        self.next_screen()

    def post_game(self):
        """
        Display results screen with option for replay
        """
        self.screen = PostGameScreen(self.window)
        self.screen.p1_score = self.p1_score
        self.screen.p2_score = self.p2_score
        self.screen.loop()
        self.next = self.screen.mode
        self.p1_score = 0
        self.p2_score = 0
        self.next_screen()

    def next_screen(self):
        """
        Handle switching between screens
        """
        if self.next == "welcome":
            self.welcome()
        if self.next == "ranked":
            self.ranked()
        if self.next == "practice":
            self.practice()
        if self.next == "post_game":
            self.post_game()
        if self.next == "quit":
            pygame.quit()


def main():
    game = ScreenSwitcher()
    pygame.init()
    game.next_screen()


if __name__ == "__main__":
    main()
