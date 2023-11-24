# Databricks notebook source
# MAGIC  %pip install -r requirements.txt

# COMMAND ----------

import os
from main import main
import json

folder = "/dbfs/mnt/production/dataplatform/silver/sharepoint/innolab/"

for filename in os.listdir(folder):
    path = os.path.join(folder, filename)
    try:
        with open(path, 'r') as json_file: 
            inputparams = json.load(json_file)
            main(inputparams)
            json_file.close()
    except Exception as e:
        print(filename, e)
        continue
