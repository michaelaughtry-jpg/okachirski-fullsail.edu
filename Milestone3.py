import csv
import sqlite3
import sys
from html import escape
from pathlib import Path

# Get current directory
folder = Path(__file__).resolve().parent
if getattr(sys, 'frozen', False):
    folder = Path(sys.executable).resolve().parent


def charts(groups):
    # Generate two labeled SVG bar charts based on the same counts
    for title, counts in groups:
        # Find the maximum value among all counts
        maximum = max(values[0] for values in counts.values())
        # Calculate height of each chart
        height = 110 + len(counts) * 45
        # Write SVG file
        with open(folder / (title.lower() + '_chart.svg'), 'w', encoding='utf-8') as file:
            file.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="760" height="{height}" viewBox="0 0 760 {height}">')
            file.write('<rect width="100%" height="100%" fill="white"/>')
            file.write('<g font-family="Arial" font-size="17" fill="#183047">')
            file.write(f'<text x="20" y="30" font-size="23">Records by {title.lower()}</text>')
            file.write('<text x="20" y="56" font-size="14">Bar length and labels show record counts</text>')
            y = 80
            for label, values in sorted(counts.items()):
                # Calculate width of bar
                width = values[0] * 420 / maximum
                # Write text label
                file.write(f'<text x="20" y="{y + 20}">{escape(label)}</text>')
                # Write bar
                file.write(f'<rect x="210" y="{y}" width="{width}" height="28" fill="#2878a9"/>')
                # Write record count next to bar
                file.write(f'<text x="{220 + width}" y="{y + 20}">{values[0]}</text>')
                y += 45
            file.write('</g></svg>')
    print('Saved protocol_chart.svg and result_chart.svg in:', folder)
    print('Open these files in Edge or Chrome to view the bar graphs.')


try:
    # Connect to saved traffic without modifying the database
    database = sqlite3.connect((folder / 'traffic.db').as_uri() + '?mode=ro', uri=True)
    try:
        rows = database.execute(
            'SELECT protocol, service, sum, result, reason FROM traffic').fetchall()
    finally:
        database.close()

    if not rows:
        raise ValueError('No records. Run Milestone2.py first.')

    protocols = {}
    results = {}
    total = 0
    for protocol, service, size, result, reason in rows:
        if not isinstance(size, int) or size < 0:
            raise ValueError('Saved byte counts must be nonnegative integers.')
        total += size
        for counts, label in [(protocols, protocol), (results, result)]:
            label = str(label).strip().lower()
            if label not in counts:
                counts[label] = [0, 0]
            counts[label][0] += 1
            counts[label][1] += size

    groups = [('Protocol', protocols), ('Result', results)]
    summary = [['Overall', 'all', len(rows), total]]
    for title, counts in groups:
        for label, values in sorted(counts.items()):
            summary.append([title, label, values[0], values[1]])

    print('IoT Traffic Reports- All Saved Records')
    while True:
        print('\n1 summary\n2 records\n3 export CSV\n4 graphs\n0 exit')
        choice = input('Choose: ').strip()
        if choice == '0':
            break
        try:
            if choice == '1':
                print('total records:', len(rows))
                print('total bytes:', total)
                print('group | category | records | bytes')
                for row in summary[1:]:
                    print(*row, sep=' | ')
            elif choice == '2':
                print('protocol | service | bytes | result | reason')
                for row in rows:
                    print(*row, sep=' | ')
            elif choice == '3':
                with open(folder / 'results.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['protocol', 'service', 'total_bytes', 'result', 'reason'])
                    writer.writerows(rows)
                with open(folder / 'summary.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['group', 'category', 'records', 'total_bytes'])
                    writer.writerows(summary)
                print('Saved results.csv and summary.csv in:', folder)
            elif choice == '4':
                charts(groups)
            else:
                print('Enter 0, 1, 2, 3, or 4.')
        except (OSError, csv.Error) as error:
            print('Could not save the report:', error)
except (OSError, ValueError, sqlite3.Error) as error:
    print('Could not load traffic:', error)
    print('Keep traffic.db beside Milestone3.py or its executable.')