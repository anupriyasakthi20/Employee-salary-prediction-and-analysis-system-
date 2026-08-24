import tkinter as tk
from tkinter import messagebox
import pandas as pd
import joblib
import requests
from pathlib import Path
import re


# ============================================================
# FILE LOCATIONS
# ============================================================

BASE = Path(__file__).resolve().parent

CSV_FILE = BASE / "employee_salary_dataset_ml_300.csv"
MODEL_FILE = BASE / "employee_salary_model.pkl"


# ============================================================
# N8N CLOUD PRODUCTION WEBHOOK
# ============================================================

N8N_WEBHOOK_URL = (
    "https://niviii.app.n8n.cloud/webhook/fa1d3bb3-140d-4743-91bf-d6e05827ea79"
)


# ============================================================
# CALL N8N
# ============================================================

def call_n8n(
    employee_id,
    name,
    email,
    experience,
    education_level,
    performance_rating,
    skill_score,
    previous_salary_percentile,
    prediction,
    risk
):

    payload = {
        "employee_id": str(employee_id),
        "name": str(name),
        "email": str(email),
        "experience": float(experience),
        "education_level": float(education_level),
        "performance_rating": float(performance_rating),
        "skill_score": float(skill_score),
        "previous_salary_percentile": float(previous_salary_percentile),
        "prediction": str(prediction),
        "risk": str(risk)
    }

    try:

        response = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

    except requests.exceptions.Timeout:

        raise RuntimeError(
            "n8n request timed out.\n\n"
            "Make sure your n8n workflow is Published."
        )

    except requests.exceptions.ConnectionError:

        raise RuntimeError(
            "Could not connect to n8n Cloud.\n\n"
            "Check your internet connection and n8n Production URL."
        )

    except requests.exceptions.HTTPError as e:

        raise RuntimeError(
            f"n8n returned HTTP error:\n\n{e}\n\n"
            f"URL:\n{N8N_WEBHOOK_URL}"
        )

    # --------------------------------------------------------
    # Read n8n response
    # --------------------------------------------------------

    try:

        result = response.json()

    except ValueError:

        raise RuntimeError(
            "n8n did not return JSON.\n\n"
            f"Response received:\n{response.text[:500]}"
        )

    # --------------------------------------------------------
    # Find recommendation
    # --------------------------------------------------------

    recommendation = ""

    if isinstance(result, dict):

        recommendation = (
            result.get("recommendation")
            or result.get("output")
            or result.get("text")
            or ""
        )

    elif isinstance(result, list) and len(result) > 0:

        first = result[0]

        if isinstance(first, dict):

            recommendation = (
                first.get("recommendation")
                or first.get("output")
                or first.get("text")
                or ""
            )

    recommendation = str(recommendation).strip()

    if not recommendation:

        raise RuntimeError(
            "n8n did not return a recommendation.\n\n"
            "Check the 'Respond to Webhook' node.\n\n"
            f"n8n response:\n{result}"
        )

    return recommendation


# ============================================================
# SAVE EMPLOYEE DATA TO CSV
# ============================================================

def save_csv(values):

    new_row = pd.DataFrame([values])

    if CSV_FILE.exists():

        try:

            existing_df = pd.read_csv(CSV_FILE)

        except Exception:

            existing_df = pd.DataFrame()

        # Make sure all required columns exist
        for column in new_row.columns:

            if column not in existing_df.columns:

                existing_df[column] = ""

        for column in existing_df.columns:

            if column not in new_row.columns:

                new_row[column] = ""

        # Keep same column order
        new_row = new_row[existing_df.columns]

        final_df = pd.concat(
            [existing_df, new_row],
            ignore_index=True
        )

    else:

        final_df = new_row

    final_df.to_csv(
        CSV_FILE,
        index=False
    )


# ============================================================
# ERROR MESSAGE HELPERS
# ============================================================

def show_error(label, message):

    label.config(
        text=message,
        fg="red"
    )


def clear_error(label):

    label.config(
        text=""
    )


# ============================================================
# EMAIL VALIDATION
# ============================================================

def is_valid_email(email):

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return re.match(pattern, email) is not None


# ============================================================
# EMPLOYEE ID VALIDATION
# ============================================================

def validate_employee_id(event=None):

    value = e_eid.get().strip()

    if not value:

        show_error(
            err_eid,
            "Employee ID is required"
        )

        return False

    if not value.isdigit():

        show_error(
            err_eid,
            "Only numbers allowed"
        )

        return False

    clear_error(err_eid)

    return True


