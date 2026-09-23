import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score
)
from sklearn.decomposition import PCA

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv("../data/processed/customer_segments.csv")

FEATURES = [
    "recency_days",
    "total_orders",
    "avg_spend_per_order",
    "customer_lifetime_days",
    "purchase_frequency",
    "total_spend"
]

X = df[FEATURES]

# ==============================
# SCALE DATA
# ==============================
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X)

# ==============================
# ELBOW + SILHOUETTE + DBI
# ==============================
K_RANGE = range(2, 8)

inertias = []
sil_scores = []
dbi_scores = []

print("\n===================================")
print("KMEANS CLUSTER EVALUATION")
print("===================================\n")

for k in K_RANGE:

    model = KMeans(
        n_clusters=k,
        init="k-means++",
        n_init=20,
        random_state=42
    )

    labels = model.fit_predict(X_scaled)

    inertia = model.inertia_

    sil = silhouette_score(
        X_scaled,
        labels
    )

    dbi = davies_bouldin_score(
        X_scaled,
        labels
    )

    inertias.append(inertia)
    sil_scores.append(sil)
    dbi_scores.append(dbi)

    print(
        f"K={k} | "
        f"Inertia={inertia:.2f} | "
        f"Silhouette={sil:.4f} | "
        f"DBI={dbi:.4f}"
    )

best_k = K_RANGE[sil_scores.index(max(sil_scores))]

print("\n===================================")
print(f"Best K by Silhouette Score = {best_k}")
print("===================================\n")

# ==============================
# ELBOW METHOD
# ==============================
plt.figure(figsize=(8,5))

plt.plot(
    list(K_RANGE),
    inertias,
    marker="o"
)

plt.title("Elbow Method")
plt.xlabel("Number of Clusters")
plt.ylabel("Inertia")
plt.grid(True)

plt.show()

# ==============================
# SILHOUETTE GRAPH
# ==============================
plt.figure(figsize=(8,5))

plt.plot(
    list(K_RANGE),
    sil_scores,
    marker="o"
)

plt.title("Silhouette Score vs K")
plt.xlabel("Number of Clusters")
plt.ylabel("Silhouette Score")
plt.grid(True)

plt.show()

# ==============================
# DBI GRAPH
# ==============================
plt.figure(figsize=(8,5))

plt.plot(
    list(K_RANGE),
    dbi_scores,
    marker="o"
)

plt.title("Davies-Bouldin Index vs K")
plt.xlabel("Number of Clusters")
plt.ylabel("DBI (Lower is Better)")
plt.grid(True)

plt.show()

# ==============================
# FINAL KMEANS MODEL (K=3)
# ==============================
kmeans = KMeans(
    n_clusters=3,
    init="k-means++",
    n_init=20,
    random_state=42
)

labels = kmeans.fit_predict(X_scaled)

# ==============================
# CORRELATION HEATMAP
# ==============================
plt.figure(figsize=(12,8))

sns.heatmap(
    df[FEATURES].corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Feature Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    "feature_correlation_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==============================
# SEGMENT DISTRIBUTION
# ==============================
plt.figure(figsize=(6,4))

pd.Series(labels).value_counts().sort_index().plot(
    kind="bar"
)

plt.title("Customer Segment Distribution")
plt.xlabel("Cluster")
plt.ylabel("Number of Customers")

plt.show()

# ==============================
# PCA CLUSTER VISUALIZATION
# ==============================
pca = PCA(n_components=2)

X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(8,6))

scatter = plt.scatter(
    X_pca[:, 0],
    X_pca[:, 1],
    c=labels,
    cmap="viridis",
    s=20
)

plt.title("Customer Segments (PCA Projection)")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")

plt.colorbar(scatter, label="Cluster")

plt.show()

print("\n===================================")
print("Evaluation Completed Successfully")
print("Generated:")
print("1. Elbow Method")
print("2. Silhouette Score Graph")
print("3. Davies-Bouldin Graph")
print("4. Correlation Heatmap")
print("5. Segment Distribution")
print("6. PCA Cluster Visualization")
print("===================================")