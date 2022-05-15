import csv
import uuid
from google.cloud import bigtable

project_name = 'learngcp-pde'
instance_name = 'vminstance-demo1'
file = 'forestfires.csv'

client = bigtable.Client(project=project_name, admin=True)
instance = client.instance(instance_name)
table = instance.table('fires')
rows = []

with open(file) as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for line in rd:
        line = dict(line)
        row_key = line['X'] + '#' + line['Y'] + '#' + line['month'] + '#' + line['day'] + '#' + str(uuid.uuid4())[:8]
        row = table.row(row_key)
        row.set_cell('fwi', 'ffmc', line['FFMC'])
        row.set_cell('fwi', 'dmc', line['DMC'])
        row.set_cell('fwi', 'dc', line['DC'])
        row.set_cell('fwi', 'isi', line['ISI'])
        row.set_cell('metric', 'temp', line['temp'])
        row.set_cell('metric', 'RH', line['RH'])
        row.set_cell('metric', 'wind', line['wind'])
        row.set_cell('metric', 'rain', line['rain'])
        row.set_cell('metric', 'area', line['area'])
        rows.append(row)

table.mutate_rows(rows)
