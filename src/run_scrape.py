"""Scrape listings + detail pages and save data/raw_books.csv"""
import pandas as pd
from scraper import scrape_listings, scrape_details

if __name__ == "__main__":
    listing = pd.DataFrame(scrape_listings())
    print("listing rows:", len(listing))
    detail = pd.DataFrame(scrape_details(listing["url"].tolist()))
    df = listing.merge(detail, on="url")
    df.to_csv("data/raw_books.csv", index=False)
    print("saved", df.shape)