# ============================================================
# NAME VALIDATION
# ============================================================

def validate_name(event=None):

    value = e_name.get().strip()

    if not value:

        show_error(
            err_name,
            "Name is required"
        )

        return False

    if not re.fullmatch(r"[A-Za-z ]+", value):

        show_error(
            err_name,
            "Only letters allowed"
        )

        return False

    clear_error(err_name)

    return True


# ============================================================
# EMAIL VALIDATION
# ============================================================

def validate_email(event=None):

    value = e_email.get().strip()

    if not value:

        show_error(
            err_email,
            "Email is required"
        )

        return False

    if not is_valid_email(value):

        show_error(
            err_email,
            "Enter a valid email"
        )

        return False

    clear_error(err_email)

    return True


# ============================================================
# EXPERIENCE VALIDATION
# ============================================================

def validate_experience(event=None):

    value = e_exp.get().strip()

    if not value:

        show_error(
            err_exp,
            "Enter 0 - 40 years"
        )

        return False

    try:

        number = float(value)

    except ValueError:

        show_error(
            err_exp,
            "Numbers only"
        )

        return False

    if not 0 <= number <= 40:

        show_error(
            err_exp,
            "Must be 0 - 40 years"
        )

        return False

    clear_error(err_exp)

    return True


# ============================================================
# EDUCATION LEVEL VALIDATION
# ============================================================

def validate_education(event=None):

    value = e_edu.get().strip()

    if not value:

        show_error(
            err_edu,
            "Enter 1-5"
        )

        return False

    try:

        number = float(value)

    except ValueError:

        show_error(
            err_edu,
            "Numbers only"
        )

        return False

    if not 1 <= number <= 5:

        show_error(
            err_edu,
            "Must be 1-5"
        )

        return False

    clear_error(err_edu)

    return True


# ============================================================
# PERFORMANCE VALIDATION
# ============================================================

def validate_performance(event=None):

    value = e_perf.get().strip()

    if not value:

        show_error(
            err_perf,
            "Enter 1 5"
        )

        return False

    try:

        number = float(value)

    except ValueError:

        show_error(
            err_perf,
            "Numbers only"
        )

        return False

    if not 1 <= number <= 5:

        show_error(
            err_perf,
            "Must be 1 - 5"
        )

        return False

    clear_error(err_perf)

    return True


# ============================================================
# SKILL SCORE VALIDATION
# ============================================================

def validate_skill(event=None):

    value = e_skill.get().strip()

    if not value:

        show_error(
            err_skill,
            "Enter 0 - 100"
        )

        return False

    try:

        number = float(value)

    except ValueError:

        show_error(
            err_skill,
            "Numbers only"
        )

        return False

    if not 0 <= number <= 100:

        show_error(
            err_skill,
            "Must be 0 - 100"
        )

        return False

    clear_error(err_skill)

    return True


# ============================================================
# PREVIOUS SALARY PERCENTILE VALIDATION
# ============================================================

def validate_previous_salary(event=None):

    value = e_prev.get().strip()

    if not value:

        show_error(
            err_prev,
            "Enter 0 - 100"
        )

        return False

    try:

        number = float(value)

    except ValueError:

        show_error(
            err_prev,
            "Numbers only"
        )

        return False

    if not 0 <= number <= 100:

        show_error(
            err_prev,
            "Must be 0 - 100"
        )

        return False

    clear_error(err_prev)

    return True


# ============================================================
# VALIDATE ALL FIELDS
# ============================================================

def validate_all():

    valid = True

    if not validate_employee_id():

        valid = False

    if not validate_name():

        valid = False

    if not validate_email():

        valid = False

    if not validate_experience():

        valid = False

    if not validate_education():

        valid = False

    if not validate_performance():

        valid = False

    if not validate_skill():

        valid = False

    if not validate_previous_salary():

        valid = False

    return valid


# ============================================================
# PREDICTION
# ============================================================

