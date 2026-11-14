"""Pytest checks for the wine MLOps pipeline."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from carshare_mlops.data import (
    FEATURE_COLUMNS,
    load_wine_dataset,
    make_synthetic_shift,
    split_and_label_data,
)
from carshare_mlops.model import evaluate_model, train_model


def test_bundled_wine_dataset_loads_with_expected_schema():
    data = load_wine_dataset()
    assert data.shape == (178, 14)  # 178 samples, 13 features + 1 target
    assert set(FEATURE_COLUMNS + ["wine_class"]).issubset(data.columns)
    assert not data[FEATURE_COLUMNS + ["wine_class"]].isna().any().any()


def test_wine_classes_are_valid():
    data = load_wine_dataset()
    assert set(data["wine_class"].unique()) == {0, 1, 2}


def test_split_produces_correct_classes():
    data = load_wine_dataset()
    split = split_and_label_data(data)
    assert set(split.y_train.unique()).issubset({0, 1, 2})
    assert set(split.y_test.unique()).issubset({0, 1, 2})
    assert len(split.X_train) + len(split.X_test) == len(data)
    assert len(split.class_names) == 3


def test_split_is_reproducible():
    data = load_wine_dataset()
    first = split_and_label_data(data)
    second = split_and_label_data(data)
    pd.testing.assert_frame_equal(first.X_train, second.X_train)
    pd.testing.assert_series_equal(first.y_test, second.y_test)


def test_random_forest_trains_and_returns_valid_classification_metrics():
    data = load_wine_dataset()
    split = split_and_label_data(data)
    model = train_model(split.X_train, split.y_train)
    metrics, predictions, probabilities = evaluate_model(model, split.X_test, split.y_test)

    assert len(predictions) == len(split.y_test)
    assert probabilities.shape == (len(split.y_test), 3)  # 3 classes
    assert np.all((probabilities >= 0.0) & (probabilities <= 1.0))
    assert set(np.unique(predictions)).issubset({0, 1, 2})
    assert set(metrics) == {"accuracy", "precision", "recall", "f1_score"}
    assert all(0.0 <= value <= 1.0 for value in metrics.values())


def test_synthetic_drift_batch_is_reproducible_and_does_not_mutate_reference():
    data = load_wine_dataset()
    reference = split_and_label_data(data).X_test[FEATURE_COLUMNS].reset_index(drop=True)
    reference_before = reference.copy(deep=True)

    shifted = make_synthetic_shift(reference)
    shifted_again = make_synthetic_shift(reference)

    pd.testing.assert_frame_equal(shifted, shifted_again)
    pd.testing.assert_frame_equal(reference, reference_before)
    # Check that synthetic shifts were applied
    assert np.allclose(shifted["alcohol"], reference["alcohol"] * 1.05)
    assert np.allclose(shifted["malic_acid"], reference["malic_acid"] * 0.95)


def test_evidently_report_is_created(tmp_path):
    pytest.importorskip("evidently")
    from carshare_mlops.monitoring import generate_drift_report

    data = load_wine_dataset()
    reference = split_and_label_data(data).X_test[FEATURE_COLUMNS].reset_index(drop=True)
    current = make_synthetic_shift(reference)
    output = tmp_path / "drift_report.html"

    returned_path = generate_drift_report(reference, current, output)

    assert returned_path == output
    assert output.exists()
    assert output.stat().st_size > 1_000
