"""Draw each Frame to a Pillow image."""

import hashlib

from PIL import Image, ImageDraw

from gh_flappy_graph import constants
from gh_flappy_graph.game.animator import Frame
from gh_flappy_graph.game.pipes import Pipe, day_level, quartile_thresholds

_STAR_COUNT = 45
_backgrounds: dict[str, Image.Image] = {}


def _lerp(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _background(theme_name: str) -> Image.Image:
    if theme_name in _backgrounds:
        return _backgrounds[theme_name]
    theme = constants.THEMES[theme_name]
    img = Image.new("RGB", (constants.CANVAS_WIDTH, constants.CANVAS_HEIGHT))
    draw = ImageDraw.Draw(img)

    sky_bottom = constants.CANVAS_HEIGHT - constants.GROUND_HEIGHT
    for y in range(sky_bottom):
        draw.line(
            [(0, y), (constants.CANVAS_WIDTH, y)],
            fill=_lerp(theme["bg_top"], theme["bg_bottom"], y / sky_bottom),
        )

    # deterministic star field so every frame shares the same sky
    for i in range(_STAR_COUNT):
        seed = int(hashlib.sha256(f"star:{i}".encode()).hexdigest(), 16)
        sx = seed % constants.CANVAS_WIDTH
        sy = (seed // constants.CANVAS_WIDTH) % (sky_bottom - 20)
        size = 2 if seed % 7 == 0 else 1
        draw.ellipse([sx, sy, sx + size, sy + size], fill=theme["star"])

    draw.rectangle(
        [0, sky_bottom, constants.CANVAS_WIDTH, constants.CANVAS_HEIGHT],
        fill=theme["ground"],
    )
    draw.line([(0, sky_bottom), (constants.CANVAS_WIDTH, sky_bottom)], fill=theme["ground_stripe"], width=2)
    _backgrounds[theme_name] = img
    return img


def _draw_week_column(draw: ImageDraw.ImageDraw, pipe: Pipe, thresholds: tuple[int, int, int], theme: dict) -> None:
    gap_rows = set(range(pipe.gap_start, pipe.gap_start + pipe.gap_len))
    for row in range(constants.DAYS_PER_WEEK):
        if row in gap_rows:
            continue
        y = constants.row_y(row)
        draw.rounded_rectangle(
            [pipe.x, y, pipe.x + constants.CELL_SIZE, y + constants.CELL_SIZE],
            radius=constants.CELL_RADIUS,
            fill=theme["day_shades"][day_level(pipe.day_counts[row], thresholds)],
            outline=theme["cell_outline"],
        )


def _draw_sparkles(draw: ImageDraw.ImageDraw, frame: Frame, theme: dict) -> None:
    """Celebrate clearing a max-intensity week with a small burst near the bird."""
    for pipe in frame.pipes:
        if pipe.intensity < constants.SPARKLE_INTENSITY:
            continue
        mid = pipe.x + constants.PIPE_WIDTH / 2
        if abs(mid - constants.BIRD_X) > 30:
            continue
        seed = int(hashlib.sha256(f"sparkle:{pipe.week_index}:{frame.index}".encode()).hexdigest(), 16)
        for i in range(5):
            dx = (seed >> (i * 8) & 0x3F) - 32
            dy = (seed >> (i * 8 + 6) & 0x3F) - 32
            sx, sy = constants.BIRD_X + dx, frame.bird_y + dy
            draw.polygon(
                [(sx, sy - 3), (sx + 2, sy), (sx, sy + 3), (sx - 2, sy)],
                fill=theme["sparkle"],
            )


def _draw_bird(draw: ImageDraw.ImageDraw, y: float, tick: int, velocity: float = 0.0, bird: dict | None = None, outline=(8, 12, 20)) -> None:
    colors = bird or constants.BIRD_THEMES["classic"]
    bx, by = constants.BIRD_X, y
    r = constants.BIRD_RADIUS
    tilt = max(-3, min(3, velocity))  # subtle beak-up/down by vertical speed

    flap = tick % 9
    wing_dy = -4 if flap < 3 else (0 if flap < 6 else 4)

    draw.ellipse([bx - r, by - r, bx + r, by + r], fill=colors["body"], outline=outline)
    draw.ellipse([bx - r + 3, by, bx + r - 3, by + r - 1], fill=colors["belly"])

    draw.polygon(
        [(bx - r + 2, by), (bx - r - 6, by + wing_dy), (bx - 1, by + 4)],
        fill=colors["wing"],
        outline=outline,
    )

    draw.polygon(
        [(bx + r - 1, by - 2 + tilt), (bx + r + 6, by + 1 + tilt * 1.5), (bx + r - 1, by + 4 + tilt)],
        fill=colors["beak"],
        outline=outline,
    )

    ex, ey = bx + 3, by - 4
    draw.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=constants.BIRD_EYE_WHITE)
    draw.ellipse([ex, ey - 1, ex + 2, ey + 1], fill=constants.BIRD_EYE_PUPIL)


def _draw_bold_text(draw: ImageDraw.ImageDraw, xy, text: str, fill, anchor: str) -> None:
    for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
        draw.text((xy[0] + dx, xy[1] + dy), text, fill=fill, anchor=anchor)


def render_frame(frame: Frame, score: int = 0, thresholds: tuple[int, int, int] = (1, 1, 1), bird_theme: str = "classic", theme_name: str = "dark") -> Image.Image:
    theme = constants.THEMES[theme_name]
    img = _background(theme_name).copy()
    draw = ImageDraw.Draw(img)

    ground_y = constants.CANVAS_HEIGHT - constants.GROUND_HEIGHT
    for pipe in frame.pipes:
        _draw_week_column(draw, pipe, thresholds, theme)
        if pipe.month_label:
            draw.text(
                (pipe.x + constants.PIPE_WIDTH / 2, ground_y + 6),
                pipe.month_label,
                fill=theme["month"],
                anchor="ma",
            )

    _draw_sparkles(draw, frame, theme)
    _draw_bird(draw, frame.bird_y, frame.index, frame.bird_velocity, constants.BIRD_THEMES[bird_theme], theme["cell_outline"])

    _draw_bold_text(draw, (constants.CANVAS_WIDTH - 16, 10), str(score), theme["score"], "ra")
    return img


def render_stats_card(score: int, total: int, streak: int, bird_theme: str = "classic", theme_name: str = "dark") -> Image.Image:
    theme = constants.THEMES[theme_name]
    img = _background(theme_name).copy()
    draw = ImageDraw.Draw(img)

    cx = constants.CANVAS_WIDTH / 2
    cy = constants.CANVAS_HEIGHT / 2 - 20
    _draw_bird(draw, cy - 34, 0, 0.0, constants.BIRD_THEMES[bird_theme], theme["cell_outline"])
    _draw_bold_text(draw, (cx, cy - 40), "Y E A R   C O M P L E T E", theme["score"], "mm")
    lines = [
        f"{total:,} contributions",
        f"{score} weeks flown",
        f"best streak: {streak} days",
    ]
    for i, line in enumerate(lines):
        draw.text((cx, cy + i * 22), line, fill=theme["score"], anchor="mm")
    return img


def render_frames(frames: list[Frame], bird_theme: str = "classic", theme_name: str = "dark") -> list[Image.Image]:
    thresholds = quartile_thresholds([c for f in frames for p in f.pipes for c in p.day_counts])
    images = []
    score = 0
    passed = set()
    for frame in frames:
        for pipe in frame.pipes:
            key = pipe.week_index
            if pipe.x + constants.PIPE_WIDTH < constants.BIRD_X and key not in passed:
                passed.add(key)
                score += 1
        images.append(render_frame(frame, score, thresholds, bird_theme, theme_name))
    return images
