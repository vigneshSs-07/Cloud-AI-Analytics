# **Use the client libraries inside Compute Engine to access BigQuery data through Service Account**

##### Task Creating and managing service accounts Using Console
1. You will first create a new service account from the Cloud Console.
2. Go to Navigation menu > IAM & Admin, select Service accounts and click on + Create Service Account.
3. Fill necessary details with:
    a. Service account name: demosaa
    b. Now click Create and Continue and then add the following roles:
    c. Role: BigQuery Data Viewer and BigQuery User


###### Create a VM instance
1. In the Cloud Console, go to Compute Engine > VM Instances, and click Create Instance.
2. Create your VM with the following information:
    a. export ZONE=us-west1-b
    b. gcloud compute instances create "bigquery-instance" \
        --zone $ZONE \
        --machine-type "n1-standard-1" \
        --image-project "debian-cloud" \
        --image-family "debian-10" \
        --subnet "default" \
        --service-account=demosaa@sravanitest.iam.gserviceaccount.com \
        --scopes=https://www.googleapis.com/auth/cloud-platform --tags=http-server,https-server
3. SSH into bigquery-instance by clicking on the SSH button.
    a. gcloud compute ssh --zone "us-west1-b" "bigquery-instance"  --project "sravanitest"
    b. gcloud compute ssh bigquery-instance --project=sravanitest --zone=us-west1-b --troubleshoot
4. After SSH into bigquery-instance by clicking on the SSH button.
    a. In the SSH window, install the necessary dependencies by running the following commands:
        1. sudo apt-get install -y git python3-pip
        2. pip3 install --upgrade pip
        3. pip3 install google-cloud-bigquery
        4. pip3 install pyarrow
        5. pip3 install pandas
        6. pip3 install db-dtypes
5. Script file to get data from bigQuery
echo "
from google.auth import compute_engine
from google.cloud import bigquery
credentials = compute_engine.Credentials(
    service_account_email='YOUR_SERVICE_ACCOUNT')
query = '''
SELECT
year,
COUNT(1) as num_babies
FROM
publicdata.samples.natality
WHERE
year > 2000
GROUP BY
year
'''
client = bigquery.Client(
    project='YOUR_PROJECT_ID',
    credentials=credentials)
print(client.query(query).to_dataframe())
" > query1.py
6. Add the Project ID to query.py with:
    a. sed -i -e "s/YOUR_PROJECT_ID/$(gcloud config get-value project)/g" query1.py
7. Add the service account email to query.py with:
    a. sed -i -e "s/YOUR_SERVICE_ACCOUNT/demosaa@$(gcloud config get-value project).iam.gserviceaccount.com/g" query1.py
8. The application will now use the permissions that are associated with this service account. Now run the query with the following Python command:
    a. python3 query.py
9. To delete the Vm instance
    a. gcloud compute instances delete bigquery-instance --zone=us-west1-b