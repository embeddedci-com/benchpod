PY := .venv/bin/python
KICAD_PY ?= /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3

.PHONY: all pdf figures geometry upload clean

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

# Publish the PDF for the website's Downloads page. Needs the Spaces credentials in the environment
# (S3_ENDPOINT, S3_BUCKET, S3_ACCESS_KEY_ID, S3_SECRET_ACCESS_KEY, as the server uses them).
upload: pdf
	AWS_ACCESS_KEY_ID="$$S3_ACCESS_KEY_ID" AWS_SECRET_ACCESS_KEY="$$S3_SECRET_ACCESS_KEY" AWS_DEFAULT_REGION=us-east-1 \
	aws s3 cp BenchPod-datasheet.pdf "s3://$$S3_BUCKET/public/downloads/BenchPod-datasheet.pdf" \
		--endpoint-url "$$S3_ENDPOINT" --acl public-read --content-type application/pdf \
		--cache-control "public, max-age=3600"

clean:
	rm -f datasheet.html BenchPod-datasheet.pdf
