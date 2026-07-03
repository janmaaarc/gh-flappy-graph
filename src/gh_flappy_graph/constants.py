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

BIRD_X = 110
BIRD_RADIUS = 9
BIRD_EASE = 0.22
MAX_BIRD_SPEED = 6.0

SCROLL_SPEED = 3.5

BG_TOP = (10, 14, 26)
BG_BOTTOM = (22, 30, 48)
GROUND_COLOR = (23, 30, 46)
GROUND_STRIPE = (40, 50, 72)
STAR_COLOR = (110, 120, 150)

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

PIPE_START_OFFSET = 40  # first pipe spawns just off-screen, no dead air

HEADER_COLOR = (200, 210, 230)
SCORE_COLOR = (200, 210, 230)
LEGEND_COLOR = (130, 145, 175)
MONTH_COLOR = (130, 145, 175)

# GitHub dark-theme contribution shades: level 0 (empty) to 4 (busiest).
DAY_SHADES = [
    (34, 42, 58),
    (14, 68, 41),
    (0, 109, 50),
    (38, 166, 65),
    (57, 211, 83),
]
CELL_OUTLINE = (8, 12, 20)


def row_y(row: int) -> float:
    return SKY_MARGIN + row * (CELL_SIZE + CELL_GAP)
