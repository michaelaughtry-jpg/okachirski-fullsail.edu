# IoT Traffic Analysis

**Advanced Software Engineering — Michael Aughtry**

Documentation for Milestones 1, 2 & 3.

This Python command-line app reads traffic records from CSV, flags
Telnet services or traffic over 500 bytes, and stores the results in SQLite.
Milestone 3 adds a menu to view totals, review records, export CSV files,
and generate two bar charts.

## Development Milestones

| Milestone | Implemented work |
| --- | --- |
| 1 | Read the sample CSV and print its rows using `Milestone.py`. |
| 2 | Parse fields, calculate total bytes, apply classification rules and save results in SQLite using `Milestone2.py` and `traffic.py`. |
| 3 | Review saved records through a text menu, show totals, export CSV files and generate protocol and result charts using `Milestone3.py`. |

## Files

- `Milestone.py`: Original CSV reader that prints the rows without saving them.
- `Milestone2.py`: Imports and classifies the CSV records, then saves them.
- `traffic.py`: Contains the total-byte and high-traffic functions.
- `Milestone3.py`: Displays the reporting menu.
- `IoT - 23 Import.csv`: Sample input with protocol, service, orig_bytes and resp_bytes columns.
- `traffic.db`: SQLite database containing the saved traffic records.
- `BUILD.bat`: Builds the Windows executable using PyInstaller.
- `RUN.bat`: Runs the Windows executable and keeps the window open afterward.

## Run with Python

Install Python 3. The application uses Python's standard library; no additional
packages are needed to run the source code.

Keep the Python files and sample CSV together. Open PowerShell in that folder.

To run the original Milestone 1 CSV reader:

```powershell
py Milestone.py
```

This prints the CSV rows, including the header, and does not create a database.
It is optional when using the completed project.

For Milestone 2, if you do not already have saved records, run the importer once:

```powershell
py Milestone2.py
```

Running the importer again adds another copy of the records. If your
`traffic.db` already has the intended data, skip the import step.

For Milestone 3, start the reporting menu:

```powershell
py Milestone3.py
```

## Menu

| Choice | Action |
| --- | --- |
| 1 | Show total records, total bytes, and totals by protocol and result. |
| 2 | Show each record, including its service, classification and reason. |
| 3 | Save `results.csv` and `summary.csv`. |
| 4 | Create `protocol_chart.svg` and `result_chart.svg`. |
| 0 | Exit. |

Open the SVG charts in Edge or Chrome. Open the CSV exports in Excel or a text
editor. Reports are saved beside the reporting script or executable.
Exporting again replaces the previous report files.

The report reads all saved records once when it starts. Restart it after a new
import to refresh the data. Viewing reports does not add database records.

## CSV Input

The importer expects a file named `IoT - 23 Import.csv` in the current folder,
with these exact column names:

```csv
protocol,service,orig_bytes,resp_bytes
tcp,http,1200,3400
udp,dns,60,100
tcp,telnet,400,500
```

`orig_bytes` and `resp_bytes` must contain whole numbers that Python can convert
with `int()`. Missing columns or nonnumeric byte fields cause the importer to
stop. This version does not reject invalid rows individually.

## SQLite Storage

Milestone 2 creates `traffic.db` if needed and inserts one row per CSV record
into the `traffic` table. Changes are committed after the import loop.

| Column | Saved value |
| --- | --- |
| `protocol` | Protocol from the CSV, such as TCP or UDP. |
| `service` | Service from the CSV, such as Telnet or DNS. |
| `sum` | Sent bytes plus received bytes. |
| `result` | `flagged` or `not flagged`. |
| `reason` | Explanation for the classification. |

Open `traffic.db` in DB Browser for SQLite, choose **Browse Data**, and select
`traffic` to inspect the stored rows. Keep a backup before changing the database.

## Classification Rules

- A Telnet service is flagged with the reason `telnet service`.
- Otherwise, sent bytes plus received bytes greater than 500 are flagged as `high traffic`.
- Exactly 500 bytes or fewer are `not flagged`, with the reason `low traffic`.
- The Telnet rule takes precedence when both conditions match.

These are simple review rules. A flagged record is not proof of an attack.

## Run the Windows Application

Extract `IoTTrafficDashboard-Windows.zip`. Keep these files together:

- `IoTTrafficDashboard.exe`
- `traffic.db`
- `RUN.bat`

Double-click `RUN.bat`, then choose a menu option. Python is not required to run
the packaged executable. Keep the extracted folder somewhere you can save
reports, such as Documents.

## Build on Windows

Python and internet access are needed for the build. Keep `BUILD.bat`,
`RUN.bat`, `Milestone3.py` and `traffic.db` in the same project folder.
Double-click `BUILD.bat`. It installs PyInstaller into a local virtual
environment, packages the report application, and creates a release ZIP.

To rebuild after that environment has been created, run:

```powershell
.\.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm --onefile --console --name IoTTrafficDashboard Milestone3.py
```

The executable is created in `dist`. The build script also copies it and the
database into `release` and creates `IoTTrafficDashboard-Windows.zip`.
Run the release application and check every menu option before submitting it.
The executable runs the reporting feature; the CSV importer remains a Python script.

## Troubleshooting

- **Database cannot be opened:** Keep `traffic.db` beside `Milestone3.py` or the executable.
- **No records:** Import the CSV once using `Milestone2.py`.
- **CSV not found:** Run the importer from the folder containing the sample CSV.
- **Reports cannot be saved:** Use a folder where you have write permission. Close an export in Excel before replacing it.
- **Build fails:** Keep the error message and check that Python is installed and internet access is available.

## Check the Sample Results

For a fresh import of the included 10-record sample, the reports should show:

- 10 records and 7,068 total bytes.
- 6 TCP records and 4 UDP records.
- 3 flagged records and 7 records not flagged.

Compare both charts and CSV exports with the displayed summary. Counts will
increase if the CSV has been imported more than once. Opening Milestone 3 alone
does not add records.

## Current Limitations

Reports combine all saved records. This version does not select individual
imports or classification runs. Duplicate import prevention, saved rule settings,
run status/version tracking and complete missing-input handling are not implemented.
The importer expects the supplied four-column CSV format rather than raw Zeek logs.

## GitHub

Use the class-provided GitHub Classroom repository. Commit source files, sample
input and documentation with descriptive messages. Ignore `.venv`, `__pycache__`,
`build`, `dist`, release files and generated databases in source control.
Include the database separately with the Windows binary so the reports have data.
