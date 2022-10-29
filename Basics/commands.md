### Configure your GCP environment in Cloud Shell

0. Set the project-id
    1. gcloud config set project theta-device-359600

1. Set the region to us-central1
    a. gcloud config set compute/region us-central1

2. To view the project region setting, run the following command
    b. gcloud config get-value compute/region

3. Set the zone to us-central1-a
    c. gcloud config set compute/zone us-central1-a

4. To view the project zone setting, run the following command
    d. gcloud config get-value compute/zone

5. View the project id for your project:
    e. gcloud config get-value project

6. View details about the project
    f. gcloud compute project-info describe --project $(gcloud config get-value project)

7. To Unset project id, Region and Zone 
    g. gcloud config unset project
    h. gcloud config unset compute/zone
    i. gcloud config unset compute/region
