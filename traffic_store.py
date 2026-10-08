"""Bounded Zeek TSV import and transactional SQLite persistence."""
from contextlib import closing
from hashlib import sha256
from pathlib import Path
from datetime import datetime, timezone
import ipaddress
import math
import sqlite3

MAX_BYTES = 20 * 1024 * 1024
REQUIRED = ('ts', 'uid', 'id.orig_h', 'id.resp_h', 'proto', 'service', 'orig_bytes', 'resp_bytes')

class ImportProblem(ValueError):
    """An input cannot be imported safely."""

class DuplicateImport(ImportProblem):
    pass

def connect(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys = ON')
    return db

def initialize(path):
    with closing(connect(path)) as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS imports (
            id INTEGER PRIMARY KEY, filename TEXT NOT NULL,
            source_hash TEXT NOT NULL, row_limit INTEGER NOT NULL,
            imported_at TEXT NOT NULL, row_count INTEGER NOT NULL,
            UNIQUE(source_hash, row_limit));
        CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY, import_id INTEGER NOT NULL REFERENCES imports(id),
            ts REAL NOT NULL, uid TEXT NOT NULL, orig_host TEXT NOT NULL,
            resp_host TEXT NOT NULL, proto TEXT NOT NULL, service TEXT,
            orig_bytes INTEGER, resp_bytes INTEGER);
        CREATE INDEX IF NOT EXISTS connections_import ON connections(import_id);
        ''')
        db.commit()

def parse_log(payload, row_limit):
    if not 1 <= row_limit <= 10000:
        raise ImportProblem('Choose a row limit between 1 and 10,000.')
    if len(payload) > MAX_BYTES:
        raise ImportProblem('File exceeds the 20 MiB limit. Use a smaller log excerpt.')
    try:
        lines = payload.decode('utf-8-sig').splitlines()
    except UnicodeDecodeError as exc:
        raise ImportProblem('Expected an uncompressed UTF-8 Zeek TSV log.') from exc
    fields = None
    separator = '\t'
    unset, empty = '-', '(empty)'
    records = []
    for line_number, line in enumerate(lines, 1):
        if line.startswith('#separator '):
            if line[len('#separator '):] != r'\x09':
                raise ImportProblem('Only tab-separated Zeek logs are supported.')
        elif line.startswith('#unset_field\t'):
            unset = line.split('\t', 1)[1]
        elif line.startswith('#empty_field\t'):
            empty = line.split('\t', 1)[1]
        elif line.startswith('#fields\t'):
            fields = line.split(separator)[1:]
            if len(fields) != len(set(fields)) or any(k not in fields for k in REQUIRED):
                raise ImportProblem('Header must contain unique fields including: ' + ', '.join(REQUIRED))
        elif not line or line.startswith('#'):
            continue
        else:
            if fields is None:
                raise ImportProblem('Missing Zeek #fields header before data.')
            values = line.split(separator)
            if len(values) != len(fields):
                raise ImportProblem(f'Line {line_number}: column count does not match header.')
            row = dict(zip(fields, values))
            try:
                timestamp = float(row['ts'])
                if not math.isfinite(timestamp) or timestamp < 0:
                    raise ValueError('timestamp must be finite and nonnegative')
                for key in ('id.orig_h', 'id.resp_h'):
                    ipaddress.ip_address(row[key])
                for key in ('uid', 'proto'):
                    if not row[key].strip() or row[key] in (unset, empty):
                        raise ValueError(f'{key} is required')
                numbers = []
                for key in ('orig_bytes', 'resp_bytes'):
                    value = row[key]
                    if value in (unset, empty):
                        numbers.append(None)
                    else:
                        number = int(value)
                        if number < 0 or number > 9223372036854775807:
                            raise ValueError(f'{key} must be a nonnegative SQLite integer')
                        numbers.append(number)
                service = None if row['service'] in (unset, empty) else row['service']
                records.append((timestamp, row['uid'], row['id.orig_h'], row['id.resp_h'],
                                row['proto'], service, *numbers))
            except ValueError as exc:
                raise ImportProblem(f'Line {line_number}: {exc}') from exc
            if len(records) == row_limit:
                break
    if not records:
        raise ImportProblem('No traffic records found.')
    return records

def import_log(path, filename, payload, row_limit=10000):
    records = parse_log(payload, row_limit)
    initialize(path)
    digest = sha256(payload).hexdigest()
    with closing(connect(path)) as db:
        try:
            with db:
                cursor = db.execute(
                    'INSERT INTO imports(filename,source_hash,row_limit,imported_at,row_count) VALUES(?,?,?,?,?)',
                    (Path(filename).name, digest, row_limit, datetime.now(timezone.utc).isoformat(), len(records)))
                import_id = cursor.lastrowid
                for offset in range(0, len(records), 500):
                    db.executemany('''INSERT INTO connections
                        (import_id,ts,uid,orig_host,resp_host,proto,service,orig_bytes,resp_bytes)
                        VALUES(?,?,?,?,?,?,?,?,?)''',
                        [(import_id, *row) for row in records[offset:offset + 500]])
        except sqlite3.IntegrityError as exc:
            if db.execute('SELECT id FROM imports WHERE source_hash=? AND row_limit=?', (digest,row_limit)).fetchone():
                raise DuplicateImport('This file has already been imported with this row limit.') from exc
            raise
    return import_id, len(records)

def read_dashboard(path):
    initialize(path)
    with closing(connect(path)) as db:
        total = db.execute('SELECT COUNT(*) FROM connections').fetchone()[0]
        history = [dict(r) for r in db.execute('SELECT * FROM imports ORDER BY id DESC')]
        preview = [dict(r) for r in db.execute('SELECT * FROM connections ORDER BY id DESC LIMIT 100')]
    return total, history, preview
