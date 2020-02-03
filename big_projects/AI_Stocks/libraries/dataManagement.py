import os
class dataManagement():

    def loadData(base_data_path):
        # Variables
        data = []

        # Function gathers data from all files in directory, in (YYYY-MM-DD, HH:mm, price) format
        data_files = [file for file in os.listdir(base_data_path)]
        for file_name in data_files:
            try:
                with open(base_data_path + "\\" + file_name, 'r') as file:
                    data.append(file.read())
            except:
                print(print("Error: Could not load data from path : " + base_data_path + file_name))
                return

        # Returns list of DATA's gathered from all files located in 'base_data_path' directory
        return data