import os, sys
import pandas as pd
import yaml
from datetime import datetime

class dataManagement():

    def loadData(self, base_data_path):
        # Variables
        processed_data = []

        # Function gathers data from all files in directory, in (YYYY-MM-DD, HH:mm, price, ...) format
        data_files = [file for file in os.listdir(base_data_path)]
        for file_name in data_files:
            try:
                print(str(datetime.now().time()) + " - LOADING DATA - ")
                processed_data = pd.read_csv(str(base_data_path + "\\" + file_name))
                print(str(datetime.now().time()) + " - DATA LOADED - ")
            except IOError as e:
                print(str(datetime.now().time()) + "Error: Could not load data from path : " + base_data_path + file_name + " - (" + str(e) + ")")
                return

        # Returns list of DATA's gathered from all files located in 'base_data_path' directory
        return processed_data

    def loadConfig(self):
        # Function gathers parameters from .\config\admin.conf' file in dict format
        with open(os.path.dirname(sys.argv[0]) + '\\config\\admin.conf', 'r') as file:
            data = yaml.load(file)

        # Returns list of arguments key - value
        return data