def submit():

    # --------------------------------------------------------
    # Validate everything before prediction
    # --------------------------------------------------------

    if not validate_all():

        messagebox.showerror(
            "Input Error",
            "Please correct the highlighted fields."
        )

        return

    try:

        # ----------------------------------------------------
        # Get values from UI
        # ----------------------------------------------------

        employee_id = e_eid.get().strip()
        name = e_name.get().strip()
        email = e_email.get().strip()

        experience = float(
            e_exp.get().strip()
        )

        education_level = float(
            e_edu.get().strip()
        )

        performance_rating = float(
            e_perf.get().strip()
        )

        skill_score = float(
            e_skill.get().strip()
        )

        previous_salary_percentile = float(
            e_prev.get().strip()
        )


        # ----------------------------------------------------
        # Check ML model
        # ----------------------------------------------------

        if not MODEL_FILE.exists():

            raise RuntimeError(
                "ML model file not found.\n\n"
                "Run this command first:\n"
                "python train_model.py"
            )


        # ----------------------------------------------------
        # Load trained ML model
        # ----------------------------------------------------

        model = joblib.load(
            MODEL_FILE
        )


        # ----------------------------------------------------
        # Create input dataframe
        # IMPORTANT:
        # These names must match train_model.py
        # ----------------------------------------------------

        input_data = pd.DataFrame([
            {
                "Experience": experience,
                "Education Level": education_level,
                "Performance Rating": performance_rating,
                "Skill Score": skill_score,
                "Previous Salary Percentile": previous_salary_percentile
            }
        ])


        # ----------------------------------------------------
        # ML PREDICTION
        # ----------------------------------------------------

        prediction = str(
            model.predict(input_data)[0]
        ).upper()


        # ----------------------------------------------------
        # Retention risk level
        # ----------------------------------------------------

        risk_mapping = {

            "VERY HIGH": "LOW",

            "HIGH": "LOW",

            "MEDIUM": "MEDIUM",

            "LOW": "HIGH"
        }

        risk = risk_mapping.get(
            prediction,
            "MEDIUM"
        )


        # ----------------------------------------------------
        # Display processing message
        # ----------------------------------------------------

        out_pred.config(
            text=f"Prediction: {prediction}"
        )

        out_risk.config(
            text=f"Retention Risk: {risk}"
        )

        out_rec.config(
            text=(
                "AI Recommendation: "
                "Generating through Gemini 2.5 Flash..."
            )
        )

        root.update_idletasks()


        # ----------------------------------------------------
        # SEND DATA TO N8N
        # Gemini + Gmail happen inside n8n
        # ----------------------------------------------------

        recommendation = call_n8n(

            employee_id=employee_id,

            name=name,

            email=email,

            experience=experience,

            education_level=education_level,

            performance_rating=performance_rating,

            skill_score=skill_score,

            previous_salary_percentile=previous_salary_percentile,

            prediction=prediction,

            risk=risk
        )


        # ----------------------------------------------------
        # DISPLAY AI RECOMMENDATION
        # ----------------------------------------------------

        out_rec.config(
            text=f"AI Recommendation: {recommendation}"
        )


        # ----------------------------------------------------
        # SAVE DATA TO CSV
        # ----------------------------------------------------

        save_csv({

            "Employee ID": employee_id,

            "Name": name,

            "Email": email,

            "Experience": experience,

            "Education Level": education_level,

            "Performance Rating": performance_rating,

            "Skill Score": skill_score,

            "Previous Salary Percentile":
                previous_salary_percentile,

            "Prediction": prediction,

            "Risk Level": risk,

            "Recommendation": recommendation
        })


        # ----------------------------------------------------
        # SUCCESS MESSAGE
        # ----------------------------------------------------

        messagebox.showinfo(

            "Success",

            "Prediction completed successfully!\n\n"

            "✓ ML prediction completed\n"
            "✓ Gemini recommendation generated\n"
            "✓ Recommendation email sent through n8n/Gmail\n"
            "✓ Employee data saved to CSV"
        )


    # ========================================================
    # ERRORS
    # ========================================================

    except requests.exceptions.RequestException as e:

        messagebox.showerror(

            "n8n Error",

            "Could not connect to n8n Cloud.\n\n"
            f"{e}"
        )

    except Exception as e:

        messagebox.showerror(

            "Error",

            str(e)
        )


# ============================================================
# CLEAR BUTTON
# ============================================================

def clear():

    entries = [

        e_eid,
        e_name,
        e_email,
        e_exp,
        e_edu,
        e_perf,
        e_skill,
        e_prev

    ]

    for entry in entries:

        entry.delete(
            0,
            tk.END
        )


    # Clear error messages
    error_labels = [

        err_eid,
        err_name,
        err_email,
        err_exp,
        err_edu,
        err_perf,
        err_skill,
        err_prev

    ]

    for label in error_labels:

        clear_error(label)


    # Clear result
    out_pred.config(
        text="Prediction:"
    )

    out_risk.config(
        text="Retention Risk:"
    )

    out_rec.config(
        text="AI Recommendation:"
    )


