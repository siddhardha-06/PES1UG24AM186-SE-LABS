"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (200, 230, 245)
COLOR_TEXT = (30, 30, 30)

_big_font = None  # created on first use, after pygame.init()


def draw_scene(surface, balloons):
    surface.fill(COLOR_BG)
    for b in balloons:
        pygame.draw.circle(surface, b.color, (int(b.x), int(b.y)), b.radius)
        pygame.draw.line(surface, (120, 120, 120), (b.x, b.y + b.radius), (b.x, b.y + b.radius + 12), 2)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_round_over(surface, font, reason, score):
    """End-of-round screen: dims the field and shows the final score."""
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 190))
    surface.blit(overlay, (0, 0))

    global _big_font
    if _big_font is None:
        _big_font = pygame.font.SysFont("consolas", 48, bold=True)
    big_font = _big_font
    cx, cy = surface.get_width() // 2, surface.get_height() // 2
    lines = [
        (font, reason, (180, 40, 40), cy - 60),
        (big_font, f"Final Score: {score}", COLOR_TEXT, cy),
        (font, "Press R to play again", COLOR_TEXT, cy + 60),
    ]
    for f, text, color, y in lines:
        surf = f.render(text, True, color)
        surface.blit(surf, surf.get_rect(center=(cx, y)))


def draw_banner(surface, font, text):
    surf = font.render(text, True, (180, 40, 40))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)
