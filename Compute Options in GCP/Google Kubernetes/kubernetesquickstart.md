# Kubernetes Engine: Qwik Start

1. Google Kubernetes Engine (GKE) provides a managed environment for deploying, managing, and scaling your containerized applications using Google infrastructure. 
2. The Kubernetes Engine environment consists of multiple machines (specifically Compute Engine instances) grouped to form a container cluster. 

### Cluster orchestration with Google Kubernetes Engine

1. Google Kubernetes Engine (GKE) clusters are powered by the **Kubernetes** -- an open source cluster management system. 
2. Kubernetes provides the mechanisms through which you interact with your container cluster.You use Kubernetes commands and resources to deploy and manage your applications, perform administrative tasks, set policies, and monitor the health of your deployed workloads.
3. Kubernetes draws on the same design principles that run popular Google services and provides the same benefits:  
    a. automatic management
    b. monitoring and liveness probes for application containers
    c. automatic scaling
    d. rolling updates and more. 

####

4. A ***GKE cluster*** consists of at least ***one cluster master machine*** and multiple worker machines called ***nodes***. 
    a. Nodes are ***Compute Engine virtual machine (VM) instances*** that run the Kubernetes processes necessary to make them part of the cluster.
5. GKE uses Kubernetes objects to create and manage your cluster's resources. Kubernetes provides the Deployment object for deploying stateless applications like web servers.
6. Service objects define rules and load balancing for accessing your application from the internet.

### Kubernetes on Google Cloud

When you run a GKE cluster, you also gain the benefit of advanced cluster management features that Google Cloud provides. These include:

1. ***Load balancing*** for Compute Engine instances
2. ***Node pools*** to designate subsets of nodes within a cluster for additional flexibility
3. ***Automatic scaling*** of your cluster's node instance count
4. ***Automatic upgrades*** for your cluster's node software
5. ***Node auto-repair*** to maintain node health and availability
6. ***Logging and Monitoring*** with Cloud Monitoring for visibility into your cluster

### Task 1. Set a default compute zone

1. Set the default compute region
    a. gcloud config set compute/region us-east4
2. Set the default compute zone 
    b. export ZONE=$(gcloud config set compute/zone us-east4-a)
    c. export ZONE=$(gcloud config get-value compute/zone)

### Task 2. Create a GKE cluster

1. Note: Cluster names must start with a letter and end with an alphanumeric, and cannot be longer than 40 characters.
    a. gcloud container clusters create --machine-type=e2-medium --zone=$ZONE lab-cluster 

### Task 3. Get authentication credentials for the cluster

1. Authenticate with the cluster
    a. gcloud container clusters get-credentials lab-cluster 

### Task 4. Deploy an application to the cluster

1. You can now deploy a containerized application to the cluster. For this lab, you'll run hello-app in your cluster.
2. To create a new Deployment hello-server from the hello-app container image, run the following kubectl create command:
    a. kubectl create deployment hello-server-gcp --image=gcr.io/google-samples/hello-app:1.0

    ***NOTE*** This Kubernetes command creates a Deployment object that represents hello-server. 
    In this case, 
    a. --image specifies a container image to deploy. 
    The command pulls the example image from a Container Registry bucket. gcr.io/google-samples/hello-app:1.0 indicates the specific image version to pull. If a version is not specified, the latest version is used.
3. To create a Kubernetes Service, which is a Kubernetes resource that lets you expose your application to external traffic, run the following kubectl expose command:
    a. kubectl expose deployment hello-server-gcp --type=LoadBalancer --port 8080

    ***NOTE:***
    In this command:
        1. --port specifies the port that the container exposes.
        2. type="LoadBalancer" creates a Compute Engine load balancer for your container.
4. To inspect the hello-server Service, run kubectl get:
    a. kubectl get service
5. To view the application from your web browser, open a new tab and enter the following address, replacing [EXTERNAL IP] with the EXTERNAL-IP for hello-server.
    a. http://[EXTERNAL-IP]:8080
        http://35.245.179.251:8080

### Task 5. Deleting the cluster

1. To delete the cluster, run the following command:
    a. gcloud container clusters delete lab-cluster 
2. When prompted, type Y to confirm.
    a. Deleting the cluster can take a few minutes.
    
    
### Resources

1.  For more information on deleted GKE clusters from the Google Kubernetes Engine (GKE) article, Deleting a cluster.
    a. https://cloud.google.com/kubernetes-engine/docs/how-to/deleting-a-cluster