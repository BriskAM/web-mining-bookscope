#!/usr/bin/env bash
# Full pipeline: scrape -> clean -> analyse -> mine -> classify
set -e
python src/run_scrape.py
python src/clean.py
python src/eda.py
python src/text_mining.py
python src/clustering.py
python src/classifier.py
