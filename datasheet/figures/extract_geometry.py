"""Extract board outlines, mounting holes and connector boxes from the tagged KiCad PCBs.

Runs under KiCad's bundled Python (it needs pcbnew):

    /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3 \
        figures/extract_geometry.py figures/geometry.json

The PCBs are read from the git tags below, not the working copy, so the datasheet always matches a
released board revision. The JSON is committed: drawing the figures does not need KiCad.
"""
import json
import os
import subprocess
import sys
import tempfile

import pcbnew

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BOARDS = {
    "digital": ("refs/tags/digital-v3r3", "pcb/benchpod-digital/vbench-pod.kicad_pcb"),
    "analog": ("refs/tags/analog-v3r4", "pcb/benchpod-analog/vbench-pod.kicad_pcb"),
}
# Footprints the datasheet shows. Everything else on the board is left out of the figures.
PARTS = {
    "digital": ["J1", "J4", "J5", "J6", "J7", "USB1", "USB2", "USBC1", "LED1", "SW1", "SW2", "CN1", "J10", "J11"],
    "analog": ["J8", "J9", "J10", "J11", "CN1"],
}

T = pcbnew.ToMM


def load(tag, path):
    data = subprocess.run(["git", "-C", REPO, "show", f"{tag}:{path}"], check=True, capture_output=True).stdout
    with tempfile.NamedTemporaryFile(suffix=".kicad_pcb", delete=False) as f:
        f.write(data)
    try:
        return pcbnew.LoadBoard(f.name)
    finally:
        os.unlink(f.name)


def board_geometry(brd, refs):
    outline = []
    for d in brd.GetDrawings():
        if d.GetLayer() == pcbnew.Edge_Cuts and d.GetShapeStr() == "Polygon":
            o = d.GetPolyShape().Outline(0)
            outline = [[round(T(o.CPoint(i).x), 3), round(T(o.CPoint(i).y), 3)] for i in range(o.PointCount())]
    if not outline:
        sys.exit("no Edge.Cuts polygon found")
    holes, parts = [], {}
    for fp in brd.GetFootprints():
        ref = fp.GetReference()
        if "MountingHole" in fp.GetFPIDAsString():
            drill = max(T(p.GetDrillSize().x) for p in fp.Pads())  # the hole, not the via ring
            holes.append({"x": round(T(fp.GetX()), 3), "y": round(T(fp.GetY()), 3), "d": round(drill, 2)})
        if ref in refs:
            cy = fp.GetCourtyard(pcbnew.F_CrtYd)
            bb = cy.BBox() if cy.OutlineCount() else fp.GetBoundingBox(False)
            parts[ref] = {"box": [round(T(bb.GetX()), 3), round(T(bb.GetY()), 3), round(T(bb.GetWidth()), 3),
                                  round(T(bb.GetHeight()), 3)],
                          "rot": fp.GetOrientationDegrees(), "value": fp.GetValue()}
    missing = set(refs) - set(parts)
    if missing:
        sys.exit(f"footprints not found: {sorted(missing)}")
    return {"outline": outline, "holes": sorted(holes, key=lambda h: (h["y"], h["x"])), "parts": parts}


def main():
    out = {}
    for name, (tag, path) in BOARDS.items():
        out[name] = {"tag": tag.split("/")[-1], **board_geometry(load(tag, path), PARTS[name])}
    with open(sys.argv[1], "w") as f:
        json.dump(out, f, indent=1)


main()
