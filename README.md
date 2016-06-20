#CLOUD-METRIC

Cloud-Metric is an application framework for estimating cost of running applications on Amazon Web Services 
and Google Cloud Platform. It is quite portable and lightweight. It is designed and developed for software engineers who
want to see during development phase how their application is doing in terms of cost on the public clouds - AWS and GCP and also for 
researchers in academia with enough funding who want to migrate their (on-premise) applications to public clouds. 

###Features
Cloud-Metric provides the following features:

  **Resource Mining**  - meters user's development environment and output the results on application interface.
  
  **Resource Monitoring** - monitors instances resources such as CPU, Memory, Disk storage, provides monitoring metrics for both inividual machines
  and entire clusters. 
  
  **Cost Estimation** - provides monthly on-demand cost estimates of the metered environment on Amazon Web Services and Google Cloud Platform.
  provides individual machines monthly on-demand costs and cost of entire cluster. It also provide users the ability to see the varying costs
  of instances on all regions in AWS and GCP. 
  
  **Instance Matching** - matches each machine in user's environment to the closest matching instance type on AWS and GCP
  
  **Instance Recommendation** - Cloud Metric provides recommendation of instances types on AWS and GCP based on the resource utilisation on the user's development environment
  
  
###Tools

Cloud Metric is developed in [Python 2.7](https://www.python.org/download/releases/2.7/), 
[Flask](http://flask.pocoo.org/), and a [MongoDB](https://www.mongodb.com/). 

###Deployment
Cloud Metric is composed of two components: 

- Flask App
- External mining and monitoring scripts

Here I am going to show you the steps required to deploy cloud metric app in [Docker](https://www.docker.com/) 
container using [Docker Compose](https://docs.docker.com/compose/overview/)

We are ready to go! :shipit:

I assume that you are in your ubuntu virtual machine 

####Step 1: **Install docker** by running the following commands:

1. `sudo aptitude  update`

2. `sudo aptitude -y upgrade`

3. `sudo aptitude install linux-image-extra-'uname -r`

4. `sudo sh -c "wget -qO- https://get.docker.io/gpg | apt-key add -"`

5. `sudo sh -c "echo deb http://get.docker.io/ubuntu docker main\ > /etc/apt/sources.list.d/docker.list"
`
6. `sudo aptitude update`

7. `sudo aptitude install lxc-docker`


####Step 2: Run the following commands to install **Docker Compose**

- `sudo apt-get install python-pip`

- `pip install docker-compose`

####Step 3: Running the application
Create a directory to store the application

`mkdir [directoryname]`

`cd [directoryname]`

Use `git` to clone the app from the repo

`git clone https://github.com/ajallow07/Cloud_Cost_Estimator`

`cd Cloud_Cost_Estimator`

Build the an image using docker compose

`sudo docker-compose build`

Start the application by

`sudo docker-compose up`

Go to your browser and type in `http://[your container IP]:5000`, you should see the application interface!

Now you got cloud metric running the app and mongodb in a single docker container :clap: :clap: :clap:


**External Mining and Monitoring files**

To register you environment on cloud metric app, you need to run:

```resource_mining.py``` - which meters your individual instances and sends the data to the app's monogDB

```monitoring.py``` - which retrieve the resources (CPU, Memory, and Disk) utilization in your instance and send the data to app's monogoDB
every `60` seconds. You can change this value to anything value you want.

To successfully run this files you need to install [pymongo](https://api.mongodb.com/python/current/), 
and [psutil](https://pypi.python.org/pypi/psutil) by using the following commands:

`sudo apt-get install python-pymongo`

`sudo apt-get install python-psutil`

Once installation is done you simply run the `resource_miner.py` once by typing:

`python resource_miner.py [IP of your mongoDB] [Your Cluster Name]`

and run `monitor.py` as a process by typing:

`python monitor.py [IP of your monogDB] [Your Cluster Name]`

Congratulations! You've got your environment monitored and meter by Cloud Metric :clap::clap::clap:






  

