"""
GameEngine: owns all balloons, spawns new ones, and handles clicks.

Three balloon types (normal, bonus, penalty), each with its own color
and points - see BALLOON_TYPES in game/balloon.py. The player has 3
lives: each non-penalty balloon that falls past the bottom costs one,
and the game ends at zero. No timer yet.
"""

import random

from game.balloon import Balloon, NORMAL, BONUS, PENALTY
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 45
STARTING_LIVES = 3

# Relative spawn chances for each balloon type.
SPAWN_WEIGHTS = {NORMAL: 70, BONUS: 15, PENALTY: 15}


class GameEngine:
    def __init__(self):
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = STARTING_LIVES
        self.game_over = False

    def _spawn_balloon(self):
        radius = random.randint(16, 44)
        x = random.randint(radius + 10, WIDTH - radius - 10)
        speed = random.uniform(1.5, 3.0)
        kind = random.choices(list(SPAWN_WEIGHTS), weights=list(SPAWN_WEIGHTS.values()))[0]
        self.balloons.append(Balloon(x=x, y=-radius, radius=radius, speed=speed, kind=kind))

    def handle_click(self, pos):
        if self.game_over:
            return
        popped = check_pop(self.balloons, pos)
        if popped is not None:
            self.balloons.remove(popped)
            self.score += popped.points

    def update(self):
        if self.game_over:
            return

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_balloon()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for b in self.balloons:
            b.update()

        # Missing a balloon costs a life, except penalty balloons, which
        # the player is supposed to let fall.
        remaining = []
        for b in self.balloons:
            if b.is_past_bottom(HEIGHT):
                if b.kind != PENALTY:
                    self.lives -= 1
            else:
                remaining.append(b)
        self.balloons = remaining

        if self.lives <= 0:
            self.lives = 0
            self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.balloons)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (10, 36))
        if self.game_over:
            renderer.draw_banner(surface, font, f"Game Over - Final Score: {self.score}")
