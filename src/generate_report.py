"""
    @author: Asifur Rahman
    @program: generate_report.py
    @description: 
            This program connects to the tpd_incidents.db SQLite database and generates
            summary reports on police incidents, including counts by status, department-wise breakdowns,
            and most recent incidents. This simulates an analytical report-generation step
            within a real-world data engineering pipeline. 
"""

# required libraries
import sqlite3
import os
import pandas as pd
from datetime import datetime

# defining the path to existing SQLite DB file
db_path = os.path.join(os.path.dirname(__file__), "../tpd_incidents.db")

# connecting to the database
connection = sqlite3.connect(db_path)
# creating the cursor object to retrieve data from the existing DB
cursor = connection.cursor()

print("Generating reports from incidents database...\n")

"""
    Report 1: Number of incidents by status
"""
# Count of the incidents by status
print("Incidents by status:")

# query from created DB with valid data
query1 = """
SELECT status, COUNT(*) AS count
FROM incidents
GROUP BY status;
"""

for row in cursor.execute(query1):
    print(f" - {row[0]}: {row[1]}")

"""
    Report 2: Number of incidents by department
"""
# count of the incidents per department
print("\n Incidents by Department:")

# query from the created DB
query2 = """
SELECT department, COUNT(*) AS count
FROM incidents
GROUP BY department
ORDER BY count DESC;
"""
for row in cursor.execute(query2):
    print(f" - {row[0]}: {row[1]}")

"""
    Report 3: 3 Most recent incidents
"""
print("\n Most Recent Incidents:")
query3 = """
SELECT incident_id, date, department, status
FROM incidents
ORDER BY date DESC
LIMIT 3;
"""
for row in cursor.execute(query3):
    print(f" - [{row[1]}] {row[0]} ({row[2]}) -> {row[3]}")

# new functionality; exporting reports to CSV
print("\n Exporting reports to CSV")

# ensure the reports folder exists
report_dir = os.path.join(os.path.dirname(__file__), "../reports")
os.makedirs(report_dir, exist_ok=True)

# query 1: Status report
cursor.execute(query1)
status_df = pd.DataFrame(cursor.fetchall(), columns=["status", "count"])
status_df.to_csv(os.path.join(report_dir, "incidents_by_status.csv"), index=False)

# query 2: Department report
cursor.execute(query2)
dept_df = pd.DataFrame(cursor.fetchall(), columns=["department", "count"])
dept_df.to_csv(os.path.join(report_dir, "incidents_by_department.csv"), index=False)

# query 3: Recent incidents report
cursor.execute(query3)
recent_df = pd.DataFrame(cursor.fetchall(), columns=["incidents_id", "date", "department", "status"])
recent_df.to_csv(os.path.join(report_dir, "recent_incidents.csv"), index=False)

print("Reports save in /reports folder.")

# close the connection to save resources
connection.close()
print("\n Report generation complete.")