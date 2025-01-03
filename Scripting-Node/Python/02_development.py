#===============================================================================
# Name   : development
# Author : Ahmad Alamiri
# Version: v1.0 (for Compound Discoverer 3.3 SP3; CD3.3.3)
# Aim    : A Python script that saves data exported from Compound Discoverer in the form of a 'json' file, which can subsequently be used in script debugging and development. 
#===============================================================================


# Load Libraries
# Load a package/module that is capable of reading JSON files.
import json    # JSON encoder and decoder.
import os    # Miscellaneous operating system interfaces.
import sys    # System-specific parameters and functions.
import traceback    # Print or retrieve a stack traceback.
#==============================


# Read Command Line Arguments
# Read the Command Line arguments passed by Compound Discoverer upon initiation of the scripting node feature.
# We are only interested in the 2nd ([1]) argument, which contains the location of the would be newly-created node_args.json file. 
# This file contains essential information about the exported data, including location(s) of the exported text files as well as the row IDs, columns, and column attributes of the exported tables.
# Define Input File ('node_args.json' file) - located in the 2nd ([1]) argument of the variable 'args'.
input_file = sys.argv[1]
#==============================


# Read 'node_args.json' file.
try:
    with open(input_file, mode='r') as f:
        node_args = json.load(f)
    print('Successfully read Compound Discoverer node_args.json file!')

except Exception as e:
    print('Failed to read Compound Discoverer node_args.json file: ' + str(e))
    print(traceback.format_exc())
    exit(1)      
#==============================


# Debugging/Development
# Save data ('script_data.json').
# First define the script data objects to be saved.
script_data = {
    'sys_argv': sys.argv,
    'input_file': input_file,
    'node_args': node_args
    }


# Define Output File name, directory, and path.
# This will save the 'script_data.json' file in the same location as the script used in the Scripting Node - adjust file save location as desired.
script_data_outfilename = 'script_data.json'
directory = os.path.dirname(sys.argv[0])
script_data_outfilepath = os.path.join(directory, script_data_outfilename)


# Save data.
try:
    with open(script_data_outfilepath, mode='w') as f:
        json.dump(script_data, f)
    print('Successfully saved script_data.json file!')

except Exception as e:
    print('Failed to save script_data.json file: ' + str(e))
    print(traceback.format_exc())
    exit(1)


# Load the saved 'script_data.json' file for debugging or script development purposes.
# Be sure to adjust the current Working Directory. Alternatively, point to the path of the saved file.
# working_directory = os.path.dirname(sys.argv[0])
# os.chdir(working_directory)


# Uncomment/use command line below as needed.
# try:
#     with open('script_data.json', mode='r') as f:
#         script_data = json.load(f)
#     print('Successfully read script_data.json file!')

# except Exception as e:
#     print('Failed to read script_data.json file: ' + str(e))
#     print(traceback.format_exc())
#     exit(1)
#==============================


# Continue script development...