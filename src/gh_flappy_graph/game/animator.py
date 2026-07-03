"""Advance pipes frame-by-frame and steer the bird toward each upcoming gap."""

import dataclasses
from dataclasses import dataclass

from gh_flappy_graph import constants
from gh_flappy_graph.game.bird import BirdState, next_bird_state
from gh_flappy_graph.game.pipes import Pipe


@dataclass(frozen=True)
class Frame:
    bird_y: float
    bird_velocity: float
    pipes: list[Pipe]
    index: int
    crashed: bool = False


def generate_frames(pipes: list[Pipe]) -> list[Frame]:
    if not pipes:
        return []

    bird = BirdState(y=constants.CANVAS_HEIGHT / 2)
    current = list(pipes)
    frames = []
    index = 0

    while current[-1].x + constants.PIPE_WIDTH > 0:
        ahead = next((p for p in current if p.x + constants.PIPE_WIDTH >= constants.BIRD_X), None)
        # busier weeks scroll faster: your grind is the difficulty curve
        speed = constants.SCROLL_SPEED * (1 + constants.SPEED_RAMP * (ahead.intensity if ahead else 0))
        current = [dataclasses.replace(p, x=p.x - speed) for p in current]

        upcoming = next(
            (p for p in current if p.x + constants.PIPE_WIDTH >= constants.BIRD_X),
            None,
        )
        target_y = upcoming.gap_center if upcoming else constants.CANVAS_HEIGHT / 2
        bird = next_bird_state(bird, target_y, index)

        visible = [p for p in current if p.x < constants.CANVAS_WIDTH and p.x + constants.PIPE_WIDTH > 0]
        frames.append(Frame(bird_y=bird.y, bird_velocity=bird.velocity, pipes=visible, index=index))
        index += 1

        # hardcore: a gapless wall reaching the bird ends the run with a tumble
        wall = next((p for p in visible if p.gap_len == 0), None)
        if wall and wall.x <= constants.BIRD_X + constants.BIRD_RADIUS:
            vy = 0.0
            ground = constants.CANVAS_HEIGHT - constants.GROUND_HEIGHT - constants.BIRD_RADIUS
            y = bird.y
            for _ in range(constants.CRASH_FRAMES):
                vy += constants.CRASH_GRAVITY
                y = min(y + vy, ground)
                frames.append(Frame(bird_y=y, bird_velocity=vy, pipes=visible, index=index, crashed=True))
                index += 1
            break

    return frames
