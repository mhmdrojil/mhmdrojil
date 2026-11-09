#!/usr/bin/env python3
"""Refresh the STATS block in README.md from the GitHub REST API (stdlib only)."""

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

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
