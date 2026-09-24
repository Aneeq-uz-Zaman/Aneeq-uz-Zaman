"""Generates the GitHub stat cards used in README.md.

The public github-readme-stats instance is chronically 503, so the cards are
rendered here from the GitHub GraphQL API and committed as SVGs.
Run `python generate_stats.py` (needs an authenticated `gh`).
"""

import json
import subprocess
from collections import Counter

LOGIN = "Aneeq-uz-Zaman"
W, H = 480, 200

# Everything is scoped to PUBLIC, non-fork repos, so the card shows the same
# numbers a visitor to the profile would see — and does not drift depending on
# whether the token running this script can see private work.
QUERY = """
query($login:String!, $prq:String!){
  user(login:$login){
    createdAt
    contributionsCollection{ totalCommitContributions }
    repositories(first:100, ownerAffiliations:OWNER, isFork:false, privacy:PUBLIC){
      totalCount
      nodes{
        languages(first:12, orderBy:{field:SIZE, direction:DESC}){
          edges{ size node{ name color } }
        }
      }
    }
  }
  search(query:$prq, type:ISSUE){ issueCount }
}
"""

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
SANS = "ui-sans-serif,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"

THEMES = {
    "dark": {
        "panel": "#0e2331", "panel_op": "0.92", "hair": "rgba(255,255,255,0.08)",
        "text": "#e8f1f7", "muted": "#9db2c2", "dim": "#6f8797",
        "accent": ["#2ed3b7", "#8cf1de", "#ff8a3d"], "track": "rgba(255,255,255,0.07)",
        "frame": "#173340",
    },
    "light": {
        "panel": "#ffffff", "panel_op": "0.95", "hair": "rgba(7,16,24,0.10)",
        "text": "#0b1b26", "muted": "#4d6b7c", "dim": "#6f8797",
        "accent": ["#0f9e8a", "#2aa79b", "#e2661a"], "track": "rgba(7,16,24,0.07)",
        "frame": "#cbdde7",
    },
}


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fetch():
    raw = subprocess.run(
        ["gh", "api", "graphql", "-F", f"login={LOGIN}",
         "-F", f"prq=author:{LOGIN} is:pr is:public", "-f", f"query={QUERY}"],
        capture_output=True, text=True, check=True,
    ).stdout
    d = json.loads(raw)["data"]
    u = d["user"]
    repos = u["repositories"]

    langs, colors = Counter(), {}
    for node in repos["nodes"]:
        for edge in node["languages"]["edges"]:
            langs[edge["node"]["name"]] += edge["size"]
            colors[edge["node"]["name"]] = edge["node"]["color"] or "#8b949e"

    total = sum(langs.values()) or 1
    return {
        "repos": repos["totalCount"],
        "prs": d["search"]["issueCount"],
        "commits": u["contributionsCollection"]["totalCommitContributions"],
        "since": u["createdAt"][:7],
        "langs": [(n, s / total * 100, colors[n]) for n, s in langs.most_common()],
        "lang_count": len(langs),
    }


def shell(t, k, title, body):
    a1, a2, a3 = t["accent"]
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'fill="none" font-family="{SANS}" role="img" aria-label="{esc(title)}">',
        "  <defs>",
        f'    <linearGradient id="g-{k}" x1="0" y1="0" x2="1" y2="1" spreadMethod="reflect">'
        f'<stop offset="0" stop-color="{a1}"/><stop offset="0.5" stop-color="{a2}"/>'
        f'<stop offset="1" stop-color="{a3}"/>'
        f'<animateTransform attributeName="gradientTransform" type="translate" '
        f'values="-0.3 0;0.3 0;-0.3 0" dur="9s" repeatCount="indefinite"/></linearGradient>',
        "  </defs>",
        f'  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="{t["panel"]}" '
        f'fill-opacity="{t["panel_op"]}" stroke="{t["frame"]}"/>',
        f'  <text x="24" y="36" font-family="{MONO}" font-size="12.5" fill="{t["dim"]}" '
        f'letter-spacing="1.8">{esc(title)}</text>',
        f'  <line x1="24" y1="50" x2="{W - 24}" y2="50" stroke="{t["hair"]}"/>',
        f'  <line x1="24" y1="50" x2="96" y2="50" stroke="url(#g-{k})" stroke-width="1.5"/>',
        body,
        "</svg>",
    ]) + "\n"


