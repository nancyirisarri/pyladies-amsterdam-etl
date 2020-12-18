PyLadies Amsterdam ETL Repository
==============================

Repository for PyLadies Amsterdam talk on December 22, 2020.

This repository follows the [Cookiecutter Data Science](https://github.com/BigDataRepublic/cookiecutter-data-science) 
repository structure.

The talk slides can be found [here](https://drive.google.com/file/d/1vnCyq5y_vQLuJ3A5D99D4caTzQmSeS4Y/view?usp=sharing).

## tl;dr
* The script `pyladiesamsterdametl/data/extract.py` indicates which data sources to download, which are in turn needed 
by the R scripts.
    * The code downloads data from the [COVID-19 dataset - RIVM Data Catalogus](https://data.rivm.nl/covid-19/).
* The script `pyladiesamsterdametl/data/transform.py` executes the R scripts 
under `pyladiesamsterdametl/models` on the data.
    * For example, a script `pyladiesamsterdametl/models/source_1/source1.R` performs operations on the data
    and writes an output data frame to _source1.csv_.
    * To illustrate Cloud Monitoring, the script `pyladiesamsterdametl/models/source_2/source2.R` throws an error. See
    the section _Running in Kubernetes Engine, step 5_ to set up email alerts for errrors.
* The output CSV files are uploaded to Google BigQuery. The dataset name can be changed, but the table name will be
the same as the R script file name.
    * For example, for a script `pyladiesamsterdametl/models/source_1/source1.R` as a dataset and table 
    `source_1.source1`.
* The data in Google BigQuery tables can be used further.
    * For example, to make a dashboard of [Daily Updates of Total Hospital Admissions of COVID-19 Patients by Province](https://datastudio.google.com/s/s0uOTLi4KEA).   
* The application is deployed to Google Kubernetes Engine as a CronJob that runs daily. The configuration files under
`k8s-deploy/` indicate which sources and R scripts should be executed, as well as the Google Cloud Platform project
to use and the Google BigQuery dataset to write the output to.

Project Organization
------------

    ├── README.md                   <- The top-level README for developers using this project.
    ├── data
    │   ├── external                <- Data from third party sources.
    │   ├── interim                 <- Intermediate data that has been transformed.
    │   ├── processed               <- The final, canonical data sets for modeling.
    │   └── raw                     <- The original, immutable data dump.
    │
    ├── docs                        <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models                      <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks                   <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                               the creator's initials, and a short `-` delimited description, e.g.
    │                               `1.0-jqp-initial-data-exploration`.
    │
    ├── references                  <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports                     <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures                 <- Generated graphics and figures to be used in reporting
    │
    ├── environment.yml             <- The conda environment file to reproduce the analysis environment. eg.
    │                               `conda env create -f environment.yml`
    │
    ├── githubrequirements.txt      <- Pip references to github repo's, referred to by `environment.yml`
    │
    └── pyladiesamsterdametl        <- Source code for use in this project.
        ├── __init__.py             <- Makes pyladiesamsterdametl a Python module
        │
        ├── main.py                 <- Runs the ETL pipeline
        │
        ├── data                    <- Scripts to download or generate data
        │   |   extract.py
        │   |   load.py
        │   └── transform.py
        │
        ├── features                <- Scripts to turn raw data into features for modeling
        │
        ├── logs                    <- Scripts to handle logs
        │   └── logs.py
        │
        ├── models                  <- Scripts to make calculations, train models, make predictions
        |   ├── source_1
        |   |      └── source1.R    <- Aggregate hospital admissions by province.
        │   └── source_2
        |           └── source2.R   <- Throws an error.
        │
        └── visualization           <- Scripts to create exploratory and results oriented visualizations


--------

## Getting started

Your local Python environment should be up and running with a Conda environment:
```shell script
conda env create -f environment.yml
```

## Setup

1. In the Google Cloud Platform console, make a [new project](https://console.cloud.google.com/projectcreate).

2. To run commands programatically instead of using the Google Cloud Platform console,
install and initialize the [Cloud SDK](https://cloud.google.com/sdk/docs/quickstart). 

3. Make a Kubernetes Engine cluster. You can use the Google Cloud Platform console or the following commands:
    1. Set environment variable `PROJECT_NAME` with the name of the project that you just made above. 
    2. Set environment variable `CLUSTER_NAME` with a desired cluster name.
    3. If you installed the Cloud SDK you can run the following command, otherwise do the same from the 
    project console:
    ```
    gcloud beta container --project $PROJECT_NAME clusters create $CLUSTER_NAME --zone "europe-west4-a" --no-enable-basic-auth --cluster-version "1.16.15-gke.4300" --release-channel "None" --machine-type "e2-medium" --image-type "COS" --disk-type "pd-standard" --disk-size "100" --metadata disable-legacy-endpoints=true --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --num-nodes "3" --enable-stackdriver-kubernetes --enable-ip-alias --network "projects/$PROJECT_NAME/global/networks/default" --subnetwork "projects/$PROJECT_NAME/regions/europe-west4/subnetworks/default" --default-max-pods-per-node "110" --no-enable-master-authorized-networks --addons HorizontalPodAutoscaling,HttpLoadBalancing --enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0    
    ```

4. Since we want to run the application from a Kubernetes cluster, [create a service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts). 
For this application, it needs the _Storage Admin_ and _BigQuery Admin_ permissions. Then, create a key
for the service account and download it to your computer as a JSON file. 

5. [Download](https://www.docker.com/products/docker-desktop) and install Docker.

## Running Locally
1. Build the image:
    ```shell script
    cd docker-local
    ./build.sh
    ```

2. To run the container locally:
    1. In the file `docker-local/run.sh`, change the `-v` flag to the path of the service account key 
    (JSON file) that you downloaded in _Setup, step 4_. 
    2. In the file `docker-local/env.list`, change the values of the following variables to the name 
    of the Google Cloud Platform project that you created in _Setup, step 1_:
        * RAW_DATA_PROJECT_GCP
        * LOG_FILES_PROJECT_GCP
        * GOOGLE_CLOUD_PROJECT
    3. Run the following command: 
        ```shell script
        cd docker-local
        ./run.sh
        ```

3. Hopefully everything worked. You can check by going to the _Google BigQuery_ service of your 
Google Cloud Platform project. There should be a dataset _source_1_ and table _source1_. 

## Running in Kubernetes Engine
1. Build the image:
    ```shell script
    cd docker-local
    ./build.sh
    ```

2. Tag the image using your Google Cloud Platform project as an environment variable _PROJECT_NAME_:
    ```shell script
    docker tag pyladies-amsterdam-etl eu.gcr.io/${PROJECT_NAME}/pyladies-amsterdam-etl     
    ```

3. In order for the pods in Kubernetes Engine to access the image, push it to Container Registry. 
    1. [Configure Docker](https://cloud.google.com/container-registry/docs/advanced-authentication#gcloud-helper) 
    to authenticate directly with Container Registry:
    ```shell script
    # You may already be logged in, but run the following to be sure.
    gcloud auth login
    gcloud auth configure-docker
    ``` 
    2. Push the image to Container Registry:
    ```shell script
    docker push eu.gcr.io/${PROJECT_NAME}/pyladies-amsterdam-etl
    ```

4. Deploy the application as a CronJob in Kubernetes Engine.
    1. Install Kubernetes command line client _kubectl_:
    ```shell script
    gcloud components install kubectl
    ```
    2. Communicate with the cluster created in _Setup, step 3_
    ```shell script
    gcloud container clusters get-credentials $CLUSTER_NAME --project=$PROJECT_NAME --zone=europe-west4-a
    ```
    3. Encode the service account key so that it can be applied as a [secret object](https://cloud.google.com/kubernetes-engine/docs/concepts/secret).
    To do this, depending on your platform you can use a tool such as `base64`. In the file _k8s-deploy/secrets.yaml_, replace _BASE64_ENCODED_KEY_ 
    with the encoded key.
    4. Apply the configuration files:
    ```shell script
    kubectl apply -f k8s-deploy/namespace.yaml
    kubectl apply -f k8s-deploy/secrets.yaml
    kubectl apply -f k8s-deploy/configmap.test.yaml
    kubectl apply -f k8s-deploy/cronjob.test.yaml
    ```
   
5. Create an alert:
    1. In the Google Cloud Platform console, go to _Logging_ and then _Logs-based Metrics_. Create a metric for the following 
    query, replacing _PROJECT_NAME_ and _CLUSTER_NAME_ to your values:
    ```shell script
    resource.type="k8s_container"
    resource.labels.project_id="PROJECT_NAME"
    resource.labels.location="europe-west4-a"
    resource.labels.cluster_name="CLUSTER_NAME"
    resource.labels.namespace_name="pyladies-amsterdam-etl"
    textPayload:"CRITICAL"      
    ```
    2. Find the newly-created Metric and click on _Create alert for metric_. The default values of 
    **Aggregator** as _sum_, **Period** of _10 minutes_, and the **Configuration** can be left as is.
    In step 2, add if needed as a _Notification Channel_ and set the e-mail address that will receive the alert.

<p><small>Project based on the <a target="_blank" href="https://github.com/BigDataRepublic/cookiecutter-data-science">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
