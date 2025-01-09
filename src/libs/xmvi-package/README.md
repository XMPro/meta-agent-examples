# XMPro Vector Insights (XMVI)

XMPro Vector Insights (XMVI) is a Python library designed for analyzing and visualizing embedding data. It provides a flexible and extensible framework for calculating similarity measures, applying scaling techniques, and performing basic statistical analysis on embedding data.

## Features

- **Multiple Similarity Measures**: Calculate cosine, Euclidean, and inner product similarities between embeddings and reference vectors.
- **Flexible Reference Vector**: Use mean, median, or custom reference vectors for similarity calculations.
- **Various Scaling Techniques**: Apply normalization, L2 normalization, standard scaling, robust scaling, or min-max scaling to your embeddings.
- **Basic Statistical Analysis**: Compute mean, median, standard deviation, min, and max for your embedding data.
- **Custom Function Application**: Apply any custom function to your embeddings for further analysis.
- **Flexible and Extensible**: Easily add new similarity measures or scaling techniques.

## Installation

Install XMVI using pip:

```bash
pip install xmvi
```

## Usage

Here's a basic example of how to use XMVI:

```python
from xmvi import EmbeddingAnalyzer, SimilarityType, ScalingType, NormalizationType

# Sample embeddings
embeddings = {
    'key1': [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    'key2': [[2, 3, 4], [5, 6, 7], [8, 9, 10]]
}

# Create an EmbeddingAnalyzer instance
analyzer = EmbeddingAnalyzer(embeddings)

# Calculate cosine similarity with mean as reference
cosine_sim = analyzer.calculate_similarity(SimilarityType.COSINE, 'mean')

# Scale embeddings using standard scaler
scaled_embeddings = analyzer.scale_embeddings(ScalingType.STANDARD_SCALER)

# Get basic statistics of embeddings
stats = analyzer.get_statistics()

# Apply a custom function to embeddings
squared_embeddings = analyzer.apply_function(lambda x: x**2)

print("Cosine Similarity:", cosine_sim)
print("Scaled Embeddings:", scaled_embeddings)
print("Statistics:", stats)
print("Squared Embeddings:", squared_embeddings)
```

## Advanced Usage

### Custom Reference Vector

You can use a custom reference vector for similarity calculations:

```python
import numpy as np

custom_ref = np.array([1, 2, 3])
custom_sim = analyzer.calculate_similarity(SimilarityType.COSINE, custom_ref)
```

### Different Normalization Types

When using normalization, you can specify the type:

```python
normalized_embeddings = analyzer.scale_embeddings(ScalingType.NORMALIZATION, NormalizationType.L1)
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