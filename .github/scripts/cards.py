"""Generate the profile stats cards (stats, top languages, streak, pinned repos) as SVG.

Runs in GitHub Actions with GITHUB_TOKEN; no third-party services, no dependencies.
Usage: python cards.py <login> <out_dir> <repo> [<repo> ...]
"""
import datetime as dt
import json
import os
import pathlib
import sys
import textwrap
import urllib.request
from xml.sax.saxutils import escape

LOGIN, OUT, PINS = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3:]
OUT.mkdir(parents=True, exist_ok=True)

BG, BORDER, TITLE, TEXT, MUTED, ICON = "#0d1117", "#1d4636", "#00ff9c", "#e6edf3", "#8b949e", "#00ff9c"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Sans-Serif"

OCTICONS = {
    "star": "M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z",
    "commits": "M1.643 3.143 .427 1.927A.25.25 0 0 0 0 2.104V5.75c0 .138.112.25.25.25h3.646a.25.25 0 0 0 .177-.427L2.715 4.215a6.5 6.5 0 1 1-1.18 4.458.75.75 0 1 0-1.493.154 8.001 8.001 0 1 0 1.6-5.684ZM7.75 4a.75.75 0 0 1 .75.75v2.992l2.028.812a.75.75 0 0 1-.557 1.392l-2.5-1A.751.751 0 0 1 7 8.25v-3.5A.75.75 0 0 1 7.75 4Z",
    "pr": "M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25Zm5.677-.177L9.573.677A.25.25 0 0 1 10 .854V2.5h1A2.5 2.5 0 0 1 13.5 5v5.628a2.251 2.251 0 1 1-1.5 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354ZM3.75 2.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm0 9.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm8.25.75a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Z",
    "repo": "M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z",
}


def gql(query, **variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        body = json.load(r)
    if body.get("errors"):
        raise SystemExit(f"GraphQL error: {body['errors']}")
    return body["data"]


def card(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(label)}">\n'
            f'<style>text{{font-family:{FONT}}} .fade{{opacity:0;animation:fade .6s ease-in-out forwards}}'
            f'@keyframes fade{{to{{opacity:1}}}}</style>\n'
            f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="14" fill="{BG}" stroke="{BORDER}"/>\n'
            f'{body}\n</svg>\n')


def icon(name, x, y, color=ICON):
    return f'<path transform="translate({x} {y})" fill="{color}" d="{OCTICONS[name]}"/>'


def fmt(d, year=False):
    return d.strftime("%b %-d, %Y" if year else "%b %-d") if os.name != "nt" else \
        d.strftime("%b %d, %Y" if year else "%b %d").replace(" 0", " ")


# ------------------------------------------------------------------ data
user = gql("""query($login:String!){ user(login:$login){
  name createdAt
  pullRequests{ totalCount }
  contributionsCollection{ totalCommitContributions }
  repositories(first:100, ownerAffiliations:OWNER, isFork:false, privacy:PUBLIC){ nodes{
    name stargazerCount
    languages(first:20, orderBy:{field:SIZE, direction:DESC}){ edges{ size node{ name color } } } } }
}}""", login=LOGIN)["user"]

first_name = (user["name"] or LOGIN).split()[0]
repos = [r for r in user["repositories"]["nodes"] if r["name"].lower() != LOGIN.lower()]
stars = sum(r["stargazerCount"] for r in repos)

# ------------------------------------------------------------------ stats card
rows = [("star", "Total Stars Earned:", stars),
        ("commits", "Total Commits (last year):", user["contributionsCollection"]["totalCommitContributions"]),
        ("pr", "Total PRs:", user["pullRequests"]["totalCount"])]
