

# Mass OCR + LLM Cleanup Workflow: Batch Scanned-Document to Markdown Tool

Utility
-------
This script is an end-to-end pipeline designed to process a large batch of scanned document images
and convert them into a single readable Markdown file. It automates typical preprocessing needed
for OCR (format conversion, cropping, resizing/enhancement), extracts text using an OCR model, then
uses a language model to clean and normalize the OCR output for human-friendly reading, and finally
merges all pages into one consolidated Markdown document.

What it does (high-level)
-------------------------
1) Image format normalization:
    Converts all images in a "raw" input directory from a specified source format (e.g., HEIC)
    into PNG to ensure consistent downstream processing.

2) Assisted batch cropping:
    Invokes a cropping step across the directory so you can focus OCR on relevant regions
    (e.g., removing borders, margins, scanner artifacts).

3) OCR-oriented enhancement:
    Resizes and optionally applies grayscale processing to improve OCR accuracy and reduce noise.

4) OCR extraction to text:
    Runs OCR for each processed image using an Ollama-hosted OCR-capable model, producing
    per-image/per-page text outputs (Markdown-oriented extraction prompt).

5) LLM-based text cleanup:
    Sends the OCR text through a language model to fix common OCR defects (broken words, spacing,
    punctuation), remove repetitive layout artifacts (headers/footers/page numbers), and preserve
    essential structure (titles, lists). The cleaning is intended to be faithful: it should not
    invent content or translate.

6) Consolidation:
    Merges all cleaned text files into a single Markdown file for easier reading, searching,
    and downstream use.

Typical use case
----------------
- You have many photos/scans of printed pages (books, notes, reports).
- You want a repeatable pipeline that converts them into one readable Markdown document.
- You want OCR text that is cleaned of common scanning/OCR artifacts without changing meaning.

Directory expectations
----------------------
- Input images are placed in the configured "raw_pics" directory.
- Intermediate processed images and output text are written to dedicated directories
  (e.g., clean_pics, raw_text_OCR, clean_text), culminating in a merged Markdown output.

Notes
-----
- Requires a running Ollama server and the referenced OCR/LLM models available locally.
- The conversion input format must match the source images in the input directory.
"""