"""Exploratory analysis: saves figures to reports/"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

df = pd.read_csv("data/clean_books.csv")

def save(name):
    plt.tight_layout(); plt.savefig(f"reports/{name}.png", dpi=130); plt.close()

df["rating"].value_counts().sort_index().plot.bar(color="#4c72b0", title="Rating distribution")
save("rating_dist")

df["price"].plot.hist(bins=25, color="#55a868", title="Price distribution (GBP)")
save("price_dist")

top = df["category"].value_counts().head(12)
top.sort_values().plot.barh(color="#c44e52", title="Top 12 categories")
save("top_categories")

df.groupby("category")["price"].mean().loc[top.index].sort_values().plot.barh(
    color="#8172b2", title="Average price, top categories")
save("avg_price_by_category")

print("avg price by rating:\n", df.groupby("rating")["price"].mean().round(2))
print("in stock %:", round(df["in_stock"].mean() * 100, 1))
