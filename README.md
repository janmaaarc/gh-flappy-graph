# gh-flappy-graph

Turn your GitHub contribution graph into a Flappy Bird animation.

Each week of contributions becomes a pipe. Busier weeks mean tighter gaps. The bird auto-flies through your entire year of coding.

![Example](example.gif?v=2)

## Usage

### GitHub Action

Update your game GIF daily. Add `.github/workflows/update-game.yml` to your profile repo:

```yaml
name: Update Flappy Graph

on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  update-game:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 2  # needed for the amend-based bloat prevention
      - uses: janmaaarc/gh-flappy-graph@v1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          output-path: 'gh-flappy-graph.gif'
```

Then display it in your README:

```markdown
![My Flappy Graph](gh-flappy-graph.gif)
```

**Action inputs:**

| Input | Required | Default | Description |
|---|---|---|---|
| `github-token` | yes | | Token for fetching contributions (usually `secrets.GITHUB_TOKEN`) |
| `username` | no | repo owner | Username to generate the game for |
| `output-path` | no | `gh-flappy-graph.gif` | Where to save the animation (`.gif` or `.webp`) |
| `fps` | no | `30` | Animation frame rate (1-60) |
| `bird` | no | `classic` | Bird theme: `classic`, `red`, `blue`, `ghost` |
| `theme` | no | `dark` | Canvas theme: `dark`, `light` |
| `weeks` | no | full year | Only render the last N weeks |
| `commit-message` | no | `Update flappy graph GIF` | Commit message |

The action amends the previous update commit (instead of stacking a multi-MB commit per day) whenever the last commit message matches `commit-message`.

### CLI

```bash
pip install git+https://github.com/janmaaarc/gh-flappy-graph.git

export GH_TOKEN=your_token   # needs read:user scope
gh-flappy-graph <username>

# options
gh-flappy-graph torvalds -o game.gif --fps 30 --max-frame 200
gh-flappy-graph torvalds --bird red
gh-flappy-graph torvalds --theme light      # for light-mode READMEs
gh-flappy-graph torvalds --weeks 12         # shorter loop, ~4x smaller file

# auto-switching dark/light in your README:
# generate both game-dark.gif and game-light.gif, then:
# <picture>
#   <source media="(prefers-color-scheme: dark)" srcset="game-dark.gif">
#   <img alt="Flappy Graph" src="game-light.gif">
# </picture>
```

## How it works

1. Fetches your contribution calendar via the GitHub GraphQL API.
2. Each week becomes a column of its real 7 day cells, colored with GitHub's contribution shades.
3. A gap is carved through the week's quietest consecutive days, so the bird literally flies through the days you didn't commit. Busy weeks get tighter gaps and scroll faster.
4. A bird eases through every gap on autopilot, a closing stats card shows totals and best streak, and the whole run is saved as a looping GIF.

Pipe placement is deterministic per profile, so the animation only changes when your contributions do.

## Development

```bash
git clone https://github.com/janmaaarc/gh-flappy-graph.git
cd gh-flappy-graph
uv sync
uv run pytest
```

## License

MIT
