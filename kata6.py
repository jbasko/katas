"""
    2013-03-28
    Given a list of profiling records for nested function calls
    with each record containing start_time and end_time,
    work out the nesting of records.

    >>> records = [{'start_time': 2, 'end_time': 9}, {'start_time': 1, 'end_time': 10}]
    >>> make_report(records)
    {'start_time': 1, 'end_time': 10, 'children': [{'start_time': 2, 'end_time': 9, 'children': []}]}

    >>> records.append({'start_time': 5, 'end_time': 6})
    >>> records.append({'start_time': 3, 'end_time': 4})
    >>> report = make_report(records)
    >>> report['start_time'], report['end_time'], len(report['children'])
    (1, 10, 1)
    >>> report['children'][0]['start_time'], report['children'][0]['end_time']
    (2, 9)
    >>> len(report['children'][0]['children'])
    2
    >>> x = report['children'][0]['children']
    >>> x[0]['start_time'], x[0]['end_time']
    (3, 4)
    >>> x[1]['start_time'], x[1]['end_time']
    (5, 6)
    >>> records.append({'start_time': 9.5, 'end_time': 9.9})
    >>> report = make_report(records)
    >>> len(report['children'])
    2
"""


def make_report(raw_records):

    def sort_by_start_time(record):
        return record['start_time']

    records = sorted(raw_records, key=sort_by_start_time)
    records[0]['children'] = []

    report = records[0]
    for i in range(1, len(records)):
        records[i]['children'] = []
        if records[i]['start_time'] < records[i - 1]['end_time']:
            # is a child of the previous record
            records[i - 1]['children'].append(records[i])
        else:
            # is a sibling of the previous record, must find parent
            # parent is the most recent previous record which has greater end_time
            for j in range(i - 1, -1, -1):
                if records[j]['end_time'] > records[i]['end_time']:
                    records[j]['children'].append(records[i])
                    break

    return report

