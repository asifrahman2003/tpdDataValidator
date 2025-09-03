"""
    @author: Asifur Rahman
    @program: streamlit_app.py
    @description:
        This is a Streamlit dashboard that visualizes validated police incident reports
        stored in the tpd_incidents.db database. Displays incident counts by 
        status and department, and shows the most recent reports.
"""

# required libraries
import streamlit as st
import pandas as pd
import sqlite3
import os
import plotly.express as px

# set the title of the app
st.title("Tucson Police Department Incident Report Dashboard")
st.caption("Data Pipeline, created by Asifur Rahman")

# connecting to the SQLite database
db_path = os.path.join(os.path.dirname(__file__), "../tpd_incidents.db")
connection = sqlite3.connect(db_path)

# loading data into pandas DataFrame
df = pd.read_sql_query("SELECT * FROM incidents", connection)

# close the connection after loading for saving resources
connection.close()

# sidebar filters
departments = df["department"].unique().tolist()
selected_depts = st.sidebar.multiselect("Filter by Department", departments, default=departments)

statuses = df["status"].unique().tolist()
selected_statuses = st.sidebar.multiselect("Filter by Status", statuses, default=statuses)

# filtering data
filtered_df = df[
    df["department"].isin(selected_depts) &
    df["status"].isin(selected_statuses)
]

# summary metrics
st.subheader("Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Incidents", len(filtered_df))
col2.metric("Departments", len(filtered_df["department"].unique()))
col3.metric("Statuses", len(filtered_df["status"].unique()))

# incidents by status
st.subheader("Incidents by Status")
status_counts = filtered_df["status"].value_counts().reset_index()
status_counts.columns = ["status", "count"]
fig_status = px.pie(
    status_counts,
    names="status",
    values="count",
    title="Incidents by Status",
    color_discrete_sequence=px.colors.qualitative.Safe
)
st.plotly_chart(fig_status)

st.download_button(
    label="Download Status Report CSV",
    data=status_counts.to_csv(index=False),
    file_name="status_report.csv",
    mime="text/csv"
)

# incidents by department
st.subheader("Incidents by Department")
dept_counts = filtered_df["department"].value_counts().reset_index()
dept_counts.columns = ["department", "count"]
fig_dept = px.pie(
    dept_counts,
    names="department",
    values="count",
    title="Incidents by Department",
    hole=0.4,
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig_dept)

st.download_button(
    label="Download Department Report CSV",
    data=dept_counts.to_csv(index=False),
    file_name="department_report.csv",
    mime="text/csv"
)

# recent incidents
st.subheader("Most Recent Incidents")
recent = filtered_df.sort_values(by="date", ascending=False).head(5)
recent_table = recent[["incident_id", "date", "department", "status"]]
st.table(recent_table)

st.download_button(
    label="Download Recent Incidents CSV",
    data=recent_table.to_csv(index=False),
    file_name="recent_incidents.csv",
    mime="text/csv"
)