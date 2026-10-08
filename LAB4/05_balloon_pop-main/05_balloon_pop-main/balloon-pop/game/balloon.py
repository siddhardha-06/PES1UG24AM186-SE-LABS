"""
Balloon: falls from the top of the screen. The player must pop it
before it reaches the bottom. Balloons vary in size - this matters for
how click detection should work.
"""

import pygame

# Balloon types: each has its own color and the score change applied
# when it is popped.
NORMAL = "normal"
BONUS = "bonus"
PENALTY = "penalty"

BALLOON_TYPES = {
    NORMAL:  {"color": (220, 90, 120), "points": 10},   # pink: regular points
    BONUS:   {"color": (240, 190, 40), "points": 30},   # gold: extra points
    PENALTY: {"color": (60, 60, 70),   "points": -20},  # dark grey: loses points
}


class Balloon:
    def __init__(self, x, y, radius, speed, kind=NORMAL):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.kind = kind
        self.color = BALLOON_TYPES[kind]["color"]
        self.points = BALLOON_TYPES[kind]["points"]

    def update(self):
        self.y += self.speed

    def is_past_bottom(self, height):
        return self.y - self.radius > height

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius), int(self.y - self.radius),
            self.radius * 2, self.radius * 2,
        )
