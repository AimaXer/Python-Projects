import os, sys
import yaml

class dataManagement():

    def loadData(base_data_path):
        # Variables
        data = []
        processed_data = []

        # Function gathers data from all files in directory, in (YYYY-MM-DD, HH:mm, price) format
        data_files = [file for file in os.listdir(base_data_path)]
        for file_name in data_files:
            try:
                with open(base_data_path + "\\" + file_name, 'r') as file:
                    for line in file:
                        processed_data.append(line[:-2])
            except IOError as e:
                print("Error: Could not load data from path : " + base_data_path + file_name + " - (" + str(e) + ")")
                return

        # Returns list of DATA's gathered from all files located in 'base_data_path' directory
        return processed_data

    def loadConfig():
        # Function gathers parameters from .\config\admin.conf' file in dict format
        with open(os.path.dirname(sys.argv[0]) + '\\config\\admin.conf', 'r') as file:
            data = yaml.load(file)

        # Returns list of arguments key - value
        return data