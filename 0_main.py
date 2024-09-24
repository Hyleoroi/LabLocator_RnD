# Databricks notebook source
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

# DBTITLE 1,Main
# Run the main function for all requests from json_list
for json_dict in json_list:
    try:
        main(json_dict)
    except Exception as e:
        print(f"Error generating req-id: json_dict['req-id']", e)
        continue
