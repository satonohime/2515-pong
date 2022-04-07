import pygame
import random

from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from .base_screen import Screen
from models import Ball, Paddle
import os


class GameScreen(Screen):
    def __init__(self, *args, **kwargs):
        # Call the parent constructor
        super().__init__(*args, **kwargs)

        # Create objects and initialize parameters
        self.ball = Ball()
        self.base_speed = 2
        self.ball.launch(
            hspeed=random.choice([self.base_speed, -self.base_speed]),
            vspeed=random.choice([self.base_speed, -self.base_speed]),
        )
        self.p1 = Paddle("left")
        self.p2 = Paddle("right")
        self.paddles = pygame.sprite.Group()
        self.paddles.add(self.p1, self.p2)
        self.p1_score = 0
        self.p2_score = 0
        self.powershot_p1 = False
        self.powershot_p2 = False
        self.delay = False
        self.auto_close = False
        self.ranked = False
        self.ball_side = ""
        self.paddle_hit_sound = pygame.mixer.Sound(
            os.path.join("sound", "paddle_hit.mp3")
        )
        self.wall_hit_sound = pygame.mixer.Sound(os.path.join("sound", "wall_hit.mp3"))
        self.out_sound = pygame.mixer.Sound(os.path.join("sound", "out_bound.mp3"))
        self.powershot_charge = pygame.mixer.Sound(
            os.path.join("sound", "powershot.mp3")
        )
        self.win_text = self.create_text_surface("POINT: PLAYER 1")

        # Adjust volume of sounds
        self.sounds = [
            self.paddle_hit_sound,
            self.wall_hit_sound,
            self.out_sound,
            self.powershot_charge,
        ]
        for sound in self.sounds:
            sound.set_volume(0.2)

    def process_event(self, event):
        # In this screen, we don't have events to manage - pass
        pass

    def create_text_surface(self, text):
        """
        Code resued from L2_event_loop.py
        """
        arial = pygame.font.SysFont("arial", 24)
        text_surface = arial.render(text, True, (0, 0, 0))
        return text_surface

    def process_loop(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            self.p2.up()
        if keys[pygame.K_l]:
            self.p2.down()
        if keys[pygame.K_LSHIFT]:
            self.powershot_p1 = True
            pygame.mixer.Sound.play(self.powershot_charge)
        if keys[pygame.K_q]:
            self.p1.up()
        if keys[pygame.K_a]:
            self.p1.down()
        if keys[pygame.K_RSHIFT]:
            self.powershot_p2 = True
            pygame.mixer.Sound.play(self.powershot_charge)

        if self.ball.rect.y + self.ball.size >= WINDOW_HEIGHT:
            pygame.mixer.Sound.play(self.wall_hit_sound)
            if -1.0 < self.ball.vspeed < 0:
                self.ball.vspeed = -1.0
        elif self.ball.rect.y <= self.ball.size:
            pygame.mixer.Sound.play(self.wall_hit_sound)
            if 0 < self.ball.vspeed < 1.0:
                self.ball.vspeed = 1.0

        if self.p1.rect.colliderect(self.ball.rect):
            self.ball.rect.x = self.p1.rect.x + self.p1.size[0] + self.ball.size / 2
            pygame.mixer.Sound.play(self.paddle_hit_sound)
            if self.powershot_p1:
                self.ball.bounce("right", True, True)
            else:
                self.ball.bounce("right")

        if self.p2.rect.colliderect(self.ball.rect):
            self.ball.rect.x = self.p2.rect.x - self.ball.size
            pygame.mixer.Sound.play(self.paddle_hit_sound)
            if self.powershot_p2:
                self.ball.bounce("left", True, True)
            else:
                self.ball.bounce("left")

        if self.ball.hspeed > 0:
            self.ball_side = "right"
        else:
            self.ball_side = "left"

        # Update the ball position
        self.ball.update()

        # Update the paddles' positions
        self.paddles.update()

        # Blit everything
        self.paddles.draw(self.window)

        p1_score_text = self.create_text_surface(str(self.p1_score))
        p2_score_text = self.create_text_surface(str(self.p2_score))

        if self.ranked:
            self.window.blit(p1_score_text, (30, 30))
            self.window.blit(p2_score_text, (WINDOW_WIDTH - 30, 30))
        self.window.blit(self.ball.image, self.ball.rect)

        if self.delay:
            pygame.mixer.Sound.play(self.out_sound)
            self.window.blit(self.win_text, (WINDOW_WIDTH / 2 - 50, WINDOW_HEIGHT / 2))
            pygame.display.flip()
            pygame.time.delay(3000)

            # reset ball launch direction
            self.ball.launch(
                hspeed=random.choice([self.base_speed, -self.base_speed]),
                vspeed=random.choice([self.base_speed, -self.base_speed]),
            )

            # indicate that screen has not been force closed
            self.auto_close = True
            self.running = False

        if self.ball.off_limits:
            if self.ball_side == "left":
                self.win_text = self.create_text_surface("POINT: PLAYER 2")
            self.bgcolor = (255, 178, 178)
            self.delay = True
