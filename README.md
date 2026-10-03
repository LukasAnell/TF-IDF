# TF-IDF

TF-IDF analysis of five Project Gutenberg books on evolution and ethics, for CS 24200 Project 1. The write-up is in `report/report.pdf`.

| ID | Book | Author |
|---|---|---|
| 1228 | On the Origin of Species | Charles Darwin |
| 2300 | The Descent of Man | Charles Darwin |
| 2940 | Evolution and Ethics | T. H. Huxley |
| 46129 | The Data of Ethics | Herbert Spencer |
| 4341 | Mutual Aid | Peter Kropotkin |

## Setup

Requires [uv](https://docs.astral.sh/uv/) (Python 3.12+). From the repository root:

```bash
uv sync
```

## Running

Run each step in order from the repository root. Each step reads the previous step's output from `data/` and writes its own.

```bash
uv run src/tf_idf/parsing_helpers/download_books.py
uv run src/tf_idf/parsing_helpers/trim.py
uv run src/tf_idf/parsing_helpers/normalize.py
uv run src/tf_idf/parsing_helpers/tokenizer.py
uv run src/tf_idf/vectorize.py
uv run src/tf_idf/analysis.py
```

`analysis.py` prints the top terms and similarity matrices to the terminal and saves the plots to `figures/`.

## Report

The report (`report/`) is written in LaTeX and uses the figures from `figures/`:

```bash
cd report
latexmk -pdf report.tex
```
