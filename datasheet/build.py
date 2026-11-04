"""Build BenchPod-datasheet.pdf from datasheet.md.

    make            # figures + PDF
    make pdf        # PDF only (figures already drawn)

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
    src = open(os.path.join(HERE, "datasheet.md"), encoding="utf-8").read()
    meta = dict(re.findall(r"^<!--\s*(\w+):\s*(.*?)\s*-->$", src, re.M))
    body = markdown.markdown(src, extensions=["tables", "attr_list", "md_in_html", "sane_lists", "fenced_code"])
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{meta.get('title', 'BenchPod datasheet')}</title>
<link rel="stylesheet" href="style.css">
<style>@page {{ @bottom-left {{ content: "{meta.get('footer', '')}"; }} }}</style>
</head><body>{body}</body></html>"""
    html_path = os.path.join(HERE, "datasheet.html")
    open(html_path, "w", encoding="utf-8").write(html)
    out = os.path.join(HERE, "BenchPod-datasheet.pdf")
    subprocess.run([chrome(), "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out}", "file://" + html_path], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(out)


main()
