"""Milestone 1 UI: import traffic; classification and graphs are later milestones."""
from pathlib import Path
import sqlite3
import streamlit as st
from traffic_store import import_log, read_dashboard, ImportProblem, DuplicateImport

DATABASE = Path(__file__).resolve().parent / 'data' / 'traffic.db'
st.set_page_config(page_title='IoT Traffic Analysis Dashboard', layout='wide')
st.title('IoT Traffic Analysis Dashboard')
st.caption('Milestone 1 — Import traffic into SQLite')
st.write('Upload an uncompressed Zeek connection log with a tab-separated #fields header. '
         'Imports are limited to 20 MiB and 10,000 records.')
file = st.file_uploader('Select a traffic log', type=['log', 'tsv', 'txt'])
limit = st.number_input('Maximum records to import', min_value=1, max_value=10000, value=10000, step=100)
if st.button('Import traffic', disabled=file is None):
    try:
        with st.spinner('Validating and saving records…'):
            import_id, count = import_log(DATABASE, file.name, file.getvalue(), int(limit))
        st.success(f'Imported {count} records successfully (import {import_id}).')
    except DuplicateImport as exc:
        st.warning(str(exc))
    except ImportProblem as exc:
        st.error(str(exc))
    except (sqlite3.Error, OSError):
        st.error('Database could not be updated. Check folder permissions and close other writers, then retry.')
try:
    total, history, preview = read_dashboard(DATABASE)
    st.metric('Saved traffic records', total)
    st.subheader('Import history')
    if history:
        st.dataframe(history, use_container_width=True)
        st.subheader('Most recent 100 saved records')
        st.dataframe(preview, use_container_width=True)
    else:
        st.info('No imports yet. Try samples/sample_conn.log from the project folder.')
except (sqlite3.Error, OSError):
    st.error('Unable to read the database. Check permissions and try again.')
