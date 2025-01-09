from xmvipackage.src.xmvi import EmbeddingAnalyzer, SimilarityType, ScalingType

# Example usage
if __name__ == "__main__":
    # Sample embeddings
    embeddings = {
        'key1': [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        'key2': [[2, 3, 4], [5, 6, 7], [8, 9, 10]]
    }

    analyzer = EmbeddingAnalyzer(embeddings)

    # Calculate similarities
    cosine_sim_mean = analyzer.calculate_similarity(SimilarityType.COSINE, 'mean')
    euclidean_sim_median = analyzer.calculate_similarity(SimilarityType.EUCLIDEAN, 'median')
    inner_product_sim_mean = analyzer.calculate_similarity(SimilarityType.INNER_PRODUCT, 'mean')

    # Scale embeddings
    scaled_embeddings = analyzer.scale_embeddings(ScalingType.STANDARD_SCALER)

    # Get statistics
    stats = analyzer.get_statistics()

    # Apply custom function
    squared_embeddings = analyzer.apply_function(lambda x: x**2)

    # Reset embeddings to original
    analyzer.reset_embeddings()

    print("Cosine Similarity (Mean):", cosine_sim_mean)
    print("Euclidean Similarity (Median):", euclidean_sim_median)
    print("Inner Product Similarity (Mean):", inner_product_sim_mean)
    print("Scaled Embeddings:", scaled_embeddings)
    print("Statistics:", stats)
    print("Squared Embeddings:", squared_embeddings)