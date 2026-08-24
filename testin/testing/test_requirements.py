from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]

APP_CANDIDATES = [
    os.getenv("APP_FILE", ""),
    "employee_salary_prediction.py",
    "employee_salary_analysis.py",
    "main.py",
    "app.py",
    "Pasted code(3).py",
]


def find_app():
    for name in APP_CANDIDATES:
        if name and (ROOT / name).exists():
            return ROOT / name
    return None


def test_main_application_exists():
    app = find_app()

    assert app is not None, (
        "Main Tkinter Python file was not found. "
        "Set APP_FILE to your actual filename."
    )


def test_dataset_exists():
    assert (ROOT / "employee_salary_dataset_ml_300.csv").exists(), (
        "employee_salary_dataset_ml_300.csv is missing."
    )


def test_model_exists():
    assert (ROOT / "employee_salary_model.pkl").exists(), (
        "employee_salary_model.pkl is missing."
    )


def test_testing_requirements_exists():
    assert (
        Path(__file__).resolve().parent / "requirements.txt"
    ).exists()
