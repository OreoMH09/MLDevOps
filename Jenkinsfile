pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.11'
        VENV_PATH = '.venv'
        MLFLOW_TRACKING_URI = 'sqlite:///mlflow.db'
        PYTHON_EXE = 'C:\\Users\\Sanika Naik\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
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
                    "%PYTHON_EXE%" -m venv %VENV_PATH%
                    call %VENV_PATH%\\Scripts\\activate.bat
                    "%PYTHON_EXE%" -m pip install --upgrade pip
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing project dependencies...'
                bat '''
                    call %VENV_PATH%\\Scripts\\activate.bat
                    "%PYTHON_EXE%" -m pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running Pytest tests...'
                bat '''
                    call %VENV_PATH%\\Scripts\\activate.bat
                    "%PYTHON_EXE%" -m pytest -v --junitxml=test-results.xml --cov=carshare_mlops --cov-report=xml --cov-report=html
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }
        
        stage('Train Model & Generate Reports') {
            steps {
                echo 'Running ML pipeline: training model and generating reports...'
                bat '''
                    call %VENV_PATH%\\Scripts\\activate.bat
                    "%PYTHON_EXE%" main.py
                '''
            }
        }
        
        stage('Archive Artifacts') {
            steps {
                echo 'Archiving outputs and reports...'
                archiveArtifacts artifacts: 'outputs/**/*', fingerprint: true
                archiveArtifacts artifacts: 'mlflow.db', fingerprint: true, allowEmptyArchive: true
                archiveArtifacts artifacts: 'htmlcov/**/*', fingerprint: true, allowEmptyArchive: true
            }
        }
        
        stage('Publish MLflow Metrics') {
            steps {
                echo 'Publishing MLflow metrics...'
                echo 'Metrics saved in outputs/classification_metrics.json'
                echo 'Check Build Artifacts for detailed metrics'
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
