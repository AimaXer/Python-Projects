# Import main class from '.\\libraries'
from libraries.dataManagement import dataManagement as dM
import sys, os

# Global variables in single dict variable
global_vars = {
    "BASE_DATA_PATH":"" + os.path.dirname(sys.argv[0]) + "\\DATA"
}

# Main function
def main():
    try:
        data = dM.loadData(global_vars['BASE_DATA_PATH'])
    except:
        print("Error: Error in loadData")
        return
    #DEBUG
    print(str(data[0]))

    #DEBUG

if __name__ == '__main__':
    main()





