# Import main class from '.\\libraries'
from libraries.dataManagement import dataManagement as dM
from libraries.strategiesFunctions import strategiesFunctions as sF
import sys, os
from datetime import datetime

# Global variables in single dict variable
global_vars = dM.loadConfig()
trend_effectivness = []

# Prinf calculation results function
def resultGUI(results_tab):
    print(str(datetime.now().time()) + " --- CALCULATION RESULTS --- :")
    for iterator in enumerate(len(results_tab)):
        #print(str(iterator + 1) + ". " + str(results_tab[iterator] * 100)) + "%")
        print(str(results_tab[iterator]))

# Main function
def main():
    try:
        data = dM.loadData(os.path.dirname(sys.argv[0]) + global_vars['BASE_DATA_PATH'])
    except IOError as e:
        print(str(datetime.now().time()) + "Error: Error in loadData - (" + str(e) + ")")
        return
    
    #trend_effectivness = sF.trendStrategy(data, global_vars['CALCULATE_INTERVAL'])
    
    #trend_effectivness.append(sF.trendStrategy(data, 48, 40))
    
    sF.main(data)

    resultGUI(trend_effectivness)
if __name__ == '__main__':
    main()





