"""
    @author: Asifur Rahman
    @program: validate_data.py
    @description: 
        This program validates raw incident report data by checking for missing fields, 
        invalid formats (for example, incorrect dates), and allowed values (for example, status). 
        That said, it separates valid and invalid records, attaching error messages to the 
        invalid ones. This script represents the data quality assurance phase 
        within a typical data engineering workflow. 
"""


# import mock API data
from fetch_api import fetch_incident_data
from datetime import datetime

# define status values are valid
VALID_STATUS = {"Open", "Closed", "Investigating"}

# function to validate if date string is in correct format (YYYY-MM-DD)
def is_date_valid(date_str):
    try:
        # attempt to parse the date string
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        # if parsing fails, its not a valid date string
        return False
    
# main function to validate a list of incident records
def validate_incidents(incident_list):
    # store valid records here
    valid_incidents = []
    # store records with errors here
    invalid_incidents = []
    # track unique incident IDs to catch duplicates
    seen_ids = set()

    # loop through each incident in the list
    for incident in incident_list:
        # track any issues with this particular incident
        errors = []

        # validate incident_id: required and must be unique
        if not incident.get("incident_id"):
            errors.append("Missing incident_id.")
        elif incident["incident_id"] in seen_ids:
            errors.append("Duplicate incident_id.")
        else:
            seen_ids.add(incident["incident_id"])

        # validate department field is not empty
        if not incident.get("department"):
            errors.append("Missing department.")

        # validate date format (must be in YYYY-MM-DD)
        if not is_date_valid(incident.get("date", "")):
            errors.append("Invalid date format or value.")

        # validate that the status is one of the allowed values
        if incident.get("status") not in VALID_STATUS:
            errors.append("Invalid status value.")

        # validate that a report exists and is not null/empty
        if not incident.get("report"):
            errors.append("Missing report.")

        # categorize the record based on whether it had any errors
        if errors:
            incident["errors"] = errors     # attaches error messages to the record
            invalid_incidents.append(incident)
        else:
            valid_incidents.append(incident)

    return valid_incidents, invalid_incidents

# (for testing purposes only)
if __name__ == "__main__":
    # fetch the simulated raw data
    raw_data = fetch_incident_data()

    # run the validation
    valid, invalid = validate_incidents(raw_data)

    # output results
    print(f"\n valid incidents: {len(valid)}")
    print(f"Invalid incidents: {len(invalid)}")

    for item in invalid:
        print(f" - {item["incident_id"]} errors: {item["errors"]}")