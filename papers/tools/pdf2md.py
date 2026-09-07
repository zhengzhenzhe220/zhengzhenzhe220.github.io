#!/usr/bin/env python3
"""
pdf2md.py — batch-convert the PDFs in papers/ to Markdown with pymupdf4llm.

Layout (all relative to the papers/ directory, the parent of tools/):
    papers/<name>.pdf                  source PDFs
    papers/fulltext/<name>.md          converted markdown (+ frontmatter)
    papers/fulltext/assets/<name>/     images extracted from that PDF
    papers/INDEX.md                    generated index: filename + page count

Behaviour:
  - Skips a PDF whose .md exists and is newer than the PDF (unless --force).
  - Each .md starts with YAML frontmatter: source, pages, converter, converted_at.
  - After converting, rebuilds papers/INDEX.md from every .md in fulltext/.

Usage:
    uv run tools/pdf2md.py --limit 3          # test on the first 3 PDFs
    uv run tools/pdf2md.py                     # convert everything (incremental)
    uv run tools/pdf2md.py --force a.pdf b.pdf # force-reconvert specific files
"""

import argparse
import datetime
import os
import re
import sys

import pymupdf                      # PyMuPDF, for the page count
import pymupdf4llm                  # the converter

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
PAPERS_DIR = os.path.dirname(TOOLS_DIR)
FULLTEXT_DIR = os.path.join(PAPERS_DIR, "fulltext")
ASSETS_DIR = os.path.join(FULLTEXT_DIR, "assets")
INDEX_PATH = os.path.join(PAPERS_DIR, "INDEX.md")


def list_pdfs():
    """Top-level PDFs in papers/, sorted case-insensitively."""
    out = []
    for name in os.listdir(PAPERS_DIR):
        if name.lower().endswith(".pdf") and os.path.isfile(os.path.join(PAPERS_DIR, name)):
            out.append(name)
    return sorted(out, key=str.lower)


def needs_convert(pdf_path, md_path, force):
    if force:
        return True
    if not os.path.exists(md_path):
        return True
    # skip when the md is newer than the pdf
    return os.path.getmtime(md_path) < os.path.getmtime(pdf_path)


def sanitize(s):
    """Fix surrogate code points that pymupdf4llm can emit for astral glyphs
    (e.g. math bold 𝐀 = U+1D400 arriving as a UTF-16 surrogate pair). The
    UTF-16 round-trip recombines valid pairs into the real character; any lone
    surrogate is replaced so the text always encodes to UTF-8."""
    return s.encode("utf-16", "surrogatepass").decode("utf-16", "replace")


def frontmatter(source_name, pages):
    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    return (
        "---\n"
        f"source: {source_name}\n"
        f"pages: {pages}\n"
        "converter: pymupdf4llm\n"
        f"converted_at: {now}\n"
        "---\n\n"
    )


def convert_one(pdf_name, force):
    """Convert a single PDF. Returns (status, pages) where status is
    'converted' | 'skipped' | 'error:<msg>'."""
    pdf_path = os.path.join(PAPERS_DIR, pdf_name)
    stem = os.path.splitext(pdf_name)[0]
    md_path = os.path.join(FULLTEXT_DIR, stem + ".md")

    if not needs_convert(pdf_path, md_path, force):
        # still need the page count for the index; read it cheaply
        try:
            with pymupdf.open(pdf_path) as d:
                return "skipped", d.page_count
        except Exception:
            return "skipped", None

    try:
        with pymupdf.open(pdf_path) as d:
            pages = d.page_count
    except Exception as e:
        return f"error: cannot open ({e})", None

    # Filesystem-safe folder name for images. pymupdf4llm rewrites spaces/parens
    # in image_path itself, so passing an already-safe name keeps the folder we
    # create and the folder it writes to in sync (e.g. "TON24 (1)" -> "TON24_1").
    safe_stem = re.sub(r"[^A-Za-z0-9._-]+", "_", stem)
    img_rel = os.path.join("assets", safe_stem)
    img_dir = os.path.join(ASSETS_DIR, safe_stem)
    os.makedirs(img_dir, exist_ok=True)

    # Run from fulltext/ so pymupdf4llm's relative image links (image_path)
    # resolve to assets/<stem>/… — clean paths inside the .md.
    prev_cwd = os.getcwd()
    try:
        os.chdir(FULLTEXT_DIR)
        md_body = pymupdf4llm.to_markdown(
            pdf_path,
            write_images=True,
            image_path=img_rel,
            image_format="png",
            dpi=150,
            show_progress=False,
        )
    except Exception as e:
        return f"error: convert failed ({e})", pages
    finally:
        os.chdir(prev_cwd)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(frontmatter(pdf_name, pages))
        f.write(sanitize(md_body))

    # drop the images dir if the PDF had none, to avoid empty folders
    try:
        if not os.listdir(img_dir):
            os.rmdir(img_dir)
    except OSError:
        pass

    return "converted", pages


