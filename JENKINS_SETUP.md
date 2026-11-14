# Jenkins CI/CD Setup Guide

This guide walks you through setting up Jenkins for automated testing and deployment of the Wine Classification ML pipeline.

## Prerequisites

- Jenkins installed and running
- Python 3.11 installed on Jenkins server
- Git installed on Jenkins server

## 1. Install Jenkins (if not already installed)

### Windows Installation:

1. **Download Jenkins:**
   - Go to https://www.jenkins.io/download/
   - Download the Windows installer (LTS version)

2. **Install Jenkins:**
   - Run the installer
   - Follow the installation wizard
   - Default port: 8080
   - Initial admin password location: `C:\Program Files\Jenkins\secrets\initialAdminPassword`

3. **Access Jenkins:**
   - Open browser: http://localhost:8080
   - Enter the initial admin password
   - Install suggested plugins
   - Create admin user

## 2. Configure Jenkins

### Install Required Plugins:

1. Go to **Manage Jenkins** → **Manage Plugins** → **Available**
2. Search and install:
   - Pipeline
   - Git Plugin
   - HTML Publisher Plugin
   - JUnit Plugin
   - Cobertura Plugin (for coverage reports)
   - Blue Ocean (optional, for better UI)

3. Restart Jenkins after installation

### Configure Python:

1. Go to **Manage Jenkins** → **Global Tool Configuration**
2. Add Python installation or configure path to your Python 3.11

## 3. Create Jenkins Pipeline Job

### Option A: Pipeline from SCM (if using Git)

1. Click **New Item**
2. Enter name: `Wine_Classification_Pipeline`
3. Select **Pipeline**
4. Click **OK**

5. In **Pipeline** section:
   - Definition: `Pipeline script from SCM`
   - SCM: `Git`
   - Repository URL: `<your-git-repo-url>`
   - Branch: `*/main` or `*/master`
   - Script Path: `Jenkinsfile`

6. Save

### Option B: Direct Pipeline Script (no Git required)

1. Click **New Item**
2. Enter name: `Wine_Classification_Pipeline`
3. Select **Pipeline**
4. Click **OK**

5. In **Pipeline** section:
   - Definition: `Pipeline script`
   - Copy and paste the entire Jenkinsfile content

6. Configure Build Triggers (optional):
   - ✅ Poll SCM: `H/5 * * * *` (every 5 minutes)
   - ✅ Build periodically: `H 2 * * *` (daily at 2 AM)

7. Save

## 4. Pipeline Stages Explained

The Jenkins pipeline includes these stages:

### 1. **Checkout**
- Pulls the latest code from repository

### 2. **Setup Python Environment**
- Creates virtual environment
- Upgrades pip

### 3. **Install Dependencies**
- Installs all packages from requirements.txt

### 4. **Run Tests**
- Executes pytest with coverage
- Generates JUnit XML report
- Generates HTML coverage report

### 5. **Train Model & Generate Reports**
- Runs the main ML pipeline
- Trains Random Forest model
- Generates metrics and predictions
- Creates Evidently drift report
- Logs to MLflow

### 6. **Archive Artifacts**
- Archives all outputs
- Publishes HTML reports
- Stores MLflow database

### 7. **Publish MLflow Metrics**
- Displays key metrics in console
- Makes metrics visible in Jenkins

## 5. Run the Pipeline

1. Go to your pipeline job
2. Click **Build Now**
3. Watch the pipeline execute in real-time
4. View stage progress in **Stage View**

## 6. View Reports

After successful build:

### Test Results:
- Click **Test Results** in build page
- View test execution details

### Coverage Report:
- Click **Coverage Report**
- Browse code coverage statistics

### Evidently Drift Report:
- Click **Evidently Data Drift Report**
- Interactive HTML report with drift analysis

### Console Output:
- Click **Console Output**
- View full execution logs including metrics

### Artifacts:
- Click **Build Artifacts**
- Download:
  - `outputs/classification_metrics.json`
  - `outputs/test_predictions.csv`
  - `outputs/eda_summary.json`
  - `outputs/evidently_wine_data_drift.html`
  - `mlflow.db`