body = f'<text x="25" y="35" font-size="18" font-weight="600" fill="{TITLE}">{escape(first_name)}\'s GitHub Stats</text>'
for i, (ic, label, value) in enumerate(rows):
    y = 55 + i * 25
    body += (f'<g class="fade" style="animation-delay:{150 + i * 150}ms">{icon(ic, 25, y)}'
             f'<text x="50" y="{y + 12.5}" font-size="14" font-weight="600" fill="{TEXT}">{label}</text>'
             f'<text x="245" y="{y + 12.5}" font-size="14" font-weight="700" fill="{TEXT}">{value}</text></g>')
(OUT / "stats.svg").write_text(card(360, 141, body, f"{first_name}'s GitHub stats"), encoding="utf-8")

# ------------------------------------------------------------------ top languages card
langs = {}
for r in repos:
    for e in r["languages"]["edges"]:
        n = e["node"]["name"]
        size, color = langs.get(n, (0, e["node"]["color"]))
        langs[n] = (size + e["size"], color or "#8b949e")
top = sorted(langs.items(), key=lambda kv: -kv[1][0])[:6]
total = sum(v[0] for _, v in top) or 1
bar_w, x = 310.0, 25.0
body = (f'<text x="25" y="35" font-size="18" font-weight="600" fill="{TITLE}">Most Used Languages</text>'
        f'<clipPath id="bar"><rect x="25" y="50" width="{bar_w}" height="8" rx="4"/></clipPath><g clip-path="url(#bar)">')
for name, (size, color) in top:
    w = bar_w * size / total
    body += f'<rect x="{x:.2f}" y="50" width="{w + 0.5:.2f}" height="8" fill="{color}"/>'
    x += w
