PyLadies Amsterdam ETL Repository
==============================

Repository for PyLadies Amsterdam talk on December 22, 2020.

Note that the `Project Organization` below is provided as an example, so many directories are empty.

Project Organization
------------

    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── environment.yml    <- The conda environment file to reproduce the analysis environment. eg.
    │                         `conda env create -f environment.yml`
    │
    ├── githubrequirements.txt <- Pip references to github repo's, referred to by `environment.yml`
    │
    └── pyladies.amsterdam.etl                <- Source code for use in this project.
        ├── __init__.py    <- Makes pyladies.amsterdam.etl a Python module
        │
        ├── data           <- Scripts to download or generate data
        │   |   extract.py
        │   |   load.py
        │   └── transform.py
        │
        ├── logs           <- Scripts to handle logs
        │   └── logs.py
        │
        ├── models         <- Scripts to train models and then use trained models to make
        │                     predictions
        │
        └── visualization  <- Scripts to create exploratory and results oriented visualizations


--------

## Getting started:

One should be up and running with the following steps.

### Shortcut creating the environment using conda 
To get started in this project, you first need to setup an environment:

    conda env create -f environment.yml


<p><small>Project based on the <a target="_blank" href="https://github.com/BigDataRepublic/cookiecutter-data-science">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
