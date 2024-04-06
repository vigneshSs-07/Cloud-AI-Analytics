>>> **PROFESSIONAL DATA ENGINEER** - *Google Cloud Platform*
------------------------

> TITLE: "Introduction to Google Cloud - Cloud Storage Bucket Lock"
> 
> Author:
  >- Name: "Vignesh Sekar"
  >- Designation: "Data Engineer"
  >- Tags: [Google Cloud, DataEngineer, Python, PySpark, SQL, BigData]

--------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Google Cloud Storage - Bucket Lock

- Cloud Storage allows you to configure object retention with temporary retention, a specific Retention Policy which automatically tracks retention expiration for objects, and even event based holds which allow you determine when a Retention Policy begins.

- With Bucket Lock, you can meet regulatory and compliance requirements, such as those associated with FINRA, SEC, and CFTC. You can also use Bucket Lock to address certain health care industry retention regulations.

- Combined with Cloud Storage Object Lifecycle Management, you can create a complete data retention strategy, for example automatically removing data from buckets when retention policies are met.


### Task 1. Create a new bucket

* The Cloud Storage utility tool, **gsutil** is installed and ready to use in Google Cloud. In this lab you use gsutil in the Google Cloud Shell.
  
1. Create a new Cloud Storage bucket to use.
   
2. Define an environment variable named Cloud Storage_BUCKET and use your Project ID as the bucket name. Use the following command which uses the Cloud SDK to get your Project ID:
   
  - export BUCKET="$(gcloud config get-value project)"
  
3. Next, make a new bucket using the following gsutil command:
   
  - gsutil mb "gs://$BUCKET"

### Task 2. Define a Retention Policy

1. You can define the Retention Policy using seconds, days, months, and years using the Cloud Storage gsutil tool. As an example, in Cloud Shell, create a Retention Policy for 10 seconds:
   
  - gsutil retention set 10s "gs://$BUCKET"
  
    * Note: You can also use 10d for 10 days, 10m for 10 months or 10y for 10 years. To learn more, use the command: gsutil help retention set.
  
2. Verify the Retention Policy for a bucket:
   
  - gsutil retention get "gs://$BUCKET"
  
3. Now the bucket has a Retention Policy, add a dummy transaction records object to test it:
   
  - gsutil cp /home/cloudaianalytics/CloudStorage/soft_delete_demo.txt "gs://$BUCKET/"
  
4. Review the retention expiration:
   
  - gsutil ls -L "gs://$BUCKET/dummy_transactions"  
  
5.  When the Retention Policy expires for the given object, it can then be deleted.To extend a Retention Policy, use the gsutil retention set command to update the Retention Policy.


### Task 3. Lock the Retention Policy

1. While unlocked, you can remove the Retention Policy from the bucket or reduce the retention time. After you lock the Retention Policy, it cannot be removed from the bucket or the retention time reduced.
   
2. Lock the Retention Policy:
   
    - gsutil retention lock "gs://$BUCKET/"


### Task 4. Temporary hold

1.  Set a temporary hold on the dummy transactions object:
   
  - gsutil retention temp set "gs://$BUCKET/dummy_transactions"
  
2.  By placing a temporary hold on the object, delete operations are not possible unless the object is released from the hold. As an example, attempt to delete the object:
   
  - gsutil rm "gs://$BUCKET/dummy_transactions"
  
      * You should see the following error message: AccessDeniedException: 403 Object 'YOUR-BUCKET-NAME/dummy_transactions is under active Temporary hold and cannot be deleted, overwritten or archived until hold is removed.
  
3.  Use the following command to release the hold:
   
  - gsutil retention temp release "gs://$BUCKET/dummy_transactions"
  
4.  Now you can delete the file unless the Retention Policy for the file hasn't expired. Otherwise wait a few moments and try again.
   
  - gsutil rm "gs://$BUCKET/dummy_transactions"


### Task 5. How to remove a Retention Policy

1.  Delete an empty bucket using the following command:
   
  - gsutil rb "gs://$BUCKET/"
