import sqlite3
import pandas as pd
import os

# Path to real-world cleaned CSV
csv_path = "/Users/asifrahman/Documents/tpdDataValidator/realWorldData/real_incidents_cleaned.csv"
db_path = os.path.join(os.path.dirname(__file__), "../tpd_incidents.db")

# Load CSV
df = pd.read_csv(csv_path)

# Connect to DB
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get highest current incident_id
cursor.execute("SELECT incident_id FROM incidents ORDER BY id DESC LIMIT 1")
last_id = cursor.fetchone()
if last_id:
    base_num = int(last_id[0].replace("TPD", ""))
else:
    base_num = 1000

# Assign new unique incident IDs
new_ids = [f"TPD{base_num + i + 1}" for i in range(len(df))]
df["incident_id"] = new_ids


# Insert query with all required fields
insert_query = """
INSERT INTO incidents (
    incident_id, officer_id, department, date, location, status, report
) VALUES (?, ?, ?, ?, ?, ?, ?)
"""

# Insert rows
for _, row in df.iterrows():
    cursor.execute(insert_query, (
        row["incident_id"],
        row["officer_id"],
        row["department"],
        row["date"],
        row["location"],
        row["status"],
        row["report"]
    ))

conn.commit()
conn.close()

print(f"Successfully inserted {len(df)} real-world incidents.")
