from xmdimpackage.src.xmdim import PCAAnalyzer, ScalingType

# Example usage
if __name__ == "__main__":
    # Sample embeddings
    embeddings = {
        'key1': [[1, 2, 3, 4], [4, 5, 6, 7], [7, 8, 9, 10], [10, 11, 12, 13]],
        'key2': [[2, 3, 4, 5], [5, 6, 7, 8], [8, 9, 10, 11], [11, 12, 13, 14]]
    }

    analyzer = PCAAnalyzer(embeddings)

    # Perform PCA
    transformed_data = analyzer.perform_pca(n_components=2, scaling=ScalingType.STANDARD)
    print("Transformed Data:", transformed_data)

    # Get explained variance ratio
    explained_variance = analyzer.get_explained_variance_ratio()
    print("Explained Variance Ratio:", explained_variance)

    # Get cumulative explained variance
    cumulative_variance = analyzer.get_cumulative_explained_variance()
    print("Cumulative Explained Variance:", cumulative_variance)

    # Get loadings
    loadings = analyzer.get_loadings()
    print("Loadings:", loadings)

    # Inverse transform
    reconstructed_data = analyzer.inverse_transform()
    print("Reconstructed Data:", reconstructed_data)

    # Get reconstruction error
    error = analyzer.get_reconstruction_error()
    print("Reconstruction Error:", error)

    # Get optimal number of components
    optimal_components = analyzer.get_optimal_components(variance_threshold=0.95)
    print("Optimal Number of Components:", optimal_components)

    # Project new data
    new_data = {
        'key1': [[2, 3, 4, 5], [5, 6, 7, 8]],
        'key2': [[3, 4, 5, 6], [6, 7, 8, 9]]
    }
    projected_data = analyzer.project_new_data(new_data)
    print("Projected New Data:", projected_data)