# News NLP Text Analysis

This project converts a Blackcoffer-style text analytics assignment into a cleaner NLP portfolio project. The original workflow scraped article text, stored each article as a text file, and calculated business-facing linguistic indicators such as polarity, subjectivity, Fog Index, average sentence length, complex-word count, and personal pronoun frequency.

The repository keeps the original Python assignment script in `src/blackcoffer_analysis.py`, adds a reusable metric module in `src/text_metrics.py`, and presents the output through a Dash app instead of a generic Streamlit page.

## What This Demonstrates

- Web/text ingestion workflow for article corpora.
- Rule-based sentiment scoring using positive and negative lexicons.
- Readability scoring with complex-word and sentence-length metrics.
- Editorial review prioritization using Fog Index and sentiment thresholds.
- Dash dashboard design for analytics storytelling.

## Repository Structure

- `src/blackcoffer_analysis.py` - original coursework script.
- `src/text_metrics.py` - cleaned reusable metric functions.
- `data/news_metrics_sample.csv` - safe portfolio sample of computed metrics.
- `artifacts/Output.xlsx` - original output workbook retained as an artifact.
- `dash_app.py` - interactive Dash dashboard.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python dash_app.py
```

Then open the local Dash URL shown in the terminal.

## Portfolio Note

The public repo avoids publishing the full scraped article corpus as the primary dataset. The sample metrics file is enough to demonstrate the analysis and dashboard without turning the repository into a raw data dump.
