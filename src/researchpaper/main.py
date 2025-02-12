import pymupdf
from pymupdf import Document, Rect
import time
from .constants import REFERENCES_MARK
from .exceptions import NoTableOfContentFound, NoReferenceMarkFound
import re


def analyze(filepath):
    doc = pymupdf.open(filepath)
    for page in doc:
        print(page.bound())
        blocks = page.get_text("blocks")
        for block in blocks:
            rect = Rect(*block[:4])
            print(f"Block: {block[4]} - Area: {rect.height}")


def get_bib_references(filepath):
    doc = pymupdf.open(filepath)
    try:
        reference_mark, page_no = find_in_toc(doc.get_toc())
    except NoTableOfContentFound:
        reference_mark, page_no = advance_search(doc)
    except NoReferenceMarkFound:
        return
    print(page_no)
    results = []
    for page in doc[page_no - 1:-1]:
        blocks = page.get_text("blocks")
        for block in blocks:
            results.extend(extract_references(block[4]))
    for result in results:
        print(result)
    print(len(results))


def find_in_toc(toc):
    if not toc:
        print("No Table of Contents found in the PDF.")
        raise NoTableOfContentFound()

    for entry in toc:
        _, title, page = entry
        if title.lower() in REFERENCES_MARK:
            return title, page

    raise NoReferenceMarkFound()


def advance_search(doc: Document) -> tuple[str, str]:
    pass


def extract_references(text):
    ref_pattern = re.compile(r"""
        ^\s*(?:\[\d+]|\d+\.\s*|\d+\)\s*)?  # Match [1], 1., 1)
        ([A-Z][a-zA-Z,.\s-]+)                   # Authors
        \s*\(?(\d{4})\)?\.?                     # Year in (YYYY)
        (.*?)                                   # Title
        (https?://\S+)?                     # DOI/URL (optional)
        """, re.DOTALL | re.VERBOSE | re.MULTILINE)

    matches = ref_pattern.findall(text)
    extracted_refs = []

    for match in matches:
        author, year, title, link = match
        extracted_refs.append({
            "author": author.strip(),
            "year": year.strip(),
            "title": title.strip(),
            "link": link.strip() if link else None
        })

    return extracted_refs
