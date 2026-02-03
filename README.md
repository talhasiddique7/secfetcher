# secfetcher

**Grab SEC EDGAR filings in bulk** — by quarter or by year, straight from the official master index. Pick your forms and file types; skip the rest.

[![PyPI version](https://img.shields.io/pypi/v/secfetcher.svg)](https://pypi.org/project/secfetcher/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 📖 Docs

| Where | What you get |
|-------|----------------|
| **[📄 Full documentation](https://talhasiddique7.github.io/sec-fetcher/)** | Install, quickstart, CLI, form allowlist, API reference — all in one place. |
| [docs/index.html](docs/index.html) | Open locally in your browser. |

---

## Install

**Requires Python 3.10+.**

```bash
pip install secfetcher
```

Using a venv (recommended):

```bash
python -m venv .venv
. .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install secfetcher
```

*PyPI package:* `secfetcher` · *Import / CLI:* `secfetch` or `secfetcher`

---

## Quick start

### Python

```python
from secfetcher import download_quarter, download_year

# One quarter
download_quarter(
    year=2024,
    quarter=3,
    forms=["10-Q", "10-K"],
    data_dir="data",
    file_types=[".xml", ".htm", ".html", ".pdf"],
)

# Full year
download_year(year=2024, forms=["8-K"], data_dir="data", file_types=[".htm", ".html"])
```

### CLI

```bash
secfetch quarter --year 2024 --quarter 3 --forms 10-Q 10-K --data-dir data --file-types .xml .htm .html .pdf
secfetch year --year 2024 --forms 8-K --data-dir data --file-types .htm .html
python -m secfetch --help
```

---

## SEC User-Agent

The SEC requires a User-Agent with your contact info. Set it once:

```bash
export SEC_USER_AGENT="Your Name or Company contact@example.com"
```

You can also pass `user_agent` in code or via the CLI.

---

## Form types

Only allowlisted SEC form types are accepted (e.g. `10-Q`, `10-K`, `8-K`). The list is in `data/config/form_types.json` (created on first run) — edit it to add or remove types. [See the full list in the docs →](https://talhasiddique7.github.io/sec-fetcher/#form-types)

---

## Where files go

Downloads are grouped by **year** and **quarter**:

```
data/
  index/master/<year>/QTR<n>/   ← master index cache
  filings/<year>/QTR<q>/<form>/<cik>/<accession>/   ← your downloads
  _state/manifest.json
```

## Resume vs redownload

If you run again for the same year/quarter, **secfetch** will detect existing data. You can:

- **Resume** (default) — skip filings already downloaded; only fetch the rest.
- **Redownload** — remove existing data for that run and download everything again.

From the CLI, use `--redownload` to force a full re-fetch, or answer the prompt when you run without the flag. From the API, pass `redownload=True`.

---

## Development

```bash
git clone https://github.com/talhasiddique7/sec-fetcher.git && cd sec-fetcher
python -m venv .venv && . .venv/bin/activate
pip install -e ".[test]"
pytest
```

---

## Releasing to PyPI

Push a version tag (e.g. `v0.1.1`) or trigger the workflow from the Actions tab.

---

## License

[MIT](LICENSE)
