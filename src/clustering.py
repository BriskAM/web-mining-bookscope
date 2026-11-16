"""Unsupervised topic clusters from descriptions (TF-IDF + KMeans + SVD plot)"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import silhouette_score

df = pd.read_csv("data/clean_books.csv").fillna({"description": ""})
df = df[df["description"].str.len() > 0].reset_index(drop=True)
vec = TfidfVectorizer(stop_words="english", max_features=4000, min_df=3)
X = vec.fit_transform(df["description"])

best = max(((k, silhouette_score(X, KMeans(k, n_init=5, random_state=0).fit_predict(X)))
            for k in range(4, 9)), key=lambda t: t[1])
print("best k=%d silhouette=%.3f" % best)
km = KMeans(best[0], n_init=10, random_state=0).fit(X)
df["cluster"] = km.labels_

terms = vec.get_feature_names_out()
for c in range(best[0]):
    top = km.cluster_centers_[c].argsort()[::-1][:8]
    print(f"cluster {c} ({(df.cluster==c).sum()} books):", ", ".join(terms[top]))

xy = TruncatedSVD(2, random_state=0).fit_transform(X)
plt.scatter(xy[:, 0], xy[:, 1], c=df["cluster"], cmap="tab10", s=8)
plt.title("Description clusters (SVD projection)")
plt.tight_layout(); plt.savefig("reports/clusters.png", dpi=130)
df[["title", "category", "cluster"]].to_csv("reports/clusters.csv", index=False)
