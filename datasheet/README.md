# BenchPod datasheet

Source of the BenchPod product datasheet and the Wi-Fi bridge accessory datasheet (PDFs). Edit `datasheet.md` or
`wifi-bridge.md`, then run `make`.

| File | What |
|---|---|
| `datasheet.md` | The text and tables (Markdown; `<div class="page-break"></div>` starts a new page) |
| `wifi-bridge.md` | The Wi-Fi bridge datasheet, same format; its `<!-- output: -->` line names the PDF |
| `style.css` | Print layout: US Letter, fonts, colors, tables, footer |
| `figures/draw.py` | Draws the port and dimension figures; the port names on the figures are set here |
| `figures/geometry.json` | Board outlines, holes and connector positions, extracted from the tagged KiCad PCBs |
| `figures/extract_geometry.py` | Rebuilds `geometry.json` from the board tags (needs KiCad; `make geometry`) |
| `build.py` | Markdown to HTML to PDF through headless Chrome |

```bash
make            # figures + both PDFs
make pdf        # BenchPod-datasheet.pdf only
make bridge     # BenchPod-WiFi-bridge-datasheet.pdf only (not on the Downloads page)
make geometry   # after a new board tag: update the tags in figures/extract_geometry.py first
make upload     # publish the PDF to the website's Downloads page (needs the Spaces S3_* variables)
```

Needs Python 3 and Google Chrome (set `CHROME=` for another Chromium). The first `make` creates `.venv`.

Port names (DUT 5V, I/O HEADER, ...) are the user-facing names. Board reference designators stay out
of the datasheet.
