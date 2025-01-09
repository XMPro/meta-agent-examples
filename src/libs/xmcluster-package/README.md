# XMCluster

XMCluster is a Python library designed for performing density-based clustering on embedding data using DBSCAN (Density-Based Spatial Clustering of Applications with Noise). It provides a flexible and extensible framework for conducting cluster analysis, optimizing clustering parameters, and analyzing cluster characteristics.

## Features

- **DBSCAN Clustering**: Perform density-based clustering on your embedding data.
- **Cluster Statistics**: Get basic statistics about the clusters, including the number of clusters, number of noise points, and cluster sizes.
- **Cluster Quality Metrics**: Calculate various cluster quality metrics such as Silhouette score, Calinski-Harabasz index, and Davies-Bouldin index.
- **Optimal Parameter Finding**: Find the optimal epsilon parameter for DBSCAN using a grid search and the Silhouette score.
- **Cluster Centroids**: Calculate the centroids of each cluster.
- **Intra-cluster Distances**: Calculate the average distance of points to their cluster centroid.

## Installation

Install XMCluster using pip:

```bash
pip install xmcluster
```

## Usage

Here's a basic example of how to use XMCluster:

```python
from xmcluster import DBSCANAnalyzer, ClusterMetric

# Sample embeddings
embeddings = {
    'key1': [[1, 2], [2, 2], [2, 3], [8, 7], [8, 8], [25, 80]],
    'key2': [[1, 2], [2, 2], [2, 3], [8, 7], [8, 8], [25, 80]]
}

# Create a DBSCANAnalyzer instance
analyzer = DBSCANAnalyzer(embeddings)

# Perform DBSCAN clustering
cluster_labels = analyzer.perform_dbscan(eps=3, min_samples=2)

# Get cluster statistics
stats = analyzer.get_cluster_statistics()

# Calculate silhouette score
silhouette = analyzer.calculate_cluster_metric(ClusterMetric.SILHOUETTE)

# Find optimal epsilon
optimal_eps = analyzer.find_optimal_epsilon(min_samples=2, eps_range=(0.1, 10.0), n_steps=20)

print("Cluster Labels:", cluster_labels)
print("Cluster Statistics:", stats)
print("Silhouette Scores:", silhouette)
print("Optimal Epsilon:", optimal_eps)
```

## Advanced Usage

### Cluster Centroids and Intra-cluster Distances

```python
centroids = analyzer.get_cluster_centroids()
intra_distances = analyzer.get_intra_cluster_distances()

print("Cluster Centroids:", centroids)
print("Intra-cluster Distances:", intra_distances)
```

### Different Cluster Quality Metrics

```python
calinski_harabasz = analyzer.calculate_cluster_metric(ClusterMetric.CALINSKI_HARABASZ)
davies_bouldin = analyzer.calculate_cluster_metric(ClusterMetric.DAVIES_BOULDIN)

print("Calinski-Harabasz Index:", calinski_harabasz)
print("Davies-Bouldin Index:", davies_bouldin)
```

## Dependencies

- numpy
- scikit-learn

## Contributing

We welcome contributions! Please see our contributing guidelines for more details.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any queries or support, please contact [your contact information].