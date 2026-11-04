PY := .venv/bin/python
KICAD_PY ?= /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3

.PHONY: all pdf figures geometry clean

all: figures pdf

$(PY):
	python3 -m venv .venv && $(PY) -m pip -q install -r requirements.txt

# Re-read the tagged KiCad PCBs (only needed after a new board tag; needs KiCad).
geometry:
	$(KICAD_PY) figures/extract_geometry.py figures/geometry.json 2>/dev/null

figures: $(PY)
	$(PY) figures/draw.py

pdf: $(PY)
	$(PY) build.py

clean:
	rm -f datasheet.html BenchPod-datasheet.pdf
