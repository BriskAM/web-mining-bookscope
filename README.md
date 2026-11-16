# BookScope – Web Mining of an Online Bookstore

A mid-level **web mining** project covering the full pipeline: web scraping, data cleaning,
exploratory analysis, text mining and machine learning on data from
[Books to Scrape](https://books.toscrape.com), a sandbox site built for scraping practice.

## Pipeline
| Stage | File | What it does |
|---|---|---|
| Web content mining | `src/scraper.py`, `src/run_scrape.py` | Crawls 50 listing pages + 1000 detail pages (threaded, retries, polite delay) |
| Cleaning | `src/clean.py` | Parses prices, removes duplicates, normalises text, builds price bands |
| EDA | `src/eda.py` | Rating/price/category distributions -> `reports/*.png` |
| Text mining | `src/text_mining.py` | TF-IDF keywords per category -> `reports/top_terms.csv` |
| Clustering | `src/clustering.py` | KMeans topic clusters of descriptions (+ SVD plot) |
| Classification | `src/classifier.py` | Predicts category from description (Logistic Regression) |

## Run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
./run_all.sh
```

## Results
- 1000 books, 50 categories scraped; no missing values after cleaning.
- Price is almost independent of rating (mean ~35 GBP at every rating level).
- TF-IDF recovers meaningful category vocabulary, e.g. Food and Drink -> *recipes, cookbook, kitchen*; Mystery -> *detective, murder, case*.
- KMeans finds 6 clusters (one clean "cooking" cluster); silhouette is low (~0.003), typical for short, diverse text.
- Category classifier reaches ~41% accuracy on 8 imbalanced classes (chance is much lower); see `reports/classification_report.txt`.

## Limitations
Descriptions are short and many categories are tiny, which limits clustering and classification quality.
Only a sandbox site was scraped, respecting a small request delay.
