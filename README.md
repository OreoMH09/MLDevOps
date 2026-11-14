# ML DevOps POE: Wine Classification

**Tools demonstrated:** Pytest + MLflow + Evidently  
**Domain:** Wine Chemistry / Quality Analysis  
**Use case:** Classify wines into different cultivar categories using chemical measurements.

## 1. Dataset (no CSV download)

The project uses the dataset bundled inside scikit-learn:

```python
from sklearn.datasets import load_wine
wine = load_wine()
```

Sklearn provides this built-in dataset which contains 178 samples of wines with 13 chemical features:

- `alcohol`: Alcohol content
- `malic_acid`: Malic acid content
- `ash`: Ash content
- `alcalinity_of_ash`: Alkalinity of ash
- `magnesium`: Magnesium content
- `total_phenols`: Total phenols
- `flavanoids`: Flavanoid content
- `nonflavanoid_phenols`: Non-flavanoid phenol content
- `proanthocyanins`: Proanthocyanin content
- `color_intensity`: Color intensity
- `hue`: Hue
- `od280_od315_of_diluted_wines`: OD280/OD315 of diluted wines
- `proline`: Proline content

The target variable is `wine_class` with 3 classes (0, 1, 2) representing different wine cultivars.

The source data is already packaged with scikit-learn. The project does **not** download a separate CSV. Scikit-learn is included in `requirements.txt`; install the Python requirements once when setting up the project.

## 2. Problem statement

Wine producers want to classify wines into cultivar categories based on their chemical composition. We use all 13 chemical features as input to predict the wine class (0, 1, or 2).

This is a multi-class classification problem with 3 balanced classes. The model helps identify wine cultivars based on their chemical properties, which is useful for quality control and authentication in the wine industry.

## 3. The three tools

### Pytest - automated testing

`tests/test_pipeline.py` checks:

1. The bundled dataset loads and has the expected schema (178 samples, 14 columns).
2. Required columns contain no missing values.
3. Wine classes are in the valid range (0, 1, 2).
4. The train/test split is reproducible and stratified.
5. The Random Forest model produces valid predictions and metrics for multi-class classification.
6. The synthetic current batch is deterministic and does not mutate the reference data.
7. Evidently creates an HTML report (the test runs when Evidently is installed).

Run:

```bash
python -m pytest -q
```

### MLflow - experiment tracking

The training run is saved under experiment `Wine_Classification` in a local SQLite tracking store (`mlflow.db`). The run records:

- Model parameters (tree count, depth, leaf size, random seed)
- Evaluation metrics (accuracy, weighted precision, recall, F1)
- Dataset, domain, target-rule, and monitoring tags
- The trained scikit-learn model and its inferred signature
- The Evidently HTML report, metrics JSON, and prediction CSV as artifacts

Open the user interface after running the pipeline:

```bash
python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000
```

Then visit `http://127.0.0.1:5000`.

### Evidently - data drift monitoring

The project compares:

- **Reference data:** held-out test features from the bundled wine dataset.
- **Current data:** a deterministic synthetic copy of those features with deliberate shifts.

The controlled demonstration applies percentage shifts to chemical measurements (e.g., alcohol +5%, malic acid -5%). Evidently's `DataDriftPreset` evaluates feature-distribution differences and writes:

`outputs/evidently_wine_data_drift.html`

The current batch is artificial. Explain it as a simulated data-drift example, not actual production drift.

## 4. Model

The solution uses `RandomForestClassifier` with 300 trees, maximum depth 5, minimum leaf size 2, and a fixed random seed. The code evaluates weighted accuracy, precision, recall, F1 score, and a confusion matrix on the held-out partition.

Do not memorize a hard-coded score: the script prints the result produced by the environment in which it runs. The dataset is small (178 rows), and the model is a baseline demonstration rather than a production-ready system.

## 5. Run on Windows

1. Extract the ZIP.
2. Open the extracted folder in VS Code, PyCharm, or another IDE.
3. Ensure Python 3.11 is installed and available through the Windows Python launcher (`py -3.11`).
4. Double-click `setup_windows.bat` once. It creates `.venv` and installs `requirements.txt`.
5. Double-click `run_windows.bat`. It runs Pytest first and only starts the pipeline if tests pass.
6. Open `outputs/evidently_wine_data_drift.html` in a browser.
7. Double-click `start_mlflow_ui.bat` to inspect the MLflow experiment. Keep its terminal open while viewing the UI.

## 6. Run from the IDE terminal

```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q
python main.py
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

## 7. Files produced

| File | Purpose |
|---|---|
| `outputs/eda_summary.json` | Dataset shape, null counts, split sizes, class distribution |
| `outputs/classification_metrics.json` | Accuracy, precision, recall, F1 and confusion matrix |
| `outputs/test_predictions.csv` | Actual and predicted test labels with class probabilities |
| `outputs/synthetic_current_features.csv` | Artificial current feature batch used for the drift demo |
| `outputs/evidently_wine_data_drift.html` | Interactive Evidently HTML drift report |
| `mlflow.db` and `mlartifacts/` | Local MLflow experiment metadata and artifacts |

## 8. Viva explanation in 30 seconds

"I selected the wine chemistry domain and used scikit-learn's built-in wine dataset, which loads in Python without downloading a separate CSV. I used 13 chemical features (alcohol, acids, phenols, etc.) to classify wines into 3 cultivar categories. Pytest validates the data, split, model outputs and simulated drift batch. MLflow tracks the experiment parameters, metrics, model and artifacts. Evidently compares reference features with a deliberately shifted synthetic batch and generates an HTML data-drift report. The model uses Random Forest for multi-class classification."

## 9. Notes

- Jenkins provides CI/CD automation for the ML pipeline (optional)
- Internet is needed once to install the packages in `requirements.txt`, but not to fetch the dataset after scikit-learn is installed
- This is an academic demonstration. It is not a live wine quality control system and the synthetic current batch is not real production data

## 10. CI/CD with Jenkins

The project includes a complete Jenkins pipeline (`Jenkinsfile`) that automates:
- Running Pytest tests with coverage
- Training the model
- Generating Evidently drift reports
- Logging to MLflow
- Archiving all artifacts

**Quick Setup:**
1. Install Jenkins: https://www.jenkins.io/download/
2. Create Pipeline job pointing to this repository
3. Build automatically runs: Tests → Train → Reports → Archive

See `JENKINS_SETUP.md` for detailed instructions.

## Official documentation

- Sklearn wine dataset: https://scikit-learn.org/stable/datasets/toy_dataset.html#wine-dataset
- Sklearn datasets API: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_wine.html
- MLflow Tracking Quickstart: https://mlflow.org/docs/latest/ml/tracking/quickstart
- Evidently Data Drift preset: https://evidentlyai.github.io/evidently/api-reference/main/evidently/presets.html
- Pytest getting started: https://docs.pytest.org/en/stable/getting-started.html
