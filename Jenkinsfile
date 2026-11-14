pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.11'
        VENV_PATH = '.venv'
        MLFLOW_TRACKING_URI = 'sqlite:///mlflow.db'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from repository...'
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                bat '''
                    py -3.11 -m venv %VENV_PATH%
                    call %VENV_PATH%\\Scripts\\activate.bat
                    py -3.11 -m pip install --upgrade pip
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing project dependencies...'
                bat '''
                    call %VENV_PATH%\\Scripts\\activate.bat
                    py -3.11 -m pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running Pytest tests...'
                bat '''
                    call %VENV_PATH%\\Scripts\\activate.bat
                    py -3.11 -m pytest -v --junitxml=test-results.xml --cov=carshare_mlops --cov-report=xml --cov-report=html
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report',
                        reportTitles: 'Code Coverage'
                    ])
                }
            }
        }
        
        stage('Train Model & Generate Reports') {
            steps {
                echo 'Running ML pipeline: training model and generating reports...'
                bat '''
                    call %VENV_PATH%\\Scripts\\activate.bat
                    py -3.11 main.py
                '''
            }
        }
        
        stage('Archive Artifacts') {
            steps {
                echo 'Archiving outputs and reports...'
                archiveArtifacts artifacts: 'outputs/**/*', fingerprint: true
                archiveArtifacts artifacts: 'mlflow.db', fingerprint: true, allowEmptyArchive: true
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'outputs',
                    reportFiles: 'evidently_wine_data_drift.html',
                    reportName: 'Evidently Data Drift Report',
                    reportTitles: 'Data Drift Analysis'
                ])
            }
        }
        
        stage('Publish MLflow Metrics') {
            steps {
                echo 'Publishing MLflow metrics...'
                script {
                    def metricsFile = readJSON file: 'outputs/classification_metrics.json'
                    echo "Accuracy: ${metricsFile.accuracy}"
                    echo "Precision: ${metricsFile.precision}"
                    echo "Recall: ${metricsFile.recall}"
                    echo "F1 Score: ${metricsFile.f1_score}"
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully! ✅'
            echo 'All tests passed and model trained successfully.'
        }
        failure {
            echo 'Pipeline failed! ❌'
            echo 'Check the logs above for details.'
        }
        always {
            echo 'Cleaning up workspace...'
            cleanWs(deleteDirs: true, patterns: [[pattern: '.venv', type: 'INCLUDE']])
        }
    }
}