def card_overview(d, theme, k):
    t = THEMES[theme]
    tiles = [
        (d["repos"], "Public repos"),
        (d["commits"], "Commits (12 mo)"),
        (d["prs"], "Pull requests"),
        (d["lang_count"], "Languages"),
    ]
    out = []
    for i, (value, label) in enumerate(tiles):
        x = 24 + (i % 2) * 228
        y = 104 + (i // 2) * 58
        begin = round(0.15 + i * 0.12, 2)
        out.append(
            f'  <g opacity="0"><animate attributeName="opacity" from="0" to="1" '
            f'begin="{begin}s" dur="0.6s" fill="freeze"/>'
            f'<text x="{x}" y="{y}" font-size="30" font-weight="800" fill="url(#g-{k})" '
            f'letter-spacing="-0.5">{esc(value)}</text>'
            f'<text x="{x}" y="{y + 21}" font-family="{MONO}" font-size="12" '
            f'fill="{t["muted"]}">{esc(label)}</text></g>'
        )
    out.append(
        f'  <text x="{W - 24}" y="36" text-anchor="end" font-family="{MONO}" font-size="11.5" '
        f'fill="{t["dim"]}">since {esc(d["since"])}</text>'
    )
    return "\n".join(out)


def card_langs(d, theme, k):
    t = THEMES[theme]
    shown = [l for l in d["langs"] if l[1] >= 1.0][:8]
    scale = 100 / sum(l[1] for l in shown)
    bar_x, bar_w = 24.0, float(W - 48)

    out = [f'  <rect x="24" y="66" width="{bar_w}" height="13" rx="6.5" fill="{t["track"]}"/>']
    out.append('  <g>')
    x = bar_x
    for i, (name, pct, color) in enumerate(shown):
        seg = bar_w * pct * scale / 100
        # square the inner joins, round only the two outer ends
        rx = 6.5 if i in (0, len(shown) - 1) else 0
        out.append(
            f'    <rect x="{x:.1f}" y="66" width="{max(seg, 2):.1f}" height="13" rx="{rx}" '
            f'fill="{color}" opacity="0"><animate attributeName="opacity" from="0" to="1" '
            f'begin="{round(0.15 + i * 0.08, 2)}s" dur="0.5s" fill="freeze"/></rect>'
        )
        x += seg
    out.append('  </g>')

    for i, (name, pct, color) in enumerate(shown):
        cx = 24 + (i % 2) * 228
        cy = 108 + (i // 2) * 24
        begin = round(0.30 + i * 0.07, 2)
        out.append(
            f'  <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{begin}s" '
            f'dur="0.5s" fill="freeze"/>'
            f'<circle cx="{cx + 5}" cy="{cy - 4}" r="5" fill="{color}"/>'
            f'<text x="{cx + 18}" y="{cy}" font-family="{MONO}" font-size="12.5" '
            f'fill="{t["text"]}">{esc(name)}</text>'
            f'<text x="{cx + 204}" y="{cy}" text-anchor="end" font-family="{MONO}" font-size="12.5" '
            f'fill="{t["muted"]}">{pct * scale:.1f}%</text></g>'
        )
    return "\n".join(out)


data = fetch()
for theme in ("dark", "light"):
    for name, title, render in (
        ("stats", "GITHUB AT A GLANCE", card_overview),
        ("langs", "MOST USED LANGUAGES", card_langs),
    ):
        key = f"{name}-{theme}"
        path = f"{key}.svg"
        with open(path, "w", encoding="utf-8") as f:
            f.write(shell(THEMES[theme], key, title, render(data, theme, key)))
        print(f"wrote {path}")
