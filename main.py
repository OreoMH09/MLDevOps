"""Run the complete Pytest + MLflow + Evidently POE pipeline."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from carshare_mlops.data import (
    FEATURE_COLUMNS,
    load_wine_dataset,
    make_synthetic_shift,
    split_and_label_data,
)
from carshare_mlops.model import (
    MODEL_PARAMETERS,
    confusion_matrix_as_list,
    evaluate_model,
    train_model,
)
from carshare_mlops.monitoring import generate_drift_report
from carshare_mlops.tracking import log_experiment

PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "outputs"


def run_pipeline() -> dict[str, object]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load the bundled dataset (no separate data file or internet fetch).
    data = load_wine_dataset()
    split = split_and_label_data(data)

    # 2. Train and evaluate a classification model.
    model = train_model(split.X_train, split.y_train)
    metrics, predictions, probabilities = evaluate_model(
        model, split.X_test, split.y_test
    )
    matrix = confusion_matrix_as_list(split.y_test, predictions)

    # 3. Save EDA and evaluation artifacts.
    eda_summary = {
        "dataset": "sklearn Wine Dataset",
        "rows": int(data.shape[0]),
        "columns": list(data.columns),
        "missing_values": {key: int(value) for key, value in data.isna().sum().items()},
        "training_rows": int(len(split.X_train)),
        "test_rows": int(len(split.X_test)),
        "features": FEATURE_COLUMNS,
        "target": "wine_class",
        "target_definition": "Multi-class classification of wine cultivars (0, 1, 2)",
        "class_names": split.class_names,
        "train_target_counts": {
            str(key): int(value) for key, value in split.y_train.value_counts().sort_index().items()
        },
        "test_target_counts": {
            str(key): int(value) for key, value in split.y_test.value_counts().sort_index().items()
        },
    }
    eda_path = OUTPUT_DIR / "eda_summary.json"
    eda_path.write_text(json.dumps(eda_summary, indent=2), encoding="utf-8")

    metrics_payload = {
        **metrics,
        "confusion_matrix": matrix,
        "class_names": split.class_names,
        "interpretation": {
            "0": "Wine cultivar class 0",
            "1": "Wine cultivar class 1",
            "2": "Wine cultivar class 2",
        },
    }
    metrics_path = OUTPUT_DIR / "classification_metrics.json"
    metrics_path.write_text(json.dumps(metrics_payload, indent=2), encoding="utf-8")

    predictions_path = OUTPUT_DIR / "test_predictions.csv"
    prediction_frame = pd.DataFrame(
        {
            "actual_wine_class": split.y_test.to_numpy(),
            "predicted_wine_class": predictions,
        }
    )
    # Add probability columns for each class
    for i, class_name in enumerate(split.class_names):
        prediction_frame[f"probability_{class_name}"] = probabilities[:, i]
    prediction_frame.to_csv(predictions_path, index=False)

    # 4. Demonstrate Evidently drift monitoring with a documented synthetic batch.
    reference_features = split.X_test[FEATURE_COLUMNS].reset_index(drop=True)
    synthetic_current = make_synthetic_shift(reference_features)
    synthetic_path = OUTPUT_DIR / "synthetic_current_features.csv"
    synthetic_current.to_csv(synthetic_path, index=False)

    report_path = generate_drift_report(
        reference_data=reference_features,
        current_data=synthetic_current,
        output_path=OUTPUT_DIR / "evidently_wine_data_drift.html",
    )

    # 5. Log the experiment, model, metrics and report to MLflow.
    run_id = log_experiment(
        model=model,
        X_train=split.X_train,
        metrics=metrics,
        model_parameters=MODEL_PARAMETERS,
        class_names=split.class_names,
        report_path=report_path,
        metrics_path=metrics_path,
        predictions_path=predictions_path,
    )

    print("\n========== WINE CLASSIFICATION MLOPS POE ==========")
    print(f"Dataset rows: {len(data)} | Training rows: {len(split.X_train)} | Test rows: {len(split.X_test)}")
    print(f"Classes: {split.class_names}")
    print("\nClassification metrics:")
    for name, value in metrics.items():
        print(f"  {name:10s}: {value:.4f}")
    print(f"Confusion matrix: {matrix}")
    print(f"\nEvidently report: {report_path}")
    print(f"MLflow experiment: Wine_Classification")
    print(f"MLflow run ID: {run_id}")
    print("Open MLflow UI at http://127.0.0.1:5000 after starting it in a second terminal.")
    print("NOTE: Evidently current data is synthetically shifted for demonstration only.")

    return {
        "metrics": metrics,
        "confusion_matrix": matrix,
        "class_names": split.class_names,
        "mlflow_run_id": run_id,
        "report_path": str(report_path),
    }


if __name__ == "__main__":
    run_pipeline()
