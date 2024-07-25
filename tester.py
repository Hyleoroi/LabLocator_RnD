'''
Test script to check for mistakes in the script without the use of the databricks notebook< Fill in a request ub the /data/test_request.json file
'''

from main import main
import json

path = "C://Users//Gebruiker//coding//LabLocator_RnD//data//test_request.json"

try:
    with open(path, 'r') as json_file:
        inputparams = json.load(json_file)
        print(inputparams)
        main(inputparams,istester=True)
        json_file.close()
except Exception as e:
    print(e)