# ============================================================
# EXIT
# ============================================================

def exit_app():

    root.destroy()


# ============================================================
# TKINTER WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Employee Salary Prediction and Analysis System"
)

root.geometry(
    "1350x850"
)

root.resizable(
    False,
    False
)


# ============================================================
# MAIN HEADING
# ============================================================

heading = tk.Label(

    root,

    text="EMPLOYEE SALARY PREDICTION AND ANALYSIS SYSTEM",

    font=("Arial", 24, "bold")
)

heading.grid(

    row=0,

    column=0,

    columnspan=10,

    pady=20
)


# ============================================================
# EMPLOYEE INFORMATION
# ============================================================

tk.Label(

    root,

    text="Employee Information",

    font=("Arial", 14, "bold")
).grid(

    row=1,

    column=1,

    columnspan=3,

    pady=10
)


# ============================================================
# EMPLOYEE ID
# ============================================================

tk.Label(

    root,

    text="Employee ID",

    font=("Arial", 12)
).grid(

    row=2,

    column=1,

    padx=10,

    pady=8,

    sticky="w"
)

e_eid = tk.Entry(

    root,

    width=30,

    font=("Arial", 11)
)

e_eid.grid(

    row=2,

    column=2,

    padx=10,

    pady=8
)

err_eid = tk.Label(

    root,

    text="",

    font=("Arial", 9, "bold"),

    anchor="w"
)

err_eid.grid(

    row=2,

    column=3,

    padx=5,

    sticky="w"
)


# ============================================================
# NAME
# ============================================================

tk.Label(

    root,

    text="Name",

    font=("Arial", 12)
).grid(

    row=3,

    column=1,

    padx=10,

    pady=8,

    sticky="w"
)

e_name = tk.Entry(

    root,

    width=30,

    font=("Arial", 11)
)

e_name.grid(

    row=3,

    column=2,

    padx=10,

    pady=8
)

err_name = tk.Label(

    root,

    text="",

    font=("Arial", 9, "bold"),

    anchor="w"
)

err_name.grid(

    row=3,

    column=3,

    padx=5,

    sticky="w"
)


# ============================================================
# EMAIL
# ============================================================

tk.Label(

    root,

    text="Email",

    font=("Arial", 12)
).grid(

    row=4,

    column=1,

    padx=10,

    pady=8,

    sticky="w"
)

e_email = tk.Entry(

    root,

    width=30,

    font=("Arial", 11)
)

e_email.grid(

    row=4,

    column=2,

    padx=10,

    pady=8
)

err_email = tk.Label(

    root,

    text="",

    font=("Arial", 9, "bold"),

    anchor="w"
)

err_email.grid(

    row=4,

    column=3,

    padx=5,

    sticky="w"
)


# ============================================================
# PROFESSIONAL INFORMATION
# ============================================================

tk.Label(

    root,

    text="Professional Information",

    font=("Arial", 14, "bold")
).grid(

    row=1,

    column=6,

    columnspan=3,

    pady=10
)


# ============================================================
# EXPERIENCE
# ============================================================

tk.Label(

    root,

    text="Experience (Years)",

    font=("Arial", 12)
).grid(

    row=2,

    column=6,

    padx=10,

    pady=8,

    sticky="w"
)

e_exp = tk.Entry(

    root,

    width=30,

    font=("Arial", 11)
)

e_exp.grid(

    row=2,

    column=7,

    padx=10,

    pady=8
)

err_exp = tk.Label(

    root,

    text="",

    font=("Arial", 9, "bold"),

    anchor="w"
)

err_exp.grid(

    row=2,

    column=8,

    padx=5,

    sticky="w"
)


# ============================================================
# EDUCATION LEVEL
# ============================================================

tk.Label(

    root,

    text="Education Level",

    font=("Arial", 12)
).grid(

    row=3,

    column=6,

    padx=10,

    pady=8,

    sticky="w"
)

e_edu = tk.Entry(

    root,

    width=30,

    font=("Arial", 11)
)

e_edu.grid(

    row=3,

    column=7,

    padx=10,

    pady=8
)

err_edu = tk.Label(

    root,

    text="",

    font=("Arial", 9, "bold"),

    anchor="w"
)

err_edu.grid(

    row=3,

    column=8,

    padx=5,

    sticky="w"
)


# ============================================================
# PERFORMANCE RATING
# ============================================================

