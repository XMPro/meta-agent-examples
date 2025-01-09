from xmclusterpackage.src.xmcluster import DBSCANAnalyzer, ClusterMetric

# Example usage
if __name__ == "__main__":
    # Sample embeddings
    embeddings = {
        'key1': [[1, 2], [2, 2], [2, 3], [8, 7], [8, 8], [25, 80]],
        'key2': [[1, 2], [2, 2], [2, 3], [8, 7], [8, 8], [25, 80]]
    }

    analyzer = DBSCANAnalyzer(embeddings)

    # Perform DBSCAN clustering
    cluster_labels = analyzer.perform_dbscan(eps=3, min_samples=2)
    print("Cluster Labels:", cluster_labels)

    # Get cluster statistics
    stats = analyzer.get_cluster_statistics()
    print("Cluster Statistics:", stats)

    # Calculate silhouette score
    silhouette = analyzer.calculate_cluster_metric(ClusterMetric.SILHOUETTE)
    print("Silhouette Scores:", silhouette)

    # Find optimal epsilon
    optimal_eps = analyzer.find_optimal_epsilon(min_samples=2, eps_range=(0.1, 10.0), n_steps=20)
    print("Optimal Epsilon:", optimal_eps)

    # Get cluster centroids
    centroids = analyzer.get_cluster_centroids()
    print("Cluster Centroids:", centroids)

    # Get intra-cluster distances
    intra_distances = analyzer.get_intra_cluster_distances()
    print("Intra-cluster Distances:", intra_distances)