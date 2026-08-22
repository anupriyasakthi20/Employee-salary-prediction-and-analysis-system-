# Employee Salary Prediction and Analysis System
# Day 1 Prototype

print("==============================================")
print("  EMPLOYEE SALARY PREDICTION AND ANALYSIS SYSTEM")
print("==============================================")

# Get employee details
employee_name = input("Enter Employee Name: ")

experience = float(input("Enter Years of Experience: "))

education_level = float(input("Enter Education Level Score (%): "))

performance_rating = float(input("Enter Performance Rating (%): "))

skill_score = float(
    input("Enter Skill/Certification Score (%): ")
)

previous_salary_percentile = float(
    input("Enter Previous Salary Percentile (%): ")
)

# Convert experience into a score
experience_score = min((experience / 20) * 100, 100)

# Calculate salary score
salary_score = (
    experience_score * 0.25
    + education_level * 0.20
    + performance_rating * 0.30
    + skill_score * 0.15
    + previous_salary_percentile * 0.10
)

# Determine salary category
if salary_score >= 80:
    salary_category = "VERY HIGH"

elif salary_score >= 65:
    salary_category = "HIGH"

elif salary_score >= 50:
    salary_category = "MEDIUM"

else:
    salary_category = "LOW"

# Generate recommendation
if salary_category == "VERY HIGH":
    recommendation = (
        "Excellent profile. Consider for leadership track and "
        "a retention bonus to prevent poaching."
    )

elif salary_category == "HIGH":
    recommendation = (
        "Strong performer. Eligible for a merit-based increment."
    )

elif salary_category == "MEDIUM":
    recommendation = (
        "Moderate salary band. Recommend skill development "
        "programs and periodic performance review."
    )

else:
    recommendation = (
        "Below-market compensation indicated. Recommend training, "
        "mentorship, and a compensation review to reduce attrition risk."
    )

# Display result
print("\n==============================================")
print("          EMPLOYEE SALARY RESULT")
print("==============================================")

print("Employee Name:", employee_name)
print("Salary Score:", round(salary_score, 2))
print("Salary Category:", salary_category)
print("Recommendation:", recommendation)

print("==============================================")
