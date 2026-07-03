"""Rendering, physics, and layout constants."""

# Columns are real contribution-graph weeks: 7 day cells, Sunday top.
CELL_SIZE = 24
CELL_GAP = 5
CELL_RADIUS = 5
DAYS_PER_WEEK = 7

SKY_MARGIN = 10
GROUND_HEIGHT = 24
GRID_HEIGHT = DAYS_PER_WEEK * CELL_SIZE + (DAYS_PER_WEEK - 1) * CELL_GAP
CANVAS_WIDTH = 820
CANVAS_HEIGHT = SKY_MARGIN * 2 + GRID_HEIGHT + GROUND_HEIGHT

PIPE_WIDTH = CELL_SIZE
PIPE_SPACING = 56

# Gap is carved from the quietest consecutive days of each week.
GAP_DAYS_QUIET = 3
GAP_DAYS_BUSY = 2
MAX_ROW_JUMP = 1  # ponytail: 1-row steps keep the bird collision-free at current scroll speed

PIPE_START_OFFSET = 40  # first pipe spawns just off-screen, no dead air

BIRD_X = 110
BIRD_RADIUS = 9
BIRD_EASE = 0.22
MAX_BIRD_SPEED = 6.0

SCROLL_SPEED = 3.5
SPEED_RAMP = 0.25  # busier weeks scroll up to 25% faster

SPARKLE_INTENSITY = 0.75  # min week intensity that triggers a pass sparkle

BIRD_EYE_WHITE = (255, 255, 255)
BIRD_EYE_PUPIL = (20, 20, 30)

# body, belly, wing, beak
BIRD_THEMES = {
    "classic": {
        "body": (255, 200, 40),
        "belly": (255, 236, 160),
        "wing": (235, 160, 20),
        "beak": (255, 120, 60),
    },
    "red": {
        "body": (230, 70, 60),
        "belly": (255, 180, 170),
        "wing": (190, 40, 35),
        "beak": (255, 190, 80),
    },
    "blue": {
        "body": (80, 150, 255),
        "belly": (190, 220, 255),
        "wing": (45, 105, 210),
        "beak": (255, 160, 70),
    },
    "ghost": {
        "body": (230, 235, 245),
        "belly": (255, 255, 255),
        "wing": (180, 190, 210),
        "beak": (255, 170, 90),
    },
}

# Canvas themes: GitHub dark and light contribution palettes.
THEMES = {
    "dark": {
        "bg_top": (10, 14, 26),
        "bg_bottom": (22, 30, 48),
        "ground": (23, 30, 46),
        "ground_stripe": (40, 50, 72),
        "star": (110, 120, 150),
        "score": (200, 210, 230),
        "month": (130, 145, 175),
        "cell_outline": (8, 12, 20),
        "sparkle": (255, 235, 130),
        # level 0 (empty) to 4 (busiest)
        "day_shades": [
            (34, 42, 58),
            (14, 68, 41),
            (0, 109, 50),
            (38, 166, 65),
            (57, 211, 83),
        ],
    },
    "light": {
        "bg_top": (255, 255, 255),
        "bg_bottom": (240, 244, 248),
        "ground": (234, 238, 242),
        "ground_stripe": (200, 208, 218),
        "star": (205, 212, 222),
        "score": (60, 70, 85),
        "month": (110, 120, 135),
        "cell_outline": (208, 215, 222),
        "sparkle": (240, 160, 20),
        "day_shades": [
            (235, 237, 240),
            (155, 233, 168),
            (64, 196, 99),
            (48, 161, 78),
            (33, 110, 57),
        ],
    },
}


def row_y(row: int) -> float:
    return SKY_MARGIN + row * (CELL_SIZE + CELL_GAP)
