"""Helper bersama untuk semua aset SVG profil (palet, font pixel, bitmap, animasi ketik).

Semua output murni SVG + CSS. Tidak ada request ke server luar: font Press Start 2P
(SIL OFL) ditanam sebagai data-URI, jadi tampilannya sama di semua perangkat.
"""
import base64
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent

# --- palet: terminal gelap + warna chat Minecraft ---------------------------------
BG, PANEL, EDGE, SLOT = "#0D1117", "#161B22", "#30363D", "#21262D"
GREEN, EMERALD, DEEP = "#55FF55", "#27E835", "#14291A"
TEXT, MUTED, WHITE = "#C9D1D9", "#8B949E", "#E6EDF3"
GOLD, AQUA, RED, PINK = "#FFAA00", "#55FFFF", "#FF5555", "#FF55FF"
FONT = "'PS2P','Courier New',monospace"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def font_css():
    b64 = base64.b64encode((HERE / "PressStart2P-subset.woff").read_bytes()).decode()
    return "@font-face{font-family:'PS2P';src:url(data:font/woff;base64,%s) format('woff');}" % b64


def svg(w, h, body, css="", label=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" shape-rendering="crispEdges" role="img" aria-label="{esc(label)}">'
        f"<title>{esc(label)}</title>"
        f"<style>{font_css()}text{{font-family:{FONT}}}{css}"
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}}</style>"
        f"{body}</svg>"
    )


def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{extra}/>'


def text(x, y, s, size, fill, anchor=None, extra=""):
    a = f' text-anchor="{anchor}"' if anchor else ""
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}"{a}{extra}>{esc(s)}</text>'


# --- bitmap pixel -----------------------------------------------------------------
def bitmap(rows, x, y, px, colors):
    w = len(rows[0])
    for r in rows:
        assert len(r) == w, f"baris bitmap tidak rata: {r!r}"
    out = []
    for j, row in enumerate(rows):
        i = 0
        while i < w:
            c = row[i]
            if c == ".":
                i += 1
                continue
            k = i
            while k < w and row[k] == c:
                k += 1
            out.append(rect(x + i * px, y + j * px, (k - i) * px, px, colors[c]))
            i = k
    return "".join(out)


def bitmap_size(rows, px):
    return len(rows[0]) * px, len(rows) * px


ICONS = {
    # topi wisuda
    "cap": ([
        "....GG....",
        "..GGGGGG..",
        "GGGGGGGGGG",
        ".GGGGGGGGY",
        "..dddddd.Y",
        "..dddddd.Y",
        "..dddddd.Y",
        "...dddd...",
    ], {"G": GREEN, "d": "#1B9A2C", "Y": GOLD}),
    # kepala robot
    "robot": ([
        "....Y....",
        ".AAAAAAA.",
        "AAAAAAAAA",
        "AkkAAAkkA",
        "AkkAAAkkA",
        "AAAAAAAAA",
        "AAkkkkkAA",
        ".AAAAAAA.",
    ], {"A": AQUA, "k": BG, "Y": GOLD}),
    # chip
    "chip": ([
        "..P.P.P..",
        ".GGGGGGG.",
        "PGDDDDDGP",
        ".GDGGGDG.",
        "PGDGGGDGP",
        ".GDDDDDG.",
        "PGGGGGGGP",
        ".GGGGGGG.",
        "..P.P.P..",
    ], {"G": "#1B9A2C", "D": GREEN, "P": GOLD}),
    # drone (tampak atas)
    "drone": ([
        "PPP.....PPP",
        "..GG...GG..",
        "...GGGGG...",
        "...GkGkG...",
        "...GGGGG...",
        "..GG...GG..",
        "PPP.....PPP",
    ], {"P": GOLD, "G": EMERALD, "k": BG}),
    # mata (tanpa pupil, pupil dianimasikan terpisah)
    "eye": ([
        "...EEEEE...",
        ".EEWWWWWEE.",
        "EWWWWWWWWWE",
        "EWWWWWWWWWE",
        "EWWWWWWWWWE",
        ".EEWWWWWEE.",
        "...EEEEE...",
    ], {"E": AQUA, "W": WHITE}),
    # blok rumput (juga dipakai sebagai ikon "repos")
    "grass": ([
        "GGGGGGGG",
        "GgGGgGGG",
        "DdDDDdDD",
        "DDDdDDDD",
        "DDDDDDdD",
        "dDDDDDDD",
        "DDdDDDDD",
        "DDDDDdDD",
    ], {"G": EMERALD, "g": "#1B9A2C", "D": "#7A5230", "d": "#5A3A22"}),
    "star": ([
        "...YY...",
        "...YY...",
        "YYYYYYYY",
        ".YYYYYY.",
        "..YYYY..",
        "..YYYY..",
        ".YY..YY.",
        ".Y....Y.",
    ], {"Y": GOLD}),
    "commit": ([
        "........",
        "..AAAA..",
        ".A....A.",
        "AA....AA",
        "AA....AA",
        ".A....A.",
        "..AAAA..",
        "........",
    ], {"A": AQUA}),
    "merge": ([
        "PP....PP",
        "PP....PP",
        ".P....P.",
        "..P..P..",
        "...PP...",
        "...PP...",
        "...PP...",
        "..PPPP..",
    ], {"P": PINK}),
    "issue": ([
        "..RRRR..",
        ".RRkkRR.",
        "RRRkkRRR",
        "RRRkkRRR",
        "RRRkkRRR",
        "RRRRRRRR",
        ".RRkkRR.",
        "..RRRR..",
    ], {"R": RED, "k": BG}),
    "person": ([
        "..WWWW..",
        ".WWWWWW.",
        ".WWWWWW.",
        "..WWWW..",
        "........",
        ".WWWWWW.",
        "WWWWWWWW",
        "WWWWWWWW",
    ], {"W": WHITE}),
}


