"""Draw the datasheet figures from geometry.json (see extract_geometry.py).

    .venv/bin/python figures/draw.py

Writes figures/ports-digital.svg, figures/ports-analog.svg and figures/mechanical.svg.
Port names live here and in datasheet.md; board reference designators never reach the figures.
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
G = json.load(open(os.path.join(HERE, "geometry.json")))

plt.rcParams.update({"font.family": ["Helvetica", "Arial", "DejaVu Sans"], "svg.fonttype": "none"})
INK, MUTED, BOARD, PART, PART_EDGE, ACCENT = "#1d2733", "#6b7785", "#eef1ec", "#b9c7d6", "#3d5a78", "#0e6e7e"

# Board ref -> label on the figure. Parts sharing a label are drawn with one callout.
NAMES = {
    "digital": {
        "J5": "DUT 5V", "J6": "DUT EXT", "J1": "I/O HEADER", "LED1": "STATUS LED", "USB1": "DUT 5V (USB-A)",
        "USBC1": "HOST / POWER (USB-C)", "J7": "ETHERNET", "USB2": "BRIDGE POWER (USB-A)",
        "J4": "EXT SUPPLY IN", "SW1": "RESET", "SW2": "BOOT", "CN1": "MODULE LINK",
        "J10": "FACTORY DEBUG", "J11": "FACTORY DEBUG",
    },
    "analog": {"J10": "ADC IN (BNC)", "J8": "4-20 mA IN", "J9": "4-20 mA OUT", "J11": "DAC OUT", "CN1": "MODULE LINK"},
}
TITLES = {"digital": "Digital board", "analog": "Analog module"}


def bounds(b):
    xs = [p[0] for p in G[b]["outline"]]
    ys = [p[1] for p in G[b]["outline"]]
    return min(xs), min(ys), max(xs), max(ys)


def draw_board(ax, b, fill=BOARD, parts=True, alpha=1.0):
    d = G[b]
    ax.add_patch(Polygon(d["outline"], closed=True, fc=fill, ec=INK, lw=1.1, alpha=alpha, zorder=1))
    for h in d["holes"]:
        ax.add_patch(Circle((h["x"], h["y"]), h["d"] / 2 + 1.2, fc="white", ec=MUTED, lw=0.7, zorder=2))
    if parts:
        for ref in NAMES[b]:
            x, y, w, h = d["parts"][ref]["box"]
            ax.add_patch(Rectangle((x, y), w, h, fc=PART, ec=PART_EDGE, lw=0.7, zorder=3))


def spread(items, lo, hi, gap):
    """Place label centers near their targets, at least `gap` apart, within [lo, hi]."""
    items = sorted(items, key=lambda t: t[1])
    pos = [t[1] for t in items]
    for _ in range(200):
        for i in range(1, len(pos)):
            if pos[i] - pos[i - 1] < gap:
                mid = (pos[i] + pos[i - 1]) / 2
                pos[i - 1], pos[i] = mid - gap / 2, mid + gap / 2
        pos = [min(max(p, lo), hi) for p in pos]
    return [(t[0], p) for t, p in zip(items, pos)]


def label(ax, x, y, text, ha="center"):
    ax.text(x, y, text, ha=ha, va="center", fontsize=6.2, color="white", weight="bold", zorder=7,
            bbox=dict(boxstyle="round,pad=0.35,rounding_size=0.8", fc=ACCENT, ec="none"))


def ports_figure(b, out):
    x0, y0, x1, y1 = bounds(b)
    d = G[b]
    groups = {}
    for ref, name in NAMES[b].items():
        x, y, w, h = d["parts"][ref]["box"]
        groups.setdefault(name, []).append((x + w / 2, y + h / 2))
    sides = {"top": [], "bottom": [], "left": [], "right": []}
    for name, pts in groups.items():
        mx = sum(p[0] for p in pts) / len(pts)
        my = sum(p[1] for p in pts) / len(pts)
        dist = {"top": my - y0, "bottom": y1 - my, "left": mx - x0, "right": x1 - mx}
        side = min(dist, key=dist.get)
        if dist[side] > 30:
            side = "right"  # interior parts are labeled from the right margin
        sides[side].append((name, mx, my, pts))

    fig, ax = plt.subplots(figsize=(4.9, 5.5))  # printed at about 1:1 (125 mm wide)
    draw_board(ax, b)
    margin = 34
    for side, items in sides.items():
        if not items:
            continue
        if side in ("top", "bottom"):
            placed = spread([(it, it[1]) for it in items], x0 - 12, x1 + 12, 24)
            for k, ((name, mx, my, pts), lx) in enumerate(placed):
                row = k % (3 if len(placed) > 5 else 2) if len(placed) > 3 else 0
                ly = (y0 - 10 - row * 8) if side == "top" else (y1 + 10 + row * 8)
                for px, py in pts:
                    ax.plot([px, px, lx], [py, ly + (3 if side == "top" else -3), ly], color=ACCENT, lw=0.7, zorder=6)
                    ax.add_patch(Circle((px, py), 0.9, fc=ACCENT, ec="none", zorder=6))
                label(ax, lx, ly, name)
        else:
            placed = spread([(it, it[2]) for it in items], y0, y1, 9)
            lx = x1 + 8 if side == "right" else x0 - 8
            for (name, mx, my, pts), ly in placed:
                for px, py in pts:
                    ax.plot([px, lx], [py, ly], color=ACCENT, lw=0.7, zorder=6)
                    ax.add_patch(Circle((px, py), 0.9, fc=ACCENT, ec="none", zorder=6))
                label(ax, lx, ly, name, ha="left" if side == "right" else "right")
    ax.text((x0 + x1) / 2, y0 - 36, "FRONT EDGE", ha="center", fontsize=6.5, color=MUTED)
    ax.text((x0 + x1) / 2, y1 + 36, "REAR EDGE", ha="center", fontsize=6.5, color=MUTED)
    ax.set_xlim(x0 - margin, x1 + 45)
    ax.set_ylim(y1 + 40, y0 - 40)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(out, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


def dim(ax, a, b, off, text, vertical=False):
    """Dimension line between points a and b, offset by `off` (mm)."""
    (ax_, ay), (bx, by) = a, b
    kw = dict(color=INK, lw=0.6, zorder=6)
    if vertical:
        x = ax_ + off
        ax.plot([ax_, x + (1.5 if off > 0 else -1.5)], [ay, ay], color=MUTED, lw=0.4)
        ax.plot([bx, x + (1.5 if off > 0 else -1.5)], [by, by], color=MUTED, lw=0.4)
        ax.annotate("", (x, ay), (x, by), arrowprops=dict(arrowstyle="<->", **kw))
        ax.text(x + (2 if off > 0 else -2), (ay + by) / 2, text, rotation=90, ha="left" if off > 0 else "right",
                va="center", fontsize=7, color=INK)
    else:
        y = ay + off
        ax.plot([ax_, ax_], [ay, y + (1.5 if off > 0 else -1.5)], color=MUTED, lw=0.4)
        ax.plot([bx, bx], [by, y + (1.5 if off > 0 else -1.5)], color=MUTED, lw=0.4)
        ax.annotate("", (ax_, y), (bx, y), arrowprops=dict(arrowstyle="<->", **kw))
        ax.text((ax_ + bx) / 2, y + (2.2 if off > 0 else -2.2), text, ha="center",
                va="top" if off > 0 else "bottom", fontsize=7, color=INK)


def mechanical(out):
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 5.6))
    for ax, b in zip(axes, ["digital", "analog"]):
        x0, y0, x1, y1 = bounds(b)
        draw_board(ax, b, parts=False)
        hs = G[b]["holes"]
        tl, tr, bl = hs[0], hs[1], hs[2]
        dim(ax, (x0, y0), (x1, y0), -9, f"{x1 - x0:.2f}")
        dim(ax, (x1, y0), (x1, y1), 9, f"{y1 - y0:.2f}", vertical=True)
        dim(ax, (tl["x"], tl["y"]), (tr["x"], tr["y"]), (y1 - tl["y"]) + 9, f"{tr['x'] - tl['x']:.2f}")
        dim(ax, (tl["x"], tl["y"]), (bl["x"], bl["y"]), -(tl["x"] - x0) - 9, f"{bl['y'] - tl['y']:.2f}",
            vertical=True)
        ax.text(tl["x"] + 4, tl["y"] + 4, f"4x {tl['d']:.1f} mm", fontsize=6.5, color=MUTED, va="top")
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, TITLES[b], ha="center", va="center", fontsize=9, color=MUTED)
        ax.set_xlim(x0 - 22, x1 + 18)
        ax.set_ylim(y1 + 20, y0 - 18)
        ax.set_aspect("equal")
        ax.axis("off")
    fig.savefig(out, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


def block_diagram(out):
    """Functional block diagram: which block serves which port. Coordinates in arbitrary units."""
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    ax.set_xlim(0, 150)
    ax.set_ylim(106, 0)
    ax.axis("off")

    def region(x, y, w, h, title):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=2", fc="#f6f8f9",
                                    ec=MUTED, lw=0.8, ls=(0, (4, 2)), zorder=1))
        ax.text(x + 2, y + 3.2, title, fontsize=7.5, color=MUTED, weight="bold", va="center", zorder=2)

    def box(x, y, w, h, title, sub=""):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc="#dfe8ef",
                                    ec=PART_EDGE, lw=0.8, zorder=4))
        ax.text(x + w / 2, y + h / 2 - (1.7 if sub else 0), title, ha="center", va="center", fontsize=7.2,
                weight="bold", color=INK, zorder=5)
        if sub:
            ax.text(x + w / 2, y + h / 2 + 2.3, sub, ha="center", va="center", fontsize=5.6, color=MUTED, zorder=5)

    def port(x, y, text, ha="left"):
        ax.text(x, y, text, ha=ha, va="center", fontsize=6.2, color="white", weight="bold", zorder=6,
                bbox=dict(boxstyle="round,pad=0.3,rounding_size=0.8", fc=ACCENT, ec="none"))

    def wire(pts, text="", tx=None, ty=None):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=INK, lw=0.8, zorder=3)
        if text:
            ax.text(tx, ty, text, ha="center", va="center", fontsize=5.4, color=MUTED, zorder=5,
                    bbox=dict(boxstyle="square,pad=0.15", fc="#f6f8f9", ec="none"))

    region(26, 4, 94, 60, "DIGITAL BOARD")
    region(26, 71, 94, 33, "ANALOG MODULE")

    box(32, 12, 30, 17, "MCU", "STM32H563, 250 MHz")
    box(84, 12, 30, 17, "FPGA", "iCE40UP5K, 48 MHz")
    box(64, 34, 26, 9, "PSRAM", "8 MB, shared")
    box(94, 34, 20, 9, "I/O level", "1.8 / 3.3 V")
    box(32, 48, 30, 9, "DUT power", "eFuses, current monitors")
    box(94, 47, 20, 9, "CAN", "transceiver")

    box(32, 78, 26, 10, "ADC", "16-bit, 400 kS/s")
    box(64, 78, 26, 10, "DAC", "16-bit, 4 channels")
    box(96, 78, 20, 10, "Relays", "signal routing")
    box(32, 92, 26, 9, "Input front end", "±30 V / ±5.4 V")
    box(64, 92, 26, 9, "Output stages", "0-3.3 V, 0-5 V, ±12 V")
    box(96, 92, 20, 9, "4-20 mA", "input, output")

    # host side
    port(1, 17, "HOST / POWER")
    port(1, 25, "ETHERNET")
    port(1, 52.5, "EXT SUPPLY IN")
    wire([(20.5, 17), (32, 17)], "USB", 26.5, 17)
    wire([(16.5, 25), (32, 25)], "10/100", 25, 25)
    wire([(21, 52.5), (32, 52.5)])
    # MCU and FPGA
    wire([(62, 20.5), (84, 20.5)], "SPI", 73, 20.5)
    wire([(40, 29), (40, 48)])
    wire([(58, 29), (58, 38.5), (64, 38.5)])
    wire([(92, 29), (92, 38.5), (90, 38.5)])
    wire([(104, 29), (104, 34)])
    wire([(50, 29), (50, 45), (104, 45), (104, 47)])
    # DUT side
    port(126, 38.5, "I/O HEADER")
    wire([(114, 38.5), (126, 38.5)], "LA1-LA14", 120, 35.6)
    wire([(114, 51.5), (122, 51.5), (122, 38.5)])
    ax.text(123.5, 49, "CAN, DUT RESET", fontsize=5.2, color=MUTED, ha="left", va="center", zorder=5)
    port(126, 61, "DUT 5V")
    port(126, 68, "DUT EXT")
    wire([(47, 57), (47, 61), (126, 61)])
    wire([(124, 61), (124, 68), (126, 68)])
    # module link
    wire([(110, 29), (110, 31.5), (118, 31.5), (118, 76), (77, 76), (77, 78)])
    wire([(45, 76), (77, 76)])
    wire([(45, 76), (45, 78)])
    wire([(106, 76), (106, 78)])
    ax.text(72, 67, "MODULE LINK (24-pin FFC): ADC and DAC from the FPGA; I2C and 5 V from the MCU", fontsize=5.6,
            color=MUTED, ha="center", va="center", zorder=5)
    wire([(45, 88), (45, 92)])
    wire([(77, 88), (77, 92)])
    wire([(106, 88), (106, 92)])
    port(126, 85, "ADC IN")
    port(126, 93, "DAC OUT")
    port(126, 101, "4-20 mA IN / OUT")
    wire([(58, 96.5), (64, 96.5)])
    wire([(116, 96.5), (121, 96.5), (121, 85), (126, 85)])
    wire([(121, 93), (126, 93)])
    wire([(121, 96.5), (121, 101), (126, 101)])
    fig.savefig(out, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)

if __name__ == "__main__":
    ports_figure("digital", os.path.join(HERE, "ports-digital.svg"))
    ports_figure("analog", os.path.join(HERE, "ports-analog.svg"))
    mechanical(os.path.join(HERE, "mechanical.svg"))
    block_diagram(os.path.join(HERE, "block-diagram.svg"))
