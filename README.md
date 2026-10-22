# IoT Traffic Analysis

**Michael Aughtry — Advanced Software Engineering**

This Python command-line project reads traffic records from CSV, applies simple
classification rules, and stores the results in SQLite. It also displays saved
records and totals, exports CSV reports, and creates two bar charts.

## Milestones

| Milestone | Functionality |
| --- | --- |
| 1 | Read the sample CSV and print its rows. |
| 2 | Parse traffic fields, add byte counts, classify records and save results in SQLite. |
| 3 | Display totals and details, export reports and generate charts. |

## Repository files

| File | Purpose |
| --- | --- |
| `Milestone.py` | Reads and prints CSV rows, including the header. |
| `Milestone2.py` | Imports and classifies records, then saves them to SQLite. |
| `traffic.py` | Contains `total()` and `high()` for byte calculations. |
| `Milestone3.py` | Displays the reporting menu. |
| `IoT - 23 Import.csv` | Sample traffic records. |
| `traffic.db` | Included SQLite database with saved sample results. |
| `results.csv` | Exported record details. |
| `summary.csv` | Exported totals by protocol and result. |
| `protocol_chart.svg` | Bar chart of record counts by protocol. |
| `result_chart.svg` | Bar chart of record counts by classification. |

## Requirements

Install Python 3. No additional Python packages are needed; the project uses
Python's standard library. DB Browser for SQLite is optional for inspecting
the database.

Download and extract the repository, or clone it:

```powershell
git clone https://github.com/michaelaughtry-jpg/okachirski-fullsail.edu.git
cd okachirski-fullsail.edu
```

Run the commands below from the project folder in PowerShell.

## View the included results

The repository includes `traffic.db`, so you can start the reporting menu
without importing the CSV again:

```powershell
py Milestone3.py
```

| Choice | Action |
| --- | --- |
| 1 | Show total records, total bytes, and counts and bytes by protocol and result. |
| 2 | Show records with their service, byte total, classification and reason. |
| 3 | Save `results.csv` and `summary.csv`. |
| 4 | Create `protocol_chart.svg` and `result_chart.svg`. |
| 0 | Exit. |

Open SVG charts in Edge or Chrome. Open CSV exports in Excel or a text editor.
Report files are saved beside `Milestone3.py`; generating them again replaces
the previous files. Reports use all saved records loaded at startup. Restart
the script after importing new records to refresh the data.

## Milestone 1: Read the CSV

```powershell
py Milestone.py
```

This displays each CSV row, including the header. It does not save records or
change the database.

## Milestone 2: Import and classify

```powershell
py Milestone2.py
```

The script reads `IoT - 23 Import.csv`, calculates total bytes, applies the
classification rules, prints the results, and inserts them into `traffic.db`.
It creates the database and `traffic` table if needed.

**Each run appends records. Running it on the included database adds another
copy of the sample records.** Skip importing when you only want to view the
existing results.

## CSV format

The importer expects these exact column names:

```csv
protocol,service,orig_bytes,resp_bytes
tcp,http,1200,3400
udp,dns,60,100
tcp,telnet,400,500
```

Byte values must be whole numbers that Python can convert with `int()`.
Missing columns or invalid numeric values stop the importer.

## Classification rules

Total bytes are `orig_bytes + resp_bytes`.

| Condition, checked in order | Result | Reason |
| --- | --- | --- |
| Service is Telnet, ignoring surrounding spaces and letter case. | `flagged` | `telnet service` |
| Otherwise, total bytes exceed 500. | `flagged` | `high traffic` |
| Otherwise. | `not flagged` | `low traffic` |

Exactly 500 bytes does not trigger the byte rule. Telnet is flagged regardless
of byte total. These rules identify records for review; a flag is not proof
of an attack.

## SQLite table

The `traffic` table stores `protocol`, `service`, `sum`, `result`, and `reason`.
The `sum` column holds the total sent and received bytes. Milestone 2 commits
its inserts after processing the CSV and closes the connection.

To inspect the database, open `traffic.db` in DB Browser for SQLite, choose
**Browse Data**, and select `traffic`.

## Included sample results

The included database contains:

- 10 records and 7,068 total bytes.
- 6 TCP records and 4 UDP records.
- 3 flagged records and 7 records not flagged.

Importing the CSV again increases these totals. Viewing reports does not add
records to the database.

## Troubleshooting

- **CSV not found:** Run the importer from the folder containing `IoT - 23 Import.csv`.
- **Database cannot be opened:** Keep `traffic.db` beside `Milestone3.py`.
- **No records:** Run Milestone 2 to import the CSV.
- **Reports cannot be saved:** Use a writable folder and close exported CSV files in Excel before replacing them.
- **Counts are higher than expected:** Check whether the same CSV was imported more than once.

## Limitations

Reports combine all saved records. This version does not prevent duplicate
imports, save configurable rule settings, track classification runs, or select
individual imports. The importer expects the four-column CSV format rather
than raw Zeek logs and does not provide complete invalid-input handling.
