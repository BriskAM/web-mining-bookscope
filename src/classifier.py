"""Predict a book's category from its description (top-8 categories)."""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report, ConfusionMatrixDisplay

df = pd.read_csv("data/clean_books.csv").fillna({"description": ""})
df = df[df["description"].str.len() > 0]
top = df["category"].value_counts().head(8).index
df = df[df["category"].isin(top)]

Xtr, Xte, ytr, yte = train_test_split(df["description"], df["category"],
                                      test_size=0.25, stratify=df["category"], random_state=42)
model = make_pipeline(TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=2),
                      LogisticRegression(max_iter=1000, class_weight="balanced"))
model.fit(Xtr, ytr)
pred = model.predict(Xte)
report = classification_report(yte, pred)
print(report)
open("reports/classification_report.txt", "w").write(report)

fig, ax = plt.subplots(figsize=(8, 7))
ConfusionMatrixDisplay.from_predictions(yte, pred, ax=ax, xticks_rotation=60, colorbar=False)
plt.tight_layout(); plt.savefig("reports/confusion_matrix.png", dpi=130)
