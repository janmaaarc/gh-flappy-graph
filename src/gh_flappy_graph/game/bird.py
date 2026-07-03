"""Bird autopilot: eases toward the center of the next gap. Decorative, not physics-accurate."""

import math
from dataclasses import dataclass

from gh_flappy_graph import constants


@dataclass(frozen=True)
class BirdState:
    y: float
    velocity: float = 0.0


def next_bird_state(bird: BirdState, target_y: float, tick: int) -> BirdState:
    delta = target_y - bird.y
    velocity = delta * constants.BIRD_EASE
    velocity = max(-constants.MAX_BIRD_SPEED, min(constants.MAX_BIRD_SPEED, velocity))
    bob = math.sin(tick * 0.35) * 1.6
    return BirdState(y=bird.y + velocity + bob, velocity=velocity)
