"""MLflow Tracking integration for the wine classifier."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


EXPERIMENT_NAME = "Wine_Classification"
DEFAULT_TRACKING_URI = "sqlite:///mlflow.db"


def log_experiment(
    model: RandomForestClassifier,
    X_train: pd.DataFrame,
    metrics: dict[str, float],
    model_parameters: dict[str, Any],
    class_names: list[str],
    report_path: str | Path,
    metrics_path: str | Path,
    predictions_path: str | Path,
) -> str:
    """Log parameters, metrics, tags, model and output artifacts to MLflow."""
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", DEFAULT_TRACKING_URI)
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(EXPERIMENT_NAME)

    signature = infer_signature(X_train, model.predict(X_train))
    with mlflow.start_run(run_name="RandomForest_Wine_Classification") as run:
        params_to_log = dict(model_parameters)
        params_to_log.update(
            {
                "dataset": "sklearn.datasets.load_wine",
                "target_rule": "Multi-class classification of wine cultivars",
                "num_classes": len(class_names),
                "feature_count": len(X_train.columns),
            }
        )
        mlflow.log_params(params_to_log)
        mlflow.log_metrics(metrics)
        mlflow.set_tags(
            {
                "domain": "wine quality / chemistry",
                "problem_type": "multi-class classification",
                "model_type": "RandomForestClassifier",
                "dataset_source": "sklearn bundled dataset; no CSV download",
                "data_drift_demo": "synthetic controlled shift",
            }
        )
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="wine_classifier",
            signature=signature,
            input_example=X_train.head(3),
            skops_trusted_types=["sklearn.tree._tree.Tree"],
        )
        for artifact in (report_path, metrics_path, predictions_path):
            mlflow.log_artifact(str(artifact))
        return run.info.run_id
