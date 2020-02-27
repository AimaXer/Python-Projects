import os, sys
import pandas as pd
import yaml
from datetime import datetime
from alive_progress import alive_bar

class DataManagement():

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
        base_dir = os.path.dirname(sys.argv[0])
        with open(base_dir + '.\\config\\admin.conf', 'r') as file:
            data = yaml.load(file)

        # Returns list of arguments key - value
        return data

# Config variables
config_variables = DataManagement.loadConfig(DataManagement)

class Calculations():

    def trend_calculation(self, partial_data):
        change_sum = 0

        for interator in range(0, len(partial_data) - config_variables['MAX_HOURS_INTERVAL']):
            change_sum += (partial_data[interator] - partial_data[interator + config_variables['MAX_HOURS_INTERVAL']])
        return change_sum / len(partial_data)
    
    def change_calculation(self, partial_data):
        change_procentage_sum = 0.0
        
        for i in range(0, len(partial_data) - 1):
            change_procentage_sum += abs(partial_data[i] - partial_data[i + 1]) /  partial_data[i] * 100

        return change_procentage_sum / config_variables['COMPARE_RANGE']

    def makePrediction(self, data):
        return 1

    def main(self, data):
        ret_tab = []
        size = int(len(data[config_variables['MAIN_COLUMN_NAME']]) / config_variables['COMPARE_RANGE'])
        
        print("\n" + str(datetime.now().time()) + " - STARTING CALCULATIONS - ")
        with alive_bar(size) as bar:
            for partial_data_iterator in range(0, size):
                # data partitioning
                partial_data = [data[config_variables['MAIN_COLUMN_NAME']][iterator] for iterator in range(partial_data_iterator * config_variables['COMPARE_RANGE'], ((partial_data_iterator + 1) * config_variables['COMPARE_RANGE']) - 1)]

                # avrage_partial_change_rate - avrage procentage change in data in COMPARE_RANGE for given range
                avrage_partial_change_rate = round(self.change_calculation(partial_data), 4)

                # UDSTrend - values - (range -1 : 1) 1 - down trend , 0 - stady trend , 1 - up trend 
                UDS_partial_trend = round(self.trend_calculation(partial_data), 4)

                # prediction - 
                prediction = self.makePrediction(partial_data)

                # prediction check
                for i in range(0, config_variables['MAX_HOURS_INTERVAL']):
                    pass

                
                bar()
                ret_tab.append(UDS_partial_trend)
        print(str(datetime.now().time()) + " - CALCULATIONS COMPLETED - ")
        

        return ret_tab

class MainFunctions():
    # Prinf calculation results function
    def resultGUI(self, results_tab):
        print(str(datetime.now().time()) + " --- CALCULATION RESULTS --- :")
        for iterator in enumerate(len(results_tab)):
            print(str(results_tab[iterator]))

    # Main function
    def main(self):
        try:
            data = DataManagement.loadData(DataManagement, os.path.dirname(sys.argv[0]) + config_variables['BASE_DATA_PATH'])
        except IOError as e:
            print(str(datetime.now().time()) + "Error: Error in loadData - (" + str(e) + ")")
            return
        
        ret = Calculations().main(data)
        print(str(ret))
        # print(str(data[config_variables['MAIN_COLUMN_NAME']][0]))

if __name__ == '__main__':
    MainFunctions().main()
    print('\n' + str(datetime.now().time()) + " - DONE - ")