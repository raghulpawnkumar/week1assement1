"""Task 3: NumPy, Pandas cleaning/aggregation/joins, and Matplotlib charts."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORTS = ROOT / "reports"


def numpy_demo():
    marks = np.array([
        [78, 85, 90],
        [66, 72, 70],
        [91, 88, 95],
        [55, 63, 60],
    ])
    print("Marks shape:", marks.shape)
    print("Student averages:", marks.mean(axis=1))
    print("Subject averages:", marks.mean(axis=0))
    with_grace = marks + 5  # broadcasting adds 5 to every mark
    print("With grace marks:\n", with_grace)
    weights = np.array([0.3, 0.3, 0.4])
    print("Weighted scores:", np.dot(marks, weights))


def load_and_clean():
    employees = pd.read_csv(DATA / "employees.csv")
    print("\n--- info ---")
    employees.info()
    print("\n--- describe ---\n", employees.describe(include="all"))
    print("\nloc sample:\n", employees.loc[employees["city"] == "Chennai"])
    print("\niloc sample:\n", employees.iloc[:3])
    print("\nSalary > 50000:\n", employees[employees["salary"] > 50000])

    # Demonstrate cleaning: make 2 salary values missing and append a duplicate.
    dirty = employees.copy()
    dirty.loc[0, "salary"] = np.nan
    dirty.loc[1, "salary"] = np.nan
    dirty = pd.concat([dirty, dirty.iloc[[2]]], ignore_index=True)
    print("\nDirty rows and duplicate introduced:", len(dirty))
    dirty["salary"] = pd.to_numeric(dirty["salary"], errors="coerce")
    median_salary = dirty["salary"].median()
    dirty["salary"] = dirty["salary"].fillna(median_salary)
    dirty = dirty.drop_duplicates()
    dirty["id"] = dirty["id"].astype(int)
    dirty["salary"] = dirty["salary"].round().astype(int)
    dirty.to_csv(DATA / "employees_cleaned.csv", index=False)
    print("Cleaned rows:", len(dirty), "| median used:", median_salary)
    return employees, dirty


def summarize_and_merge(employees):
    departments = pd.read_csv(DATA / "departments.csv")
    summary = employees.groupby("department").agg(
        headcount=("id", "count"),
        average_salary=("salary", "mean"),
        maximum_salary=("salary", "max"),
    ).reset_index()
    summary.to_csv(REPORTS / "department_summary.csv", index=False)
    print("\nDepartment summary:\n", summary)

    for how in ["inner", "left", "outer"]:
        merged = summary.merge(departments, on="department", how=how, indicator=True)
        print(f"\n{how.title()} join:\n", merged)
        merged.to_csv(REPORTS / f"{how}_join.csv", index=False)

    no_employees = departments[~departments["department"].isin(employees["department"])]
    print("\nDepartments with no employees:", no_employees["department"].tolist())


def make_charts(employees):
    REPORTS.mkdir(exist_ok=True)
    # 1. Bar: average salary by department
    avg = employees.groupby("department")["salary"].mean()
    ax = avg.plot(kind="bar", title="Average Salary by Department", legend=True)
    ax.set_xlabel("Department")
    ax.set_ylabel("Average salary")
    plt.tight_layout()
    plt.savefig(REPORTS / "bar_average_salary.png")
    plt.close()

    # 2. Histogram: salary distribution
    plt.figure()
    plt.hist(employees["salary"], bins=5, label="Employees")
    plt.title("Employee Salary Distribution")
    plt.xlabel("Salary")
    plt.ylabel("Number of employees")
    plt.legend()
    plt.tight_layout()
    plt.savefig(REPORTS / "histogram_salary.png")
    plt.close()

    # 3. Scatter: salary vs employee ID
    plt.figure()
    plt.scatter(employees["id"], employees["salary"], label="Employees")
    plt.title("Salary vs Employee ID")
    plt.xlabel("Employee ID")
    plt.ylabel("Salary")
    plt.legend()
    plt.tight_layout()
    plt.savefig(REPORTS / "scatter_salary_id.png")
    plt.close()

    # 4. Line: salary by employee ID
    ordered = employees.sort_values("id")
    plt.figure()
    plt.plot(ordered["id"], ordered["salary"], marker="o", label="Salary")
    plt.title("Salary by Employee ID")
    plt.xlabel("Employee ID")
    plt.ylabel("Salary")
    plt.legend()
    plt.tight_layout()
    plt.savefig(REPORTS / "line_salary_id.png")
    plt.close()

    insights = """# Chart insights

- **Bar chart:** IT has the highest average salary among the listed departments.
- **Histogram:** Salaries are spread across several ranges, with most employees between 30,000 and 75,000.
- **Scatter plot:** The points show each employee's salary against their ID; ID alone does not imply a cause of salary differences.
- **Line chart:** The line connects salaries in employee-ID order and highlights variation between consecutive records.
"""
    (REPORTS / "chart_insights.md").write_text(insights, encoding="utf-8")


def main():
    numpy_demo()
    employees, _ = load_and_clean()
    summarize_and_merge(employees)
    make_charts(employees)
    print("\nCharts saved in reports/.")


if __name__ == "__main__":
    main()
