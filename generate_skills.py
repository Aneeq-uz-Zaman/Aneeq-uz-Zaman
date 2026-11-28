"""Generates skills-dark.svg / skills-light.svg - animated skill bars shown in README.md.

Levels mirror the Skills page of the portfolio (aneequzzaman.vercel.app).
Run `python generate_skills.py` after editing SKILLS.
"""

W = 1180
SKILLS = [
    [("Python", 95), ("Selenium & Web Scraping", 95), ("Pandas / NumPy", 93), ("Streamlit & Gradio", 85),
     ("RAG / LLM Apps", 80), ("Scikit-learn", 78)],
    [("React.js", 90), ("Next.js", 85), ("JavaScript", 85), ("MongoDB", 82),
     ("TypeScript", 75), ("C / C++", 78)],
]
THEMES = {
    "dark": dict(panel="#0e2331", hair="rgba(255,255,255,0.08)", text="#e8f1f7", muted="#9db2c2",
                 track="rgba(255,255,255,0.08)", a=["#2ed3b7", "#8cf1de", "#ff8a3d"], head="#16303f"),
    "light": dict(panel="#ffffff", hair="rgba(7,16,24,0.10)", text="#0b1b26", muted="#4d6b7c",
                  track="rgba(7,16,24,0.08)", a=["#0f9e8a", "#2aa79b", "#e2661a"], head="#dcebf2"),
}
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "ui-sans-serif,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
ROW, TOP = 52, 92
H = TOP + 6 * ROW + 30


def build(name):
    t = THEMES[name]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{t["a"][0]}"/>'
         f'<stop offset="1" stop-color="{t["a"][2]}"/></linearGradient></defs>',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="{t["panel"]}" stroke="{t["hair"]}"/>',
         f'<rect x="1" y="1" width="{W-2}" height="46" rx="18" fill="{t["head"]}" fill-opacity="0.6"/>']
    for i, c in enumerate(t["a"][::-1]):
        o.append(f'<circle cx="{26+i*20}" cy="24" r="5.5" fill="{c}"/>')
    o.append(f'<text x="{W/2}" y="28" text-anchor="middle" font-family="{MONO}" font-size="13" '
             f'fill="{t["muted"]}">skills.sh — ./show --levels</text>')
    bw = 470
    for col, items in enumerate(SKILLS):
        x = 50 + col * 570
        for i, (label, lv) in enumerate(items):
            y = TOP + i * ROW
            d = round(0.2 + (col * 6 + i) * 0.12, 2)
            o.append(f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="16" font-weight="600" fill="{t["text"]}">{label}</text>')
            o.append(f'<text x="{x+bw+30}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="14" fill="{t["muted"]}">{lv}%</text>')
            o.append(f'<rect x="{x}" y="{y+12}" width="{bw+30}" height="9" rx="4.5" fill="{t["track"]}"/>')
            o.append(f'<rect x="{x}" y="{y+12}" width="0" height="9" rx="4.5" fill="url(#g)">'
                     f'<animate attributeName="width" from="0" to="{(bw+30)*lv/100:.1f}" begin="{d}s" dur="1.4s" '
                     f'fill="freeze" calcMode="spline" keySplines="0.22 1 0.36 1" keyTimes="0;1"/></rect>')
    o.append("</svg>")
    open(f"skills-{name}.svg", "w", encoding="utf-8").write("\n".join(o))
    print("wrote", f"skills-{name}.svg")


for n in THEMES:
    build(n)
