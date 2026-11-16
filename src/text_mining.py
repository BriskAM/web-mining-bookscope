"""TF-IDF keyword mining per category -> reports/top_terms.csv"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("data/clean_books.csv").fillna({"description": ""})
df = df[df["description"].str.len() > 0]
vec = TfidfVectorizer(stop_words="english", max_features=5000, ngram_range=(1, 2), min_df=3)
X = vec.fit_transform(df["description"])
terms = vec.get_feature_names_out()

rows = []
for cat in df["category"].value_counts().head(10).index:
    idx = (df["category"] == cat).values
    mean = X[idx].mean(axis=0).A1
    rows.append({"category": cat, "top_terms": ", ".join(terms[mean.argsort()[::-1][:8]])})
out = pd.DataFrame(rows)
out.to_csv("reports/top_terms.csv", index=False)
print(out.to_string(index=False))
