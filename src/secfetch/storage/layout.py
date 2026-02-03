from __future__ import annotations

import re
from pathlib import Path


def form_dir_name(form_type: str) -> str:
    """
    Convert a form type into a safe directory name.
    Example: "10-Q/A" -> "10-Q_A"
    """
    s = form_type.strip()
    s = s.replace("/", "_")
    s = re.sub(r"\s+", "", s)
    return s


def filings_root(data_dir: Path) -> Path:
    return data_dir / "filings"


def filings_dir_for_quarter(data_dir: Path, year: int, quarter: int) -> Path:
    """Path for all filings of a quarter: data/filings/<year>/QTR<q>/."""
    return filings_root(data_dir) / str(year) / f"QTR{quarter}"


def filing_dir(
    *,
    data_dir: Path,
    year: int,
    quarter: int,
    form_type: str,
    cik: str,
    accession: str,
) -> Path:
    """Path for one filing: data/filings/<year>/QTR<q>/<form>/<cik>/<accession>."""
    return (
        filings_root(data_dir)
        / str(year)
        / f"QTR{quarter}"
        / form_dir_name(form_type)
        / cik.zfill(10)
        / accession
    )

