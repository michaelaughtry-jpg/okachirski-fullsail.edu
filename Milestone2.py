import csv
import sqlite3

database = sqlite3.connect('traffic.db') 

database.execute('''
    create table if not exists traffic (
        protocol,
        service,
        sum,
        result,
        reason
    )
''')
with open('IoT - 23 Import.csv', newline='') as file:
    reader= csv.DictReader(file)

    for row in reader:
        protocol= row['protocol']
        service= row['service']
        orig= int(row['orig_bytes'])
        resp= int(row['resp_bytes'])

        sum= orig + resp

        if service== sum > 500:
            result= 'flagged'
            reason= 'bytes over 500'
        elif sum > 500:
            result= 'flagged'
            reason= 'high traffic'
        else:
            result= 'not flagged'
            reason= 'low traffic'
        database.execute(
            'insert into traffic values (?, ?, ?, ?, ?)',
            (protocol, service, sum, result, reason)
        )

        print('protocol:', protocol)
        print('service:', service)
        print('sum bytes:', sum)
        print('result:', result)
        print('reason:', reason)
        print()

database.commit()
database.close()