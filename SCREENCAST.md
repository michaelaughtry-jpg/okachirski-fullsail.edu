# Milestone 1 recording outline
Use this as speaking notes; describe work you understand and actually performed. Do not claim research, errors, or GitHub pushes that did not happen.

1. Introduction: identify yourself and IoT Traffic Analysis Dashboard. Explain the approved no-ML scope and that Milestone 1 is the import feature. Show the relevant feature/completion criteria in your high-level design document.
2. Clean setup: create a fresh virtual environment, install requirements, and launch Streamlit. Explain that Python runs the source and there is no separate compiled web-app binary. Do this in a clean extracted copy or fresh clone rather than deleting working data.
3. Live demonstration: import sample_conn.log and show 5 records, history and preview. Repeat to show duplicate handling. Import invalid_conn.log and show no partial save. Restart the app to demonstrate persistence.
4. Code walkthrough, with readable zoom: app.py page setup, uploader, limit, button, success/error messages and saved-record display; traffic_store.py constants, connection closing, schema and foreign key, parser/header checks, numeric/IP checks, missing values, SHA-256 identity, transaction and 500-row batches, dashboard queries. Explain why placeholders are used in SQL and why the database is ignored by Git.
5. GitHub: show your actual repository and descriptive commits. Confirm raw data and databases are not tracked. Show the README and installation steps.
6. Research and hurdles: explain documented Zeek tab headers, unset byte values, transaction rollback and Streamlit reruns. Discuss any problems you actually encountered. State that synthetic validation has been performed; do not claim a real IoT-23 import until you demonstrate it.
7. End: summarize what functions now and the next planned feature: rule-based classification.

Record the whole screen with code readable and audio audible. Play the recording before uploading. Use unlisted rather than private video visibility. Confirm the link opens without your signed-in account. Submit through the FSO milestone activity; posting to Discord is optional.