tk.Label(

    root,

    text="Performance Rating",

    font=("Arial", 12)
).grid(

    row=4,

    column=6,

    padx=10,

    pady=8,

    sticky="w"
)

e_perf = tk.Entry(

    root,

    width=30,

    font=("Arial", 11)
)

e_perf.grid(

    row=4,

    column=7,

    padx=10,

    pady=8
)

err_perf = tk.Label(

    root,

    text="",

    font=("Arial", 9, "bold"),

    anchor="w"
)

err_perf.grid(

    row=4,

    column=8,

    padx=5,

    sticky="w"
)


# ============================================================
# SKILL SCORE
# ============================================================

tk.Label(

    root,

    text="Skill Score",

    font=("Arial", 12)
).grid(

    row=5,

    column=6,

    padx=10,

    pady=8,

    sticky="w"
)

e_skill = tk.Entry(

    root,

    width=30,

    font=("Arial", 11)
)

e_skill.grid(

    row=5,

    column=7,

    padx=10,

    pady=8
)

err_skill = tk.Label(

    root,

    text="",

    font=("Arial", 9, "bold"),

    anchor="w"
)

err_skill.grid(

    row=5,

    column=8,

    padx=5,

    sticky="w"
)


# ============================================================
# PREVIOUS SALARY PERCENTILE
# ============================================================

tk.Label(

    root,

    text="Previous Salary Percentile",

    font=("Arial", 12)
).grid(

    row=6,

    column=6,

    padx=10,

    pady=8,

    sticky="w"
)

e_prev = tk.Entry(

    root,

    width=30,

    font=("Arial", 11)
)

e_prev.grid(

    row=6,

    column=7,

    padx=10,

    pady=8
)

err_prev = tk.Label(

    root,

    text="",

    font=("Arial", 9, "bold"),

    anchor="w"
)

err_prev.grid(

    row=6,

    column=8,

    padx=5,

    sticky="w"
)


# ============================================================
# LIVE VALIDATION
# ============================================================

e_eid.bind(
    "<KeyRelease>",
    validate_employee_id
)

e_name.bind(
    "<KeyRelease>",
    validate_name
)

e_email.bind(
    "<KeyRelease>",
    validate_email
)

e_exp.bind(
    "<KeyRelease>",
    validate_experience
)

e_edu.bind(
    "<KeyRelease>",
    validate_education
)

e_perf.bind(
    "<KeyRelease>",
    validate_performance
)

e_skill.bind(
    "<KeyRelease>",
    validate_skill
)

e_prev.bind(
    "<KeyRelease>",
    validate_previous_salary
)


# ============================================================
# BUTTONS
# ============================================================

tk.Button(

    root,

    text="Predict Salary",

    command=submit,

    bg="blue",

    fg="white",

    font=("Arial", 11, "bold"),

    width=15

).grid(

    row=8,

    column=1,

    columnspan=2,

    pady=25
)


tk.Button(

    root,

    text="Clear",

    command=clear,

    bg="green",

    fg="white",

    font=("Arial", 11, "bold"),

    width=12

).grid(

    row=8,

    column=6,

    pady=25
)


tk.Button(

    root,

    text="Exit",

    command=exit_app,

    bg="red",

    fg="white",

    font=("Arial", 11, "bold"),

    width=12

).grid(

    row=8,

    column=7,

    pady=25
)


# ============================================================
# PREDICTED RESULT
# ============================================================

tk.Label(

    root,

    text="Predicted Result",

    font=("Arial", 14, "bold")
).grid(

    row=10,

    column=0,

    columnspan=10,

    pady=10
)


# ============================================================
# PREDICTION OUTPUT
# ============================================================

out_pred = tk.Label(

    root,

    text="Prediction:",

    font=("Arial", 12),

    anchor="center"
)

out_pred.grid(

    row=11,

    column=0,

    columnspan=10,

    pady=5
)


# ============================================================
# RISK OUTPUT
# ============================================================

out_risk = tk.Label(

    root,

    text="Retention Risk:",

    font=("Arial", 12),

    anchor="center"
)

out_risk.grid(

    row=12,

    column=0,

    columnspan=10,

    pady=5
)


# ============================================================
# AI RECOMMENDATION OUTPUT
# ============================================================

out_rec = tk.Label(

    root,

    text="AI Recommendation:",

    font=("Arial", 12),

    wraplength=1100,

    justify="left"
)

out_rec.grid(

    row=13,

    column=0,

    columnspan=10,

    pady=15
)


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()