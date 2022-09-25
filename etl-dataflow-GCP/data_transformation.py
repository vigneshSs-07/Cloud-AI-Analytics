
#import libraries
import argparse
import csv
import logging
import os
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.gcp.bigquery_tools import parse_table_schema_from_json


class DataTransformation:
    """A helper class which contains the logic to translate the file into a
  format BigQuery will accept."""

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.schema_str = ''
        schema_file = os.path.join(dir_path, 'resources', 'usa_names_year_as_date.json')
        with open(schema_file) \
                as f:
            data = f.read()
            self.schema_str = '{"fields": ' + data + '}'

    def parse_method(self, string_input):
        """This method translates a single line of comma separated values to a
    dictionary which can be loaded into BigQuery.

        Args:
            string_input: A comma separated list of values in the form of
            state_abbreviation,gender,year,name,count_of_babies,dataset_created_date
                example string_input: KS,F,1923,Dorothy,654,11/28/2016

        Returns:
            A dict mapping BigQuery column names as keys to the corresponding value
            parsed from string_input.  In this example, the data is not transformed, and
            remains in the same format as the CSV.  There are no date format transformations.

                example output:
                      {'state': 'KS',
                       'gender': 'F',
                       'year': '1923-01-01', <- This is the BigQuery date format.
                       'name': 'Dorothy',
                       'number': '654',
                       'created_date': '11/28/2016'
                       }
        """
        # Strip out return characters and quote characters.
        schema = parse_table_schema_from_json(self.schema_str)

        field_map = [f for f in schema.fields]

        # Use a CSV Reader which can handle quoted strings etc.
        reader = csv.reader(string_input.split('\n'))
        for csv_row in reader:
            month = '01'
            day = '01'
            year = csv_row[2]

            row = {}
            i = 0
            # Iterate over the values from our csv file, applying any transformation logic.
            for value in csv_row:
                # If the schema indicates this field is a date format, we must
                # transform the date from the source data into a format that
                # BigQuery can understand.
                if field_map[i].type == 'DATE':
                    # Format the date to YYYY-MM-DD format which BigQuery
                    # accepts.
                    value = '-'.join((year, month, day))

                row[field_map[i].name] = value
                i += 1

            return row


def run(argv=None):
    """The main function which creates the pipeline and runs it."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input', dest='input', required=False,
        help='Input file to read.  This can be a local file or '
             'a file in a Google Storage Bucket.',
        default='gs://spls/gsp290/data_files/head_usa_names.csv')
    parser.add_argument('--output', dest='output', required=False,
                        help='Output BQ table to write results to.',
                        default='lake.usa_names_transformed')

    # Parse arguments from the command line.
    known_args, pipeline_args = parser.parse_known_args(argv)
    data_ingestion = DataTransformation()

    p = beam.Pipeline(options=PipelineOptions(pipeline_args))
    schema = parse_table_schema_from_json(data_ingestion.schema_str)

    (p
     | 'Read From Cloud Storage' >> beam.io.ReadFromText(known_args.input,
                                                skip_header_lines=1)
     | 'String to BigQuery Row' >> beam.Map(lambda s:
                                            data_ingestion.parse_method(s))
     | 'Write to BigQuery' >> beam.io.Write(
        beam.io.BigQuerySink(
            known_args.output,
            schema=schema,
            # Creates the table in BigQuery if it does not yet exist.
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            # Deletes all data in the BigQuery table before writing.
            write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE)))
    p.run().wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
