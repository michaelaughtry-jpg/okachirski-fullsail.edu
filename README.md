# IoT Traffic Analysis Dashboard — Milestone 1
Michael Aughtry | October 7, 2026

Approved scope: no machine learning. This milestone implements the application foundation and first minor feature: importing Zeek IoT connection logs into SQLite. Heuristic classification is Milestone 2; graphs and polish are Milestone 3.

## Windows setup (PowerShell, Python 3.11 or newer)
Extract the ZIP, then open PowerShell in the project folder. A virtual environment avoids altering your system packages. Activation is unnecessary:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```
If Python 3.11 is not installed, install it or use `py -m venv .venv` with your available supported Python. Open the localhost URL printed by Streamlit. Stop the server with Ctrl+C.

macOS/Linux:
```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

## Demonstration
1. Upload `samples/sample_conn.log`; leave the limit at 10,000; click Import traffic. Expect 5 saved records, one history entry, and a preview.
2. Import the same file and limit again. Expect a duplicate warning and unchanged totals.
3. Upload `samples/invalid_conn.log`. Expect a negative-byte error and unchanged totals: no partial import.
4. Stop and restart Streamlit. Expect the previously saved data to remain.
5. Import the valid file with a limit of 2. This is a separate bounded import and adds 2 records. The identity is file SHA-256 plus row limit; overlapping subsets are intentionally separate imports.

## Input contract
Only uncompressed UTF-8 tab-separated Zeek logs are accepted. Required fields: ts, uid, id.orig_h, id.resp_h, proto, service, orig_bytes, resp_bytes. Additional fields, including dataset labels, are ignored. Timestamps must be finite and nonnegative; endpoints must be IP addresses. Missing service/byte values marked `-` or `(empty)` become SQL NULL. Missing UID, protocol, timestamp or endpoints reject the import. Byte counts must be nonnegative 64-bit integers. Maximum upload: 20 MiB; maximum selected records: 10,000. Only the selected prefix is validated. Larger files require a bounded excerpt. No packet capture, cloud services, trained models or live attack detection.

## Architecture
`app.py` handles upload, button actions and display. `traffic_store.py` handles validation, schema creation, duplicate detection, batched parameterized SQL inserts and database queries. SQLite data is stored in `data/traffic.db`, separate from source control. Import and connection records commit together; errors roll back the transaction. Connections are explicitly closed. No classification is implemented yet.

## GitHub submission
Follow your course GIT activity when creating the remote repository. Clone the empty repository on your own computer. Copy ONLY `.gitignore` into it first:
```sh
git add .gitignore
git commit -m "Initialize Python ignore rules"
git push
```
Then copy the remaining project files into that clone. Review and understand the code before making the next commit:
```sh
git add app.py traffic_store.py requirements.txt README.md samples docs
git commit -m "Implement validated Zeek imports and SQLite dashboard"
git push
```
Continue making genuine commits for your own fixes and development, and push daily. Do not backdate commits or present generated snapshot commits as a week of development. A remote repository has not been created or pushed by this package. Add the actual repository URL to your submission; invite the professor according to the course instructions. Do not upload real traffic logs, local databases or credentials. The sample logs are explicitly synthetic.

## Milestone submission
Use `docs/SCREENCAST.md` for the recording. Record the actual running application and your explanation. Upload an unlisted, accessible video and submit its URL plus the GitHub URL to FSO. The assignment PDF requests an application binary; the lecture exempts web apps. This Streamlit project is supplied as runnable source, not a Windows executable. If FSO still requires a file upload, use the source ZIP with setup instructions subject to the professor's web-app guidance. Check the video link and run on another computer before submission.

## Research
- Streamlit uploader: https://docs.streamlit.io/1.46.0/develop/api-reference/widgets/st.file_uploader
- Python SQLite API: https://docs.python.org/3/library/sqlite3.html
- Zeek connection logs: https://docs.zeek.org/en/current/reference/logs/conn.html
- IoT-23 dataset: https://www.stratosphereips.org/datasets-iot23

## Known limits
This is a local single-user course prototype. Only the selected prefix is imported, with all selected rows temporarily held in memory. No database migrations or failed-import history are implemented in Milestone 1. Synthetic inputs demonstrate behavior; full IoT-23 capture ingestion has not been validated. See `docs/VERIFICATION.md` for checks actually performed. Week 4 automated unit/integration test assignment remains separate.
