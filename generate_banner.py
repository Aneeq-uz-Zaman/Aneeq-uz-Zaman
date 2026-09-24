"""Generates dark.svg / light.svg — the animated banner at the top of README.md.

Run `python generate_banner.py` after editing the PROFILE data below.
Colors mirror the portfolio at aneequzzaman.vercel.app.
"""

import random

W, H = 1180, 610

PROFILE = {
    "name": "Muhammad Aneeq Uz Zaman",
    "handle": "aneeq-uz-zaman",
    "roles": [
        "Full Stack Developer",
        "Python Automation Engineer",
        "Data Science Student",
        "MERN Stack Builder",
    ],
    "rows": [
        ("Location ", "Lahore, Pakistan"),
        ("Education", "BS Data Science — PUCIT (CGPA 3.60/4.0)"),
        ("Focus    ", "Automation · Scraping · MERN · Data"),
        ("Portfolio", "aneequzzaman.vercel.app"),
        ("Email    ", "aneeq24dec@gmail.com"),
    ],
    "stack": [
        "Python", "JavaScript", "React", "Next.js", "Node.js", "Express",
        "MongoDB", "Tailwind", "Pandas", "Selenium", "C++", "SQL",
    ],
    "links": [
        ("github", "Aneeq-uz-Zaman"),
        ("linkedin", "in/aneeq-uz-zaman"),
        ("globe", "aneequzzaman.vercel.app"),
    ],
}

# ASCII portrait, derived from the headshot on the portfolio site.
PORTRAIT = r"""
              *#%%%%#+
          #%@@@%#%%@@@@%
       %@@@@@@@@%%@@@%%@@@%#*
      @@@@@@@@@@@@@@@@@@@@@@@@@@%#
     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
    #@@@@@@@@@#+==----=*%@@@@@@@@@@@@@*
     #@@@@@%=:..........:=*@@@@@@@@@@@@@
       #@@=................-+@@@@@@@@@@@@
        @-..........:-==+++-:-+*%@@@@@@@@%
      %@+.-=::..:-+#@@@@%#**##+==*#@@@@@@@
     @@@%@@@@%#--*@@%%%#+=+==*#*+++%@@@@@@
     @@@+=##%%%..=**+*=+=-%%*=-=+++%@@@@@@
      @%-##+=-:.:--:::...::::::-=++%@@#++%
       %=*-:::..----:........:--+++%@+====
        -.......:..-=......::--+***@%-*#.-
        -....=:=**++*....::---=+**%@%=+-:=
        =....*@%@@@*=--:::::--=*#%%@%=-:++
        +:.-*%+---=*%@@@+:--=+**#%@@%#+=:
         *.%@+::---==-:-=-=*####%%@@#+@
         @=-::+#*=--::::-=+*#%%%%@@@+*
          @=:..::..:::-+*#%##%@@@@@#+#
          *@#*++###%##%@@@@@@@@@@%#***
            %@@@@@@@@@@@@@@@@@%%#*++#@@
               #@@@@@@@@@@@%%##*==+%@@@@
                =###%#######*+--+#@@%%%@@
                +===+++***+=:-+%@@%%%%%%@@*
               @@-++++===-:-*%@@%%%%%%%%%%@@@#+
             %@@@=-=----:=*@@@%%%%%%%%%%%%%@@@@@@#
""".strip("\n").split("\n")

THEMES = {
    "dark": {
        "bg": "#071018",
        "bg2": "#0b1b26",
        "panel": "#0e2331",
        "panel_op": "0.72",
        "head": "#16303f",
        "hair": "rgba(255,255,255,0.08)",
        "text": "#e8f1f7",
        "muted": "#9db2c2",
        "dim": "#6f8797",
        "accent": ["#2ed3b7", "#8cf1de", "#ff8a3d"],
        "chip_fill": "rgba(46,211,183,0.10)",
        "chip_stroke": "rgba(46,211,183,0.35)",
        "frame": "#173340",
        "glass": "rgba(255,255,255,0.06)",
        "shadow_op": "0.55",
        "noise_op": "0.045",
        "particle": "#2ed3b7",
        "cursor": "#ff8a3d",
    },
    "light": {
        "bg": "#f3f8fb",
        "bg2": "#e4eff5",
        "panel": "#ffffff",
        "panel_op": "0.80",
        "head": "#dcebf2",
        "hair": "rgba(7,16,24,0.10)",
        "text": "#0b1b26",
        "muted": "#4d6b7c",
        "dim": "#6f8797",
        "accent": ["#0f9e8a", "#2aa79b", "#e2661a"],
        "chip_fill": "rgba(15,158,138,0.10)",
        "chip_stroke": "rgba(15,158,138,0.35)",
        "frame": "#cbdde7",
        "glass": "rgba(255,255,255,0.55)",
        "shadow_op": "0.16",
        "noise_op": "0.03",
        "particle": "#0f9e8a",
        "cursor": "#e2661a",
    },
}

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
SANS = "ui-sans-serif,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"

