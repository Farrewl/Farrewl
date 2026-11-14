#!/usr/bin/env python3
"""Buat kartu stats.svg dan langs.svg bergaya pixel dari data GitHub (dijalankan GitHub Actions).

Pakai:  GITHUB_TOKEN=... GH_USER=username python3 scripts/gen_cards.py dist
Tes:    python3 scripts/gen_cards.py dist --demo
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

from pixel import (AQUA, BG, EDGE, EMERALD, GOLD, GREEN, MUTED, PANEL, PINK, RED, TEXT, WHITE,
                   icon, rect, svg, text)

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    pullRequests { totalCount }
    issues { totalCount }
    repositories(ownerAffiliations: [OWNER], isFork: false, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
    contributionsCollection {
      contributionCalendar { totalContributions }
    }
  }
}
"""
W = 640
PALETTE = [GREEN, AQUA, GOLD, PINK, RED]


def fetch(user, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": user}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "profile-cards"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if data.get("errors") or not data.get("data", {}).get("user"):
        raise SystemExit(f"GraphQL error: {data.get('errors')}")
    u = data["data"]["user"]
    repos = u["repositories"]["nodes"]
    langs = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    stats = {
        "stars": sum(r["stargazerCount"] for r in repos),
        "commits": None,
        "prs": u["pullRequests"]["totalCount"],
        "issues": u["issues"]["totalCount"],
        "repos": u["repositories"]["totalCount"],
        "followers": u["followers"]["totalCount"],
    }
    return stats, langs, u["contributionsCollection"]["contributionCalendar"]["totalContributions"]


def fmt(n):
    return str(n) if n < 1000 else (f"{n / 1000:.1f}k" if n < 10000 else f"{n // 1000}k")


def stats_card(stats, contrib):
    slots = [("star", "stars", stats["stars"]), ("merge", "PRs", stats["prs"]),
             ("issue", "issues", stats["issues"]), ("grass", "repos", stats["repos"]),
             ("person", "followers", stats["followers"])]
    parts = []
    for i, (ic, label, val) in enumerate(slots):
        x = 68 + i * 104
        parts.append(rect(x, 14, 88, 88, PANEL) + rect(x + 2, 16, 84, 2, "#2D333B") + rect(x + 2, 16, 2, 84, "#2D333B")
                     + f'<rect x="{x + 1}" y="15" width="86" height="86" fill="none" stroke="{EDGE}" stroke-width="2"/>'
                     + icon(ic, x + 44, 44, 4)
                     + text(x + 84, 96, fmt(val), 14, "#06240B", "end", ' transform="translate(2 2)"')
                     + text(x + 84, 96, fmt(val), 14, WHITE, "end")
                     + text(x + 44, 120, label, 9, MUTED, "middle"))
    # bar XP: penuh = 1 kontribusi per hari
    segs, filled = 38, round(min(1, contrib / 365) * 38)
    bar = []
    for i in range(segs):
        on = i < filled
        extra = f' class="sg" style="animation-delay:{0.6 + i * 0.04:.2f}s"' if on else ""
        bar.append(rect(16 + i * 16, 156, 14, 10, GREEN if on else "#21262D", extra))
    cap = text(W / 2, 186, "contributions in the last year", 9, MUTED, "middle")
    num = (text(W / 2 + 2, 150, str(contrib), 14, "#06240B", "middle")
           + text(W / 2, 148, str(contrib), 14, GREEN, "middle"))
    H = 196
    css = ".sg{animation:sg .01s steps(1,end) both}@keyframes sg{from{opacity:0}to{opacity:1}}"
    body = rect(0, 0, W, H, BG) + "".join(parts) + num + "".join(bar) + cap + \
        f'<rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" fill="none" stroke="{EDGE}" stroke-width="3"/>'
    return svg(W, H, body, css, "GitHub stats")


def langs_card(langs):
    total = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:4]
    rows = []
    for i, (name, size) in enumerate(top):
        pct = size / total * 100
        y = 20 + i * 30
        filled = max(1, round(pct / 100 * 24))
        color = PALETTE[i % len(PALETTE)]
        label = name if len(name) <= 12 else name[:11] + "~"
        rows.append(text(16, y + 12, label, 11, TEXT))
        for b in range(24):
            on = b < filled
            extra = f' class="sg" style="animation-delay:{0.3 + (i * 24 + b) * 0.015:.2f}s"' if on else ""
            rows.append(rect(190 + b * 15, y, 12, 16, color if on else "#21262D", extra))
        rows.append(text(W - 16, y + 12, f"{pct:.1f}%", 11, MUTED, "end"))
    if not top:
        rows.append(text(16, 32, "no code yet", 11, MUTED))
    H = 20 + max(1, len(top)) * 30 + 6
    css = ".sg{animation:sg .01s steps(1,end) both}@keyframes sg{from{opacity:0}to{opacity:1}}"
    body = rect(0, 0, W, H, BG) + "".join(rows) + \
        f'<rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" fill="none" stroke="{EDGE}" stroke-width="3"/>'
    return svg(W, H, body, css, "Most used languages")


def main():
    out = Path(next((a for a in sys.argv[1:] if not a.startswith("--")), "dist"))
    out.mkdir(parents=True, exist_ok=True)
    if "--demo" in sys.argv:
        stats = {"stars": 3, "commits": None, "prs": 4, "issues": 1, "repos": 9, "followers": 12}
        langs = {"C++": 52000, "Python": 41000, "C": 22000, "Shell": 4000}
        contrib = 187
    else:
        user = os.environ.get("GH_USER") or os.environ["GITHUB_REPOSITORY_OWNER"]
        stats, langs, contrib = fetch(user, os.environ["GITHUB_TOKEN"])
    (out / "stats.svg").write_text(stats_card(stats, contrib), encoding="utf-8")
    (out / "langs.svg").write_text(langs_card(langs), encoding="utf-8")
    print("ok:", out / "stats.svg", out / "langs.svg")


if __name__ == "__main__":
    main()
