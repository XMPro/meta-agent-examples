from xmadpackage.src.xmad import UnsupervisedAnomalyDetector, Method, StatsMethod
from sklearn.datasets import make_blobs
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np

if __name__ == "__main__":
    # Generate some sample data with ground truth labels
    # Multivariate data: two clusters + outliers
    X, y = make_blobs(n_samples=200, centers=2, n_features=4, cluster_std=1.0, random_state=42)
    # Add some outlier points
    outliers = np.random.uniform(low=-10, high=10, size=(10, 4))
    X = np.vstack([X, outliers])
    
    # True labels: 0 for normal, 1 for outliers
    true_labels = np.concatenate([np.zeros(200, dtype=int), np.ones(10, dtype=int)])
    
    # Convert data into a dictionary format
    data = {
        'sample_key': X
    }


    # Example 1: Using DBSCAN

    # Optmimize
    detector_dbscan = UnsupervisedAnomalyDetector(data, method=Method.DBSCAN, eps=0.9, min_samples=5)
    detector_dbscan.optimize_dbscan(inplace=True)
    dbscan_labels = detector_dbscan.fit_predict()
    print("DBSCAN labels (outliers = -1):", dbscan_labels)

    # Evaluate DBSCAN
    predicted_labels_dbscan = np.where(dbscan_labels['sample_key'] == -1, 1, 0)
    cm_dbscan = confusion_matrix(true_labels, predicted_labels_dbscan)
    report_dbscan = classification_report(true_labels, predicted_labels_dbscan, digits=3)
    print("DBSCAN Confusion Matrix:\n", cm_dbscan)
    print("DBSCAN Classification Report:\n", report_dbscan)

    # Example 2: Statistical Z-score for univariate data
    univariate_data = {
        'univariate_key': np.concatenate([np.random.normal(0, 1, 200), np.random.normal(10, 0.1, 5)])
    }
    detector_stat = UnsupervisedAnomalyDetector(univariate_data, method=Method.STATISTICAL, stats_method=StatsMethod.Z_SCORE, z_threshold=3.0)
    stat_labels = detector_stat.fit_predict()
    print("Statistical Z-score labels (1 = outlier, 0 = normal):", stat_labels)

    # Example 3: Local Outlier Factor (LOF)
    detector_lof = UnsupervisedAnomalyDetector(data, method=Method.LOF, lof_neighbors=20)
    lof_labels = detector_lof.fit_predict()
    print("LOF labels (1 = outlier, 0 = normal):", lof_labels)

    # Evaluate LOF
    predicted_labels_lof = lof_labels['sample_key']
    cm_lof = confusion_matrix(true_labels, predicted_labels_lof)
    report_lof = classification_report(true_labels, predicted_labels_lof, digits=3)
    print("LOF Confusion Matrix:\n", cm_lof)
    print("LOF Classification Report:\n", report_lof)

    # Example 4: Isolation Forest
    detector_if = UnsupervisedAnomalyDetector(data, method=Method.ISOLATION_FOREST, iforest_estimators=100, iforest_contamination=0.05)
    if_labels = detector_if.fit_predict()
    print("Isolation Forest labels (1 = outlier, 0 = normal):", if_labels)

    # Evaluate Isolation Forest
    predicted_labels_if = if_labels['sample_key']
    cm_if = confusion_matrix(true_labels, predicted_labels_if)
    report_if = classification_report(true_labels, predicted_labels_if, digits=3)
    print("Isolation Forest Confusion Matrix:\n", cm_if)
    print("Isolation Forest Classification Report:\n", report_if)

    # Example 5: One-Class SVM
    detector_ocsvm = UnsupervisedAnomalyDetector(data, method=Method.ONE_CLASS_SVM, ocsvm_kernel='rbf', ocsvm_nu=0.05)
    ocsvm_labels = detector_ocsvm.fit_predict()
    print("One-Class SVM labels (1 = outlier, 0 = normal):", ocsvm_labels)

    # Evaluate One-Class SVM
    predicted_labels_ocsvm = ocsvm_labels['sample_key']
    cm_ocsvm = confusion_matrix(true_labels, predicted_labels_ocsvm)
    report_ocsvm = classification_report(true_labels, predicted_labels_ocsvm, digits=3)
    print("One-Class SVM Confusion Matrix:\n", cm_ocsvm)
    print("One-Class SVM Classification Report:\n", report_ocsvm)

    # Example 6: Gaussian Mixture Model (GMM)
    detector_gmm = UnsupervisedAnomalyDetector(data, method=Method.GMM, gmm_components=2, gmm_cov_type='full')
    gmm_labels = detector_gmm.fit_predict()
    print("GMM labels (1 = outlier, 0 = normal):", gmm_labels)

    # Evaluate GMM
    predicted_labels_gmm = gmm_labels['sample_key']
    cm_gmm = confusion_matrix(true_labels, predicted_labels_gmm)
    report_gmm = classification_report(true_labels, predicted_labels_gmm, digits=3)
    print("GMM Confusion Matrix:\n", cm_gmm)
    print("GMM Classification Report:\n", report_gmm)

    # Additional DBSCAN-specific statistics
    if detector_dbscan.method == Method.DBSCAN:
        cluster_stats = detector_dbscan.get_cluster_statistics()
        print("DBSCAN Cluster Statistics:", cluster_stats)

        optimal_eps = detector_dbscan.find_optimal_epsilon(eps_range=(0.1, 1.5), n_steps=10)
        print("Optimal DBSCAN Epsilon:", optimal_eps)

        centroids = detector_dbscan.get_cluster_centroids()
        print("DBSCAN Cluster Centroids:", centroids)

        distances = detector_dbscan.get_intra_cluster_distances()
        print("DBSCAN Intra-Cluster Distances:", distances)