ICONS = {
    "github": '<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.9a3.4 3.4 0 0 0-.9-2.6c3-.3 6.2-1.5 6.2-6.7A5.2 5.2 0 0 0 20 4.8 4.9 4.9 0 0 0 19.9 1S18.7.6 16 2.5a13 13 0 0 0-7 0C6.3.6 5.1 1 5.1 1A4.9 4.9 0 0 0 5 4.8 5.2 5.2 0 0 0 3.7 8.4c0 5.2 3.2 6.4 6.2 6.7a3.4 3.4 0 0 0-.9 2.6V22"/>',
    "linkedin": '<path d="M4 4h16v16H4z"/><path d="M8 11v6M8 8v.01M12 17v-4a2 2 0 0 1 4 0v4"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18"/>',
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def mono_w(text, size):
    return len(text) * size * 0.6


def build(theme_name):
    t = THEMES[theme_name]
    k = theme_name
    a1, a2, a3 = t["accent"]
    out = []
    add = out.append

    add(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'fill="none" font-family="{SANS}" role="img" '
        f'aria-label="{esc(PROFILE["name"])} — {esc(PROFILE["roles"][0])}">'
    )

    # ---------------------------------------------------------------- defs
    add("  <defs>")
    add(
        f'    <linearGradient id="acc-{k}" x1="0" y1="0" x2="1" y2="1" spreadMethod="reflect">'
        f'<stop offset="0" stop-color="{a1}"/><stop offset="0.5" stop-color="{a2}"/>'
        f'<stop offset="1" stop-color="{a3}"/>'
        f'<animateTransform attributeName="gradientTransform" type="translate" '
        f'values="-0.35 0;0.35 0;-0.35 0" dur="9s" repeatCount="indefinite"/></linearGradient>'
    )
    add(
        f'    <linearGradient id="border-{k}" gradientUnits="objectBoundingBox">'
        f'<stop offset="0" stop-color="{a1}" stop-opacity="0"/>'
        f'<stop offset="0.5" stop-color="{a3}" stop-opacity="0.9"/>'
        f'<stop offset="1" stop-color="{a1}" stop-opacity="0"/>'
        f'<animateTransform attributeName="gradientTransform" type="rotate" from="0 0.5 0.5" '
        f'to="360 0.5 0.5" dur="8s" repeatCount="indefinite"/></linearGradient>'
    )
    for gid, col, op in (("A", a1, "0.50"), ("B", a3, "0.45"), ("C", a2, "0.35")):
        add(
            f'    <radialGradient id="glow{gid}-{k}" cx="0.5" cy="0.5" r="0.5">'
            f'<stop offset="0" stop-color="{col}" stop-opacity="{op}"/>'
            f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>'
        )
    add(
        f'    <linearGradient id="glass-{k}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{t["glass"]}"/>'
        f'<stop offset="0.4" stop-color="{t["glass"]}" stop-opacity="0"/></linearGradient>'
    )
    add(
        f'    <linearGradient id="scan-{k}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{a1}" stop-opacity="0"/>'
        f'<stop offset="0.5" stop-color="{a1}" stop-opacity="0.10"/>'
        f'<stop offset="1" stop-color="{a1}" stop-opacity="0"/></linearGradient>'
    )
    add(f'    <filter id="soft-{k}" x="-30%" y="-30%" width="160%" height="160%">'
        f'<feGaussianBlur stdDeviation="26"/></filter>')
    add(f'    <filter id="shadow-{k}" x="-20%" y="-20%" width="140%" height="140%">'
        f'<feDropShadow dx="0" dy="10" stdDeviation="16" flood-color="#04121a" '
        f'flood-opacity="{t["shadow_op"]}"/></filter>')
    add(f'    <filter id="noise-{k}"><feTurbulence type="fractalNoise" baseFrequency="0.9" '
        f'numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>')
    add(f'    <clipPath id="frame-{k}"><rect x="0" y="0" width="{W}" height="{H}" rx="26"/></clipPath>')
    add("  </defs>")

    add(f'  <g clip-path="url(#frame-{k})">')
    add(f'    <rect width="{W}" height="{H}" fill="{t["bg"]}"/>')
    add(f'    <rect width="{W}" height="{H}" fill="{t["bg2"]}" opacity="0.55"/>')

    # ------------------------------------------------------------- glows
    add("    <!-- background floating glows -->")
    add(f'    <g filter="url(#soft-{k})">')
    for cx, cy, rx, ry, gid, dx, dy, dur in (
        (210, 130, 265, 220, "A", 26, 18, "13s"),
        (985, 470, 285, 235, "B", -30, 20, "15s"),
        (620, 105, 230, 160, "C", 22, -16, "17s"),
    ):
        add(
            f'      <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#glow{gid}-{k})">'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="0 0;{dx} {dy};0 0" dur="{dur}" repeatCount="indefinite"/></ellipse>'
        )
    add("    </g>")

    add("    <!-- noise texture -->")
    add(f'    <rect width="{W}" height="{H}" filter="url(#noise-{k})" opacity="{t["noise_op"]}"/>')

    # ---------------------------------------------------------- particles
    add("    <!-- particles -->")
    rng = random.Random(24)
    for _ in range(46):
        px, py = rng.randint(10, W - 10), rng.randint(10, H - 10)
        r = round(rng.uniform(0.8, 2.0), 1)
        dur = round(rng.uniform(4.5, 11.0), 1)
        delay = round(rng.uniform(0, 6), 1)
        rise = rng.randint(10, 30)
        add(
            f'    <circle cx="{px}" cy="{py}" r="{r}" fill="{t["particle"]}" opacity="0.30">'
            f'<animate attributeName="opacity" values="0.05;0.45;0.05" dur="{dur}s" '
            f'begin="{delay}s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="0 0;0 -{rise};0 0" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/></circle>'
        )

    add("    <!-- scanline sweep -->")
    add(
        f'    <rect x="0" y="-200" width="{W}" height="200" fill="url(#scan-{k})">'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;0 {H + 220}" '
        f'dur="7s" repeatCount="indefinite"/></rect>'
    )

    # ------------------------------------------------- LEFT: ASCII panel
    add("    <!-- ===================== LEFT: ASCII portrait panel ===================== -->")
    add(f'    <g filter="url(#shadow-{k})"><rect x="24" y="24" width="430" height="562" rx="18" '
        f'fill="{t["panel"]}" fill-opacity="{t["panel_op"]}" stroke="{t["hair"]}"/></g>')
    add(f'    <rect x="24" y="24" width="430" height="562" rx="18" fill="url(#glass-{k})"/>')
    add(f'    <rect x="24" y="24" width="430" height="46" rx="18" fill="{t["head"]}" fill-opacity="0.6"/>')
    add(f'    <circle cx="48" cy="47" r="5.5" fill="{a3}"/>'
        f'<circle cx="68" cy="47" r="5.5" fill="{a2}"/>'
        f'<circle cx="88" cy="47" r="5.5" fill="{a1}"/>')
    add(f'    <text x="430" y="51" text-anchor="end" font-family="{MONO}" font-size="12.5" '
        f'fill="{t["dim"]}">portrait.sh — zsh</text>')

    add("    <g>")
    add('      <animateTransform attributeName="transform" type="translate" '
        'values="0 -3;0 3;0 -3" dur="6s" repeatCount="indefinite"/>')
    # Pad every line to the same character count so centring the block cannot shift
    # individual rows. The padding is U+00A0, because renderers trim ordinary
    # leading/trailing spaces before applying text-anchor and that shears the art.
    span = max(len(l) for l in PORTRAIT)
    for i, line in enumerate(PORTRAIT):
        y = 122 + i * 15
        begin = round(0.25 + i * 0.04, 2)
        row = esc(line.ljust(span)).replace(" ", " ")
        add(
            f'      <text x="239" y="{y}" text-anchor="middle" xml:space="preserve" '
            f'font-family="{MONO}" font-size="12.5" fill="url(#acc-{k})" opacity="0">{row}'
            f'<animate attributeName="opacity" values="0;0.95" keyTimes="0;1" begin="{begin}s" '
            f'dur="0.4s" fill="freeze"/></text>'
        )
    add("    </g>")

    add("    <!-- ascii scanline -->")
    add(
        f'    <rect x="26" y="72" width="426" height="60" fill="url(#scan-{k})" opacity="0.8">'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;0 452;0 0" '
        f'dur="9s" repeatCount="indefinite"/></rect>'
    )

    # --------------------------------------------- RIGHT: terminal panel
    add("    <!-- ===================== RIGHT: terminal panel ===================== -->")
    add(f'    <g filter="url(#shadow-{k})"><rect x="474" y="24" width="682" height="562" rx="18" '
        f'fill="{t["panel"]}" fill-opacity="{t["panel_op"]}" stroke="{t["hair"]}"/></g>')
    add(f'    <rect x="474" y="24" width="682" height="562" rx="18" fill="url(#glass-{k})"/>')
    add(f'    <rect x="474" y="24" width="682" height="46" rx="18" fill="{t["head"]}" fill-opacity="0.6"/>')
    add(f'    <circle cx="498" cy="47" r="5.5" fill="{a3}"/>'
        f'<circle cx="518" cy="47" r="5.5" fill="{a2}"/>'
        f'<circle cx="538" cy="47" r="5.5" fill="{a1}"/>')
    add(f'    <text x="815" y="51" text-anchor="middle" font-family="{MONO}" font-size="12.5" '
        f'fill="{t["dim"]}">{esc(PROFILE["handle"])} — bash</text>')

    add("    <!-- greeting -->")
    add('    <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="0.2s" '
        'dur="0.6s" fill="freeze"/>')
    add(f'      <text x="508" y="128" font-family="{SANS}" font-size="17" fill="{t["muted"]}">'
        f'Hi <tspan font-size="18">\U0001f44b</tspan> &#160;I&#39;m</text>')
    add(f'      <text x="508" y="172" font-family="{SANS}" font-size="38" font-weight="800" '
        f'fill="{t["text"]}" letter-spacing="-1">{esc(PROFILE["name"])}</text>')
    add("    </g>")

    # --------------------------------------------------- typing roles
    add("    <!-- typing prompt -->")
    add(f'    <text x="508" y="206" font-family="{MONO}" font-size="21" font-weight="700" '
        f'fill="{a1}">&gt;</text>')
    n = len(PROFILE["roles"])
    cycle = 3.2
    total = round(cycle * n, 2)
    for i, role in enumerate(PROFILE["roles"]):
        w = round(mono_w(role, 21), 1)
        s = i / n
        t1, t2, t3 = round(s + 0.25 / n, 4), round(s + 0.65 / n, 4), round(s + 0.8 / n, 4)
        kt = f"0;{round(s, 4)};{t1};{t2};{t3};1"
        add(f'    <g opacity="0">')
        add(f'      <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" '
            f'dur="{total}s" repeatCount="indefinite"/>')
        add(f'      <defs><clipPath id="clip-{k}-{i}"><rect x="526" y="186" height="28" width="0">'
            f'<animate attributeName="width" values="0;0;{w};{w};0;0" keyTimes="{kt}" '
            f'dur="{total}s" repeatCount="indefinite"/></rect></clipPath></defs>')
        add(f'      <text x="526" y="206" font-family="{MONO}" font-size="21" font-weight="700" '
            f'fill="url(#acc-{k})" clip-path="url(#clip-{k}-{i})">{esc(role)}</text>')
        add(f'      <rect y="188" width="11" height="23" rx="1.5" fill="{t["cursor"]}" x="526">'
            f'<animate attributeName="x" values="526;526;{526 + w};{526 + w};526;526" '
            f'keyTimes="{kt}" dur="{total}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="1;1;1;0.2;1;1" keyTimes="0;0.02;0.5;0.55;0.9;1" '
            f'dur="0.9s" repeatCount="indefinite"/></rect>')
        add("    </g>")

    add("    <!-- divider -->")
    add(f'    <line x1="508" y1="230" x2="1122" y2="230" stroke="{t["hair"]}"/>')
    add(f'    <line x1="508" y1="230" x2="640" y2="230" stroke="url(#acc-{k})" stroke-width="1.5"/>')

    # ------------------------------------------------------- info rows
    for i, (label, value) in enumerate(PROFILE["rows"]):
        y = 258 + i * 33
        begin = round(1.20 + i * 0.22, 2)
        add(f'    <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{begin}s" '
            f'dur="0.5s" fill="freeze"/>')
        add(f'      <circle cx="514" cy="{y - 5}" r="3" fill="url(#acc-{k})"/>')
        add(f'      <text x="530" y="{y}" font-family="{MONO}" font-size="14.5" '
            f'fill="{t["dim"]}" xml:space="preserve">{esc(label)}</text>')
        add(f'      <text x="636" y="{y}" font-family="{MONO}" font-size="14.5" '
            f'fill="{t["muted"]}">{esc(value)}</text>')
        add("    </g>")

    # ----------------------------------------------------- stack chips
    add("    <!-- stack -->")
    add('    <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="2.3s" '
        'dur="0.5s" fill="freeze"/>')
    add(f'      <text x="508" y="441" font-family="{MONO}" font-size="12.5" fill="{t["dim"]}" '
        f'letter-spacing="2">STACK</text>')
    add(f'      <line x1="562" y1="437" x2="1122" y2="437" stroke="{t["hair"]}"/>')
    add("    </g>")

    x, y, row = 508, 456, 0
    for i, chip in enumerate(PROFILE["stack"]):
        cw = round(mono_w(chip, 13) + 34, 1)
        if x + cw > 1122:
            row += 1
            x, y = 508, 456 + row * 42
        begin = round(2.40 + i * 0.07, 2)
        add(f'    <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{begin}s" '
            f'dur="0.45s" fill="freeze"/>')
        add(f'      <rect x="{x}" y="{y}" width="{cw}" height="30" rx="15" fill="{t["chip_fill"]}" '
            f'stroke="{t["chip_stroke"]}" stroke-width="1"/>')
        add(f'      <rect x="{x}" y="{y}" width="{cw}" height="30" rx="15" fill="none" '
            f'stroke="url(#acc-{k})" stroke-width="1" opacity="0">'
            f'<animate attributeName="opacity" values="0;0.45;0" dur="3.6s" '
            f'begin="{round(i * 0.18, 2)}s" repeatCount="indefinite"/></rect>')
        add(f'      <text x="{round(x + cw / 2, 1)}" y="{y + 20}" text-anchor="middle" '
            f'font-family="{MONO}" font-size="13" fill="{t["text"]}">{esc(chip)}</text>')
        add("    </g>")
        x += cw + 10

    # ---------------------------------------------------- footer links
    add("    <!-- footer links -->")
    lx = 508
    for i, (icon, label) in enumerate(PROFILE["links"]):
        add(f'    <g transform="translate({lx},556)" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" begin="3.4s" dur="0.6s" fill="freeze"/>')
        add(f'      <rect x="-3" y="-18" width="26" height="26" rx="8" fill="{t["chip_fill"]}" '
            f'stroke="{t["chip_stroke"]}" stroke-width="1"/>')
        add(f'      <g fill="none" stroke="url(#acc-{k})" stroke-width="1.7" stroke-linecap="round" '
            f'stroke-linejoin="round" transform="translate(1,-16) scale(0.75)">{ICONS[icon]}</g>')
        add(f'      <text x="34" y="0" font-family="{MONO}" font-size="13.5" '
            f'fill="{t["text"]}">{esc(label)}</text>')
        add(f'      <animateTransform attributeName="transform" type="translate" additive="sum" '
            f'values="0 0;0 -2;0 0" dur="4s" begin="{round(i * 0.45, 2)}s" repeatCount="indefinite"/>')
        add("    </g>")
        lx += int(mono_w(label, 13.5)) + 34 + 25

    add("    <!-- animated frame border shimmer -->")
    add(f'    <rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="25" fill="none" '
        f'stroke="{t["frame"]}" stroke-width="1"/>')
    add(f'    <rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="25" fill="none" '
        f'stroke="url(#border-{k})" stroke-width="2"/>')
    add("  </g>")
    add("</svg>")
    return "\n".join(out) + "\n"


for name in ("dark", "light"):
    with open(f"{name}.svg", "w", encoding="utf-8") as f:
        f.write(build(name))
    print(f"wrote {name}.svg")
