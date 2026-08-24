from pathlib import Path
import os

import pytest


ROOT = Path(__file__).resolve().parents[1]


APP_CANDIDATES = [

    os.getenv(
        "APP_FILE",
        ""
    ),

    "employee_salary_prediction.py",

    "employee_salary_analysis.py",

    "main.py",

    "app.py",

    "Pasted code(3).py",
]


def find_app():

    for name in APP_CANDIDATES:

        if (
            name
            and
            (ROOT / name).exists()
        ):

            return ROOT / name

    return None


@pytest.fixture(scope="module")
def source():

    app = find_app()


    if app is None:

        pytest.skip(
            "Main application file not found"
        )


    return app.read_text(
        encoding="utf-8",
        errors="ignore"
    )


# ============================================================
# TKINTER TEST
# ============================================================

def test_tkinter_is_used(source):

    assert (
        "import tkinter" in source
        or
        "from tkinter" in source
    )


# ============================================================
# PREDICT BUTTON TEST
# ============================================================

def test_predict_button_exists(source):

    assert "Predict Salary" in source

    assert "command=submit" in source


# ============================================================
# CLEAR BUTTON TEST
# ============================================================

def test_clear_button_exists(source):

    assert "Clear" in source

    assert "command=clear" in source


# ============================================================
# EXIT BUTTON TEST
# ============================================================

def test_exit_button_exists(source):

    assert "Exit" in source

    assert "command=exit_app" in source


# ============================================================
# RESULT FIELD TEST
# ============================================================

def test_result_fields_exist(source):

    assert "out_pred" in source

    assert "out_risk" in source

    assert "out_rec" in source


# ============================================================
# INPUT FIELD TEST
# ============================================================

def test_required_input_fields_exist(source):

    required = [

        "e_eid",

        "e_name",

        "e_email",

        "e_exp",

        "e_edu",

        "e_perf",

        "e_skill",

        "e_prev",
    ]


    for field in required:

        assert field in source


# ============================================================
# VALIDATION FUNCTION TEST
# ============================================================

def test_validation_functions_exist(source):

    required = [

        "validate_employee_id",

        "validate_name",

        "validate_email",

        "validate_experience",

        "validate_education",

        "validate_performance",

        "validate_skill",

        "validate_previous_salary",

        "validate_all",
    ]


    for function_name in required:

        assert (
            f"def {function_name}"
            in source
        )


# ============================================================
# PREDICTION TEST
# ============================================================

def test_prediction_function_exists(source):

    assert "def submit" in source

    assert "model.predict" in source


# ============================================================
# CSV TEST
# ============================================================

def test_csv_logging_exists(source):

    assert "def save_csv" in source

    assert "to_csv" in source


# ============================================================
# N8N TEST
# ============================================================

def test_n8n_integration_exists(source):

    assert "N8N_WEBHOOK_URL" in source

    assert "requests.post" in source

    assert "call_n8n" in source
