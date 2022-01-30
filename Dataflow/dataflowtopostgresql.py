#Working
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from beam_nuggets.io import relational_db

records = [
    {'name': 'Jan', 'num': 1},
    {'name': 'Feb', 'num': 2},
    {'name': 'Mar', 'num': 3},
    {'name': 'Apr', 'num': 4},
    {'name': 'May', 'num': 5},
]

source_config = relational_db.SourceConfiguration(
    drivername='postgresql+pg8000',  #postgresql+pg8000
    host='35.239.104.9',
    port=5432,
    username='postgres',
    password='cvsgcp01',
    database='demodb',
    create_if_missing=True  # create the database if not there 
)

table_config = relational_db.TableConfiguration(
    name='months_col',
    create_if_missing=True,
    primary_key_columns=['num']
)

with beam.Pipeline(options=PipelineOptions()) as p:
    months = p | "Reading month records" >> beam.Create(records)
    months | 'Writing to DB table' >> relational_db.Write(
        source_config=source_config,
        table_config=table_config
    )

if __name__ == "__main__":
    print('demo code ran successful')