#!/usr/bin/env python3
"""Refresh the STATS block in README.md from the GitHub REST API (stdlib only)."""

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

USER = os.environ.get("GH_USER", "mhmdrojil")
README = "README.md"
START, END = "<!-- STATS:START -->", "<!-- STATS:END -->"
TOKEN = (
    os.environ.get("STATS_TOKEN")
    or os.environ.get("GITHUB_TOKEN")
    or os.environ.get("GH_TOKEN")
)


def api(path):
    req = urllib.request.Request("https://api.github.com" + path)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", USER)
    if TOKEN:
        req.add_header("Authorization", "Bearer " + TOKEN)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def try_api(path, default=None):
    try:
        return api(path)
    except (urllib.error.URLError, TimeoutError, ValueError) as e:
        print(f"warn: {path}: {e}", file=sys.stderr)
        return default


def graphql(query, variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": USER,
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def calendar(days=365):
    """Contribution days for the last N days, oldest first."""
    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          totalCommitContributions
          restrictedContributionsCount
          contributionCalendar {
            weeks { contributionDays { date contributionCount } }
          }
        }
      }
    }"""
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    try:
        data = graphql(
            query,
            {
                "login": USER,
                "from": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "to": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
        )["data"]["user"]["contributionsCollection"]
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError, TypeError) as e:
        print(f"warn: graphql: {e}", file=sys.stderr)
        return None, None
    flat = [d for w in data["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    return data["totalCommitContributions"] + data["restrictedContributionsCount"], flat


def streak(days):
    """Current consecutive days with at least one contribution."""
    counts = {d["date"]: d["contributionCount"] for d in days}
    today = datetime.now(timezone.utc).date()
    cursor = today if counts.get(today.isoformat(), 0) else today - timedelta(days=1)
    n = 0
    while counts.get(cursor.isoformat(), 0) > 0:
        n += 1
        cursor -= timedelta(days=1)
    return n


def card(path, label, value, caption, accent):
    def esc(s):
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="200" height="112" viewBox="0 0 200 112" role="img" aria-label="{esc(label)}: {esc(value)}">
  <style>
    .c{{fill:#f6f8fa;stroke:#d1d9e0;stroke-width:1}}
    .l{{font:600 11px -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#59636e;letter-spacing:.08em}}
    .v{{font:700 32px -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:{accent}}}
    .s{{font:400 11px -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;fill:#818b98}}
  </style>
  <rect class="c" x=".5" y=".5" width="199" height="111" rx="10"/>
  <text class="l" x="16" y="30">{esc(label).upper()}</text>
  <text class="v" x="16" y="70">{esc(value)}</text>
  <text class="s" x="16" y="92">{esc(caption)}</text>
</svg>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)


def bar(pct, width=18):
    n = max(1, round(pct / 100 * width)) if pct > 0 else 0
    return "█" * n + "░" * (width - n)


def main():
    user = api(f"/users/{USER}")
    repos = []
    for page in range(1, 6):
        path = (
            f"/user/repos?affiliation=owner&visibility=all&sort=pushed&per_page=100&page={page}"
            if TOKEN
            else f"/users/{USER}/repos?sort=pushed&per_page=100&page={page}"
        )
        chunk = try_api(path, [])
        if not chunk:
            break
        repos += chunk
        if len(chunk) < 100:
            break

    owned = [r for r in repos if not r.get("fork")]
    public = [r for r in owned if not r.get("private")]
    stars = sum(r.get("stargazers_count", 0) for r in public)
    forks = sum(r.get("forks_count", 0) for r in public)
    # ponytail: primary language weighted by repo size; swap to /languages per repo if it must be byte-exact
    langs = {}
    for r in owned:
        if r.get("language"):
            langs[r["language"]] = langs.get(r["language"], 0) + max(r.get("size", 0), 1)
    total_lang = sum(langs.values()) or 1

    commits = try_api(f"/search/commits?q=author:{USER}&per_page=1", {}).get("total_count")
    year_commits, days = calendar()
    os.makedirs("assets", exist_ok=True)
    if commits:
        card("assets/stats-total-commits.svg", "Total commits", f"{commits:,}", "all time", "#1f6feb")
    if year_commits is not None:
        per_day = year_commits / max(len(days), 1)
        card("assets/stats-streak.svg", "Current streak", f"{streak(days)} days", "consecutive active days", "#bf8700")
        card("assets/stats-commits-day.svg", "Commits / day", f"{per_day:.1f}", f"{year_commits:,} in the last year", "#1a7f37")

    head = [
        f"**Repos** {len(repos)} · **Public** {len(public)} · **Private** {len(owned) - len(public)} · "
        f"**Stars** {stars} · **Forks** {forks} · "
        f"**Followers** {user['followers']} · **Following** {user['following']}"
        + (f" · **Commits** {commits:,}" if commits else ""),
        "",
    ]

    rows = [f"_Updated {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC_", ""]
    if langs:
        top_langs = [
            (name, size / total_lang * 100)
            for name, size in sorted(langs.items(), key=lambda kv: -kv[1])[:6]
        ]
        rows += ["### Languages", "```"]
        for name, pct in top_langs:
            if pct >= 0.1:
                rows.append(f"{name:<14} {bar(pct)} {pct:5.1f}%")
        rows += ["```", ""]

    stats = f"{START}\n" + "\n".join(head + rows).rstrip() + f"\n{END}"

    with open(README, encoding="utf-8") as f:
        readme = f.read()
    if START in readme and END in readme:
        readme, n = re.subn(
            re.escape(START) + r".*?" + re.escape(END), lambda _: stats, readme, flags=re.S
        )
        if n != 1:
            sys.exit("error: more than one STATS block in README")
    else:
        readme = readme.rstrip() + "\n\n## 📊 GitHub Stats\n\n" + stats + "\n"

    with open(README, "w", encoding="utf-8") as f:
        f.write(readme)
    print("README stats updated")


if __name__ == "__main__":
    main()
