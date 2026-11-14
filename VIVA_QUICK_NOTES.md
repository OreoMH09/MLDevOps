# Car-Share MLOps POE - Viva Quick Notes

## Project at a glance
- Domain: Transportation / car-sharing.
- Dataset: `plotly.express.data.carshare()`; 249 rows; columns `centroid_lat`, `centroid_lon`, `car_hours`, `peak_hour`.
- Inputs: latitude, longitude, peak hour.
- Label: `1` if `car_hours >= training median`, else `0`.
- Model: Random Forest Classifier.
- Pytest: validates the pipeline.
- MLflow: tracks parameters, metrics, model and artifacts.
- Evidently: compares reference input features with an intentionally shifted synthetic batch.

## Commands to remember
```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pytest -q
python main.py
python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000
```

## Five important definitions
- **MLOps:** practices and tools that make ML development, testing, deployment and monitoring repeatable and manageable.
- **Pytest:** Python test framework; discovers `test_*.py` files and functions named `test_*`.
- **MLflow Tracking:** records experiment runs, parameters, metrics, tags and artifacts.
- **Evidently:** evaluates data/model quality and detects distribution changes such as data drift.
- **Data drift:** change in the input feature distribution between a reference dataset and a later/current dataset.

## Exact demo interpretation
Reference = real held-out car-share feature rows. Current = artificial copy with latitude +0.02, longitude -0.02, and peak_hour +4 modulo 24. The shift was created intentionally to show the report. Do not claim it is actual production drift.

## Output paths
- `outputs/eda_summary.json`
- `outputs/classification_metrics.json`
- `outputs/test_predictions.csv`
- `outputs/synthetic_current_features.csv`
- `outputs/evidently_carshare_data_drift.html`
- `mlflow.db` and `mlartifacts/`
