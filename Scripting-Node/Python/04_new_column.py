#===============================================================================
# Name   : new_column
# Author : Ahmad Alamiri
# Version: v1.0 (for Compound Discoverer 3.3 SP3; CD3.3.3)
# Aim    : A Python script that creates a new column and imports it back into Compound Discoverer. 
#===============================================================================


# Load Libraries
# Load a package/module that is capable of reading JSON files.
import json    # JSON encoder and decoder.
import os    # Miscellaneous operating system interfaces.
import pandas as pd  # Pandas is a Python library for data analysis and manipulation.
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


# Define Templates
# Define 'node_response.json' File
# Define the 'node_response' variable using the data derived from the imported JSON file (here, 'node_args'). 
node_response = {
    'CurrentWorkflowID': node_args['CurrentWorkflowID'],
    'ExpectedResponsePath': node_args['ExpectedResponsePath'],
    'ResultFilePath': node_args['ResultFilePath'],
    'NodeParameters': node_args['NodeParameters'],
    'Version': node_args['Version'],
    'Tables': node_args['Tables']
}
#==============================


# Load Table(s)
# Read table(s) exported from Compound Discoverer. 
# Tables are exported as tab-separated text files. 
# In this example, read the contents of the first table's datafile.
# Define new variable 'GCEI_Compounds_table' and read the 'GC EI Compounds' data into it.
GCEI_Compounds_table = pd.read_table(node_args['Tables'][0]['DataFile'], header=0)
#==============================


# Create Column(s)
# In this example, we will create a column 'New CD Column'.
# We will assign this column values 1 to number of rows of 'GC EI Compounds' table (the actual values of the column are irrelevant, in this case).
# We will use this column to demonstrate how to add a column to be imported back into Compound Discoverer.
new_CD_column = list(range(1, len(GCEI_Compounds_table) + 1))
#==============================


# Add Column(s).
# Add new column to the data table (here, 'modified_GCEI_Compounds_Table').
# By defining a column name, we can have both the data frame and Compound Discoverer (upon import) display 'New CD Column' as the column's heading (name).
modified_GCEI_Compounds_Table = GCEI_Compounds_table.copy()
modified_GCEI_Compounds_Table['New CD Column'] = new_CD_column
#==============================


# Create a new column using the JSON structure.
# Note: the 'ColumnName' value is the same as that of 'New CD Column' defined above (modified_GCEI_Compounds_table$new_CD_column in the table/data frame).
# In this example, we will override the 'new_CD_column' now that we are done using it (though, this may not be good practice).
new_CD_column = dict(
    ColumnName = 'New CD Column',
    ID = '',
    DataType = 'Int',
    Options = {}
    )


# Add new column to JSON structure (to be used by 'node_response.json' file). 
# Update the 'node_response' variable previously created - append the list of Tables' 'ColumnDescriptions' by one (for 'new_CD_column').
# Repeat this process for each new column as necessary.
node_response['Tables'][0]['ColumnDescriptions'].append(new_CD_column)
#==============================


# Write Files.
# Write newly created results table as a 'txt' ('.out.txt') file to temporary ('scratch') folder. 
# The '.out.txt' file will be stored in the 'DataFile' field of the 'tables' section of 'node_response' file.
# Substitute 'out.txt' for 'txt' in the would be 'node_response.json' file. 
# Write the information for 'modified_GCEI_Compounds_table'.
result_out_txt = node_response['Tables'][0]['DataFile'].replace('txt', 'out.txt')


# Write newly created table results to file. Note: write files as tab-separated (CSV) text files.
modified_GCEI_Compounds_Table.to_csv(result_out_txt, sep='\t', index=False, encoding='utf-8')


# Update 'node_response.json' table 'DataFile' path (with '.out.txt').
node_response['Tables'][0]['DataFile'] = result_out_txt


# Write 'node_response.json' file. Define 'expectedResponsePath' location.
json_out_file = node_response['ExpectedResponsePath']


# Convert 'node_response' to JSON structure.
try:
    with open(json_out_file, mode='w') as f:
        json.dump(node_response, f)
    print('Successfully saved node_response.json file!')

except Exception as e:
    print('Failed to save node_response.json file: ' + str(e))
    print(traceback.format_exc())
    exit(1)
#==============================


# OPTIONAL
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


# Save 'GCEI_Compounds_table' data.
# In this section, we will save the 'GCEI_Compounds_table' data as a tab-separated text file. However, the table can still be accessed otherwise using the 'script_data.json' file.
# Be sure to adjust the current Working Directory; othewise, the file will be saved in the same directory as the Python.exe file used to run the script.
# working_directory = os.path.dirname(sys.argv[0])
# os.chdir(working_directory)
# print(working_directory)
# Define Output File name, directory, and path.
# This will save the 'GCEI_Compounds_table.txt' file in the same location as the script used in the Scripting Node - adjust file save location as desired.
script_data_table_outfilename = 'GCEI_Compounds_table.txt'
script_data_table_outfilepath = os.path.join(directory, script_data_table_outfilename)


# Save data.
GCEI_Compounds_table.to_csv(script_data_table_outfilepath, sep='\t', index=False, encoding='utf-8')


# OPTIONAL
# Load the saved 'script_data.json' and 'GCEI_Compounds_table.txt' files for debugging or script development purposes.
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


# Load (read) the saved 'GCEI_Compounds_table.txt' file for debugging or script development purposes.
# Uncomment/use command line below as needed.
# GCEI_Compounds_table = pd.read_csv('GCEI_Compounds_table.txt', sep='\t')
#==============================
