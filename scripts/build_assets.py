#!/usr/bin/env python3
"""Bangun semua aset statis README ke ../assets.

Jalankan dari root repo:  python3 scripts/build_assets.py
Ubah teks/warna di bawah ini lalu jalankan lagi untuk membuat ulang SVG-nya.
"""
from pathlib import Path

from pixel import (AQUA, BG, DEEP, EDGE, EMERALD, GOLD, GREEN, ICONS, MUTED, PANEL, TEXT,
                   Reel, bitmap, creeper_parts, esc, grass, icon, rect, svg, text)

OUT = Path(__file__).resolve().parent.parent / "assets"
W = 640


def frame(x, y, w, h, color, sw=2):
    return (f'<rect x="{x + sw / 2}" y="{y + sw / 2}" width="{w - sw}" height="{h - sw}" '
            f'fill="none" stroke="{color}" stroke-width="{sw}"/>')


# ---------------------------------------------------------------- banner (neofetch)
FIELDS = [
    ("Name", "Ibnu Farrel A. F."),
    ("OS", "CachyOS (Arch-based)"),
    ("Uni", "Universitas Diponegoro"),
    ("Major", "Informatics, year 2"),
    ("Focus", "Embedded, AI/CV, IoT"),
    ("Goal", "Embedded Software Engineer"),
]
MC_DARK = ["#2D333B", "#AA0000", "#00AA00", "#FFAA00", "#0000AA", "#AA00AA", "#00AAAA", "#AAAAAA"]
MC_LIGHT = ["#555555", "#FF5555", "#55FF55", "#FFFF55", "#5555FF", "#FF55FF", "#55FFFF", "#FFFFFF"]


def banner():
    H, x0, per = 330, 150, 0.03
    # --- jadwal (detik)
    t_prompt, d_prompt = 0.4, 10 * 0.06
    t_creeper = t_prompt + d_prompt + 0.4
    t_head, d_head = t_creeper + 0.1, 18 * per
    t_line = t_head + d_head + 0.1
    t = t_line + 0.2
    sched = []
    for _, v in FIELDS:
        d = (7 + len(v)) * per
        sched.append((t, d))
        t += d + 0.15
    t_pal, d_pal = t + 0.1, 0.5
    t_swell = t_pal + d_pal + 0.8
    R = t_swell + 1.1 + 3.5
    T = round(R + 0.8 + 0.9 + 0.5, 2)

    reel = Reel(T, loop=True, fade_at=R)
    P = reel.p
    c = []
    c.append(reel.typed(24, 62, 11, [(0, "$", GREEN), (2, "neofetch", TEXT)],
                        t_prompt, d_prompt, t_head))

    # creeper + tanah
    u, cx, cy = 6, 44, 104
    upper, left, right = creeper_parts(u)
    a_cr = reel.appear(t_creeper)
    sw0, sw1 = t_swell, t_swell + 1.1
    reel.css.append(
        f".sw{{transform-box:fill-box;transform-origin:50% 100%;animation:sw {T}s linear infinite}}"
        f"@keyframes sw{{0%,{P(sw0)}%{{transform:scale(1)}}{P(sw1)}%{{transform:scale(1.14,1.08)}}"
        f"{P(sw1 + 0.01)}%,100%{{transform:scale(1)}}}}"
        f".fl{{animation:fl {T}s linear infinite}}"
        f"@keyframes fl{{0%,{P(sw0 + 0.2)}%{{opacity:0}}{P(sw0 + 0.21)}%,{P(sw0 + 0.5)}%{{opacity:.6}}"
        f"{P(sw0 + 0.51)}%,{P(sw0 + 0.8)}%{{opacity:0}}{P(sw0 + 0.81)}%,{P(sw1)}%{{opacity:.6}}"
        f"{P(sw1 + 0.01)}%,100%{{opacity:0}}}}")
    flash = rect(0, 0, 8 * u, 26 * u, "#FFFFFF", ' class="fl" opacity="0"')
    c.append(f'<g class="{a_cr}"><g class="sw"><g transform="translate({cx} {cy})">'
             f"{upper}{left}{right}{flash}</g></g>{grass(24, cy + 26 * u, 11)}</g>")

    # info
    c.append(reel.typed(x0, 100, 13, [(0, "ibnufarrel", GREEN), (10, "@", MUTED), (11, "cachyos", GREEN)],
                        t_head, d_head, sched[0][0]))
    a_ul = reel.appear(t_line)
    c.append(f'<g class="{a_ul}">{rect(x0, 110, 18 * 13, 2, EMERALD, " opacity=\".55\"")}</g>')
    for i, ((k, v), (s, d)) in enumerate(zip(FIELDS, sched)):
        last = i == len(FIELDS) - 1
        hold = R if last else sched[i + 1][0]
        c.append(reel.typed(x0, 136 + 24 * i, 11, [(0, k, GREEN), (7, v, TEXT)], s, d, hold))

    # palet warna ala neofetch
    pal = "".join(rect(x0 + i * 18, 270, 14, 14, a) + rect(x0 + i * 18, 288, 14, 14, b)
                  for i, (a, b) in enumerate(zip(MC_DARK, MC_LIGHT)))
    c.append(pal + reel.reveal(x0, 270, 144, 32, 8, t_pal, d_pal))

    body = (
        rect(0, 0, W, H, BG) + rect(0, 0, W, 30, PANEL) + rect(0, 30, W, 2, EDGE)
        + rect(14, 10, 10, 10, "#FF5555") + rect(30, 10, 10, 10, GOLD) + rect(46, 10, 10, 10, GREEN)
        + text(W / 2, 20, "ibnufarrel@cachyos: ~", 9, MUTED, "middle")
        + f'<g class="fade">{"".join(c)}</g>'
        + frame(0, 0, W, H, EMERALD, 3)
    )
    label = ("neofetch: Ibnu Farrel A. F., CachyOS, Universitas Diponegoro, Informatics year 2, "
             "focus on Embedded, AI/CV and IoT, aspiring Embedded Software Engineer")
    return svg(W, H, body, reel.style(), label)


