import numpy as np
from sklearn.preprocessing import Normalizer, StandardScaler, RobustScaler, MinMaxScaler
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Dict, List, Any, Union, Callable
from functools import partial

class SimilarityType(Enum):
    COSINE = auto()
    EUCLIDEAN = auto()
    INNER_PRODUCT = auto()

class ScalingType(Enum):
    NORMALIZATION = auto()
    L2_NORMALIZATION = auto()
    STANDARD_SCALER = auto()
    ROBUST_SCALER = auto()
    MIN_MAX_SCALER = auto()

class NormalizationType(Enum):
    L1 = 'l1'
    L2 = 'l2'
    MAX = 'max'

class Similarity(ABC):
    @abstractmethod
    def calculate(self, embeddings: np.ndarray, reference_vector: np.ndarray) -> np.ndarray:
        pass

class CosineSimilarity(Similarity):
    def calculate(self, embeddings: np.ndarray, reference_vector: np.ndarray) -> np.ndarray:
        return np.dot(embeddings, reference_vector) / (np.linalg.norm(embeddings, axis=1) * np.linalg.norm(reference_vector))

class EuclideanSimilarity(Similarity):
    def calculate(self, embeddings: np.ndarray, reference_vector: np.ndarray) -> np.ndarray:
        return -np.linalg.norm(embeddings - reference_vector, axis=1)

class InnerProductSimilarity(Similarity):
    def calculate(self, embeddings: np.ndarray, reference_vector: np.ndarray) -> np.ndarray:
        return np.dot(embeddings, reference_vector)

class SimilarityFactory:
    @staticmethod
    def create(similarity_type: SimilarityType) -> Similarity:
        similarity_map = {
            SimilarityType.COSINE: CosineSimilarity(),
            SimilarityType.EUCLIDEAN: EuclideanSimilarity(),
            SimilarityType.INNER_PRODUCT: InnerProductSimilarity()
        }
        return similarity_map.get(similarity_type, None)

class EmbeddingAnalyzer:
    def __init__(self, embeddings: Dict[str, List[List[float]]]):
        self.embeddings = {k: np.array(v) for k, v in embeddings.items()}
        self._original_embeddings = self.embeddings.copy()

    def calculate_similarity(self, similarity_type: SimilarityType, reference: Union[str, np.ndarray] = 'mean') -> Dict[str, np.ndarray]:
        similarity = SimilarityFactory.create(similarity_type)
        if similarity is None:
            raise ValueError(f"Unknown similarity type: {similarity_type}")

        results = {}
        for key, emb in self.embeddings.items():
            if isinstance(reference, str):
                if reference == 'mean':
                    reference_vector = np.mean(emb, axis=0)
                elif reference == 'median':
                    reference_vector = np.median(emb, axis=0)
                else:
                    raise ValueError(f"Unknown reference type: {reference}")
            else:
                reference_vector = reference
            results[key] = similarity.calculate(emb, reference_vector)
        return results

    def scale_embeddings(self, scaling_type: ScalingType, normalization_type: NormalizationType = NormalizationType.L2) -> Dict[str, np.ndarray]:
        scaler_map = {
            ScalingType.NORMALIZATION: partial(Normalizer, norm=normalization_type.value),
            ScalingType.L2_NORMALIZATION: partial(Normalizer, norm='l2'),
            ScalingType.STANDARD_SCALER: StandardScaler,
            ScalingType.ROBUST_SCALER: RobustScaler,
            ScalingType.MIN_MAX_SCALER: MinMaxScaler
        }
        
        scaler_class = scaler_map.get(scaling_type)
        if scaler_class is None:
            raise ValueError(f"Unknown scaling type: {scaling_type}")

        scaler = scaler_class()
        self.embeddings = {k: scaler.fit_transform(v) for k, v in self.embeddings.items()}
        return self.embeddings

    def reset_embeddings(self):
        self.embeddings = self._original_embeddings.copy()

    def apply_function(self, func: Callable[[np.ndarray], np.ndarray]) -> Dict[str, np.ndarray]:
        return {k: func(v) for k, v in self.embeddings.items()}

    def get_statistics(self) -> Dict[str, Dict[str, Union[float, np.ndarray]]]:
        stats = {}
        for key, emb in self.embeddings.items():
            stats[key] = {
                'mean': np.mean(emb, axis=0),
                'median': np.median(emb, axis=0),
                'std': np.std(emb, axis=0),
                'min': np.min(emb, axis=0),
                'max': np.max(emb, axis=0)
            }
        return stats