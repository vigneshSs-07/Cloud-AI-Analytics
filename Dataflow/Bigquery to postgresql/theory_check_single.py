__author__ = "Deloitte"
__version__ = "1.0.0"
__status__ = "Development"

#import libraries
import json
import os
import time
import argparse 
from util.context import Context, Settings

import logging
from google.cloud import logging
import util.logger as log 
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.io.gcp.internal.clients import bigquery
from apache_beam.metrics import Metrics
from apache_beam.metrics.metric import MetricsFilter
from beam_nuggets.io import relational_db

cloud_logger = log.log_init_gcp(__name__)

class ComputeWordLengthFn(beam.DoFn):
    def process(self, element):
        logging.info("the count is {}".format(len(element)))
        return [len(element)]


def run(context):
    home = os.environ['HOME']
    pipeline_args = ['--project', context.settings.get('projectid'),
                     '--job_name', context.settings.get('jobname'),
                     '--runner', context.settings.get('runner'),
                     '--staging_location', context.settings.get('dataflow_staging'),
                     '--temp_location', context.settings.get('tempbucket'),
                     '--region', context.settings.get('region'),
                     '--template_location', context.settings.get('template_location'),
                     '--setup_file', context.settings.get('setup')]
                   
    #Configuring pipeline parameters
    pipeline_options = PipelineOptions(pipeline_args)
      
    
    #Reading it from config yaml file
    project_id = context.settings.get('projectid')
    dataset_id = context.settings.get('sourcetablename')
    table_id = context.settings.get('tableid')

    cloud_logger.info("The Name of Project id {}".format(project_id))
    cloud_logger.info("The Name of dataset is {}".format(dataset_id))
    cloud_logger.info("The Name of source table is {}".format(table_id))

    
    
    #Custom function for reading query
    def query_formation(project_id,dataset_id,table_id,where_condition= None):
        if where_condition == None:
            return 'SELECT * FROM '\
                            '[{}:{}.{}]'.format(project_id,dataset_id, table_id)
        else:
            return 'SELECT * FROM '\
                            '[{}:{}.{}] where {}'.format(project_id,dataset_id, table_id,where_condition)

    
    # QUERY1 = 'SELECT * FROM '\
    #                 '[{}:{}.{}] '.format("dca-sandbox-project-4","00_bigquery_00", "AB_table")

    QUERY1 = 'SELECT * FROM '\
                   '[{}:{}.{}] '.format("dca-sandbox-project-4","00_bigquery_00", "diabetes")

    QUERY2 = 'select *, (TricepsThickness + DiastolicBloodPressure) as PTGlucose from `dca-sandbox-project-4.00_bigquery_00.diabetes`'

    Query3 = 'select * from `dca-sandbox-project-4.00_bigquery_00.AB_table` as ab left outer join `dca-sandbox-project-4.00_bigquery_00.example_table` as exam on ab.Conversion_A = exam.Conversion_A where ab.Day= 1;'
    
    Query4 = 'select ab.PlasmaGlucose, exam.DiastolicBloodPressure, exam.TricepsThickness from `dca-sandbox-project-4.00_bigquery_00.diabetws` as ab left join `dca-sandbox-project-4.00_bigquery_00.diabetes` as exam on ab.PatientID = exam.PatientID;'
    
    Query5 = 'SELECT * FROM `bigquery-public-data.usa_names.usa_1910_2013` limit 500'

    Query6 = 'SELECT * FROM `dca-sandbox-project-4.00_bigquery_00.Titanic`'

    print("******", Query6)
    cloud_logger.info("The Query used is {}".format(Query6))

    #Forming query
    input_query = query_formation(project_id,dataset_id,table_id)
    
    def is_perennial(plant):
        return plant['Sex'] == 'male'

    #Target database instance
    source_config = relational_db.SourceConfiguration(
        drivername=context.settings.get('drivername'),
        host=context.settings.get('host'),
        port=context.settings.get('port'),
        database=context.settings.get('database'),
        username=context.settings.get('username'),
        password=context.settings.get('password'),
        create_if_missing=context.settings.get('create_if_missing')
    ) 

    cloud_logger.info("The Database is {}".format(context.settings.get('database')))

    #Target database table
    table_config = relational_db.TableConfiguration(
        name=context.settings.get('target_tableid'),
        create_if_missing=context.settings.get('create_if_missing')
    )

    cloud_logger.info("The Target table is {}".format(context.settings.get('target_tableid')))
    
    #Implementation Of Main Logic  
    try:
        #Creating a beam Pipeline
        p = beam.Pipeline(options=pipeline_options)
        
        # Creating a pcollection
        # def print_row(element):
        #     logging.info("the count is {}".format(len(element)))

        event_1 = (
                p
                | "Read from BQ1" >> beam.io.ReadFromBigQuery(query = Query6, use_standard_sql=True )
        )
        
        # event_1 | beam.combiners.Count.Globally()
        # event_1 | 'Print result' >> beam.Map(print_row)

        #length of Column name
        #word_lengths = event_1 | "Count logic" >> beam.FlatMap(lambda word: [len(word)])

        word_lengths = (event_1 | "Source Count" >> beam.ParDo(ComputeWordLengthFn()))

        # event_2 = (
        #         event_1
        #         | "Data Processing" >>  beam.Filter(lambda record: record["Survived"] == 1)
        # )

        event_2 = (
                event_1
                | "Processing the Data" >> beam.Filter(lambda record: record["Survived"] == 1)

        )

        # event_2 = ( 
        #           event_1
        #           | 'Filter perennials' >> beam.Filter(lambda plant: plant['Sex'] == 'male')

        # )
        # event_2 = ( 
        #           event_1
        #           | 'Filter perennials' >> beam.Filter(is_perennial)

        # )

        target_word_lengths = event_2 | "Target Count" >> beam.ParDo(ComputeWordLengthFn())

        # counts = (
        #         event_1 
        #         |'count' >> beam.combiners.Count.PerElement())
      
        output1 = (
                event_2
                | 'Writing to DB1' >> relational_db.Write(
                        source_config=source_config,
                        table_config=table_config))
        
        
        result = p.run()
        result.wait_until_finish()

    except Exception as e:
        print("The error is {}".format(e))
        cloud_logger.info("The error in pipeline is {}".format(e))
        # logger.log_text(e)
        # context.logger.getLogger()
       
# https://www.programcreek.com/python/example/122923/apache_beam.CombineGlobally


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add required params')
    parser.add_argument(
        '--env',
        required=True,
        help='Add project or environment on which scripts are to be run example: bq'
    )

    args = parser.parse_args()
    jobRunID = os.getpid()
    print("**********",jobRunID )
    config_file = "/home/vsekar/BQtoPostgreSQL/bqtopostgresql/script/config.yaml"
    context = Context(config_file, args.env)
    run(context)