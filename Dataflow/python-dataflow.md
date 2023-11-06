# Dataflow: Qwik Start - Python

https://partner.cloudskillsboost.google/course_sessions/5692160/labs/408096

### Task 1. Create a Cloud Storage bucket
On the Navigation menu (Navigation menu icon), click Cloud Storage > Buckets.
Click Create bucket.
In the Create bucket dialog, specify the following attributes:
Name: To ensure a unique bucket name, use the following name: ____-bucket. Note that this name does not include sensitive information in the bucket name, as the bucket namespace is global and publicly visible.
Location type: Multi-region
Location: us
A location where bucket data will be stored.
Click Create.

If Prompted Public access will be prevented, click Confirm.

### ipeline option (runner). Executing pipeline using the default runner: DirectRunner.
INFO:oauth2client.client:Attempting refresh to obtain initial access_token
This message can be ignored.

You can now list the files that are on your local cloud environment to get the name of the OUTPUT_FILE:
ls
Copied!
Copy the name of the OUTPUT_FILE and cat into it:
cat <file name>
Copied!
Your results show each word in the file and how many times it appears.


### Task 3. Run an example pipeline remotely
Set the BUCKET environment variable to the bucket you created earlier:
BUCKET=gs://<bucket name provided earlier>
Copied!
Now you'll run the wordcount.py example remotely:
python -m apache_beam.examples.wordcount --project $DEVSHELL_PROJECT_ID \
  --runner DataflowRunner \
  --staging_location $BUCKET/staging \
  --temp_location $BUCKET/temp \
  --output $BUCKET/results/output \
  --region "filled in at lab start"
Copied!
In your output, wait until you see the message:

JOB_MESSAGE_DETAILED: Workers have started successfully.
Then continue with the lab.

### Task 4. Check that your job succeeded
Open the Navigation menu and click Dataflow from the list of services.
You should see your wordcount job with a status of Running at first.

Click on the name to watch the process. When all the boxes are checked off, you can continue watching the logs in Cloud Shell.
The process is complete when the status is Succeeded.

Test completed task

Click Check my progress to verify your performed task. If you have completed the task successfully you will be granted with an assessment score.

Run an Example Pipeline Remotely.
Click Navigation menu > Cloud Storage in the Cloud Console.

Click on the name of your bucket. In your bucket, you should see the results and staging directories.

Click on the results folder and you should see the output files that your job created:

Click on a file to see the word counts it contains.

