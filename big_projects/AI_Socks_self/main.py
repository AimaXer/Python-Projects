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

    def trendCalculation(self, partial_data):
        change_sum = 0

        for interator in range(0, len(partial_data) - 1):
            change_sum += (partial_data[interator] - partial_data[interator + 1])
        return change_sum / len(partial_data)
    
    def changeCalculation(self, partial_data):
        change_procentage_sum = 0.0
        counter = 1
        
        for i in range(0, len(partial_data) - 1):
            if abs(partial_data[i] - partial_data[i + 1]) > config_variables['PROFIT_PROCENTAGE']:
                change_procentage_sum += abs(partial_data[i] - partial_data[i + 1]) /  partial_data[i] * 100
                counter += 1

        return change_procentage_sum / counter

    def makePrediction(self, data_high, data_low, trend, change_rate):
        if trend < 0:
            # if abs(data_high[0] - data_low[len(data_low) - 1]) > ((config_variables['PROFIT_PROCENTAGE'] * config_variables['COMPARE_RANGE']) / 4):
            return -1
        elif trend > 0:
            # if abs(data_low[0] - data_high[len(data_high) - 1]) > ((config_variables['PROFIT_PROCENTAGE'] * config_variables['COMPARE_RANGE']) / 4):
            return 1
        return 0
            

    def main(self, data):
        size = int(len(data[config_variables['MAIN_COLUMN_NAME']]) / config_variables['COMPARE_RANGE'])
        accuracy = 0
        skipped_predictions = 0
        predictions_made = 0
        
        # print("\n" + str(datetime.now().time()) + " - STARTING CALCULATIONS - ")
        # with alive_bar(size) as bar:
        for partial_data_iterator in range(0, size):
            # data partitioning
            partial_data_high = [data[config_variables['MAIN_COLUMN_NAME']][iterator] for iterator in range(partial_data_iterator * config_variables['COMPARE_RANGE'], ((partial_data_iterator + 1) * config_variables['COMPARE_RANGE']) - 1)]
            partial_data_low = [data[config_variables['COMPARE_COLUMN_NAME']][iterator] for iterator in range(partial_data_iterator * config_variables['COMPARE_RANGE'], ((partial_data_iterator + 1) * config_variables['COMPARE_RANGE']) - 1)]

            # avrage_partial_change_rate - avrage procentage change in data in COMPARE_RANGE for given range
            avrage_partial_change_rate = round(self.changeCalculation(partial_data_high), 4)

            # UDS_partial_trend - values - (range -1 : 1) 1 - down trend , 0 - stady trend , 1 - up trend 
            UDS_partial_trend = round(self.trendCalculation(partial_data_high), 4)

            # prediction - return values (1 (up) ,0 (none),-1 (down)) dependung on given procentage 
            prediction = self.makePrediction(partial_data_high, partial_data_low, UDS_partial_trend, avrage_partial_change_rate)

            if prediction > 0:
                predictions_made += 1
                acc_aded = False
                for iterator in range(0, config_variables['MAX_HOURS_INTERVAL']):
                    if len(data) >= size * partial_data_iterator + iterator:
                        if partial_data_low[len(partial_data_low) - 1] < data[config_variables['MAIN_COLUMN_NAME']][size * partial_data_iterator + iterator]:
                            if not acc_aded:  
                                accuracy += 1
                                acc_aded = True
                
            elif prediction < 0:
                predictions_made += 1
                acc_aded = False
                for iterator in range(0, config_variables['MAX_HOURS_INTERVAL']):
                    if len(data) >= size * partial_data_iterator + iterator:
                        if partial_data_high[len(partial_data_high) - 1] > data[config_variables['COMPARE_COLUMN_NAME']][size * partial_data_iterator + iterator]:
                            if not acc_aded:  
                                accuracy += 1
                                acc_aded = True
            else:
                skipped_predictions += 1

            
            # bar()

        # print(str(datetime.now().time()) + " - CALCULATIONS COMPLETED - ")
        if skipped_predictions == size:
            result = 0
        else:
            result = accuracy / (size - skipped_predictions) * 100

        return round(result, 2), round(predictions_made / size * 100, 2)

class MainFunctions():

    def bestSetFinding(self, data):
        best_accuracy = 0.0
        best_prediction_procentage = 0.0
        best_COMPARE_RANGE = 0
        best_MAX_HOURS_INTERVAL = 0
        best_PROFIT_PROCENTAGE = 0

        a = 10
        b = 20
        
        with alive_bar(b - a) as bar:
            # for i in range(a, b):
            config_variables['COMPARE_RANGE'] = 49
            config_variables['MAX_HOURS_INTERVAL'] = 10
            config_variables['PROFIT_PROCENTAGE'] = 29 / 100

            accuracy, predictions_made = Calculations().main(data)

            if accuracy > best_accuracy:
                best_COMPARE_RANGE = config_variables['COMPARE_RANGE']
                best_MAX_HOURS_INTERVAL = config_variables['MAX_HOURS_INTERVAL']
                best_PROFIT_PROCENTAGE = config_variables['PROFIT_PROCENTAGE']
                best_accuracy = accuracy
                best_prediction_procentage = predictions_made
            bar()

        return best_accuracy, best_prediction_procentage, best_COMPARE_RANGE, best_MAX_HOURS_INTERVAL, best_PROFIT_PROCENTAGE


    # Main function
    def main(self):
        try:
            data = DataManagement.loadData(DataManagement, os.path.dirname(sys.argv[0]) + config_variables['BASE_DATA_PATH'])
        except IOError as e:
            print(str(datetime.now().time()) + "Error: Error in loadData - (" + str(e) + ")")
            return
        
        accuracy, predictions_made, i1, i2, i3 = self.bestSetFinding(data)

        print(" - Result (accuracy) : " + str(accuracy) + "% - \n" + " - Predictions made : " + str(predictions_made) + "% -")
        print("\n - For variables : \n - COMPARE_RANGE : " + str(i1) + "\n - MAX_HOURS_INTERVAL : " + str(i2) + "\n - PROFIT_PROCENTAGE : " + str(i3)+ '\n')

if __name__ == '__main__':
    MainFunctions().main()
    print('\n' + str(datetime.now().time()) + " - DONE - ")