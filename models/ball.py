import random
import pygame
from constants import LIMITS


class Ball(pygame.sprite.Sprite):
    """
    Model of a (bouncing) ball.
    If gravity is True, the ball will obey to gravity (aka fall down).
    """

    def __init__(self, gravity=False, color=None, size=20):
        """Constructor"""
        super().__init__()

        self.size = size
        # The ball is a circle
        self.image = pygame.Surface((size, size))
        self.image.set_colorkey((0, 0, 0))

        if not color:
            color = (255, 0, 0)
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect()

        # Spawn in the middle of the screen
        self.rect.x = LIMITS["right"] // 2
        self.rect.y = LIMITS["down"] // 2

        # Start without moving
        self.hspeed = 0
        self.vspeed = 0

        # Gravity and off limits booleans
        self.respect_gravity = gravity
        self.off_limits = False

    def launch(self, direction=None, hspeed=10, vspeed=-20):
        """Launches the ball up in the air"""
        self.hspeed = hspeed
        if direction == "left":
            self.hspeed = -self.hspeed
        self.vspeed = vspeed

    def update(self):
        """Convenience method"""

        # The vertical speed decreases over time when subject to gravity
        if self.respect_gravity:
            self.vspeed += 1

        # If the ball is not off limits, make it move
        if not self.off_limits:
            self.rect.x += self.hspeed
            self.rect.y += self.vspeed

        # Check the ball did not go off limits
        if self.rect.x > LIMITS["right"] - self.size:
            self.rect.x = LIMITS["right"] - self.size
            self.off_limits = True
        elif self.rect.x < LIMITS["left"]:
            self.rect.x = LIMITS["left"]
            self.off_limits = True

        # Check whether we need to bounce the ball
        if self.rect.y > LIMITS["down"] - self.size:
            self.rect.y = LIMITS["down"] - self.size
            self.bounce("vertical")
        elif self.rect.y < LIMITS["up"]:
            self.rect.y = LIMITS["up"]
            self.bounce("vertical")

        # Prevent the ball from bouncing for ever when on the ground
        if (
            self.respect_gravity
            and -1 < self.vspeed < 1
            and self.rect.y >= LIMITS["down"] - (self.size + 5)
        ):
            self.vspeed = 0

    def bounce(self, direction=None, power=True, powershot=False):
        """Bounce the ball"""

        # Horizontal bounces slightly decrease horizontal speed
        if direction in ("right", "left", "horizontal"):
            self.hspeed = -self.hspeed * 0.8

        # Vertical bounces decrease vertical speed
        if direction in ("up", "down", "vertical"):
            self.vspeed = -self.vspeed * 0.5

        # Power bounce: increase the speed of the ball
        if power:
            self.hspeed *= 1.3
            self.vspeed *= 1.1

        # Powershot: Greatly increase ball speed, can be used at the same time as regular power bounce
        if powershot:
            self.hspeed *= 1.5
