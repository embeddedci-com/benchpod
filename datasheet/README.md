# BenchPod datasheet

Source of the BenchPod datasheets (PDFs), one per board generation, plus the Wi-Fi bridge accessory:

| Source | PDF | Covers |
|---|---|---|
| `datasheet.md` | `BenchPod-datasheet.pdf` | The current BenchPod: digital board v3r3 with analog module v3-r4 (tags `digital-v3r3`, `analog-v3r4`) |
| `datasheet-v3.md` | `BenchPod-v3-datasheet.pdf` | The v3 single board, analog and digital on one PCB: v3-r1 and v3-r2 (tags `analog-v3r1`, `analog-v3r2`) |
| `wifi-bridge.md` | `BenchPod-WiFi-bridge-datasheet.pdf` | The Wi-Fi bridge accessory (the single board has Wi-Fi built in and needs no bridge) |

Edit the Markdown, then run `make`. When a spec, usage note or safety rule changes for every board, change it in
both BenchPod datasheets.

| File | What |
|---|---|
| `datasheet.md` | The text and tables (Markdown; `<div class="page-break"></div>` starts a new page) |
| `datasheet-v3.md`, `wifi-bridge.md` | The other datasheets, same format; the `<!-- output: -->` line names the PDF |
| `style.css` | Print layout: US Letter, fonts, colors, tables, footer |
| `figures/draw.py` | Draws the port, dimension and block figures (`*-single.svg` for the v3 single board); the port names on the figures are set here |
| `figures/geometry.json` | Board outlines, holes and connector positions, extracted from the tagged KiCad PCBs |
| `figures/extract_geometry.py` | Rebuilds `geometry.json` from the board tags (needs KiCad; `make geometry`) |
| `build.py` | Markdown to HTML to PDF through headless Chrome |

```bash
make            # figures + all three PDFs
make pdf        # BenchPod-datasheet.pdf only
make bridge     # BenchPod-WiFi-bridge-datasheet.pdf only
make v3         # BenchPod-v3-datasheet.pdf only
make geometry   # after a new board tag: update the tags in figures/extract_geometry.py first
make upload     # publish the PDF to the website's Downloads page (needs the Spaces S3_* variables)
make upload-bridge  # same for the Wi-Fi bridge datasheet
make upload-v3      # same for the v3 single-board datasheet
```

Needs Python 3 and Google Chrome (set `CHROME=` for another Chromium). The first `make` creates `.venv`.

Port names (DUT 5V, I/O HEADER, ...) are the user-facing names. Board reference designators stay out
of the datasheet.
