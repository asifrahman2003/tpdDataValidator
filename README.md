# TPD Data Validator & Reporting Pipeline

> Author: **Asifur Rahman**  
> Internship Target: **Data Engineer Intern – Tucson Police Department (TPD)**  
> Status: Completed (Mock Data, SQLite Backend, Report Generation)

## Project Overview

This project simulates a real-world **data engineering pipeline** tailored for a public safety context like the Tucson Police Department. It demonstrates how incoming incident report data can be:

- Ingested (from a simulated API)
- Validated for data integrity and consistency
- Stored in a relational database
- Queried to generate actionable summary reports

This modular pipeline follows a simplified **ETL (Extract–Transform–Load)** structure and can be easily extended to integrate **real-world datasets**, **dashboard interfaces**, or **cloud storage solutions**.

## Tech Stack

```
| Tool        | Purpose                            |
|-------------|------------------------------------|
| Python      | Core scripting language            |
| SQLite3     | Lightweight relational database    |
| JSON        | Simulated API data format          |
| SQL         | Schema + analytics queries         |
| Git / GitHub| Version control and documentation  |
```

## Project Structure
```
tpd-data-validator/
├── data/
│ └── sampleIncidentData.json   # Simulated API response
├── src/
│ ├── fetch_api.py              # Ingest data (mimic API call)
│ ├── validate_data.py          # Data cleaning + validation logic
│ ├── db_schema.sql             # SQL schema (DROP + CREATE TABLE)
│ ├── load_to_db.py             # Load validated data into DB
│ ├── generate_report.py        # Analytics reporting (SQL queries)
│ └── test_db.py                # Standalone SQLite schema test
├── tpd_incidents.db            # Generated SQLite database (after running)
├── requirements.txt            # Python dependencies (minimal)
├── .gitignore                  # Ignores venv/ and .db files
└── README.md                   # You’re here!
```

## Features

### `fetch_api.py`
Simulates fetching incident reports from an external REST API by loading structured JSON.

### `validate_data.py`
Performs integrity checks including:
- Missing fields
- Invalid date formats
- Allowed status values (`Open`, `Closed`, `Investigating`)

### `db_schema.sql`
Defines a normalized SQL table with:
- Type constraints
- Uniqueness
- CHECK constraints for valid status fields

### `load_to_db.py`
Loads only validated records into the SQLite database and skips duplicates or invalid entries.

### `generate_report.py`
Connects to the database and generates summary analytics like:
- Incidents by status
- Department-wise breakdown
- 3 most recent reports

## Example Report Output
```
Generating reports from incidents database...

Incidents by status:
 - Investigating: 1
 - Open: 1

 Incidents by Department:
 - Narcotics: 1
 - Cybercrime: 1

 Most Recent Incidents:
 - [2025-09-01] TPD1001 (Narcotics) -> Open
 - [2025-08-30] TPD1003 (Cybercrime) -> Investigating

 Report generation complete.
```

## How to Run

### 1. Clone this repo

```
git clone https://github.com/asifrahman2003/tpdDataValidator.git
cd tpdDataValidator
```
### 2. Create and activate virtual environment
```
python3 -m venv venv
source venv/bin/activate         # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the pipeline
```
python src/load_to_db.py         # Creates DB and loads validated data
python src/generate_report.py    # Generates analytics from DB
```

## Potential Future Upgrades
- Replace static JSON with live data from open APIs (for example, data.tucsonaz.gov)
- Export reports to .csv or .json
- Add a Streamlit dashboard UI
- Extend database with officer metadata, response times, crime types

## Learning Outcomes
This project demonstrates:
- Designing and validating a real-world data schema
- Witing clean, modular Python code
- Building a local ETL-style data pipeline
- Using SQL for analytical reporting
- Structuring a GitHub project for clarity and interview-readiness

## Contact

Feel free to reach out or explore more projects at:
```
- www.iamasiff.com
- asifrahman@arizona.edu
```

## License
> This project is licensed under MIT Open Licensing. ⓒ 2025 Asifur Rahman. 