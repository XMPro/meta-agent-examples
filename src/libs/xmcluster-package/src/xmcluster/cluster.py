import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from typing import Dict, List, Tuple, Any, Union
from enum import Enum, auto

class ClusterMetric(Enum):
    SILHOUETTE = auto()
    CALINSKI_HARABASZ = auto()
    DAVIES_BOULDIN = auto()

class DBSCANAnalyzer:
    def __init__(self, embeddings: Dict[str, List[List[float]]]):
        self.embeddings = {k: np.array(v) for k, v in embeddings.items()}
        self.cluster_results: Dict[str, Any] = {}

    def perform_dbscan(self, eps: float = 0.5, min_samples: int = 5) -> Dict[str, np.ndarray]:
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        for key, emb in self.embeddings.items():
            self.cluster_results[key] = {
                'labels': dbscan.fit_predict(emb),
                'core_samples_mask': np.zeros_like(dbscan.labels_, dtype=bool),
            }
            self.cluster_results[key]['core_samples_mask'][dbscan.core_sample_indices_] = True
        return {k: v['labels'] for k, v in self.cluster_results.items()}

    def get_cluster_statistics(self) -> Dict[str, Dict[str, Any]]:
        stats = {}
        for key, result in self.cluster_results.items():
            labels = result['labels']
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            n_noise = list(labels).count(-1)
            stats[key] = {
                'n_clusters': n_clusters,
                'n_noise': n_noise,
                'cluster_sizes': {i: list(labels).count(i) for i in set(labels) if i != -1}
            }
        return stats

    def calculate_cluster_metric(self, metric: ClusterMetric) -> Dict[str, float]:
        results = {}
        for key, emb in self.embeddings.items():
            labels = self.cluster_results[key]['labels']
            if metric == ClusterMetric.SILHOUETTE:
                if len(set(labels)) > 1:
                    results[key] = silhouette_score(emb, labels)
                else:
                    results[key] = None
            elif metric == ClusterMetric.CALINSKI_HARABASZ:
                from sklearn.metrics import calinski_harabasz_score
                if len(set(labels)) > 1:
                    results[key] = calinski_harabasz_score(emb, labels)
                else:
                    results[key] = None
            elif metric == ClusterMetric.DAVIES_BOULDIN:
                from sklearn.metrics import davies_bouldin_score
                if len(set(labels)) > 1:
                    results[key] = davies_bouldin_score(emb, labels)
                else:
                    results[key] = None
        return results

    def find_optimal_epsilon(self, min_samples: int = 5, 
                             eps_range: Tuple[float, float] = (0.1, 1.0), 
                             n_steps: int = 20) -> Dict[str, Dict[str, Union[float, int]]]:
        eps_values = np.linspace(eps_range[0], eps_range[1], n_steps)
        optimal_eps = {}
        for key, emb in self.embeddings.items():
            best_score = -1
            best_eps = eps_range[0]
            best_n_clusters = 0
            for eps in eps_values:
                dbscan = DBSCAN(eps=eps, min_samples=min_samples)
                labels = dbscan.fit_predict(emb)
                n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
                if n_clusters > 1:
                    score = silhouette_score(emb, labels)
                    if score > best_score:
                        best_score = score
                        best_eps = eps
                        best_n_clusters = n_clusters
            optimal_eps[key] = {
                'epsilon': best_eps,
                'silhouette_score': best_score,
                'n_clusters': best_n_clusters
            }
        return optimal_eps

    def get_cluster_centroids(self) -> Dict[str, Dict[int, np.ndarray]]:
        centroids = {}
        for key, result in self.cluster_results.items():
            labels = result['labels']
            emb = self.embeddings[key]
            centroids[key] = {}
            for label in set(labels):
                if label != -1:  # Exclude noise points
                    cluster_points = emb[labels == label]
                    centroids[key][label] = np.mean(cluster_points, axis=0)
        return centroids

    def get_intra_cluster_distances(self) -> Dict[str, Dict[int, float]]:
        distances = {}
        for key, result in self.cluster_results.items():
            labels = result['labels']
            emb = self.embeddings[key]
            distances[key] = {}
            centroids = self.get_cluster_centroids()[key]
            for label in set(labels):
                if label != -1:  # Exclude noise points
                    cluster_points = emb[labels == label]
                    distances[key][label] = np.mean(
                        np.linalg.norm(cluster_points - centroids[label], axis=1)
                    )
        return distances

