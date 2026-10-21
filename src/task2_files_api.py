"""Task 2: CSV/JSON file I/O, API calls, and environment variables."""
import csv
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
load_dotenv(ROOT / ".env")


def read_csv_rows(path):
    with open(path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def main():
    employees = read_csv_rows(DATA / "employees.csv")
    for row in employees:
        row["id"] = int(row["id"])
        row["salary"] = int(row["salary"])

    with open(DATA / "employees.json", "w", encoding="utf-8") as file:
        json.dump(employees, file, indent=2)

    high_earners = [row for row in employees if row["salary"] > 50000]
    with open(DATA / "high_earners.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=employees[0].keys())
        writer.writeheader()
        writer.writerows(high_earners)
    print(f"Rows read: {len(employees)} | High earners: {len(high_earners)}")

    api_key = os.getenv("API_KEY")
    # JSONPlaceholder is a public demo API; it does not require API_KEY.
    if api_key:
        print("API_KEY loaded from .env (value intentionally not displayed).")
    else:
        print("No API_KEY set; JSONPlaceholder demo request can still run.")

    try:
        response = requests.get(
            "https://jsonplaceholder.typicode.com/users", timeout=5
        )
        response.raise_for_status()
        users = response.json()
        for user in users[:3]:
            print(f'{user.get("id")} - {user.get("name")} - {user.get("email")}')

        # Parse nested JSON safely with .get()
        simplified = [
            {
                "id": user.get("id"),
                "name": user.get("name"),
                "city": user.get("address", {}).get("city"),
                "company": user.get("company", {}).get("name"),
            }
            for user in users
        ]
        with open(DATA / "users.json", "w", encoding="utf-8") as file:
            json.dump(simplified, file, indent=2)

    except requests.exceptions.Timeout:
        print("API request timed out.")
    except requests.exceptions.ConnectionError:
        print("Could not connect to the API.")
    except requests.exceptions.HTTPError as exc:
        print(f"API returned an HTTP error: {exc}")
    except requests.exceptions.RequestException as exc:
        print(f"API request failed: {exc}")

    try:
        missing = requests.get(
            "https://jsonplaceholder.typicode.com/users/9999", timeout=5
        )
        if missing.status_code == 404:
            print("/users/9999 -> 404 Not found")
        else:
            missing.raise_for_status()
            print("Unexpected response:", missing.status_code)
    except requests.exceptions.Timeout:
        print("404 test timed out.")
    except requests.exceptions.ConnectionError:
        print("404 test could not connect.")
    except requests.exceptions.RequestException as exc:
        print(f"404 test request failed: {exc}")


if __name__ == "__main__":
    main()
