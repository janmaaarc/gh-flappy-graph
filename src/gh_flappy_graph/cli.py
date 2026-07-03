"""CLI entrypoint: fetch contributions, build pipes, animate, render, save."""

import os

import httpx
import typer
from PIL import Image

from gh_flappy_graph import constants
from gh_flappy_graph.game.animator import generate_frames
from gh_flappy_graph.game.pipes import build_pipes
from gh_flappy_graph.game.renderer import render_frames, render_stats_card
from gh_flappy_graph.github_client import fetch_contribution_weeks

app = typer.Typer(add_completion=False)


def longest_streak(weeks) -> int:
    best = run = 0
    for week in weeks:
        for day in week.days:
            run = run + 1 if day.count > 0 else 0
            best = max(best, run)
    return best


@app.command()
def main(
    username: str = typer.Argument(..., help="GitHub username to visualize"),
    output: str = typer.Option("gh-flappy-graph.gif", "--output", "-o", help="Output GIF/WebP path"),
    fps: int = typer.Option(30, "--fps", help="Frames per second"),
    max_frame: int = typer.Option(None, "--max-frame", help="Stop after this many frames"),
    bird: str = typer.Option("classic", "--bird", "-b", help="Bird theme: classic, red, blue, ghost"),
    theme: str = typer.Option("dark", "--theme", "-t", help="Canvas theme: dark, light, halloween, ocean, sunset, mono"),
    weeks_limit: int = typer.Option(None, "--weeks", "-w", help="Only the last N weeks"),
    hardcore: bool = typer.Option(False, "--hardcore", help="A zero-contribution week ends the run"),
) -> None:
    if not 1 <= fps <= 60:
        typer.echo("--fps must be between 1 and 60.", err=True)
        raise typer.Exit(1)

    if bird not in constants.BIRD_THEMES:
        themes = ", ".join(constants.BIRD_THEMES)
        typer.echo(f"Unknown bird theme '{bird}'. Choose from: {themes}", err=True)
        raise typer.Exit(1)

    if theme not in constants.THEMES:
        typer.echo(f"Unknown theme '{theme}'. Choose from: {', '.join(constants.THEMES)}", err=True)
        raise typer.Exit(1)

    if weeks_limit is not None and weeks_limit <= 0:
        typer.echo("--weeks must be a positive integer.", err=True)
        raise typer.Exit(1)

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        typer.echo("Set GH_TOKEN or GITHUB_TOKEN to a GitHub token with read:user scope.", err=True)
        raise typer.Exit(1)

    typer.echo(f"Fetching contributions for {username}...")
    try:
        weeks = fetch_contribution_weeks(username, token)
    except (httpx.HTTPError, RuntimeError) as e:
        typer.echo(f"Failed to fetch contributions: {e}", err=True)
        raise typer.Exit(1)

    if weeks_limit:
        weeks = weeks[-weeks_limit:]

    pipes = build_pipes(weeks, hardcore=hardcore)
    frames = generate_frames(pipes)
    if max_frame:
        frames = frames[:max_frame]

    typer.echo(f"Rendering {len(frames)} frames...")
    images = render_frames(frames, bird_theme=bird, theme_name=theme)
    if not images:
        typer.echo("No contribution data to render.", err=True)
        raise typer.Exit(1)

    # show every 2nd frame at double duration: same speed, half the file
    images = images[::2]

    duration_ms = int(1000 / fps) * 2

    # hold a closing stats card for ~2 seconds
    total = sum(day.count for week in weeks for day in week.days)
    died_week = ""
    survived = len(pipes)
    if hardcore and pipes and pipes[-1].gap_len == 0:
        died_week = weeks[len(pipes) - 1].days[0].date
        survived = len(pipes) - 1
    card = render_stats_card(survived, total, longest_streak(weeks), bird, theme, died_week)
    images.extend([card] * max(int(2000 / duration_ms), 1))

    if output.lower().endswith(".webp"):
        images[0].save(
            output,
            save_all=True,
            append_images=images[1:],
            duration=duration_ms,
            loop=0,
            quality=80,
            method=4,
        )
    else:
        # single shared palette keeps GIF inter-frame compression effective
        palette_source = images[len(images) // 2].quantize(colors=128, dither=Image.NONE)
        images = [img.quantize(palette=palette_source, dither=Image.NONE) for img in images]
        images[0].save(
            output,
            save_all=True,
            append_images=images[1:],
            duration=duration_ms,
            loop=0,
            optimize=True,
        )
    typer.echo(f"Saved {output} ({len(images)} frames, {len(weeks)} weeks of data)")


if __name__ == "__main__":
    app()
