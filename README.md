# Week 1 Assessment — Python & Data Engineering

## Project structure
```text
week1-assessment/
├── data/
│   ├── employees.csv
│   └── departments.csv
├── notebooks/
│   └── hr_analysis.ipynb
├── reports/
├── src/
│   ├── task1_core.py
│   ├── task2_files_api.py
│   └── task3_analysis.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

## Setup (macOS/Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

JSONPlaceholder is a public demo API and does not need an API key. The `.env` example is included to demonstrate loading environment variables. Never commit a real `.env` file.

## Run each task
```bash
python src/task1_core.py
python src/task2_files_api.py
python src/task3_analysis.py
```
For the API task, ensure internet access is available. The script catches timeouts and connection errors.

## Run the notebook
```bash
jupyter notebook
```
Open `notebooks/hr_analysis.ipynb` and run cells from top to bottom. To export it to Python:
```bash
jupyter nbconvert --to script notebooks/hr_analysis.ipynb --output hr_analysis
```

## Terminal practice
Run these from the repository root:
```bash
mkdir -p data notebooks reports src
grep -n "Chennai" data/employees.csv
cp data/employees.csv data/employees_backup.csv
mv data/employees_backup.csv reports/employees_backup.csv
```
On Windows PowerShell, `mkdir` and `Select-String` can be used if `grep` is unavailable.

## Git workflow (perform this yourself on GitHub)
```bash
git init
git add .
git commit -m "Add assessment data and project structure"
git switch -c feature/analysis
git add src/task1_core.py
git commit -m "Implement Python core and OOP"
git add src/task2_files_api.py
git commit -m "Add CSV JSON and API handling"
git add src/task3_analysis.py
git commit -m "Add NumPy Pandas and chart analysis"
git add notebooks README.md requirements.txt .gitignore
git commit -m "Document setup and add analysis notebook"
git log --oneline --graph
```
Then create a GitHub repository named `week1-assessment`, push the branch, open a Pull Request, and merge it into `main`. To practise a README conflict, make different edits to the same README line on `main` and `feature/analysis`, then merge and resolve the conflict. Do not claim a PR was created or merged until you actually do it.

## Five-line findings summary
1. The dataset contains 8 employees.
2. Five employees earn more than 50,000.
3. IT has 3 employees; Sales and HR have 2 each; Finance has 1.
4. Four employees are based in Chennai.
5. Marketing has no employees in the supplied dataset.

## Chart insights
See `reports/chart_insights.md` after running Task 3. Charts are generated in `reports/`.
