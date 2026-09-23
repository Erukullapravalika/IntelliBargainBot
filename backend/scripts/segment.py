import os
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import silhouette_score
from scipy import stats
import joblib

# ==============================
# PATH SETUP
# ==============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed")
MODEL_PATH = os.path.join(BASE_DIR, "models")

os.makedirs(MODEL_PATH, exist_ok=True)

# ==============================
# LOAD CLEAN DATA
# ==============================
df = pd.read_csv(os.path.join(DATA_PATH, "retail_clean.csv"))
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

print("Loaded:", df.shape)

# ==============================
# CUSTOMER-LEVEL RFM
# ==============================
reference_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

customer_df = df.groupby("CustomerID").agg(
    total_orders=("InvoiceNo", "nunique"),
    total_spend=("Revenue", "sum"),
    last_purchase=("InvoiceDate", "max"),
    first_purchase=("InvoiceDate", "min")
).reset_index()

customer_df["recency_days"] = (
    reference_date - customer_df["last_purchase"]
).dt.days

customer_df["avg_spend_per_order"] = (
    customer_df["total_spend"] / customer_df["total_orders"]
)

customer_df["customer_lifetime_days"] = (
    customer_df["last_purchase"] - customer_df["first_purchase"]
).dt.days

customer_df["purchase_frequency"] = (
    customer_df["total_orders"] /
    (customer_df["customer_lifetime_days"] + 1)
)

print("Customer RFM built:", customer_df.shape)

# ==============================
# FEATURES FOR CLUSTERING
# total_spend is used directly
# — already different across
#   New / Regular / Loyal
# No duplicate columns
# ==============================
RFM_FEATURES = [
    "recency_days",
    "total_orders",
    "avg_spend_per_order",
    "customer_lifetime_days",
    "purchase_frequency",
    "total_spend"
]

# ==============================
# OUTLIER REMOVAL (Z-SCORE)
# Removes floating outliers that
# hurt silhouette score
# ==============================
before = len(customer_df)

z_scores = stats.zscore(customer_df[RFM_FEATURES])
customer_df = customer_df[
    (abs(z_scores) < 3).all(axis=1)
].reset_index(drop=True)

print(f"Outliers removed: {before - len(customer_df)}")
print(f"After outlier removal: {len(customer_df)} customers")

# ==============================
# SCALE (RobustScaler)
# Better than StandardScaler for
# real-world skewed customer data
# ==============================
scaler = RobustScaler()
X_scaled = scaler.fit_transform(customer_df[RFM_FEATURES])

# ==============================
# KMEANS (IMPROVED PARAMS)
# ==============================
kmeans = KMeans(
    n_clusters=3,
    init="k-means++",
    n_init=20,
    max_iter=500,
    random_state=42
)

customer_df["cluster"] = kmeans.fit_predict(X_scaled)

# ==============================
# SILHOUETTE SCORE
# ==============================
score = silhouette_score(X_scaled, customer_df["cluster"])
print(f"\nSilhouette Score: {score:.4f}")

if score >= 0.5:
    print("Excellent clustering! ✅")
elif score >= 0.4:
    print("Good clustering ✅")
else:
    print("Moderate clustering — acceptable for real data")

# ==============================
# ANALYZE CLUSTERS
# ==============================
centroids = pd.DataFrame(
    scaler.inverse_transform(kmeans.cluster_centers_),
    columns=RFM_FEATURES
)

print("\nCluster Centroids:")
print(centroids.round(2))

# ==============================
# MAP CLUSTERS → SEGMENTS
# Rank by total_orders ascending
# 0=New, 1=Regular, 2=Loyal
# ==============================
order_rank = centroids["total_orders"].rank().astype(int) - 1
label_map = order_rank.to_dict()

customer_df["segment"] = customer_df["cluster"].map(label_map)

print("\nSegment Distribution:")
print(customer_df["segment"].value_counts().sort_index())
print("0=New | 1=Regular | 2=Loyal")

# ==============================
# VERIFY MAPPING IS CORRECT
# ==============================
print("\nSegment Verification:")
for seg in [0, 1, 2]:
    seg_data = customer_df[customer_df["segment"] == seg]
    print(f"Segment {seg} → "
          f"avg_orders={seg_data['total_orders'].mean():.1f} | "
          f"avg_recency={seg_data['recency_days'].mean():.0f} days | "
          f"avg_spend={seg_data['total_spend'].mean():.0f}")

# ==============================
# PRODUCT FEATURES
# ==============================
product_df = df.groupby("StockCode").agg(
    product_demand=("Quantity", "sum"),
    avg_product_price=("UnitPrice", "mean")
).reset_index()

product_df["demand_tier"] = pd.qcut(
    product_df["product_demand"],
    q=3,
    labels=[0, 1, 2]
).astype(int)

# ==============================
# SAVE MODELS
# ==============================
joblib.dump(kmeans,       os.path.join(MODEL_PATH, "kmeans.pkl"))
joblib.dump(scaler,       os.path.join(MODEL_PATH, "scaler.pkl"))
joblib.dump(label_map,    os.path.join(MODEL_PATH, "label_map.pkl"))
joblib.dump(RFM_FEATURES, os.path.join(MODEL_PATH, "rfm_features.pkl"))

print("\nModels saved!")

# ==============================
# SAVE DATA
# ==============================
customer_df.to_csv(
    os.path.join(DATA_PATH, "customer_segments.csv"),
    index=False
)

product_df.to_csv(
    os.path.join(DATA_PATH, "product_features.csv"),
    index=False
)

print("Customer segments saved:", customer_df.shape)
print("Product features saved:", product_df.shape)

