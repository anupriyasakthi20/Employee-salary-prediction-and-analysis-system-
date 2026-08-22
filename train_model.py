import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# ONE CSV FILE for both training data and new UI records
DATASET_FILE = "employee_salary_dataset_ml_300.csv"
MODEL_FILE = "employee_salary_model.pkl"

FEATURES = [
    "Experience",
    "Education Level",
    "Performance Rating",
    "Skill Score",
    "Previous Salary Percentile"
]

TARGET = "Prediction"

CLASS_NAMES = ["LOW", "MEDIUM", "HIGH", "VERY HIGH"]


def train_and_save_model():
    # 1. Load the same CSV that also stores UI records
    df = pd.read_csv(DATASET_FILE)

    required_columns = FEATURES + [TARGET]
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns in dataset: {missing}")

    # 2. Convert feature columns to numbers
    for column in FEATURES:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df[TARGET] = df[TARGET].astype(str).str.strip().str.upper()

    # 3. Clean training rows
    df = df.dropna(subset=required_columns).copy()

    if len(df) < 20:
        raise ValueError("Not enough labeled rows to train the model.")

    # 4. Prepare features and target
    X = df[FEATURES]
    y = df[TARGET]

    # Make sure all four classes exist
    missing_classes = set(CLASS_NAMES) - set(y.unique())

    if missing_classes:
        raise ValueError(
            "The CSV must contain all four training classes: "
            + ", ".join(sorted(missing_classes))
        )

    print("\nDataset shape:", df.shape)
    print("\nClass distribution:")
    print(y.value_counts())

    # 5. Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    # 6. ML pipeline
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(max_iter=2000, random_state=42))
    ])

    # 7. Train
    model.fit(X_train, y_train)

    # 8. Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("\nModel: Logistic Regression")
    print("Training rows:", len(X_train))
    print("Testing rows:", len(X_test))
    print(f"Accuracy: {accuracy * 100:.2f}%")

    report = classification_report(
        y_test,
        y_pred,
        labels=CLASS_NAMES,
        zero_division=0
    )

    print("\nClassification Report:")
    print(report)

    cm = confusion_matrix(y_test, y_pred, labels=CLASS_NAMES)
    print("\nConfusion Matrix:")
    print(cm)

    # 9. Save confusion matrix plot
    disp = ConfusionMatrixDisplay(cm, display_labels=CLASS_NAMES)
    disp.plot(xticks_rotation=45)
    plt.tight_layout()
    plt.savefig("confusion_matrix.png")
    plt.close()

    # 10. Save evaluation report
    with open("model_evaluation.txt", "w", encoding="utf-8") as f:
        f.write("Employee Salary Prediction - Model Evaluation\n")
        f.write(f"Model: Logistic Regression\n")
        f.write(f"Training rows: {len(X_train)}\n")
        f.write(f"Testing rows: {len(X_test)}\n")
        f.write(f"Features: {', '.join(FEATURES)}\n")
        f.write(f"Accuracy: {accuracy * 100:.2f}%\n\n")
        f.write("Classification Report:\n")
        f.write(report)

    # 11. Save model
    joblib.dump(model, MODEL_FILE)
    print(f"\nSaved model: {MODEL_FILE}")

    return model, accuracy


if __name__ == "__main__":
    train_and_save_model()
