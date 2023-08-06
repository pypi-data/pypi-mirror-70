class ScoreColumnConstants:
    # Label and Task Type Region
    BinaryClassScoredLabelType = "Binary Class Assigned Labels"
    MultiClassScoredLabelType = "Multi Class Assigned Labels"
    RegressionScoredLabelType = "Regression Assigned Labels"
    ClusterScoredLabelType = "Cluster Assigned Labels"
    AnomalyDetectionScoredLabelType = "Anomaly Detection Assigned Labels"
    ScoredLabelsColumnName = "Scored Labels"
    ClusterAssignmentsColumnName = "Assignments"
    QuantileScoredLabelsColumnName = "Scores for quantile :"
    # Probability Region
    CalibratedScoreType = "Calibrated Score"
    ScoredProbabilitiesColumnName = "Scored Probabilities"
    ScoredProbabilitiesMulticlassColumnNamePattern = "Scored Probabilities"
    # Distance Region
    ClusterDistanceMetricsColumnNamePattern = "DistancesToClusterCenter no."


META_PROPERTY_LABEL_ENCODER_KEY = 'label_encoder'
