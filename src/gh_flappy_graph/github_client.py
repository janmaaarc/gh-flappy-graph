"""Fetch a user's GitHub contribution calendar via the GraphQL API."""

from dataclasses import dataclass

import httpx

GRAPHQL_URL = "https://api.github.com/graphql"

QUERY = """
query($userName: String!) {
  user(login: $userName) {
    contributionsCollection {
      contributionCalendar {
        weeks {
          contributionDays {
            contributionCount
            date
          }
        }
      }
    }
  }
}
"""


@dataclass(frozen=True)
class ContributionDay:
    date: str
    count: int


@dataclass(frozen=True)
class ContributionWeek:
    days: list[ContributionDay]


def fetch_contribution_weeks(username: str, token: str) -> list[ContributionWeek]:
    response = httpx.post(
        GRAPHQL_URL,
        headers={"Authorization": f"bearer {token}"},
        json={"query": QUERY, "variables": {"userName": username}},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    if "errors" in payload:
        raise RuntimeError(f"GitHub GraphQL error: {payload['errors']}")

    user = payload.get("data", {}).get("user")
    if user is None:
        raise RuntimeError(f"GitHub user '{username}' not found")

    weeks_raw = user["contributionsCollection"]["contributionCalendar"]["weeks"]
    return [
        ContributionWeek(
            days=[
                ContributionDay(date=d["date"], count=d["contributionCount"])
                for d in week["contributionDays"]
            ]
        )
        for week in weeks_raw
    ]
