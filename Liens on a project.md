>>> **PROFESSIONAL DATA ENGINEER** - *Google Cloud Platform*
------------------------

> TITLE: "Deleting Project in GCP"
> 
> Author:
  >- Name: "Vignesh Sekar"
  >- Designation: "Multi Cloud Architect"
  >- Tags: [Google Cloud, DataEngineer, Python, PySpark, SQL, BigData]
    

# Liens in GCP

1. Liens is a protection method against accidental deletion of a Google Cloud Project.

2. You can place a lien upon a project to block the project's deletion until you remove the lien. This can be useful to protect projects of particular importance.
 
3. Liens can also be placed upon a project automatically. For example, if you allow Identity and Access Management (IAM) service accounts from one project to be
      attached to resources in other projects, a lien is placed upon the project where the service accounts are located.

## Error Statement

1. Project has one or more liens on it to prevent accidental deletion" error message when trying to delete a Google Cloud Project

### Placing a lien on a project

- gcloud alpha resource-manager liens create \
  --project=[PROJECT_NAME]
  --restrictions=[PERMISSION_RESTRICTION] \
  --reason=[LIEN_REASON]
  --origin=[LIEN_ORIGIN]

### Listing liens on a project

- gcloud alpha resource-manager liens list

### Removing liens from a project

- gcloud alpha resource-manager liens delete [LIEN_NAME]

### Delete the Cloud Project again.

- gcloud projects delete PROJECT_ID

--------------------------------------------------------------------------------------------------------------------------------------------------------------------

  <div class="footer">
              copyright © 2022—2023 Cloud & AI Analytics. 
                                      All rights reserved
          </div>
