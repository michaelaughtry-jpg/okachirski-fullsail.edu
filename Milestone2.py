import csv
import sqlite3
import traffic

# Connect to database
db = sqlite3.connect('traffic.db') 

# Create table
db.execute('''
    create table if not exists traffic (
        protocol,
        service,
        sum,
        result,
        reason
    )
''')

# Open CSV file
with open('IoT - 23 Import.csv', newline='') as f:
    r = csv.DictReader(f)

    # Loop through each row in CSV
    for row in r:
        proto = row['protocol']
        serv = row['service']
        orig = int(row['orig_bytes'])
        resp = int(row['resp_bytes'])

        # Calculate sum of bytes
        sum = traffic.total(orig, resp)

        # Flag telnet service
        if serv.strip().lower() == 'telnet':
            res = 'flagged'
            reason = 'telnet service'
        # Flag high traffic
        elif traffic.high(orig, resp):
            res = 'flagged'
            reason = 'high traffic'
        # Do not flag low traffic
        else:
            res = 'not flagged'
            reason = 'low traffic'

        # Insert into database
        db.execute(
            'insert into traffic values (?, ?, ?, ?, ?)',
            (proto, serv, sum, res, reason)
        )

        # Print results
        print('protocol:', proto)
        print('service:', serv)
        print('sum bytes:', sum)
        print('result:', res)
        print('reason:', reason)
        print()

# Commit changes and close database connection
db.commit()
db.close()