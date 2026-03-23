from sklearn.cluster import KMeans
import numpy as np


def cluster_comments(comments, embeddings, num_clusters=3):

    if len(comments) < num_clusters:
        num_clusters = max(1, len(comments))

    # Convert embeddings to numpy array
    embeddings = np.array(embeddings)

    # Run KMeans
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)

    clusters = {}

    for i in range(num_clusters):
        clusters[f"cluster_{i}"] = []

    for comment, label in zip(comments, labels):
        clusters[f"cluster_{label}"].append(comment)

    # Create summary (only first few comments)
    cluster_summary = []

    for key, value in clusters.items():
        cluster_summary.append({
            "cluster": key,
            "comment_count": len(value),
            "sample_comments": value[:3]
        })

    return cluster_summary