# XMdim

XMdim is a Python library designed for performing dimensionality reduction on embedding data, with a primary focus on Principal Component Analysis (PCA). It provides a flexible and extensible framework for reducing data dimensions, analyzing variance, and reconstructing data using PCA.

## Features

- **PCA Transformation**: Perform PCA on your embedding data with customizable number of components.
- **Flexible Scaling**: Option to apply standard scaling or min-max scaling before PCA.
- **Variance Analysis**: Calculate and retrieve explained variance ratios and cumulative explained variance.
- **Component Loadings**: Access the loadings (principal components) of the PCA.
- **Data Reconstruction**: Inverse transform PCA results to reconstruct original data.
- **Reconstruction Error**: Calculate the mean squared error between original and reconstructed data.
- **Optimal Components**: Find the optimal number of components for a given variance threshold.
- **New Data Projection**: Project new data onto the existing PCA space.

## Installation

Install XMdim using pip:

```bash
pip install xmdim
```

## Usage

Here's a basic example of how to use XMdim:

```python
from xmdim import PCAAnalyzer, ScalingType

# Sample embeddings
embeddings = {
    'key1': [[1, 2, 3, 4], [4, 5, 6, 7], [7, 8, 9, 10], [10, 11, 12, 13]],
    'key2': [[2, 3, 4, 5], [5, 6, 7, 8], [8, 9, 10, 11], [11, 12, 13, 14]]
}

# Create a PCAAnalyzer instance
analyzer = PCAAnalyzer(embeddings)

# Perform PCA
transformed_data = analyzer.perform_pca(n_components=2, scaling=ScalingType.STANDARD)

# Get explained variance ratio
explained_variance = analyzer.get_explained_variance_ratio()

# Get cumulative explained variance
cumulative_variance = analyzer.get_cumulative_explained_variance()

print("Transformed Data:", transformed_data)
print("Explained Variance Ratio:", explained_variance)
print("Cumulative Explained Variance:", cumulative_variance)
```

## Advanced Usage

### Loadings and Data Reconstruction

```python
# Get loadings
loadings = analyzer.get_loadings()

# Inverse transform
reconstructed_data = analyzer.inverse_transform()

# Get reconstruction error
error = analyzer.get_reconstruction_error()

print("Loadings:", loadings)
print("Reconstructed Data:", reconstructed_data)
print("Reconstruction Error:", error)
```

### Optimal Components and New Data Projection

```python
# Get optimal number of components
optimal_components = analyzer.get_optimal_components(variance_threshold=0.95)

# Project new data
new_data = {
    'key1': [[2, 3, 4, 5], [5, 6, 7, 8]],
    'key2': [[3, 4, 5, 6], [6, 7, 8, 9]]
}
projected_data = analyzer.project_new_data(new_data)

print("Optimal Number of Components:", optimal_components)
print("Projected New Data:", projected_data)
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