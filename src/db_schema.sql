-- This will help to reset the table during development
DROP TABLE IF EXISTS incidents;

-- Creates the incidents table to store the valid police report data
CREATE TABLE incidents (
    -- Auto-increment primary key; helpful for easier query
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- external incident ID (like "TPD1001"); must be unique and not null
    incident_id TEXT UNIQUE NOT NULL,

    -- Officer who submitted the report (example "OF204")
    officer_id TEXT NOT NULL,

    -- Department name (example "Cybercrime", "Narcotics"), must be present and not NULL
    department TEXT NOT NULL,

    -- Date of the incident, stored as TEXT in YYYY-MM-DD format
    date TEXT NOT NULL,

    -- Where the incident happend (example "Downtown Tucson")
    location TEXT NOT NULL,

    -- Status of the case. Only 3 allowed values for data integrity
    status TEXT CHECK(status IN ('Open', 'Closed', 'Investigating')) NOT NULL,

    -- the full report in TEXT (can be long enough), but must be not NULL
    report TEXT NOT NULL
)