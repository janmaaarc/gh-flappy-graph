"""Each pipe is a real contribution week: 7 day cells with a gap carved
through its quietest consecutive days."""

from dataclasses import dataclass

from gh_flappy_graph import constants
from gh_flappy_graph.github_client import ContributionWeek


@dataclass(frozen=True)
class Pipe:
    x: float
    week_index: int
    intensity: float  # 0..1, week total relative to the busiest week
    day_counts: tuple[int, ...]  # always 7, Sunday first
    gap_start: int  # first day-row removed
    gap_len: int  # how many day-rows removed
    month_label: str  # "Jan" on the first week of a month, else ""

    @property
    def gap_center(self) -> float:
        if self.gap_len == 0:
            return constants.CANVAS_HEIGHT / 2
        top = constants.row_y(self.gap_start)
        bottom = constants.row_y(self.gap_start + self.gap_len - 1) + constants.CELL_SIZE
        return (top + bottom) / 2

    @property
    def gap_height(self) -> float:
        if self.gap_len == 0:
            return 0.0
        return self.gap_len * constants.CELL_SIZE + (self.gap_len - 1) * constants.CELL_GAP


def quartile_thresholds(all_day_counts: list[int]) -> tuple[int, int, int]:
    """GitHub-style quartiles over nonzero days: thresholds for levels 2, 3, 4."""
    nonzero = sorted(c for c in all_day_counts if c > 0)
    if not nonzero:
        return (1, 1, 1)

    def pct(p: float) -> int:
        return nonzero[min(int(len(nonzero) * p), len(nonzero) - 1)]

    return (pct(0.25), pct(0.5), pct(0.75))


def day_level(count: int, thresholds: tuple[int, int, int]) -> int:
    if count <= 0:
        return 0
    return 1 + sum(1 for t in thresholds if count > t)


_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _pick_gap(counts: tuple[int, ...], gap_len: int, prev_start: int) -> int:
    """Quietest window of gap_len consecutive days, restricted to starts the
    bird can actually reach from the previous gap."""
    starts = [
        s
        for s in range(len(counts) - gap_len + 1)
        if abs(s - prev_start) <= constants.MAX_ROW_JUMP
    ]
    if not starts:
        starts = list(range(len(counts) - gap_len + 1))
    best_start, best_key = starts[0], None
    for start in starts:
        total = sum(counts[start : start + gap_len])
        key = (total, abs(start - prev_start))
        if best_key is None or key < best_key:
            best_start, best_key = start, key
    return best_start


def build_pipes(weeks: list[ContributionWeek], hardcore: bool = False) -> list[Pipe]:
    totals = [sum(day.count for day in week.days) for week in weeks]
    max_total = max(totals) if totals else 0

    pipes = []
    prev_month = None
    prev_start = 2
    for index, (week, total) in enumerate(zip(weeks, totals)):
        counts = tuple(day.count for day in week.days)
        if len(counts) < constants.DAYS_PER_WEEK:
            counts = counts + (0,) * (constants.DAYS_PER_WEEK - len(counts))

        intensity = (total / max_total) if max_total else 0.0
        if hardcore and total == 0:
            # a week with zero contributions has no gap: the run ends here
            gap_len = 0
            gap_start = 0
        else:
            gap_len = constants.GAP_DAYS_BUSY if intensity > 0.5 else constants.GAP_DAYS_QUIET
            gap_start = _pick_gap(counts, gap_len, prev_start)
            prev_start = gap_start

        month_label = ""
        if week.days:
            month = int(week.days[0].date.split("-")[1])
            if month != prev_month:
                month_label = _MONTHS[month - 1]
                prev_month = month

        pipes.append(
            Pipe(
                x=constants.CANVAS_WIDTH + constants.PIPE_START_OFFSET + index * constants.PIPE_SPACING,
                week_index=index,
                intensity=intensity,
                day_counts=counts,
                gap_start=gap_start,
                gap_len=gap_len,
                month_label=month_label,
            )
        )
        if hardcore and total == 0:
            break
    return pipes
