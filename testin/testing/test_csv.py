from pathlib import Path

import pandas as pd
import joblib
import pytest


ROOT = Path(__file__).resolve().parents[1]

MODEL_FILE = ROOT / "employee_salary_model.pkl"


FEATURES = [
    "Experience",
    "Education Level",
    "Performance Rating",
    "Skill Score",
    "Previous Salary Percentile",
]


ALLOWED_CLASSES = {
    "VERY HIGH",
    "HIGH",
    "MEDIUM",
    "LOW",
}


@pytest.fixture(scope="module")
def model():

    if not MODEL_FILE.exists():

        pytest.skip(
            "employee_salary_model.pkl not found"
        )

    return joblib.load(MODEL_FILE)


# ============================================================
# MODEL LOADING TEST
# ============================================================

def test_model_can_be_loaded(model):

    assert model is not None

    assert hasattr(
        model,
        "predict"
    )


# ============================================================
# SINGLE PREDICTION TEST
# ============================================================

def test_prediction_returns_one_salary_category(model):

    sample = pd.DataFrame([
        {
            "Experience": 6.0,

            "Education Level": 4.0,

            "Performance Rating": 4.0,

            "Skill Score": 80.0,

            "Previous Salary Percentile": 70.0,
        }
    ])


    prediction = str(
        model.predict(sample)[0]
    ).upper()


    assert prediction in ALLOWED_CLASSES, (

        f"Unexpected salary category returned: "
        f"{prediction}"
    )


# ============================================================
# MULTIPLE PREDICTION TEST
# ============================================================

def test_prediction_for_multiple_employees(model):

    samples = pd.DataFrame([

        {
            "Experience": 2.0,

            "Education Level": 2.0,

            "Performance Rating": 2.0,

            "Skill Score": 40.0,

            "Previous Salary Percentile": 30.0,
        },

        {
            "Experience": 10.0,

            "Education Level": 5.0,

            "Performance Rating": 5.0,

            "Skill Score": 95.0,

            "Previous Salary Percentile": 90.0,
        }

    ])


    predictions = model.predict(
        samples
    )


    assert len(predictions) == 2


    assert all(
        str(p).upper() in ALLOWED_CLASSES
        for p in predictions
    )


# ============================================================
# FEATURE TEST
# ============================================================

def test_required_features():

    sample = pd.DataFrame([
        {
            "Experience": 6.0,

            "Education Level": 4.0,

            "Performance Rating": 4.0,

            "Skill Score": 80.0,

            "Previous Salary Percentile": 70.0,
        }
    ])


    assert list(sample.columns) == FEATURES
