import numpy as np
from typing import Dict, List, Union, Any, Tuple
from enum import Enum, auto
from sklearn.metrics import silhouette_score

# Unsupervised methods
from sklearn.cluster import DBSCAN
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.mixture import GaussianMixture
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score

class Method(Enum):
    DBSCAN = auto()
    STATISTICAL = auto()
    LOF = auto()
    ISOLATION_FOREST = auto()
    ONE_CLASS_SVM = auto()
    GMM = auto()

class StatsMethod(Enum):
    Z_SCORE = auto()
    IQR = auto()

class ClusterMetric(Enum):
    SILHOUETTE = auto()
    CALINSKI_HARABASZ = auto()
    DAVIES_BOULDIN = auto()

class UnsupervisedAnomalyDetector:
    def __init__(self,
                 data: Dict[str, Union[List[float], List[List[float]]]],
                 method: Method = Method.DBSCAN,
                 stats_method: StatsMethod = StatsMethod.Z_SCORE,
                 eps: float = 0.5,
                 min_samples: int = 5,
                 z_threshold: float = 3.0,
                 iqr_multiplier: float = 1.5,
                 lof_neighbors: int = 20,
                 iforest_estimators: int = 100,
                 iforest_contamination: float = 0.1,
                 ocsvm_kernel: str = 'rbf',
                 ocsvm_nu: float = 0.1,
                 gmm_components: int = 2,
                 gmm_cov_type: str = 'full'):
        """
        data: dictionary mapping keys to either:
              - Univariate: List[float]
              - Multivariate: List[List[float]] (each element is a feature vector)

        method: Unsupervised anomaly detection method.
        stats_method: Statistical method for univariate/multivariate anomaly detection.
        eps, min_samples: DBSCAN parameters.
        z_threshold: Z-score threshold for anomalies.
        iqr_multiplier: IQR multiplier for anomalies.
        lof_neighbors: Number of neighbors for LOF.
        iforest_estimators: Number of estimators for Isolation Forest.
        iforest_contamination: Contamination fraction for Isolation Forest.
        ocsvm_kernel, ocsvm_nu: One-Class SVM parameters.
        gmm_components: Number of mixture components for GMM.
        gmm_cov_type: Covariance type for GMM.
        """
        self.data = {}
        self.is_multivariate = {}
        for k, v in data.items():
            arr = np.array(v)
            self.data[k] = arr
            if arr.ndim == 1:
                self.is_multivariate[k] = False
            elif arr.ndim == 2:
                self.is_multivariate[k] = True
            else:
                raise ValueError("Data must be either 1D (univariate) or 2D (multivariate).")

        self.method = method
        self.stats_method = stats_method
        self.eps = eps
        self.min_samples = min_samples
        self.z_threshold = z_threshold
        self.iqr_multiplier = iqr_multiplier
        self.lof_neighbors = lof_neighbors
        self.iforest_estimators = iforest_estimators
        self.iforest_contamination = iforest_contamination
        self.ocsvm_kernel = ocsvm_kernel
        self.ocsvm_nu = ocsvm_nu
        self.gmm_components = gmm_components
        self.gmm_cov_type = gmm_cov_type

        self.results: Dict[str, Any] = {}
        self.labels: Dict[str, np.ndarray] = {}

    def fit_predict(self) -> Dict[str, np.ndarray]:
        if self.method == Method.DBSCAN:
            return self._dbscan_detect()
        elif self.method == Method.STATISTICAL:
            return self._statistical_detect()
        elif self.method == Method.LOF:
            return self._lof_detect()
        elif self.method == Method.ISOLATION_FOREST:
            return self._iforest_detect()
        elif self.method == Method.ONE_CLASS_SVM:
            return self._ocsvm_detect()
        elif self.method == Method.GMM:
            return self._gmm_detect()

    def _prepare_data(self, arr: np.ndarray, key: str) -> np.ndarray:
        return arr.reshape(-1, 1) if not self.is_multivariate[key] else arr

    def _dbscan_detect(self) -> Dict[str, np.ndarray]:
        for key, arr in self.data.items():
            emb = self._prepare_data(arr, key)
            dbscan = DBSCAN(eps=self.eps, min_samples=self.min_samples)
            labels = dbscan.fit_predict(emb)
            self.results[key] = {'labels': labels}
            self.labels[key] = labels
        return self.labels

    def _statistical_detect(self) -> Dict[str, np.ndarray]:
        for key, arr in self.data.items():
            if self.is_multivariate[key]:
                # For multivariate, use norm
                norms = np.linalg.norm(arr, axis=1)
                anomalies = self._apply_statistical(norms)
            else:
                anomalies = self._apply_statistical(arr)
            self.labels[key] = anomalies
        return self.labels

    def _apply_statistical(self, data: np.ndarray) -> np.ndarray:
        if self.stats_method == StatsMethod.Z_SCORE:
            return self._z_score_detect(data)
        else:
            return self._iqr_detect(data)

    def _z_score_detect(self, data: np.ndarray) -> np.ndarray:
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return np.zeros_like(data, dtype=int)
        z_scores = (data - mean) / std
        return np.where(np.abs(z_scores) > self.z_threshold, 1, 0)

    def _iqr_detect(self, data: np.ndarray) -> np.ndarray:
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        lower_bound = q1 - self.iqr_multiplier * iqr
        upper_bound = q3 + self.iqr_multiplier * iqr
        return np.where((data < lower_bound) | (data > upper_bound), 1, 0)

    def _lof_detect(self) -> Dict[str, np.ndarray]:
        for key, arr in self.data.items():
            emb = self._prepare_data(arr, key)
            lof = LocalOutlierFactor(n_neighbors=self.lof_neighbors)
            labels = lof.fit_predict(emb)
            # LOF returns -1 for anomalies, +1 for normal
            # Convert to 1 for anomaly, 0 for normal
            labels = np.where(labels == -1, 1, 0)
            self.labels[key] = labels
        return self.labels

    def _iforest_detect(self) -> Dict[str, np.ndarray]:
        for key, arr in self.data.items():
            emb = self._prepare_data(arr, key)
            iforest = IsolationForest(n_estimators=self.iforest_estimators, contamination=self.iforest_contamination)
            pred = iforest.fit_predict(emb)
            # Isolation Forest returns -1 for anomalies, +1 for normal
            labels = np.where(pred == -1, 1, 0)
            self.labels[key] = labels
        return self.labels

    def _ocsvm_detect(self) -> Dict[str, np.ndarray]:
        for key, arr in self.data.items():
            emb = self._prepare_data(arr, key)
            oc_svm = OneClassSVM(kernel=self.ocsvm_kernel, nu=self.ocsvm_nu)
            pred = oc_svm.fit_predict(emb)
            # OneClassSVM returns -1 for anomalies, +1 for normal
            labels = np.where(pred == -1, 1, 0)
            self.labels[key] = labels
        return self.labels

    def _gmm_detect(self) -> Dict[str, np.ndarray]:
        # Use a Gaussian Mixture model. Anomalies: points with low probability under fitted GMM
        for key, arr in self.data.items():
            emb = self._prepare_data(arr, key)
            gmm = GaussianMixture(n_components=self.gmm_components, covariance_type=self.gmm_cov_type)
            gmm.fit(emb)
            scores = gmm.score_samples(emb)
            # Define threshold as a percentile of scores
            threshold = np.percentile(scores, 5)  # 5th percentile as anomaly cutoff
            labels = np.where(scores < threshold, 1, 0)
            self.labels[key] = labels
        return self.labels

    def get_cluster_statistics(self) -> Dict[str, Dict[str, Any]]:
        if self.method != Method.DBSCAN:
            raise ValueError("Cluster statistics only available for DBSCAN method.")
        stats = {}
        for key, result in self.results.items():
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
        if self.method != Method.DBSCAN:
            raise ValueError("Cluster metrics only available for DBSCAN method.")
        results = {}
        for key, arr in self.data.items():
            labels = self.results[key]['labels']
            emb = arr.reshape(-1, 1) if not self.is_multivariate[key] else arr
            if len(set(labels)) > 1:
                if metric == ClusterMetric.SILHOUETTE:
                    results[key] = silhouette_score(emb, labels)
                elif metric == ClusterMetric.CALINSKI_HARABASZ:
                    results[key] = calinski_harabasz_score(emb, labels)
                elif metric == ClusterMetric.DAVIES_BOULDIN:
                    results[key] = davies_bouldin_score(emb, labels)
            else:
                results[key] = None
        return results

    def find_optimal_epsilon(self, 
                             eps_range: Tuple[float, float] = (0.1, 1.0), 
                             n_steps: int = 20) -> Dict[str, Dict[str, Union[float, int]]]:
        if self.method != Method.DBSCAN:
            raise ValueError("Epsilon optimization only available for DBSCAN method.")

        eps_values = np.linspace(eps_range[0], eps_range[1], n_steps)
        optimal_eps = {}
        for key, arr in self.data.items():
            emb = arr.reshape(-1, 1) if not self.is_multivariate[key] else arr
            best_score = -1
            best_eps = eps_range[0]
            best_n_clusters = 0
            for eps in eps_values:
                dbscan = DBSCAN(eps=eps, min_samples=self.min_samples)
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
    

    def optimize_dbscan(self, 
                        eps_range: Tuple[float, float] = (0.1, 1.0), 
                        min_samples_range: Tuple[int, int] = (3, 20), 
                        n_steps: int = 20,
                        inplace: bool = False) -> Dict[str, Dict[str, Union[float, int]]]:
        if self.method != Method.DBSCAN:
            raise ValueError("DBSCAN optimization only available for DBSCAN method.")
        
        eps_values = np.linspace(eps_range[0], eps_range[1], n_steps)
        min_samples_values = range(min_samples_range[0], min_samples_range[1] + 1)
        optimal_params = {}

        for key, arr in self.data.items():
            emb = arr.reshape(-1, 1) if not self.is_multivariate[key] else arr
            best_score = -1
            best_params = {'epsilon': eps_range[0], 'min_samples': min_samples_range[0]}
            for eps in eps_values:
                for min_samples in min_samples_values:
                    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
                    labels = dbscan.fit_predict(emb)
                    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
                    if n_clusters > 1:
                        score = silhouette_score(emb, labels)
                        if score > best_score:
                            best_score = score
                            best_params = {'epsilon': eps, 'min_samples': min_samples}
            optimal_params[key] = {
                **best_params,
                'silhouette_score': best_score
            }

        # if inplace:   #TODO this doesn't really account for the multiple data keys
        #     print(optimal_params)
        #     single_item_optimal_params = optimal_params[optimal_params.keys()[0]]
        #     self.eps = single_item_optimal_params["eps"]
        #     self.min_samples = single_item_optimal_params["min_samples"]

        return optimal_params
    

    

    def get_cluster_centroids(self) -> Dict[str, Dict[int, np.ndarray]]:
        if self.method != Method.DBSCAN:
            raise ValueError("Cluster centroids only available for DBSCAN method.")

        centroids = {}
        for key, result in self.results.items():
            labels = result['labels']
            arr = self.data[key]
            emb = arr.reshape(-1, 1) if not self.is_multivariate[key] else arr
            centroids[key] = {}
            for label in set(labels):
                if label != -1:  # Exclude noise points
                    cluster_points = emb[labels == label]
                    centroids[key][label] = np.mean(cluster_points, axis=0)
        return centroids

    def get_intra_cluster_distances(self) -> Dict[str, Dict[int, float]]:
        if self.method != Method.DBSCAN:
            raise ValueError("Intra-cluster distances only available for DBSCAN method.")

        distances = {}
        all_centroids = self.get_cluster_centroids()
        for key, result in self.results.items():
            labels = result['labels']
            arr = self.data[key]
            emb = arr.reshape(-1, 1) if not self.is_multivariate[key] else arr
            distances[key] = {}
            centroids = all_centroids[key]
            for label in set(labels):
                if label != -1:
                    cluster_points = emb[labels == label]
                    distances[key][label] = np.mean(
                        np.linalg.norm(cluster_points - centroids[label], axis=1)
                    )
        return distances