def read_pages_from_md(md_path):
    """Pull the `pages:` value out of a converted .md's frontmatter."""
    try:
        with open(md_path, encoding="utf-8") as f:
            if f.readline().strip() != "---":
                return None
            for line in f:
                if line.strip() == "---":
                    break
                if line.startswith("pages:"):
                    return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return None


def rebuild_index():
    """Regenerate papers/INDEX.md from every .md in fulltext/."""
    rows = []
    if os.path.isdir(FULLTEXT_DIR):
        for name in sorted(os.listdir(FULLTEXT_DIR), key=str.lower):
            if not name.endswith(".md"):
                continue
            md_path = os.path.join(FULLTEXT_DIR, name)
            pages = read_pages_from_md(md_path) or "?"
            stem = name[:-3]
            rows.append((stem, pages, name))

    now = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    lines = [
        "# Papers — full-text index",
        "",
        f"Generated by `tools/pdf2md.py` at {now}. {len(rows)} document(s).",
        "",
        "| # | Paper | Pages | Markdown |",
        "|---|-------|-------|----------|",
    ]
    for i, (stem, pages, md_name) in enumerate(rows, 1):
        lines.append(f"| {i} | {stem} | {pages} | [fulltext/{md_name}](fulltext/{md_name}) |")
    lines.append("")
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return len(rows)


def main():
    ap = argparse.ArgumentParser(description="Convert papers/*.pdf to fulltext/*.md")
    ap.add_argument("--limit", type=int, default=None,
                    help="only process the first N PDFs (for a test run)")
    ap.add_argument("--force", action="store_true",
                    help="reconvert even if the .md is newer than the PDF")
    ap.add_argument("pdfs", nargs="*",
                    help="specific PDF filenames to convert (default: all)")
    args = ap.parse_args()

    os.makedirs(FULLTEXT_DIR, exist_ok=True)
    os.makedirs(ASSETS_DIR, exist_ok=True)

    targets = args.pdfs if args.pdfs else list_pdfs()
    if args.limit is not None:
        targets = targets[:args.limit]

    if not targets:
        print("No PDFs found.")
        return

    print(f"Processing {len(targets)} PDF(s) from {PAPERS_DIR}\n")
    n_conv = n_skip = n_err = 0
    for i, name in enumerate(targets, 1):
        status, pages = convert_one(name, args.force)
        tag = status.split(":")[0]
        if tag == "converted":
            n_conv += 1
            print(f"[{i}/{len(targets)}] ✓ {name}  ({pages} pages)")
        elif tag == "skipped":
            n_skip += 1
            print(f"[{i}/{len(targets)}] – {name}  (up to date, skipped)")
        else:
            n_err += 1
            print(f"[{i}/{len(targets)}] ✗ {name}  {status}", file=sys.stderr)

    total = rebuild_index()
    print(f"\nDone: {n_conv} converted, {n_skip} skipped, {n_err} errors.")
    print(f"INDEX.md updated: {total} document(s) listed.")


if __name__ == "__main__":
    main()
