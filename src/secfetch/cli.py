from __future__ import annotations

import argparse
import json
import sys

from secfetch import download_quarter, download_year
from secfetch.downloader import DownloadResult, has_existing_data_for_quarter

# Spinner chars for loading style (cycle per completion)
SPINNER = "|/-\\"

# ANSI colors for progress (no-op if not a TTY)
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
BOLD = "\033[1m"
RESET = "\033[0m"


def _progress_callback(
    current: int, total: int, result: DownloadResult | None, in_progress: int = 0
) -> None:
    if total == 0:
        return
    spin = "..." if result is None else SPINNER[(current - 1) % len(SPINNER)]
    # Colourful: label in cyan, count in green, spinner in yellow, in_progress in magenta
    in_progress_part = f" {MAGENTA}({in_progress} downloading){RESET}" if in_progress else ""
    msg = f"\r  {CYAN}{BOLD}Processing{RESET} {GREEN}{current}/{total}{RESET} {YELLOW}{spin}{RESET}{in_progress_part}  "
    sys.stderr.write(msg)
    sys.stderr.flush()


def _prompt_resume_or_redownload(year: int, quarter: int | None) -> bool:
    """Ask user: resume or redownload? Returns True for redownload, False for resume."""
    qlabel = f"Q{quarter}" if quarter is not None else "all quarters"
    sys.stderr.write(
        f"Existing data found for {year} {qlabel}. "
        "Resume (skip already downloaded) or Redownload (delete and fetch again)? [Resume/Redownload]: "
    )
    sys.stderr.flush()
    try:
        line = sys.stdin.readline().strip().lower()
    except (EOFError, KeyboardInterrupt):
        return False
    return line in ("redownload", "r", "re-download", "redownload")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="secfetch")
    sub = p.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("quarter", help="Download filings for a quarter")
    q.add_argument("--year", type=int, required=True)
    q.add_argument("--quarter", type=int, required=True, choices=[1, 2, 3, 4])
    q.add_argument("--forms", nargs="*", default=["10-Q"], help="Form types (default: 10-Q)")
    q.add_argument("--data-dir", default="data")
    q.add_argument("--file-types", nargs="+", default=[".htm", ".html", ".xml", ".xbrl", ".pdf"])
    q.add_argument("--include-amended", action="store_true")
    q.add_argument("--concurrency", type=int, default=6)
    q.add_argument("--user-agent", default=None)
    q.add_argument("--redownload", action="store_true", help="Delete existing data for this run and download again")

    y = sub.add_parser("year", help="Download filings for a year (all quarters)")
    y.add_argument("--year", type=int, required=True)
    y.add_argument("--forms", nargs="*", default=["10-Q"], help="Form types (default: 10-Q)")
    y.add_argument("--data-dir", default="data")
    y.add_argument("--file-types", nargs="+", default=[".htm", ".html", ".xml", ".xbrl", ".pdf"])
    y.add_argument("--include-amended", action="store_true")
    y.add_argument("--concurrency", type=int, default=6)
    y.add_argument("--user-agent", default=None)
    y.add_argument("--redownload", action="store_true", help="Delete existing data and download again")

    args = p.parse_args(argv)

    if not getattr(args, "forms", None):
        args.forms = ["10-Q"]
    redownload = getattr(args, "redownload", False)
    data_dir = args.data_dir

    if args.cmd == "quarter":
        has_existing = has_existing_data_for_quarter(data_dir, args.year, args.quarter)
        if has_existing and not redownload and sys.stdin.isatty():
            redownload = _prompt_resume_or_redownload(args.year, args.quarter)
    else:
        quarters = getattr(args, "quarters", (1, 2, 3, 4))
        has_existing = any(
            has_existing_data_for_quarter(data_dir, args.year, q) for q in quarters
        )
        if has_existing and not redownload and sys.stdin.isatty():
            redownload = _prompt_resume_or_redownload(args.year, None)

    try:
        if args.cmd == "quarter":
            res = download_quarter(
                year=args.year,
                quarter=args.quarter,
                forms=args.forms,
                data_dir=args.data_dir,
                file_types=args.file_types,
                include_amended=args.include_amended,
                concurrency=args.concurrency,
                user_agent=args.user_agent,
                redownload=redownload,
                on_progress=_progress_callback,
            )
        else:
            res = download_year(
                year=args.year,
                forms=args.forms,
                data_dir=args.data_dir,
                file_types=args.file_types,
                include_amended=args.include_amended,
                concurrency=args.concurrency,
                user_agent=args.user_agent,
                redownload=redownload,
                on_progress=_progress_callback,
            )
    finally:
        # Clear progress line so JSON output starts clean
        sys.stderr.write("\r" + " " * 60 + "\r")
        sys.stderr.flush()

    print(json.dumps([r.__dict__ for r in res], indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

