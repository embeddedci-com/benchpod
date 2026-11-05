"""Build a datasheet PDF from its Markdown source.

    make            # figures + both PDFs
    make pdf        # BenchPod-datasheet.pdf from datasheet.md
    make bridge     # BenchPod-WiFi-bridge-datasheet.pdf from wifi-bridge.md
    python build.py [source.md]   # default datasheet.md

The PDF name comes from the source's "<!-- output: name.pdf -->" line (default BenchPod-datasheet.pdf).

Markdown -> HTML (style.css) -> PDF through headless Chrome. The first lines of datasheet.md up to
the first "## " heading are the cover block.
"""
import os
import re
import shutil
import subprocess
import sys

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME_CANDIDATES = [
    os.environ.get("CHROME", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium", "chromium-browser",
]


def chrome():
    for c in CHROME_CANDIDATES:
        if c and (os.path.exists(c) or shutil.which(c)):
            return c
    sys.exit("Chrome not found; set CHROME=/path/to/chrome")


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "datasheet.md"
    src = open(os.path.join(HERE, name), encoding="utf-8").read()
    meta = dict(re.findall(r"^<!--\s*(\w+):\s*(.*?)\s*-->$", src, re.M))
    body = markdown.markdown(src, extensions=["tables", "attr_list", "md_in_html", "sane_lists", "fenced_code"])
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{meta.get('title', 'BenchPod datasheet')}</title>
<link rel="stylesheet" href="style.css">
<style>@page {{ @bottom-left {{ content: "{meta.get('footer', '')}"; }} }}</style>
</head><body>{body}</body></html>"""
    html_path = os.path.join(HERE, os.path.splitext(os.path.basename(name))[0] + ".html")
    open(html_path, "w", encoding="utf-8").write(html)
    out = os.path.join(HERE, meta.get("output", "BenchPod-datasheet.pdf"))
    subprocess.run([chrome(), "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out}", "file://" + html_path], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(out)


main()
