"""CLI entrypoint: fetch contributions, build pipes, animate, render, save."""

import os

import httpx
import typer
from PIL import Image

from gh_flappy_graph import constants

from gh_flappy_graph.game.animator import generate_frames
from gh_flappy_graph.game.pipes import build_pipes
from gh_flappy_graph.game.renderer import render_frames
from gh_flappy_graph.github_client import fetch_contribution_weeks

app = typer.Typer(add_completion=False)


@app.command()
def main(
    username: str = typer.Argument(..., help="GitHub username to visualize"),
    output: str = typer.Option("gh-flappy-graph.gif", "--output", "-o", help="Output GIF path"),
    fps: int = typer.Option(30, "--fps", help="Frames per second"),
    max_frame: int = typer.Option(None, "--max-frame", help="Stop after this many frames"),
    bird: str = typer.Option("classic", "--bird", "-b", help="Bird theme: classic, red, blue, ghost"),
) -> None:
    if fps <= 0:
        typer.echo("--fps must be a positive integer.", err=True)
        raise typer.Exit(1)

    if bird not in constants.BIRD_THEMES:
        themes = ", ".join(constants.BIRD_THEMES)
        typer.echo(f"Unknown bird theme '{bird}'. Choose from: {themes}", err=True)
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

    pipes = build_pipes(weeks)
    frames = generate_frames(pipes)
    if max_frame:
        frames = frames[:max_frame]

    typer.echo(f"Rendering {len(frames)} frames...")
    images = render_frames(frames, bird_theme=bird)
    # show every 2nd frame at double duration: same speed, half the file
    images = images[::2]
    if not images:
        typer.echo("No contribution data to render.", err=True)
        raise typer.Exit(1)

    duration_ms = int(1000 / fps) * 2
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
