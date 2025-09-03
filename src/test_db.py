"""
    @author: Asifur Rahman
    @program: test_db.py
    @description: 
        This is a minimal test script to verify SQLite database functionality. 
        Here, we create a sample table with constraints (for example, CHECK on status values), 
        ensuring that the development environment supports schema creation 
        and SQL execution before running the full data pipeline. 
"""


# importing the built-in SQLite3 module to interact with SQLite databases
import sqlite3

# connect to a database file named "test.db"
# in this case if the file does not exist, SQLite will automatically create one
connection = sqlite3.connect("test.db")
# create a cursor object - this will allow us to run SQL commands
cursor = connection.cursor()

# drop the table if it already exists
# in this case its useful so we can recreate the table fresh every time
cursor.execute(
    """
        DROP TABLE IF EXISTS test;
    """
)

# create a new table named "test" with two columns
# "id" is an auto-incrementing integer primary key
# "status" is a text field that only allows values: "Open" or "Closed"
cursor.execute(
    """
        CREATE TABLE test (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT CHECK(status IN ('Open', 'Closed')) NOT NULL
        );
    """
)

# save the changes to the database file
connection.commit()

# close the connection to free up resources
connection.close()

# print success message to confirm it worked
print("Table created successfully")