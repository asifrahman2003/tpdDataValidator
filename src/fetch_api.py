"""
    @author: Asifur Rahman
    @program: fetch_api.py
    @description: 
        This program simulates fetching incident report data from an external API by 
        reading structured JSON from a local file. This serves as the 
        ingestion step of a data engineering pipeline, mimicking a real-world
        data retrieval scenario from RESTful endpoints or external data feeds.
"""

# required libraries for the program to work
import json
import os

def fetch_incident_data():
    # load the JSON data as if fetched from an API
    file_path = os.path.join(os.path.dirname(__file__), "../data/sampleIncidentData.json")
    with open(file_path, "r") as file:
        data = json.load(file)

    return data

# testing program
if __name__ == "__main__":
    incidents = fetch_incident_data()
    print(f"Fetched {len(incidents)} incident reports: ")

    for incident in incidents:
        print(f" - {incident["incident_id"]}: {incident["status"]}")