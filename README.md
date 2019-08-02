# Pharmaceutical Patents Similarity using LSTM and CNN
<sub>By: Heba El-Shimy</sub>
<br>
<sub>For: Heriot-Watt Masters Thesis</sub>
<hr>

## Contents:
1. [Description](#description)
1. [Installation notes](#installation-notes)
1. [Running the program](#running-the-program)

<br>

## Description:

This is a program that is able to accepts new invention documents in the form of PDF files, parse the textual as well as visual and chemical content and compare it to a database of patents in the pharmaceutical field. The program's output is the most similar patents found in the database that cross a previously set similarity threshold. The similar patents can then be reviewed by a subject matter expert to take a decision on whether the similarity is significant enough to form an overlap, thus the document at hand can not be granted the patent.

<br>

## Installation notes:

This repository contains a docker file that will automatically install all the programs dependencies and can run on any operation system on a local machine or in the cloud.

In order to start working with the program, you will need to install Docker, Docker Compose, and optionally Git if you want to clone or fork this repository. Please check the links below to install these requirements.

<br>

**For Windows**

- [Download Docker for Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
- [Docker installation steps](https://docs.docker.com/docker-for-windows/install/)
- [Get started with Docker](https://docs.docker.com/docker-for-windows/)

<br>

**For Linux Ubuntu**

- [Install Docker on Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- [Post-installation notes and managing docker as non-root](https://docs.docker.com/install/linux/linux-postinstall/)

> The above steps will work on any Debian-based linux, but for other distros, please check the official documentation on Docker [https://docs.docker.com/](https://docs.docker.com/)

<br>

**For MacOS**

- [Download Docker of MacOS](https://hub.docker.com/editions/community/docker-ce-desktop-mac)
- [Docker installation steps](https://docs.docker.com/docker-for-mac/install/)
- [Get started with Docker](https://docs.docker.com/docker-for-mac/)

<br>

**General links and notes for any OS**

- [Download and install Docker Compose](https://docs.docker.com/compose/install/)
- [Get started with Docker Compose](https://docs.docker.com/compose/gettingstarted/)

<br>

## Running the program

1. Download or clone this repository and navigate into it using any command line interface.
  
2. If you're using MacOS or Windows, make sure that Docker service is running in the background.
  
3. Run the following command to start the containers. Note that for the first run, docker will install the base images and all dependencies, it is expected to take around 20 minutes (depending on the network and computer specs) for it to download and install everything and for the containers to be up.  

```
sudo docker-compose -f docker-compose-LocalExecutor.yml up -d
```  

4. Check if containers are running by typing in the following command. Make note of the `CONTAINER ID` for the conatiner with `NAME` __project_webserver_1__.   

```
docker ps
```  

5. You will need to gain access inside the airflow container (named project_webserver), to be able to run some other programs. To access the container, type in the followinf command and replace the word `CONTAINER_ID` with the value noted in the previous step.  

```
docker exec -it CONTAINER_ID /bin/bash
```  

6. Run the Jupyter Notebooks by typing in the following command:  

```
jupyter notebook --no-browser --ip=0.0.0.0
```  

Then navigate to `http://localhost:8888` in your browser.

A webpage will open with the current folder structure, navigate to the `notebooks` folder and click on the notebook you would like to run.  


> Note: These notebooks contain only a very limited subset of the data and were used mainly as a sandbox for quickly testing and iterating over ideas before writing them to the production scripts that run on airflow on the full dataset.

7. Airflow web server is running by default in the background, to access its web interface navigate to `http://localhost:8080` in your browser. From there you can manage all DAGs and Tasks by running them, viewing their logs, deleting them, etc.  

<br>

## Pipelines

**1. Training Pipeline**
This pipeline's tasks will be triggered automatically when a file is added/created inside the `Dataset` folder. It can also be started manually through the web interface. It's tasks can be tested as units using airflow by typing the following command:  

```
airflow test dag_id task_id execution_date
```

For example to test the text_preprcessing task in the training pipeline, in the previous command you will replace
`dag_id`: training_pipeline
`task_id`: create_dataset
`execution_date`: 2019-08-01

The pipeline looks as follows:
