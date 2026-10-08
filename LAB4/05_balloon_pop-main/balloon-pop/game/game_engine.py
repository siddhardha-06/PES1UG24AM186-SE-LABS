"""
GameEngine: owns all balloons, spawns new ones, and handles clicks.

Three balloon types (normal, bonus, penalty), each with its own color
and points - see BALLOON_TYPES in game/balloon.py. The player has 3
lives: each non-penalty balloon that falls past the bottom costs one,
and the game ends at zero. Each round also lasts 30 seconds. When time
or lives run out the round ends, the final score is shown, and
new_round() starts again from scratch.
"""

import math
import random

from game.balloon import Balloon, NORMAL, BONUS, PENALTY
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 45
STARTING_LIVES = 3
ROUND_SECONDS = 30

# Relative spawn chances for each balloon type.
SPAWN_WEIGHTS = {NORMAL: 70, BONUS: 15, PENALTY: 15}


class GameEngine:
    def __init__(self):
        self.new_round()

    def new_round(self):
        """Reset score, lives, timer and balloons for a fresh round."""
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = STARTING_LIVES
        self.time_left = ROUND_SECONDS
        self.game_over = False
        self.end_reason = ""

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

    def update(self, dt):
        """Advance the game by dt seconds."""
        if self.game_over:
            return

        self.time_left -= dt
        if self.time_left <= 0:
            self.time_left = 0
            self.game_over = True
            self.end_reason = "Time's up!"
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
            self.end_reason = "Out of lives!"

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.balloons)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (10, 36))
        renderer.draw_text(surface, font, f"Time: {math.ceil(self.time_left)}", (10, 62))
        if self.game_over:
            renderer.draw_round_over(surface, font, self.end_reason, self.score)
