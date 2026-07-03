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

CRASH_GRAVITY = 0.9  # hardcore mode: downward accel per frame after hitting a gapless week
CRASH_FRAMES = 24  # tumble frames rendered after the crash

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
    "halloween": {
        "bg_top": (20, 12, 28),
        "bg_bottom": (38, 22, 48),
        "ground": (30, 20, 40),
        "ground_stripe": (55, 38, 70),
        "star": (130, 110, 150),
        "score": (235, 215, 190),
        "month": (170, 140, 180),
        "cell_outline": (12, 8, 18),
        "sparkle": (255, 200, 80),
        "day_shades": [
            (40, 34, 50),
            (80, 45, 10),
            (150, 75, 10),
            (220, 110, 20),
            (255, 150, 40),
        ],
    },
    "ocean": {
        "bg_top": (8, 18, 32),
        "bg_bottom": (14, 34, 58),
        "ground": (16, 30, 48),
        "ground_stripe": (32, 52, 76),
        "star": (100, 130, 160),
        "score": (200, 225, 240),
        "month": (120, 150, 175),
        "cell_outline": (6, 12, 22),
        "sparkle": (150, 240, 255),
        "day_shades": [
            (30, 42, 60),
            (10, 60, 90),
            (0, 100, 130),
            (0, 150, 170),
            (60, 210, 220),
        ],
    },
    "sunset": {
        "bg_top": (25, 12, 30),
        "bg_bottom": (60, 25, 45),
        "ground": (40, 18, 36),
        "ground_stripe": (70, 35, 58),
        "star": (160, 120, 140),
        "score": (245, 220, 210),
        "month": (190, 140, 150),
        "cell_outline": (16, 8, 20),
        "sparkle": (255, 210, 150),
        "day_shades": [
            (45, 35, 55),
            (120, 40, 80),
            (190, 60, 90),
            (240, 100, 90),
            (255, 160, 90),
        ],
    },
    "mono": {
        "bg_top": (12, 12, 14),
        "bg_bottom": (28, 28, 32),
        "ground": (22, 22, 26),
        "ground_stripe": (44, 44, 50),
        "star": (90, 90, 100),
        "score": (225, 227, 232),
        "month": (140, 142, 150),
        "cell_outline": (8, 8, 10),
        "sparkle": (255, 255, 255),
        "day_shades": [
            (36, 38, 42),
            (70, 72, 78),
            (120, 124, 130),
            (180, 184, 190),
            (240, 242, 245),
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