## 7. Troubleshooting

### Issue: Python not found
**Solution:** Add Python to system PATH or configure in Jenkins Global Tool Configuration

### Issue: pip install fails
**Solution:** 
- Check internet connectivity
- Try: `python -m pip install --default-timeout=1000 -r requirements.txt`

### Issue: Tests fail
**Solution:**
- Check console output for specific test failures
- Verify all dependencies are installed
- Run tests locally first: `python -m pytest -v`

### Issue: MLflow errors
**Solution:**
- Ensure `mlflow.db` directory is writable
- Check MLflow installation: `python -m pip show mlflow`

### Issue: Evidently import errors
**Solution:**
- Verify evidently==0.7.19 is installed
- Check compatible dependencies: `python-multipart>=0.0.18`

## 8. Jenkins Pipeline Features

### ✅ Automated Testing
- Runs 7 unit tests automatically
- Includes data validation, model training, and drift tests

### ✅ Code Coverage
- Generates coverage reports
- Tracks which code is tested

### ✅ ML Experiment Tracking
- Logs models to MLflow
- Tracks metrics across builds

### ✅ Data Drift Monitoring
- Generates Evidently reports
- Compares reference vs current data

### ✅ Artifact Management
- Stores all outputs
- Easy download and review

### ✅ Build History
- Track all builds
- Compare metrics over time

## 9. Viva Questions & Answers

### Q: What does Jenkins do in your project?
**A:** "Jenkins automates our ML pipeline by running tests, training the model, generating drift reports, and tracking experiments with MLflow. Every time code is pushed, Jenkins ensures quality through automated testing and creates reproducible ML artifacts."

### Q: What are the stages in your Jenkins pipeline?
**A:** "The pipeline has 7 stages: Checkout, Setup Environment, Install Dependencies, Run Tests (Pytest), Train Model, Archive Artifacts, and Publish Metrics. Each stage has a specific purpose in the CI/CD workflow."

### Q: How does Jenkins integrate with MLflow?
**A:** "After model training, Jenkins archives the mlflow.db database and publishes metrics like accuracy, precision, and recall. The pipeline also displays these metrics in the console output for quick review."

### Q: What happens if tests fail?
**A:** "If pytest tests fail, the pipeline stops immediately and doesn't proceed to training. This prevents bad code from being deployed. Jenkins marks the build as failed and sends notifications."

### Q: How do you view the Evidently report?
**A:** "Jenkins publishes the Evidently HTML report as a build artifact. You can click on 'Evidently Data Drift Report' in the build page to view the interactive drift analysis in the browser."

### Email Notifications:
Add to Jenkinsfile post section:
```groovy
post {
    failure {
        emailext (
            subject: "Build Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
            body: "Check console output at ${env.BUILD_URL}",
            to: "your-email@example.com"
        )
    }
}
```

### Slack Notifications:
Install Slack Notification plugin and add:
```groovy
post {
    success {
        slackSend color: "good", message: "Build succeeded!"
    }
}
```

### Parallel Execution:
Run tests and linting in parallel:
```groovy
stage('Quality Checks') {
    parallel {
        stage('Tests') {
            steps {
                bat 'python -m pytest'
            }
        }
        stage('Lint') {
            steps {
                bat 'python -m flake8 .'
            }
        }
    }
}
```

## 11. Quick Reference Commands

```powershell
# Test locally before Jenkins
python -m pytest -v --cov=carshare_mlops

# Run pipeline manually
python main.py

# View MLflow UI
python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000

# Check Jenkins logs
Get-Content "C:\Program Files\Jenkins\jenkins.log" -Tail 50
```

## Summary

Your Jenkins pipeline now provides:
- ✅ Automated testing with Pytest
- ✅ ML experiment tracking with MLflow
- ✅ Data drift monitoring with Evidently
- ✅ Code coverage reports
- ✅ Artifact archival
- ✅ Build history and metrics tracking

This demonstrates a complete CI/CD workflow for ML projects! 🚀