# ---------------------------------------------------------------- judul section
def header(cmd):
    size, x = 14, 40
    cols = 2 + len(cmd)
    start, dur = 0.3, cols * 0.06
    reel = Reel(start + dur + 0.1, loop=False)
    line = reel.typed(x, 23, size, [(0, "$", GREEN), (2, cmd, TEXT)], start, dur, keep=True)
    lx = x + cols * size + 28
    dash = (f'<line x1="{lx}" y1="17" x2="{W - 14}" y2="17" stroke="{EMERALD}" stroke-opacity=".35" '
            f'stroke-width="2" stroke-dasharray="6 6"/>')
    rows, colors = ICONS["grass"]
    body = (rect(0, 0, W, 34, BG) + bitmap(rows, 8, 5, 3, colors) + line + dash + frame(0, 0, W, 34, EDGE))
    return svg(W, 34, body, reel.style(), f"$ {cmd}")


# ---------------------------------------------------------------- about
ABOUT = [
    ("cap", ["Informatics Student @ Undip"]),
    ("robot", ["Exploring AI, Computer Vision,", "& Autonomous Systems"]),
    ("chip", ["Tinkering with IoT & Sensor Networks"]),
]


def about():
    size, per, x = 14, 0.04, 76
    items, t = [], 0.3
    for ri, (_, lines) in enumerate(ABOUT):
        for li, ln in enumerate(lines):
            d = len(ln) * per
            items.append((ri, li, len(lines), ln, t, d))
            t += d + 0.2
    reel = Reel(round(t + 0.1, 2), loop=False)
    parts = []
    for ri, (ic, _) in enumerate(ABOUT):
        y0 = 14 + 58 * ri
        parts.append(rect(16, y0, 44, 44, PANEL) + frame(16, y0, 44, 44, EDGE) + icon(ic, 38, y0 + 22, 3))
    for n, (ri, li, nl, ln, s, d) in enumerate(items):
        y0 = 14 + 58 * ri
        base = y0 + 29 if nl == 1 else y0 + (19 if li == 0 else 41)
        last = n == len(items) - 1
        hold = None if last else items[n + 1][4]
        parts.append(reel.typed(x, base, size, [(0, ln, TEXT)], s, d, hold, keep=last))
    H = 14 + 58 * 2 + 44 + 14
    body = rect(0, 0, W, H, BG) + "".join(parts) + frame(0, 0, W, H, EDGE)
    label = "Informatics Student @ Undip. Exploring AI, Computer Vision, & Autonomous Systems. Tinkering with IoT & Sensor Networks."
    return svg(W, H, body, reel.style(), label)


# ---------------------------------------------------------------- lab
TILES = [
    ("chip", "Embedded", "C and C++"),
    ("eye", "Vision", "OpenCV, YOLOv8"),
    ("drone", "Autonomy", "ROS 2, PyMavlink"),
    ("bars", "IoT", "MQTT, sensors"),
]
BAR_COLORS = ["#1B9A2C", "#27E835", "#55FF55", "#B6FFB6"]


