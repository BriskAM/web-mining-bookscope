"""Clean raw scraped data -> data/clean_books.csv"""
import pandas as pd

def clean(df):
    df = df.drop_duplicates(subset="upc").copy()
    df["price"] = df["price"].str.replace(r"[^\d.]", "", regex=True).astype(float)
    df["description"] = df["description"].fillna("").str.replace(r"\s+", " ", regex=True).str.strip()
    df["desc_len"] = df["description"].str.split().str.len()
    df["price_band"] = pd.cut(df["price"], [0, 20, 35, 50, 100], labels=["budget", "mid", "premium", "luxury"])
    return df

if __name__ == "__main__":
    out = clean(pd.read_csv("data/raw_books.csv"))
    out.to_csv("data/clean_books.csv", index=False)
    print(out.shape, out.isna().sum().to_dict())
