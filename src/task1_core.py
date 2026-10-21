"""Task 1: Python core, OOP, control flow, and exceptions."""

class InvalidSalaryError(Exception):
    """Raised when an employee salary is negative."""


def bonus(salary, rate=0.1, *extras, **options):
    result = salary * rate + sum(extras)
    if "cap" in options:
        result = min(result, options["cap"])
    return result


class Employee:
    def __init__(self, name, salary):
        if salary < 0:
            raise InvalidSalaryError(f"Invalid salary: {salary}")
        self.name = name
        self.salary = salary

    def annual_salary(self):
        return self.salary * 12

    def get_details(self):
        return f"{self.name}: salary={self.salary}"


class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def get_details(self):
        return f"{super().get_details()}, team_size={self.team_size}"


def run_task1():
    employees = [
        {"id": 1, "name": "Arun", "department": "Sales", "salary": 30000, "city": "Chennai"},
        {"id": 2, "name": "Priya", "department": "HR", "salary": 45000, "city": "Chennai"},
        {"id": 3, "name": "Rahul", "department": "IT", "salary": 60000, "city": "Bangalore"},
        {"id": 4, "name": "Divya", "department": "IT", "salary": 75000, "city": "Chennai"},
        {"id": 5, "name": "Karthik", "department": "Finance", "salary": 90000, "city": "Mumbai"},
        {"id": 6, "name": "Meena", "department": "Sales", "salary": 52000, "city": "Bangalore"},
        {"id": 7, "name": "Suresh", "department": "IT", "salary": 68000, "city": "Chennai"},
        {"id": 8, "name": "Anitha", "department": "HR", "salary": 48000, "city": "Mumbai"},
    ]

    print("Bonus example:", bonus(50000, 0.1, 500, 250, cap=6000))
    employee = Employee("Priya", 45000)
    manager = Manager("Divya", 75000, team_size=4)
    print(employee.get_details(), "| annual:", employee.annual_salary())
    print(manager.get_details())

    try:
        Employee("Test", -500)
    except InvalidSalaryError as exc:
        print(f"Error: {exc}")
    finally:
        print("Transaction finished")

    above_50000 = [e["name"] for e in employees if e["salary"] > 50000]
    print("Above 50000:", above_50000)

    raised = list(map(lambda e: {**e, "salary": round(e["salary"] * 1.1, 2)}, employees))
    print("10% raise example:", raised[0]["name"], raised[0]["salary"])

    chennai = list(filter(lambda e: e["city"] == "Chennai", employees))
    print("Chennai:", [e["name"] for e in chennai])

    for e in employees:
        if e["salary"] == 0:
            continue
        print("Loop salary:", e["salary"])
        if e["salary"] > 85000:
            print("Stopping after first salary above 85000")
            break


if __name__ == "__main__":
    run_task1()
