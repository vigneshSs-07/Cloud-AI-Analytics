# File Store

1. Filestore instances are fully managed file servers on Google Cloud that can be connected to Compute Engine VMs, GKE clusters, and your on-premises machines
2. Support both HDD and SSD. Network attached storage(NAS)/managed NFS file servers on Google Cloud
3. Costly compared to Cloud Storage.

### Task 1. Create a VM instance

1. Navigate to VM Instances by going to Navigation Menu > Compute Engine > VM Instances and click Create instance.
2. Set up your VM with the following information:

    Configuration	Value
        Name	nfs-client
        Region	us-central1(Iowa)
        Zone	us-central1-c
        Series	N1
        Machine Type	1 vCPU (n1-standard-1)
        Boot Disk	Debian GNU/Linux 11 (bullseye)
        Firewall	Allow HTTP traffic

3. Click Create.

### Task 2. Create a Cloud Filestore instance

1. Go to Navigation menu > APIs and Services > Library.
2. Search for Cloud Filestore API and click Enable if it is not already enabled.
3. Navigate to Navigation Menu > Filestore.If you get an error message be sure you navigated to Filestore and not Firestore.
4. Click Create Instance at the top of the page.
5. Create your Cloud Filestore instance with the following information:

    Configuration	Value
        Instance ID	nfs-server
        Instance type	Basic
        Storage type	HDD
        Allocate capacity	1 TB
        Region	us-central1
        Zone	us-central1-a
        Network	default
        File share name	vol1
        Access control	Grant access to all clients on the VPC network
6. Click Create.

### Task 3. Mount the Cloud Filestore fileshare on a Compute Engine VM

1. Navigate Navigation Menu > Compute Engine > VM Instances.
2. In the list of VM instances, click the SSH button for nfs-client to open a terminal window connected to that instance.
3. In SSH shell install NFS by running the following commands:
    a. sudo apt-get -y update
    b. sudo apt-get -y install nfs-common
4. Make a mount directory for the Cloud Filestore fileshare by running the following command:
    c. sudo mkdir /mnt/test
5. Mount the fileshare by running the mount command and specifying the Cloud Filestore instance IP address and fileshare name:
    d. sudo mount 10.48.245.82:/vol1 /mnt/test

6. Make the fileshare accessible by changing the permissions:
    e. sudo chmod go+rw /mnt/test

### Task 4. Create a file on the fileshare

1. In the terminal window that is connected to the nfs-client instance, run the following to create a file named testfile:
    a. echo 'This is a Google CLoud Platform' > /mnt/test/testfile
2. Confirm the file was created by running the following command:
    b. ls /mnt/test
3. You can see the content of the file by running the following command:
    c. nano /mnt/test/testfile