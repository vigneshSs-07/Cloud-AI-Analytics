>>> **PROFESSIONAL DATA ENGINEER** - *Google Cloud Platform*
------------------------------------------------------------------------------------------------------------------------------------------------------------------------

> TITLE: "Basics of Cloud BigQuery - Google Cloud Platform"
> 
> Author:
  >- Name: "Vignesh Sekar S"
  >- Designation: "Data Engineer"
  >- Tags: [Google Cloud, DataEngineer, BigQuery]

------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Task 1. Query a public dataset

```

SELECT
 weight_pounds, state, year, gestation_weeks
FROM
 `bigquery-public-data.samples.natality`
ORDER BY weight_pounds DESC LIMIT 10;

```

### Task 2. Create a new dataset

-- `vaulted-journal-420209.demo_dataset`

### Task 3. Upload data into a new table

-- nyc_tlc_yellow_trips_2018_subset_1.csv

### Task 4. Query a custom dataset

```

#standardSQL
SELECT
  *
FROM
  nyctaxi.2018trips
ORDER BY
  fare_amount DESC
LIMIT  5

```

### Task 5. Ingest a new dataset from Google Cloud Storage

1. Google Cloud Storage path

   * spls/gsp072/baby-names/yob2014.txt
   * File Format - CSV
   * Table name - names_2014
   * name:string,gender:string,count:integer 


### Task 6. Query a custom dataset

```

#standardSQL
SELECT
 name, count
FROM
 `vaulted-journal-420209.demo_dataset.kf_demo_dataset_010`
WHERE
 gender = 'M'
ORDER BY count DESC LIMIT 5;


```

### Task 7. Create tables from other tables with DDL

```
#standardSQL

CREATE TABLE
  `vaulted-journal-420209.demo_dataset.kf_demo_dataset_0101` AS
SELECT
 name, count
FROM
 `vaulted-journal-420209.demo_dataset.kf_demo_dataset_010`
WHERE
 gender = 'F'
ORDER BY count ASC LIMIT 5;

```


--------------------------------------------------------------------------------------------------------------------------------------------------------------------

  <div class="footer">
              copyright © 2023—2024 Cloud & AI Analytics. 
                                      All rights reserved
          </div>