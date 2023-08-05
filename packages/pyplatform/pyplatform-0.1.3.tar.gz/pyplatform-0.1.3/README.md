### Pyplatform is a data analytics platform architeture built around Google BigQuery in a hybrid cloud environment.

the platorm:
-  provides fast, scalable and reliable SQL database
-  abstracts away the infrastuture by builiding data pipelines with serverless compute solutions in python runtime environments
-  simplifies development environment by using jupyter lab as the main tool

<img align="left" style="width: 1200px;" src="https://github.com/mhadi813/pyplatform/blob/master/samples/pyplatform%20image/pyplatform.png">

## Installation


```python
pip install pyplatform
```

## Setting up development environment
```
git clone https://github.com/mhadi813/pyplatform
cd pyplatform
conda env create -f pyplatform_dev.yml
```


### [Environment variables](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#saving-environment-variables)





```python
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/default_service_account.json'
os.environ['DATASET'] = 'default_bigquery_dataset_name'
os.environ['STORAGE_BUCKET'] = 'default_storage_bucket_id'
```

## Usage
## common data pipeline architectures:

### - Http sources

<img align="left" style="width: 740px;" src="https://github.com/mhadi813/pyplatform/blob/master/samples/pyplatform%20image/http_sources.png">

### - On-prem servers

<img align="left" style="width: 740px;" src="https://github.com/mhadi813/pyplatform/blob/master/samples/pyplatform%20image/on-prem_sources.png">

### - Bigquery integration with Azure Logic Apps

<img align="left" style="width: 740px;" src="https://github.com/mhadi813/pyplatform/blob/master/samples/pyplatform%20image/logic_apps_integration.png">

### - Event driven ETL process

<img align="left" style="width: 740px;" src="https://github.com/mhadi813/pyplatform/blob/master/samples/pyplatform%20image/event_driven.png">

### - Streaming pipelines

<img align="left" style="width: 740px;" src="https://github.com/mhadi813/pyplatform/blob/master/samples/pyplatform%20image/streaming.png">

## Exploring modules


```python

import pyplatform as pyp
pyp.show_me()

```
