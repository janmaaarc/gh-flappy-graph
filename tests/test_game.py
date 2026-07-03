from gh_flappy_graph.game.animator import generate_frames
from gh_flappy_graph.game.pipes import build_pipes, day_level, quartile_thresholds
from gh_flappy_graph.game.renderer import render_frame
from gh_flappy_graph.github_client import ContributionDay, ContributionWeek
from gh_flappy_graph import constants


def make_weeks(day_lists):
    return [
        ContributionWeek(days=[ContributionDay(date="2026-01-01", count=c) for c in days])
        for days in day_lists
    ]


def test_busy_week_gets_tighter_gap():
    pipes = build_pipes(make_weeks([[0] * 7, [9] * 7]))
    assert pipes[0].gap_len == constants.GAP_DAYS_QUIET
    assert pipes[1].gap_len == constants.GAP_DAYS_BUSY


def test_gap_carved_at_quietest_days():
    pipes = build_pipes(make_weeks([[5, 5, 0, 0, 0, 5, 5]]))
    assert pipes[0].gap_start == 2


def test_build_pipes_deterministic():
    weeks = make_weeks([[1, 0, 2, 0, 3, 0, 4], [2, 2, 2, 2, 2, 2, 2]])
    assert build_pipes(weeks) == build_pipes(weeks)


def test_short_week_padded_to_seven_days():
    pipes = build_pipes(make_weeks([[3, 3]]))
    assert len(pipes[0].day_counts) == 7


def test_shade_bounds():
    thresholds = quartile_thresholds([1, 2, 3, 4, 5, 6, 7, 8])
    assert day_level(0, thresholds) == 0
    assert day_level(8, thresholds) == 4
    assert day_level(1, thresholds) == 1


def test_frames_scroll_everything_off_screen():
    frames = generate_frames(build_pipes(make_weeks([[1] * 7, [2] * 7])))
    assert frames
    last_pipes = frames[-1].pipes
    assert last_pipes == [] or all(
        p.x + constants.PIPE_WIDTH <= constants.SCROLL_SPEED for p in last_pipes
    )


def test_bird_stays_on_canvas():
    frames = generate_frames(build_pipes(make_weeks([[9] * 7, [0] * 7, [9] * 7])))
    for f in frames:
        assert 0 <= f.bird_y <= constants.CANVAS_HEIGHT


def test_render_frame_produces_canvas_sized_image():
    frames = generate_frames(build_pipes(make_weeks([[4] * 7, [8] * 7])))
    img = render_frame(frames[0])
    assert img.size == (constants.CANVAS_WIDTH, constants.CANVAS_HEIGHT)


def test_bird_never_clips_cells():
    import random
    random.seed(3)
    weeks = make_weeks([[random.choice([0, 2, 6, 15]) for _ in range(7)] for _ in range(52)])
    pipes = build_pipes(weeks)
    frames = generate_frames(pipes)
    margin = constants.BIRD_RADIUS
    for f in frames:
        for p in f.pipes:
            crossing = p.x - margin <= constants.BIRD_X <= p.x + constants.PIPE_WIDTH + margin
            if crossing:
                gap_top = p.gap_center - p.gap_height / 2
                gap_bottom = p.gap_center + p.gap_height / 2
                assert gap_top - 2 <= f.bird_y <= gap_bottom + 2, (
                    f"frame {f.index}: bird {f.bird_y:.0f} outside gap "
                    f"[{gap_top:.0f}, {gap_bottom:.0f}]"
                )


def test_all_bird_themes_render():
    frames = generate_frames(build_pipes(make_weeks([[4] * 7, [8] * 7])))
    for theme in constants.BIRD_THEMES:
        img = render_frame(frames[0], bird_theme=theme)
        assert img.size == (constants.CANVAS_WIDTH, constants.CANVAS_HEIGHT)


def test_identical_consecutive_weeks_have_distinct_indices():
    pipes = build_pipes(make_weeks([[0] * 7, [0] * 7]))
    assert pipes[0].week_index != pipes[1].week_index


def test_light_theme_renders():
    frames = generate_frames(build_pipes(make_weeks([[4] * 7, [8] * 7])))
    img = render_frame(frames[0], theme_name="light")
    assert img.size == (constants.CANVAS_WIDTH, constants.CANVAS_HEIGHT)


def test_stats_card_renders():
    from gh_flappy_graph.game.renderer import render_stats_card
    img = render_stats_card(score=52, total=6110, streak=41)
    assert img.size == (constants.CANVAS_WIDTH, constants.CANVAS_HEIGHT)


def test_longest_streak():
    from gh_flappy_graph.cli import longest_streak
    weeks = make_weeks([[0, 0, 0, 0, 1, 1, 1], [1, 1, 1, 0, 0, 0, 0]])
    assert longest_streak(weeks) == 6
