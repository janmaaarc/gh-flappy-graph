"""Draw each Frame to a Pillow image."""

import hashlib

from PIL import Image, ImageDraw

from gh_flappy_graph import constants
from gh_flappy_graph.game.animator import Frame
from gh_flappy_graph.game.pipes import Pipe, day_shade, quartile_thresholds

_STAR_COUNT = 45


def _lerp(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _build_background() -> Image.Image:
    img = Image.new("RGB", (constants.CANVAS_WIDTH, constants.CANVAS_HEIGHT))
    draw = ImageDraw.Draw(img)

    sky_bottom = constants.CANVAS_HEIGHT - constants.GROUND_HEIGHT
    for y in range(sky_bottom):
        draw.line(
            [(0, y), (constants.CANVAS_WIDTH, y)],
            fill=_lerp(constants.BG_TOP, constants.BG_BOTTOM, y / sky_bottom),
        )

    # deterministic star field so every frame shares the same sky
    for i in range(_STAR_COUNT):
        seed = int(hashlib.sha256(f"star:{i}".encode()).hexdigest(), 16)
        sx = seed % constants.CANVAS_WIDTH
        sy = (seed // constants.CANVAS_WIDTH) % (sky_bottom - 20)
        size = 2 if seed % 7 == 0 else 1
        draw.ellipse([sx, sy, sx + size, sy + size], fill=constants.STAR_COLOR)

    draw.rectangle(
        [0, sky_bottom, constants.CANVAS_WIDTH, constants.CANVAS_HEIGHT],
        fill=constants.GROUND_COLOR,
    )
    draw.line([(0, sky_bottom), (constants.CANVAS_WIDTH, sky_bottom)], fill=constants.GROUND_STRIPE, width=2)
    return img


_BACKGROUND = _build_background()


def _draw_week_column(draw: ImageDraw.ImageDraw, pipe: Pipe, thresholds: tuple[int, int, int]) -> None:
    gap_rows = set(range(pipe.gap_start, pipe.gap_start + pipe.gap_len))
    for row in range(constants.DAYS_PER_WEEK):
        if row in gap_rows:
            continue
        y = constants.row_y(row)
        draw.rounded_rectangle(
            [pipe.x, y, pipe.x + constants.CELL_SIZE, y + constants.CELL_SIZE],
            radius=constants.CELL_RADIUS,
            fill=day_shade(pipe.day_counts[row], thresholds),
            outline=constants.CELL_OUTLINE,
        )


def _draw_bird(draw: ImageDraw.ImageDraw, y: float, tick: int, velocity: float = 0.0, theme: dict | None = None) -> None:
    colors = theme or constants.BIRD_THEMES["classic"]
    bx, by = constants.BIRD_X, y
    r = constants.BIRD_RADIUS
    tilt = max(-3, min(3, velocity))  # subtle beak-up/down by vertical speed

    flap = tick % 9
    wing_dy = -4 if flap < 3 else (0 if flap < 6 else 4)

    draw.ellipse([bx - r, by - r, bx + r, by + r], fill=colors["body"], outline=constants.CELL_OUTLINE)
    draw.ellipse([bx - r + 3, by, bx + r - 3, by + r - 1], fill=colors["belly"])

    draw.polygon(
        [(bx - r + 2, by), (bx - r - 6, by + wing_dy), (bx - 1, by + 4)],
        fill=colors["wing"],
        outline=constants.CELL_OUTLINE,
    )

    draw.polygon(
        [(bx + r - 1, by - 2 + tilt), (bx + r + 6, by + 1 + tilt * 1.5), (bx + r - 1, by + 4 + tilt)],
        fill=colors["beak"],
        outline=constants.CELL_OUTLINE,
    )

    ex, ey = bx + 3, by - 4
    draw.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=constants.BIRD_EYE_WHITE)
    draw.ellipse([ex, ey - 1, ex + 2, ey + 1], fill=constants.BIRD_EYE_PUPIL)


def _draw_legend(draw: ImageDraw.ImageDraw) -> None:
    y = constants.CANVAS_HEIGHT - constants.GROUND_HEIGHT + 6
    box = 11
    x = constants.CANVAS_WIDTH - 14 - (box + 4) * len(constants.DAY_SHADES) - 60
    draw.text((x - 8, y), "Less", fill=constants.LEGEND_COLOR, anchor="ra")
    for shade in constants.DAY_SHADES:
        draw.rounded_rectangle([x, y, x + box, y + box], radius=3, fill=shade)
        x += box + 4
    draw.text((x + 8, y), "More", fill=constants.LEGEND_COLOR, anchor="la")


def render_frame(frame: Frame, score: int = 0, thresholds: tuple[int, int, int] = (1, 1, 1), header: str = "", bird_theme: str = "classic") -> Image.Image:
    img = _BACKGROUND.copy()
    draw = ImageDraw.Draw(img)

    ground_y = constants.CANVAS_HEIGHT - constants.GROUND_HEIGHT
    for pipe in frame.pipes:
        _draw_week_column(draw, pipe, thresholds)
        # keep month labels clear of the fixed legend in the bottom-right
        if pipe.month_label and pipe.x < constants.CANVAS_WIDTH - 230:
            draw.text(
                (pipe.x + constants.PIPE_WIDTH / 2, ground_y + 6),
                pipe.month_label,
                fill=constants.MONTH_COLOR,
                anchor="ma",
            )

    _draw_bird(draw, frame.bird_y, frame.index, frame.bird_velocity, constants.BIRD_THEMES[bird_theme])

    if header:
        draw.text((14, 8), header, fill=constants.HEADER_COLOR, anchor="la")
    _draw_legend(draw)
    _draw_score(draw, score)
    return img


def _draw_score(draw: ImageDraw.ImageDraw, score: int) -> None:
    # default bitmap font is tiny; render 2x then paste would cost a copy per frame,
    # so fake weight by drawing at slight offsets instead
    text = str(score)
    x, y = constants.CANVAS_WIDTH - 16, 10
    for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
        draw.text((x + dx, y + dy), text, fill=constants.SCORE_COLOR, anchor="ra")


def render_frames(frames: list[Frame], header: str = "", bird_theme: str = "classic") -> list[Image.Image]:
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
        images.append(render_frame(frame, score, thresholds, header, bird_theme))
    return images