def lab_icon(kind, cx, cy, px=4):
    if kind == "eye":
        rows, colors = ICONS["eye"]
        ox, oy = round(cx - 11 * px / 2), round(cy - 7 * px / 2)
        pupil = bitmap(["PPP", "PkP", "PPP"], ox + 4 * px, oy + 2 * px, px, {"P": EMERALD, "k": BG})
        return bitmap(rows, ox, oy, px, colors) + f'<g class="pu">{pupil}</g>'
    if kind == "bars":
        ox, oy = round(cx - 11 * px / 2), round(cy - 8 * px / 2)
        out = []
        for i, hgt in enumerate([2, 4, 6, 8]):
            out.append(rect(ox + i * 3 * px, oy + (8 - hgt) * px, 2 * px, hgt * px, BAR_COLORS[i],
                            f' class="sb" style="animation-delay:{i * 0.25}s"'))
        return "".join(out)
    return icon(kind, cx, cy, px)


def lab():
    tw, th, gap = 302, 80, 12
    mx = (W - 2 * tw - gap) // 2
    parts = []
    for i, (kind, title, sub) in enumerate(TILES):
        x = mx + (i % 2) * (tw + gap)
        y = 12 + (i // 2) * (th + gap)
        parts.append(
            rect(x, y, tw, th, PANEL) + rect(x + 2, y + 2, tw - 4, 2, "#2D333B") + rect(x + 2, y + 2, 2, th - 4, "#2D333B")
            + frame(x, y, tw, th, EDGE)
            + rect(x + 12, y + 12, 56, 56, BG) + frame(x + 12, y + 12, 56, 56, EDGE)
            + lab_icon(kind, x + 40, y + 40)
            + text(x + 82, y + 38, title, 14, GREEN) + text(x + 82, y + 60, sub, 10, MUTED))
    H = 12 + 2 * th + gap + 12
    css = (".sb{animation:sb 2.4s steps(1,end) infinite}"
           "@keyframes sb{0%,70%{opacity:1}75%,95%{opacity:.25}100%{opacity:1}}"
           ".pu{animation:look 6s steps(1,end) infinite}"
           "@keyframes look{0%{transform:translateX(0)}20%{transform:translateX(-8px)}"
           "40%{transform:translateX(0)}60%{transform:translateX(8px)}80%{transform:translateX(0)}}")
    body = rect(0, 0, W, H, BG) + "".join(parts) + frame(0, 0, W, H, EDGE)
    label = "Lab: Embedded (C and C++), Vision (OpenCV, YOLOv8), Autonomy (ROS 2, PyMavlink), IoT (MQTT, sensors)"
    return svg(W, H, body, css, label)


# ---------------------------------------------------------------- footer
def footer():
    H, u = 120, 3
    upper, left, right = creeper_parts(u)
    gy = 88
    reel = Reel(1.9, loop=False)
    l1 = reel.typed(24, 40, 12, [(0, "$", GREEN), (2, "exit", TEXT)], 0.3, 0.3, 0.8)
    l2 = reel.typed(24, 62, 10, [(0, "thanks for stopping by", MUTED)], 1.0, 0.8, keep=True)
    css = (".wk{animation:wk 24s steps(117,end) infinite}"
           "@keyframes wk{from{transform:translateX(-620px)}to{transform:translateX(80px)}}"
           ".l1{animation:lg .6s steps(1,end) infinite}.l2{animation:lg2 .6s steps(1,end) infinite}"
           "@keyframes lg{0%{transform:translateY(0)}50%{transform:translateY(-3px)}}"
           "@keyframes lg2{0%{transform:translateY(-3px)}50%{transform:translateY(0)}}")
    walker = (f'<g transform="translate(580 0)"><g class="wk"><g transform="translate(0 {gy - 26 * u})">{upper}'
              f'<g class="l1">{left}</g><g class="l2">{right}</g></g></g></g>')
    body = rect(0, 0, W, H, BG) + l1 + l2 + walker + grass(0, gy, 80) + frame(0, 0, W, H, EDGE)
    return svg(W, H, body, css + reel.style(), "$ exit. thanks for stopping by.")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = {
        "banner.svg": banner(),
        "h-about.svg": header("cat about.md"),
        "about.svg": about(),
        "h-stack.svg": header("ls ~/stack"),
        "h-stats.svg": header("./stats.sh"),
        "footer.svg": footer(),
    }
    for name, data in files.items():
        (OUT / name).write_text(data, encoding="utf-8")
        print(f"{name:14s} {len(data) / 1024:5.1f} KB")


if __name__ == "__main__":
    main()
