import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from typing import Dict, List, Tuple, Any, Union
from enum import Enum, auto

class ScalingType(Enum):
    NONE = auto()
    STANDARD = auto()
    MIN_MAX = auto()

class PCAAnalyzer:
    def __init__(self, embeddings: Dict[str, List[List[float]]]):
        self.embeddings = {k: np.array(v) for k, v in embeddings.items()}
        self.pca_results: Dict[str, Any] = {}
        self.scaler = None

    def perform_pca(self, n_components: Union[int, float, str] = 0.95, scaling: ScalingType = ScalingType.STANDARD) -> Dict[str, np.ndarray]:
        if scaling == ScalingType.STANDARD:
            self.scaler = StandardScaler()
        elif scaling == ScalingType.MIN_MAX:
            self.scaler = MinMaxScaler()
        
        for key, emb in self.embeddings.items():
            if self.scaler:
                emb = self.scaler.fit_transform(emb)
            
            pca = PCA(n_components=n_components)
            transformed = pca.fit_transform(emb)
            
            self.pca_results[key] = {
                'pca': pca,
                'transformed': transformed,
                'original_shape': emb.shape
            }
        
        return {k: v['transformed'] for k, v in self.pca_results.items()}

    def get_explained_variance_ratio(self) -> Dict[str, np.ndarray]:
        return {k: v['pca'].explained_variance_ratio_ for k, v in self.pca_results.items()}

    def get_cumulative_explained_variance(self) -> Dict[str, np.ndarray]:
        return {k: np.cumsum(v['pca'].explained_variance_ratio_) for k, v in self.pca_results.items()}

    def get_loadings(self) -> Dict[str, np.ndarray]:
        return {k: v['pca'].components_.T for k, v in self.pca_results.items()}

    def inverse_transform(self) -> Dict[str, np.ndarray]:
        inverse_transformed = {}
        for key, result in self.pca_results.items():
            inv_transform = result['pca'].inverse_transform(result['transformed'])
            if self.scaler:
                inv_transform = self.scaler.inverse_transform(inv_transform)
            inverse_transformed[key] = inv_transform
        return inverse_transformed

    def get_reconstruction_error(self) -> Dict[str, float]:
        errors = {}
        for key, result in self.pca_results.items():
            original = self.embeddings[key]
            reconstructed = self.inverse_transform()[key]
            errors[key] = np.mean(np.square(original - reconstructed))
        return errors

    def get_optimal_components(self, variance_threshold: float = 0.95) -> Dict[str, int]:
        optimal_components = {}
        for key, result in self.pca_results.items():
            cumulative_variance = np.cumsum(result['pca'].explained_variance_ratio_)
            optimal_components[key] = np.argmax(cumulative_variance >= variance_threshold) + 1
        return optimal_components

    def project_new_data(self, new_data: Dict[str, List[List[float]]]) -> Dict[str, np.ndarray]:
        projected_data = {}
        for key, data in new_data.items():
            if key in self.pca_results:
                data_array = np.array(data)
                if self.scaler:
                    data_array = self.scaler.transform(data_array)
                projected_data[key] = self.pca_results[key]['pca'].transform(data_array)
            else:
                raise KeyError(f"No PCA model found for key: {key}")
        return projected_data