def icon(name, cx, cy, px):
    rows, colors = ICONS[name]
    w, h = bitmap_size(rows, px)
    return bitmap(rows, round(cx - w / 2), round(cy - h / 2), px, colors)


# --- creeper & rumput ------------------------------------------------------------
SKIN = ["#2FD943", "#25B837", "#1D9A2E"]
FACE = "#06240B"
FACE_CELLS = {(1, 2), (2, 2), (5, 2), (6, 2), (1, 3), (2, 3), (5, 3), (6, 3),
              (3, 4), (4, 4), (2, 5), (3, 5), (4, 5), (5, 5),
              (2, 6), (3, 6), (4, 6), (5, 6), (2, 7), (5, 7)}


def creeper_parts(u, seed=3):
    """Kembalikan (badan+kepala, kaki kiri, kaki kanan) dalam koordinat lokal 8u x 26u."""
    rnd = random.Random(seed)
    cells = {}
    for row in range(26):
        for col in range(8):
            cells[(col, row)] = FACE if (col, row) in FACE_CELLS else rnd.choices(SKIN, weights=[5, 3, 2])[0]

    def block(c0, c1, r0, r1):
        out = []
        for row in range(r0, r1):
            col = c0
            while col < c1:
                color = cells[(col, row)]
                k = col
                while k < c1 and cells[(k, row)] == color:
                    k += 1
                out.append(rect(col * u, row * u, (k - col) * u, u, color))
                col = k
        return "".join(out)

    return block(0, 8, 0, 20), block(0, 4, 20, 26), block(4, 8, 20, 26)


def grass(x, y, cols, cell=8, seed=7):
    """Strip tanah rumput 4 baris tinggi."""
    rnd = random.Random(seed)
    top = [EMERALD, "#1FB82B", "#3DEB4B"]
    mid = ["#1FB82B", "#5A3A22", "#16902A"]
    dirt = ["#5A3A22", "#4A2F1B", "#6B4529", "#3E2716"]
    out = []
    for cx in range(cols):
        px_ = x + cx * cell
        out.append(rect(px_, y, cell, cell, rnd.choice(top)))
        out.append(rect(px_, y + cell, cell, cell, rnd.choice(mid)))
        out.append(rect(px_, y + 2 * cell, cell, cell, rnd.choice(dirt)))
        out.append(rect(px_, y + 3 * cell, cell, cell, rnd.choice(dirt)))
    return "".join(out)


