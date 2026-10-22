# IoT Traffic Analysis

**Michael Aughtry — Advanced Software Engineering**

Documentation for Milestones 1, 2 and 3.

This Python command-line application reads CSV traffic records, flags Telnet
services or traffic over 500 bytes, and saves the results in SQLite. It also
shows totals and record details, exports CSV reports, and creates two bar charts.

## Milestones

| Milestone | Features |
| --- | --- |
| 1 | Read the sample CSV and display its rows. |
| 2 | Parse traffic fields, calculate total bytes, classify records and save results in SQLite. |
| 3 | Display totals and records, export CSV reports and create protocol and result charts. |

## Files

- `App.py`: Combined menu for all three milestones.
- `traffic.py`: Functions for adding bytes and checking the 500-byte threshold.
- `Milestone.py`: Original CSV reader.
- `Milestone2.py`: Original import, classification and storage script.
- `Milestone3.py`: Original reporting menu.
- `IoT - 23 Import.csv`: Sample input file.
- `traffic.db`: Database containing saved traffic records.

## Setup and run

Install Python 3. The application uses Python's standard library, so no extra
packages are required.

Extract the project folder. Keep `App.py`, `traffic.py` and the sample CSV
together. Keep `traffic.db` there too if you already have saved records.
Open PowerShell in that folder and run:

```powershell
py App.py
```

## Combined menu

| Choice | Action |
| --- | --- |
| 1 | Choose a CSV file and display its rows, including the header. |
| 2 | Choose a CSV, classify its records and confirm saving them to SQLite. |
| 3 | Show totals and all saved records with their reasons. |
| 4 | Save `results.csv` and `summary.csv`. |
| 5 | Create `protocol_chart.svg` and `result_chart.svg`. |
| 0 | Exit. |

At the file prompt, press Enter to use `IoT - 23 Import.csv`. You can also enter
another CSV path. Relative paths are resolved from the application folder.
For option 2, type `y` to save or another answer to cancel.

If the database already contains the intended records, go straight to option 3.
Importing the same CSV again adds duplicate records. Viewing records and reports
does not add data. Reports refresh each time you select a report option.

## Original milestone scripts

The separate scripts are also available:

```powershell
py Milestone.py
py Milestone2.py
py Milestone3.py
```

Run the command for the script you want. `Milestone.py` only prints CSV rows.
`Milestone2.py` imports immediately without asking for confirmation and appends
records. `Milestone3.py` has its own four-option reporting menu and loads data
at startup. Restart that script to see later imports.

Use `App.py` for the combined menu described above.

## CSV input

The input needs these exact column names:

```csv
protocol,service,orig_bytes,resp_bytes
tcp,http,1200,3400
udp,dns,60,100
tcp,telnet,400,500
```

The combined importer requires nonnegative whole-number byte counts and all
four required columns. Invalid input stops the import before records are saved.
The original separate importer has less validation.

## Classification rules

1. A Telnet service is flagged with the reason `telnet service`.
2. Otherwise, total bytes greater than 500 are flagged as `high traffic`.
3. Other records are `not flagged`, with the reason `low traffic`.

Total bytes means `orig_bytes + resp_bytes`. Exactly 500 bytes alone does not
flag a record. Telnet takes precedence when both rules match.
These are simple review rules; a flagged record is not proof of an attack.

## SQLite storage

Importing creates `traffic.db` if needed. The `traffic` table stores:

| Column | Contents |
| --- | --- |
| `protocol` | Protocol such as TCP or UDP. |
| `service` | Service such as Telnet, HTTP or DNS. |
| `sum` | Total sent and received bytes. |
| `result` | `flagged` or `not flagged`. |
| `reason` | Explanation for the classification. |

The combined importer commits the records together and rolls back its inserts
if a database write fails. Open `traffic.db` in DB Browser for SQLite, select
**Browse Data**, then choose `traffic` to inspect the records.

## Reports

`results.csv` contains the saved record details. `summary.csv` contains counts
and byte totals by protocol and classification, plus overall totals.

The two SVG charts display record counts by protocol and classification. Open
them in Edge or Chrome. Open CSV reports in Excel or a text editor.

Reports are saved in the application folder. Generating them again replaces
previous report files. Reports include all saved records.

For one fresh import of the included sample, expect:

- 10 records and 7,068 total bytes.
- 6 TCP records and 4 UDP records.
- 3 flagged records and 7 records not flagged.

## Troubleshooting

- **Python command fails:** Check that Python 3 is installed.
- **CSV not found:** Check the filename or enter the full path.
- **Database missing:** Use option 2 to import records and create it.
- **No records:** Import a CSV before viewing reports.
- **Reports cannot be saved:** Use a folder where you have write permission and close exported files in Excel before replacing them.
- **Counts are too high:** Check whether the same CSV was imported more than once.

## Current limitations

Reports combine all saved records. Automatic duplicate-source prevention, saved
rule settings, classification run history and individual run selection are not
implemented. The input is the four-column CSV format, not raw Zeek logs.

## GitHub

Use the class-provided GitHub Classroom repository. Commit source files, sample
input and this README with descriptive commit messages. Ignore local virtual
environments, `__pycache__`, generated databases and report files in source
control. Keep a backup of your working database outside the repository.
