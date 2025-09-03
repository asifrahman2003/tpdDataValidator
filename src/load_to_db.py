"""
    @author: Asifur Rahman
    @program: load_to_db.py
    @description: 
        This program connects to the SQLite database (tpd_incidents.db), initializes the schema 
        from a SQL file, and inserts validated incident records into the database. 
        This script represents the transformation and loading (T & L) stages of 
        an ETL (Extract, Transform and Load) pipeline, ensuring only clean and structurally valid data is stored.
"""

# required libraries to make the program work
import sqlite3
import os
from validate_data import validate_incidents
from fetch_api import fetch_incident_data

# connect to the actual database file; created if it doesn't exist
db_path = os.path.join(os.path.dirname(__file__), "../tpd_incidents.db")
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# load and run the SQL schema to create the incidents table
schema_path = os.path.join(os.path.dirname(__file__), "db_schema.sql")
with open(schema_path, "r") as f: 
    schema_sql = f.read()

# execute all SQL statements in the file (DROP TABLE + CREATE TABLE)
cursor.executescript(schema_sql)
print("Database schema created.")

# load and validate the raw data from simulated JSON file (in real case we do it using RESTAPI)
raw_data = fetch_incident_data()
valid_data, _ = validate_incidents(raw_data)

# defining the SQL insert statement
insert_query = """
                    INSERT INTO incidents (
                    incident_id, officer_id, department, date, location, status, report
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """

# insert each valid incident into the database
for incident in valid_data:
    try:
        cursor.execute(insert_query, (
            incident["incident_id"],
            incident["officer_id"],
            incident["department"],
            incident["date"],
            incident["location"],
            incident["status"],
            incident["report"],
        ))
    except sqlite3.IntegrityError as e:
        # if a duplicate or constraint issue occurs, skip it
        print(f"Skipping incident {incident['incident_id']}: {e}")

# save changes and close the database
connection.commit()
connection.close()

print(f"Loaded {len(valid_data)} valid incidents(s) into the database.")