body += "</g>"
for i, (name, (size, color)) in enumerate(top):
    cx, cy = 25 + (i % 2) * 165, 82 + (i // 2) * 25
    body += (f'<g class="fade" style="animation-delay:{300 + i * 150}ms"><circle cx="{cx + 5}" cy="{cy - 4}" r="5" fill="{color}"/>'
             f'<text x="{cx + 17}" y="{cy}" font-size="11" fill="{TEXT}">{escape(name)} {100 * size / total:.2f}%</text></g>')
h = max(140, 82 + ((len(top) + 1) // 2) * 25 - 2)
(OUT / "top-langs.svg").write_text(card(360, h, body, "Most used languages"), encoding="utf-8")

# ------------------------------------------------------------------ streak card
today = dt.datetime.now(dt.timezone.utc).date()
created = dt.date.fromisoformat(user["createdAt"][:10])
days = {}
start = created
while start <= today:
    end = min(start + dt.timedelta(days=364), today)
    cal = gql("""query($login:String!,$from:DateTime!,$to:DateTime!){ user(login:$login){
      contributionsCollection(from:$from,to:$to){ contributionCalendar{ weeks{ contributionDays{ date contributionCount } } } } } }""",
              login=LOGIN, **{"from": f"{start}T00:00:00Z", "to": f"{end}T23:59:59Z"})
    for wk in cal["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]:
        for d in wk["contributionDays"]:
            days[dt.date.fromisoformat(d["date"])] = d["contributionCount"]
    start = end + dt.timedelta(days=1)

total_contrib = sum(days.values())
ordered = sorted(d for d in days if d <= today)
longest, longest_range, run, run_start = 0, None, 0, None
for d in ordered:
    if days[d] > 0:
        run, run_start = (run + 1, run_start) if run else (1, d)
        if run > longest:
            longest, longest_range = run, (run_start, d)
    else:
        run = 0
# current streak: today may still be empty without breaking it
cur, d = 0, today if days.get(today, 0) > 0 else today - dt.timedelta(days=1)
cur_end = d
while days.get(d, 0) > 0:
    cur += 1
    d -= dt.timedelta(days=1)
cur_range = (d + dt.timedelta(days=1), cur_end) if cur else None


def span(r):
    if not r:
        return "—"
    a, b = r
    return fmt(a) if a == b else f"{fmt(a)} - {fmt(b)}"


W, H = 724, 195
c1, c2, c3 = W / 6, W / 2, W * 5 / 6
fire = ("M0 -14 C4 -8 9 -5 9 1 C9 7 5 11 0 11 C-5 11 -9 7 -9 1 C-9 -3 -6 -6 -4 -9 "
        "C-3 -5 -1 -3 1 -3 C1 -7 0 -11 0 -14 Z")
body = f'''<line x1="{W/3:.1f}" y1="28" x2="{W/3:.1f}" y2="170" stroke="{BORDER}"/>
<line x1="{2*W/3:.1f}" y1="28" x2="{2*W/3:.1f}" y2="170" stroke="{BORDER}"/>
<g class="fade" style="animation-delay:200ms" text-anchor="middle">
  <text x="{c1:.1f}" y="79" font-size="28" font-weight="700" fill="{TITLE}">{total_contrib}</text>
  <text x="{c1:.1f}" y="114" font-size="14" fill="{TEXT}">Total Contributions</text>
  <text x="{c1:.1f}" y="145" font-size="12" fill="{MUTED}">{fmt(created, True)} - Present</text>
</g>
<g class="fade" style="animation-delay:400ms" text-anchor="middle">
  <circle cx="{c2:.1f}" cy="71" r="40" fill="none" stroke="{TITLE}" stroke-width="5"/>
  <rect x="{c2-13:.1f}" y="14" width="26" height="26" fill="{BG}"/>
  <path transform="translate({c2:.1f} 28)" d="{fire}" fill="{TITLE}"/>
  <text x="{c2:.1f}" y="81" font-size="28" font-weight="700" fill="{TEXT}">{cur}</text>
  <text x="{c2:.1f}" y="140" font-size="14" font-weight="700" fill="{TITLE}">Current Streak</text>
  <text x="{c2:.1f}" y="166" font-size="12" fill="{MUTED}">{span(cur_range)}</text>
</g>
<g class="fade" style="animation-delay:600ms" text-anchor="middle">
  <text x="{c3:.1f}" y="79" font-size="28" font-weight="700" fill="{TITLE}">{longest}</text>
  <text x="{c3:.1f}" y="114" font-size="14" fill="{TEXT}">Longest Streak</text>
  <text x="{c3:.1f}" y="145" font-size="12" fill="{MUTED}">{span(longest_range)}</text>
</g>'''
(OUT / "streak.svg").write_text(card(W, H, body, f"{total_contrib} contributions, current streak {cur}, longest {longest}"), encoding="utf-8")

# ------------------------------------------------------------------ pinned repo cards
for name in PINS:
    r = gql("""query($o:String!,$n:String!){ repository(owner:$o,name:$n){
      name description stargazerCount forkCount primaryLanguage{ name color } } }""", o=LOGIN, n=name)["repository"]
    lines = textwrap.wrap(r["description"] or "", 56)[:3]
    body = (f'{icon("repo", 25, 22)}'
            f'<text x="50" y="35" font-size="18" font-weight="600" fill="{TITLE}">{escape(r["name"])}</text>')
    for i, line in enumerate(lines):
        body += f'<text x="25" y="{65 + i * 18}" font-size="13" fill="{TEXT}">{escape(line)}</text>'
    x, y = 25, 128
    if r["primaryLanguage"]:
        lang = r["primaryLanguage"]
        body += (f'<circle cx="{x + 6}" cy="{y - 4}" r="6" fill="{lang["color"] or MUTED}"/>'
                 f'<text x="{x + 18}" y="{y}" font-size="13" fill="{TEXT}">{escape(lang["name"])}</text>')
        x += 18 + len(lang["name"]) * 7.5 + 18
    body += (f'{icon("star", x, y - 12)}'
             f'<text x="{x + 22}" y="{y}" font-size="13" fill="{TEXT}">{r["stargazerCount"]}</text>')
    (OUT / f"pin-{name}.svg").write_text(card(400, 150, body, f"{r['name']}: {r['description'] or ''}"), encoding="utf-8")

print(f"stars={stars} langs={[n for n, _ in top]} total={total_contrib} current={cur} longest={longest}")
