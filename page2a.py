import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Employee Salary Prediction and Analysis System")
root.geometry("900x650")


def submit():
    employee_id = entry_employee_id.get()
    name = entry_name.get()
    experience = entry_experience.get()
    education_level = entry_education_level.get()
    performance_rating = entry_performance_rating.get()
    skill_score = entry_skill_score.get()
    previous_salary_percentile = entry_previous_salary_percentile.get()

    if not employee_id or not name or not experience or not education_level or not performance_rating or not skill_score or not previous_salary_percentile:
        messagebox.showerror("Error", "Please enter all employee details.")
        return

    try:
        experience = float(experience)
        education_level = float(education_level)
        performance_rating = float(performance_rating)
        skill_score = float(skill_score)
        previous_salary_percentile = float(previous_salary_percentile)

        if not (0 <= experience <= 40):
            messagebox.showerror("Error", "Experience must be between 0 and 40 years.")
            return

        if not (0 <= education_level <= 100):
            messagebox.showerror("Error", "Education Level must be between 0 and 100.")
            return

        if not (0 <= performance_rating <= 100):
            messagebox.showerror("Error", "Performance Rating must be between 0 and 100.")
            return

        if not (0 <= skill_score <= 100):
            messagebox.showerror("Error", "Skill Score must be between 0 and 100.")
            return

        if not (0 <= previous_salary_percentile <= 100):
            messagebox.showerror("Error", "Previous Salary Percentile must be between 0 and 100.")
            return

        experience_score = min((experience / 20) * 100, 100)

        salary_score = (
            experience_score * 0.25
            + education_level * 0.20
            + performance_rating * 0.30
            + skill_score * 0.15
        )

        final_score = (
            salary_score * 0.90
            + previous_salary_percentile * 0.10
        )

        if final_score >= 40:
            category = "VERY HIGH"
            risk = "LOW"
            recommendation = "Maintain competitive pay and offer growth opportunities."

        elif final_score >= 15:
            category = "HIGH"
            risk = "LOW"
            recommendation = "Eligible for a merit-based increment; monitor market benchmarks."

        elif final_score >= 10:
            category = "MEDIUM"
            risk = "MEDIUM"
            recommendation = "Suggest skill development programs and periodic performance review."

        else:
            category = "LOW"
            risk = "HIGH"
            recommendation = "Recommend training, mentorship, and a compensation review."

        output_prediction.config(
            text=f"Prediction: {category}\nSalary Score: {final_score:.2f}"
        )

        output_risk.config(
            text=f"Retention Risk: {risk}"
        )

        output_recommendation.config(
            text=f"Recommendation: {recommendation}"
        )

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")


def clear():
    entry_employee_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_experience.delete(0, tk.END)
    entry_education_level.delete(0, tk.END)
    entry_performance_rating.delete(0, tk.END)
    entry_skill_score.delete(0, tk.END)
    entry_previous_salary_percentile.delete(0, tk.END)

    output_prediction.config(text="Prediction:")
    output_risk.config(text="Retention Risk:")
    output_recommendation.config(text="Recommendation:")


def exit_app():
    root.destroy()


# Heading1
heading1 = tk.Label(
    root,
    text="EMPLOYEE SALARY PREDICTION AND ANALYSIS SYSTEM",
    font=("Arial", 22, "bold")
)
heading1.grid(row=0, column=0, columnspan=8, pady=20)


# Heading2
heading2 = tk.Label(
    root,
    text="Employee Information",
    font=("Arial", 14, "bold")
)
heading2.grid(row=1, column=1, columnspan=4, pady=10)


# Employee ID
tk.Label(
    root,
    text="Employee ID",
    font=("Arial", 12)
).grid(row=2, column=1, padx=10, pady=5, sticky="w")

entry_employee_id = tk.Entry(root, width=30)
entry_employee_id.grid(row=2, column=2, padx=10, pady=5)


# Name
tk.Label(
    root,
    text="Name",
    font=("Arial", 12)
).grid(row=3, column=1, padx=10, pady=5, sticky="w")

entry_name = tk.Entry(root, width=30)
entry_name.grid(row=3, column=2, padx=10, pady=5)


# Professional Information
heading3 = tk.Label(
    root,
    text="Professional Information",
    font=("Arial", 14, "bold")
)
heading3.grid(row=1, column=6, columnspan=4, pady=10)


# Experience
tk.Label(
    root,
    text="Experience (Years)",
    font=("Arial", 12)
).grid(row=2, column=6, padx=10, pady=5, sticky="w")

entry_experience = tk.Entry(root, width=30)
entry_experience.grid(row=2, column=7, padx=10, pady=5)


# Education Level
tk.Label(
    root,
    text="Education Level",
    font=("Arial", 12)
).grid(row=3, column=6, padx=10, pady=5, sticky="w")

entry_education_level = tk.Entry(root, width=30)
entry_education_level.grid(row=3, column=7, padx=10, pady=5)


# Performance Rating
tk.Label(
    root,
    text="Performance Rating",
    font=("Arial", 12)
).grid(row=4, column=6, padx=10, pady=5, sticky="w")

entry_performance_rating = tk.Entry(root, width=30)
entry_performance_rating.grid(row=4, column=7, padx=10, pady=5)


# Skill Score
tk.Label(
    root,
    text="Skill Score",
    font=("Arial", 12)
).grid(row=5, column=6, padx=10, pady=5, sticky="w")

entry_skill_score = tk.Entry(root, width=30)
entry_skill_score.grid(row=5, column=7, padx=10, pady=5)


# Previous Salary Percentile
tk.Label(
    root,
    text="Previous Salary Percentile",
    font=("Arial", 12)
).grid(row=6, column=6, padx=10, pady=5, sticky="w")

entry_previous_salary_percentile = tk.Entry(root, width=30)
entry_previous_salary_percentile.grid(row=6, column=7, padx=10, pady=5)


# Buttons
submit_btn = tk.Button(
    root,
    text="Predict Salary",
    command=submit,
    bg="blue",
    fg="white",
    font=("Arial", 11, "bold")
)
submit_btn.grid(row=8, column=1, columnspan=2, pady=20)


clear_btn = tk.Button(
    root,
    text="Clear",
    command=clear,
    bg="green",
    fg="white",
    font=("Arial", 11, "bold")
)
clear_btn.grid(row=8, column=6, columnspan=1, pady=20)


exit_btn = tk.Button(
    root,
    text="Exit",
    command=exit_app,
    bg="red",
    fg="white",
    font=("Arial", 11, "bold")
)
exit_btn.grid(row=8, column=7, columnspan=1, pady=20)


# Predicted Result
heading4 = tk.Label(
    root,
    text="Predicted Result",
    font=("Arial", 14, "bold")
)
heading4.grid(row=10, column=0, columnspan=8, pady=10)


# Output
output_prediction = tk.Label(
    root,
    text="Prediction:",
    font=("Arial", 12),
    fg="black",
    justify="left"
)
output_prediction.grid(row=11, column=0, columnspan=8, pady=5)


output_risk = tk.Label(
    root,
    text="Retention Risk:",
    font=("Arial", 12),
    fg="black",
    justify="left"
)
output_risk.grid(row=12, column=0, columnspan=8, pady=5)


output_recommendation = tk.Label(
    root,
    text="Recommendation:",
    font=("Arial", 12),
    fg="black",
    justify="left",
    wraplength=800
)
output_recommendation.grid(row=13, column=0, columnspan=8, pady=5)


root.mainloop()
