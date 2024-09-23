# Databricks notebook source
# DBTITLE 1,Install Required Packages
# MAGIC %sh
# MAGIC uv pip install geopandas fpdf2 --link-mode=copy

# COMMAND ----------

# DBTITLE 1,Import Required Libraries
import glob
import json
import os

from main import main

# COMMAND ----------

# DBTITLE 1,Load JSON Files into a List of Dictionaries
# Define the path with a wildcard to match all JSON files in the specified directory
wildcard_path = "/dbfs/mnt/production/dataplatform/silver/sharepoint/innolab/*.json"
json_files = glob.glob(wildcard_path)

# Load the content of each JSON file as a dictionary and store them in json_list
json_list: list[dict] = []
for json_file in json_files:
    with open(json_file, 'r') as file:
        json_list.append(json.load(file))

# COMMAND ----------

try:
    main(json_list[4])
except Exception as e:
    print(json_list[4], e)

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
