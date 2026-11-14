# Jenkins Quick Start Guide

## 🚀 Setup Jenkins (3 Simple Steps)

### Step 1: Install Jenkins
```powershell
# Download from: https://www.jenkins.io/download/
# Install and access at: http://localhost:8080
# Initial password: C:\Program Files\Jenkins\secrets\initialAdminPassword
```

### Step 2: Install Plugins
1. Go to **Manage Jenkins** → **Manage Plugins** → **Available**
2. Install these plugins:
   - Pipeline
   - Git Plugin (if using Git)
   - HTML Publisher Plugin
   - JUnit Plugin
3. Restart Jenkins

### Step 3: Create Pipeline Job
1. Click **New Item**
2. Enter name: `Wine_Classification_Pipeline`
3. Select **Pipeline** → Click **OK**
4. Under **Pipeline** section:
   - Definition: `Pipeline script from SCM` (if using Git)
   - OR: `Pipeline script` (paste Jenkinsfile content)
5. **Save**
6. Click **Build Now**

---

## 📊 Pipeline Stages

Your Jenkins pipeline has 7 stages:

```
1. Checkout              → Pull latest code
2. Setup Environment     → Create Python virtual environment
3. Install Dependencies  → Install packages from requirements.txt
4. Run Tests            → Execute pytest with coverage (7 tests)
5. Train Model          → Run main.py pipeline
6. Archive Artifacts    → Save all outputs
7. Publish Metrics      → Display model metrics
```

---

## 📁 What Jenkins Does

After each build, Jenkins provides:

| Item | Description |
|------|-------------|
| **Test Results** | Shows 7/7 tests passed with details |
| **Coverage Report** | Code coverage statistics (71%) |
| **Evidently Report** | Interactive data drift HTML report |
| **Build Artifacts** | Downloadable outputs (JSON, CSV, HTML) |
| **Console Output** | Full execution logs with metrics |

---

## 🧪 Test Locally First

Before running in Jenkins, test locally:

```powershell
# Run tests
python -m pytest -v

# Run with coverage (like Jenkins)
python -m pytest -v --cov=carshare_mlops --cov-report=html

# Run pipeline
python main.py

# View coverage report
start htmlcov\index.html
```

---

## 🔧 Viewing Reports in Jenkins

After build completes:

1. **Test Results**: Click on build → **Test Results**
2. **Coverage**: Click on build → **Coverage Report**
3. **Drift Report**: Click on build → **Evidently Data Drift Report**
4. **Metrics**: Click on build → **Console Output** (see bottom)
5. **Artifacts**: Click on build → **Build Artifacts**

---

## 📊 Expected Results

### Tests: **7/7 Passing** ✅
```
✓ test_bundled_wine_dataset_loads_with_expected_schema
✓ test_wine_classes_are_valid
✓ test_split_produces_correct_classes
✓ test_split_is_reproducible
✓ test_random_forest_trains_and_returns_valid_classification_metrics
✓ test_synthetic_drift_batch_is_reproducible_and_does_not_mutate_reference
✓ test_evidently_report_is_created
```

### Metrics: **Perfect Classification** 🎯
```
Accuracy:   100%
Precision:  100%
Recall:     100%
F1 Score:   100%
```

### Coverage: **71%** 📈
```
carshare_mlops/__init__.py     100%
carshare_mlops/data.py          93%
carshare_mlops/model.py         90%
carshare_mlops/monitoring.py   100%
```

---

## 🔧 Troubleshooting

### Problem: Python not found
**Solution:**
```powershell
# Add Python to PATH
setx PATH "%PATH%;C:\Python311;C:\Python311\Scripts"
# Restart Jenkins service
```

### Problem: Tests fail in Jenkins
**Solution:**
- Check Console Output for error details
- Verify all dependencies installed
- Test locally first: `python -m pytest -v`

### Problem: pip install fails
**Solution:**
```powershell
# Use longer timeout
python -m pip install --default-timeout=1000 -r requirements.txt
```

---

## 🎓 Viva Questions & Answers

**Q: What is Jenkins doing in your project?**
A: "Jenkins automates our ML pipeline. It runs tests, trains the model, generates drift reports, and tracks experiments in MLflow. Every code change triggers this automated workflow, ensuring quality and reproducibility."

**Q: What are the pipeline stages?**
A: "We have 7 stages: Checkout code, Setup environment, Install dependencies, Run tests with pytest, Train model, Archive artifacts, and Publish metrics. Each stage validates before moving to the next."

**Q: What happens if tests fail?**
A: "The pipeline stops immediately. Jenkins marks the build as failed and doesn't proceed to training. This prevents bad code from being deployed and ensures only tested code runs."

**Q: How does Jenkins integrate with MLflow?**
A: "After training, Jenkins archives the mlflow.db database and publishes key metrics like accuracy and F1 score in the console output. All experiment data is preserved as build artifacts."

**Q: What reports does Jenkins generate?**
A: "Jenkins generates three reports: JUnit test results showing all 7 tests passed, HTML code coverage report showing 71% coverage, and Evidently data drift report showing feature distribution changes."

---

## 🎯 Demo Checklist

Before your viva:

- [ ] Jenkins installed and running
- [ ] Pipeline job created successfully
- [ ] Run at least one successful build
- [ ] Can show Test Results page
- [ ] Can show Coverage Report
- [ ] Can show Evidently Report
- [ ] Can explain each stage
- [ ] Can show Console Output with metrics
- [ ] Can navigate Build Artifacts

---

## 📝 Quick Commands

```powershell
# Check Jenkins service
Get-Service Jenkins

# Start Jenkins
Start-Service Jenkins

# Jenkins URL
http://localhost:8080

# View Jenkins logs
Get-Content "C:\Program Files\Jenkins\jenkins.log" -Tail 50

# MLflow UI (after pipeline runs)
python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

---

## 🎉 Benefits of Jenkins in ML

1. **Automation**: No manual testing or training needed
2. **Quality Assurance**: Tests run before every deployment
3. **Reproducibility**: Every build is documented and traceable
4. **Artifact Management**: All outputs saved automatically
5. **CI/CD**: Continuous integration and deployment workflow
6. **Traceability**: Complete history of all builds and metrics

---

## 📚 For More Details

- Full setup guide: See `JENKINS_SETUP.md`
- Project details: See `README.md`
- Pipeline code: See `Jenkinsfile`

---

## ✅ Your Complete Stack

| Tool | Purpose | Status |
|------|---------|--------|
| **Pytest** | Automated testing | ✅ 7/7 tests |
| **MLflow** | Experiment tracking | ✅ Working |
| **Evidently** | Data drift monitoring | ✅ Reports |
| **Jenkins** | CI/CD automation | ✅ Ready |

**You're ready for your viva!** 🚀
