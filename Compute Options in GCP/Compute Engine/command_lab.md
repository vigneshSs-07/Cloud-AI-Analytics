>>> **PROFESSIONAL DATA ENGINEER** - *Google Cloud Platform*
------------------------

> TITLE: "Introduction to Google Cloud - Fundamentals: Getting Started with Compute Engine"
> 
> Author:
  >- Name: "Vignesh Sekar"
  >- Designation: "Multi Cloud Architect"
  >- Tags: [Google Cloud, DataEngineer, Python, PySpark, SQL, BigData]


### Task 1. Create a virtual machine using the Cloud console

1. In the Navigation menu (Navigation menu), click Compute Engine > VM instances - Click CREATE INSTANCE.
2. On the Create an Instance page, for Name, type my-vm-1.
3. For Region and Zone, select the region and zone assigned by Google Cloud Skills Boost.
4. For Machine type, accept the default.
5. For Boot disk, if the Image shown is not Debian GNU/Linux 10 (Buster), click Change and select Debian GNU/Linux 10 (Buster).Leave the defaults for Identity and API access unmodified.
6. For Firewall, click Allow HTTP traffic.Leave all other defaults unmodified.
7. To create and launch the VM, click Create.

# Example command
gcloud compute instances create my-vm-1 --project=mygcpdev-385300 --zone=us-central1-a --machine-type=e2-medium --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default --maintenance-policy=MIGRATE --provisioning-model=STANDARD --service-account=719529097077-compute@developer.gserviceaccount.com --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append --tags=http-server --create-disk=auto-delete=yes,boot=yes,device-name=my-vm-1,image=projects/debian-cloud/global/images/debian-11-bullseye-v20230629,mode=rw,size=10,type=projects/mygcpdev-385300/zones/us-central1-a/diskTypes/pd-balanced --no-shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring --labels=goog-ec-src=vm_add-gcloud --reservation-affinity=any


### Task 2. Create a virtual machine using the gcloud command line

1. In the Cloud console, on the top right toolbar, click the Activate Cloud Shell button (Cloud Shell icon).
2. To set your default zone to the one you just chose, enter this partial command gcloud config set compute/zone followed by the zone you chose.

    - gcloud config set compute/zone us-central1-b

3. To create a VM instance called my-vm-2 in that zone, execute this command:

    - gcloud compute instances create "my-vm-2" \
          --machine-type "n1-standard-1" \
          --image-project "debian-cloud" \
          --image-family "debian-10" \
          --subnet "default"

### Task 3. Connect between VM instances

1. In the Navigation menu, click Compute Engine > VM instances.You will see the two VM instances you created, each in a different zone.
2. To open a command prompt on the my-vm-2 instance, click SSH in its row in the VM instances list.
3. Use the ping command to confirm that my-vm-2 can reach my-vm-1 over the network:

    - ping my-vm-1.us-central1-a

4. Notice that the output of the ping command reveals that the complete hostname of my-vm-1 is my-vm-1.us-central1-a.c.PROJECT_ID.internal, where PROJECT_ID is the name of your Google Cloud Platform project. The Cloud console automatically supplies Domain Name Service (DNS) resolution for the internal IP addresses of VM instances.
5. Press Ctrl+C to abort the ping command.
6. Return to the Cloud Console tab.Click SSH in the my-vm-1 row in the VM instances list.
7. At the command prompt on my-vm-1, install the Nginx web server:

    - sudo apt-get install nginx-light -y

8. Use the nano text editor to add a custom message to the homepage of the web server:

    - sudo nano /var/www/html/index.nginx-debian.html

9. Use the arrow keys to move the cursor to the line just below the h1 header. Add text like this, and replace YOUR_NAME with your name:
10. Hi from YOUR_NAME
11. Press Ctrl+O and then press Enter to save your edited file, and then press Ctrl+X to exit the nano text editor.
12. Confirm that the web server is serving your new page. At the command prompt on my-vm-1, execute this command:

    - curl http://localhost/

13. The response will be the HTML source of the web server's home page, including your line of custom text.
14. Return to the command prompt on my-vm-2
15. To confirm that my-vm-2 can reach the web server on my-vm-1, at the command prompt on my-vm-2, execute this command:

    - curl http://my-vm-1.us-central1-a/

16. The response will again be the HTML source of the web server's home page, including your line of custom text.
17. In the Navigation menu, click Compute Engine > VM instances.
18. Copy the External IP address for my-vm-1 and paste it into the address bar of a new browser tab.



    -----------------------------------------------------------

    <div class="footer">
              copyright © 2022—2023 Cloud & AI Analytics. 
                                      All rights reserved
            </div>
