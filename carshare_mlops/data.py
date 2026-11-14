"""Data loading and preparation for the built-in sklearn wine dataset."""

from __future__ import annotations

from typing import NamedTuple

import pandas as pd
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split

# Wine dataset has 13 features - we'll use all of them
FEATURE_COLUMNS = [
    "alcohol",
    "malic_acid",
    "ash",
    "alcalinity_of_ash",
    "magnesium",
    "total_phenols",
    "flavanoids",
    "nonflavanoid_phenols",
    "proanthocyanins",
    "color_intensity",
    "hue",
    "od280_od315_of_diluted_wines",
    "proline",
]
TARGET_COLUMN = "wine_class"
TEST_SIZE = 0.20
RANDOM_STATE = 42


class DataSplit(NamedTuple):
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series
    class_names: list[str]
    train_frame: pd.DataFrame
    test_frame: pd.DataFrame


def load_wine_dataset() -> pd.DataFrame:
    """Load sklearn's bundled wine dataset; no CSV download is required."""
    wine = load_wine()
    
    # Create DataFrame with feature columns
    data = pd.DataFrame(wine.data, columns=FEATURE_COLUMNS)
    
    # Add target column
    data[TARGET_COLUMN] = wine.target
    
    # Validate
    if data.empty:
        raise ValueError("The bundled wine dataset is empty.")
    if data.isna().any().any():
        raise ValueError("The wine dataset contains missing values.")
    
    return data.copy()


def split_and_label_data(
    data: pd.DataFrame,
    test_size: float = TEST_SIZE,
    random_state: int = RANDOM_STATE,
) -> DataSplit:
    """Split the wine dataset into train and test partitions.

    The wine dataset contains 3 classes (0, 1, 2) representing different
    wine cultivars. We perform a standard multi-class classification.
    """
    required = set(FEATURE_COLUMNS + [TARGET_COLUMN])
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Input data is missing required columns: {sorted(missing)}")

    train_frame, test_frame = train_test_split(
        data.copy(), test_size=test_size, random_state=random_state, stratify=data[TARGET_COLUMN]
    )

    X_train = train_frame[FEATURE_COLUMNS].copy()
    X_test = test_frame[FEATURE_COLUMNS].copy()
    y_train = train_frame[TARGET_COLUMN].copy()
    y_test = test_frame[TARGET_COLUMN].copy()

    class_names = ["Class 0", "Class 1", "Class 2"]

    return DataSplit(
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        class_names=class_names,
        train_frame=train_frame,
        test_frame=test_frame,
    )


def make_synthetic_shift(reference_features: pd.DataFrame) -> pd.DataFrame:
    """Create a deterministic, artificial current batch to demo data drift.

    The shifts are intentionally simulated: we add small perturbations to
    chemical measurements. This is not real production data and must be
    described as a controlled classroom demonstration.
    """
    current = reference_features[FEATURE_COLUMNS].copy()
    
    # Apply synthetic shifts to demonstrate drift
    current["alcohol"] = current["alcohol"] * 1.05  # 5% increase
    current["malic_acid"] = current["malic_acid"] * 0.95  # 5% decrease
    current["ash"] = current["ash"] + 0.1  # Small absolute shift
    current["total_phenols"] = current["total_phenols"] * 1.03
    current["flavanoids"] = current["flavanoids"] * 0.97
    
    return current
