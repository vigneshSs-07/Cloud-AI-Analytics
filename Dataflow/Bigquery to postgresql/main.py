#import libraries
import json
import os
import time
import argparse 

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.io.gcp.internal.clients import bigquery
from beam_nuggets.io import relational_db

import constants as c 
print(c.projectid)

def run():
    home = os.environ['HOME']
    pipeline_args = ['--project', c.projectid,
                     '--job_name', c.jobname,
                     '--runner', c.runner,
                     '--staging_location', c.dataflow_staging,
                     '--temp_location', c.tempbucket,
                     '--region', c.region,
                     '--template_location', c.template_location,
                     '--setup_file', c.setup]
                   
    #Configuring pipeline parameters
    pipeline_options = PipelineOptions(pipeline_args)

    QUERY1 = 'select * from `datalab-336505.demodata.Titanic`'
    print("******", QUERY1)
   

    #Target database instance
    source_config = relational_db.SourceConfiguration(
        drivername=c.drivername,
        host=c.host,
        port=c.port,
        database=c.database,
        username=c.username,
        password=c.password,
        create_if_missing=c.create_if_missing
    ) 
    
    #Target database table
    table_config = relational_db.TableConfiguration(
        name=c.target_tableid, #target_tableid
        create_if_missing=c.create_if_missing
    )

    
    #Implementation Of Main Logic  
    try:
        #Creating a beam Pipeline
        p = beam.Pipeline(options=pipeline_options)
        #Creating a pcollection
        
        event_1 = (
                p
                | "Read from BQ1" >> beam.io.ReadFromBigQuery(query = QUERY1, use_standard_sql=True )
        )

        event_2 = (
                event_1
                | "Processing the Data" >> beam.Filter(lambda record: record["Survived"] == 1)

        )
      
        output1 = (
                event_2
                | 'Writing to DB1' >> relational_db.Write(
                        source_config=source_config,
                        table_config=table_config))
        
        
        result = p.run()
        result.wait_until_finish()

    except Exception as e:
        print("The error is {}".format(e))
        

if __name__ == '__main__':
    run()
    print("Run Successful")
    # gcloud dataflow jobs run titanicdemo --gcs-location="gs://gcsbucket01/template_folder/template"