# --- mesin animasi ketik ---------------------------------------------------------
class Reel:
    """Satu timeline animasi untuk satu SVG.

    Teks "diketik" dengan menutupnya memakai persegi berwarna latar yang digeser
    dengan steps() per karakter (penutup menyusut ke kanan). Kalau CSS animasi tidak
    jalan, penutup transparan sehingga teks tetap terlihat penuh.

    loop=True   -> timeline berulang; seluruh isi memudar di `fade_at` lalu mulai lagi.
    loop=False  -> diputar sekali, berhenti di keadaan akhir.
    """

    def __init__(self, total, loop=True, fade_at=None):
        self.T = total
        self.loop = loop
        self.fade_at = fade_at
        self.n = 0
        self.css = []
        # waktu cover dikembalikan ke posisi awal (setelah isi sudah memudar)
        self.jump = (fade_at + 0.9) if (loop and fade_at is not None) else None

    def p(self, t):
        return f"{max(0.0, min(100.0, t / self.T * 100)):.3f}"

    def _it(self):
        return "infinite" if self.loop else "1 both"

    def typed(self, x, y, size, runs, start, dur, hold_end=None, keep=False, cursor=GREEN):
        """runs = [(kolom, teks, warna)]. Mengembalikan markup SVG baris yang diketik."""
        self.n += 1
        i = self.n
        cols = max(c + len(s) for c, s, _ in runs)
        W = cols * size
        e = start + dur
        h = e if hold_end is None else max(e, hold_end)
        p = self.p
        txt = "".join(text(x + c * size, y, s, size, f) for c, s, f in runs)
        cover = rect(x, y - size - 1, W, int(size * 1.35) + 3, BG, f' class="c{i}" opacity="0"')
        k = rect(x, y - size, size - 2, size + 2, cursor, f' class="m{i}" opacity="0"')
        steps = f"steps({cols},end)"
        S1, S0 = "opacity:1;transform:scaleX(1)", "opacity:1;transform:scaleX(0)"
        if self.loop:
            j = self.jump
            cv = (f"0%,{p(start)}%{{{S1}}}{p(e)}%,{p(j)}%{{{S0}}}"
                  f"{p(j + 0.01)}%,100%{{{S1}}}")
            cu = (f"0%,{p(start - 0.01)}%{{opacity:0;transform:translateX(0)}}"
                  f"{p(start)}%{{opacity:1;transform:translateX(0)}}"
                  f"{p(e)}%,{p(h)}%{{opacity:1;transform:translateX({W}px)}}"
                  f"{p(h + 0.01)}%,100%{{opacity:0;transform:translateX({W}px)}}")
        else:
            cv = f"0%,{p(start)}%{{{S1}}}{p(e)}%,100%{{{S0}}}"
            if keep:
                cu = (f"0%,{p(start - 0.01)}%{{opacity:0;transform:translateX(0)}}"
                      f"{p(start)}%{{opacity:1;transform:translateX(0)}}"
                      f"{p(e)}%,100%{{opacity:1;transform:translateX({W}px)}}")
            else:
                cu = (f"0%,{p(start - 0.01)}%{{opacity:0;transform:translateX(0)}}"
                      f"{p(start)}%{{opacity:1;transform:translateX(0)}}"
                      f"{p(e)}%,{p(h)}%{{opacity:1;transform:translateX({W}px)}}"
                      f"{p(h + 0.01)}%,100%{{opacity:0;transform:translateX({W}px)}}")
        self.css.append(
            f".c{i}{{transform-box:fill-box;transform-origin:100% 50%;animation:k{i} {self.T}s {steps} {self._it()}}}"
            f"@keyframes k{i}{{{cv}}}"
            f".m{i}{{animation:m{i} {self.T}s {steps} {self._it()}}}@keyframes m{i}{{{cu}}}"
        )
        return txt + cover + f'<g class="bl">{k}</g>'

    def reveal(self, x, y, w, h, steps, start, dur):
        """Tutup area (berisi gambar) dengan latar lalu buka bertahap dari kiri."""
        self.n += 1
        i = self.n
        e = start + dur
        p = self.p
        S1, S0 = "opacity:1;transform:scaleX(1)", "opacity:1;transform:scaleX(0)"
        if self.loop:
            j = self.jump
            kf = (f"0%,{p(start)}%{{{S1}}}{p(e)}%,{p(j)}%{{{S0}}}"
                  f"{p(j + 0.01)}%,100%{{{S1}}}")
        else:
            kf = f"0%,{p(start)}%{{{S1}}}{p(e)}%,100%{{{S0}}}"
        self.css.append(
            f".c{i}{{transform-box:fill-box;transform-origin:100% 50%;"
            f"animation:k{i} {self.T}s steps({steps},end) {self._it()}}}@keyframes k{i}{{{kf}}}")
        return rect(x, y, w, h, BG, f' class="c{i}" opacity="0"')

    def appear(self, start):
        """Kelas CSS: elemen baru muncul pada detik `start` (dan tetap sampai fade)."""
        self.n += 1
        i = self.n
        p = self.p
        self.css.append(
            f".a{i}{{animation:a{i} {self.T}s linear {self._it()}}}"
            f"@keyframes a{i}{{0%,{p(start)}%{{opacity:0}}{p(start + 0.01)}%,100%{{opacity:1}}}}")
        return f"a{i}"

    def style(self):
        out = "".join(self.css)
        out += ".bl{animation:bl 1s steps(1,end) infinite}@keyframes bl{0%{opacity:1}50%{opacity:0}}"
        if self.loop and self.fade_at is not None:
            out += (f".fade{{animation:fd {self.T}s linear infinite}}"
                    f"@keyframes fd{{0%,{self.p(self.fade_at)}%{{opacity:1}}"
                    f"{self.p(self.fade_at + 0.8)}%,100%{{opacity:0}}}}")
        return out
