# Wine Classification ML Pipeline - Makefile
# Windows: Use with `make` command (install: choco install make)
# Or run commands directly in PowerShell

.PHONY: help install test coverage run mlflow clean all

help:
	@echo "Wine Classification ML Pipeline - Available Commands:"
	@echo ""
	@echo "  make install       - Install dependencies"
	@echo "  make test          - Run tests"
	@echo "  make coverage      - Run tests with coverage report"
	@echo "  make run           - Run the ML pipeline"
	@echo "  make mlflow        - Start MLflow UI"
	@echo "  make clean         - Clean generated files"
	@echo "  make all           - Install, test, and run pipeline"
	@echo ""

install:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

test:
	python -m pytest -v

coverage:
	python -m pytest -v --cov=carshare_mlops --cov-report=html --cov-report=term
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

run:
	python main.py

mlflow:
	python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000

clean:
	rm -rf outputs/*.csv outputs/*.json outputs/*.html
	rm -rf htmlcov .coverage .pytest_cache
	rm -rf mlflow.db mlartifacts
	rm -rf __pycache__ carshare_mlops/__pycache__ tests/__pycache__

all: install test run
	@echo ""
	@echo "✅ Pipeline completed successfully!"
	@echo "📊 View outputs in the 'outputs' folder"
	@echo "🔬 Start MLflow UI with: make mlflow"
