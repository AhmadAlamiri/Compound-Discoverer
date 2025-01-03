#===============================================================================
# Name   : new_column_and_new_table
# Author : Ahmad Alamiri
# Version: v1.0 (for Compound Discoverer 3.3 SP3; CD3.3.3)
# Aim    : A Python script that creates a new column and a new table and imports them back into Compound Discoverer. 
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


# Create Column(s) and Table(s)
# In this example, we will create both a new column and a new table.
# We will use the column(s) and table(s) to demonstrate how to add these objects and have them imported back into Compound Discoverer to be read by the application as part of a typical Result file.


# Create Column(s)
# In this example, we will create a column 'New CD Column'.
# We will assign this column values 1 to number of rows of 'GC EI Compounds' table (the actual values of the column are irrelevant, in this case).
# We will use this column to demonstrate how to add a column to be imported back into Compound Discoverer.
new_CD_column = list(range(1, len(GCEI_Compounds_table) + 1))
#==============================


# Create Table(s).
# In this example, we will create a table 'New CD Table' that computes the 'Area Mean' for each 'Genuine' (Control) samples and 'Suspect' (Test) samples (the contents of the table are irrelevant - perform any desired calculation instead).
# We will use this table to demonstrate how to add a table to be imported back into Compound Discoverer.
# Subset 'GCEI_Compounds_table' indices 0, 3, and 23-28, corresponding to 'GC EI Compounds ID', 'Name', and individual Area columns for each of the 6 samples (3 Genuine and 3 Suspect).
new_CD_table = GCEI_Compounds_table.iloc[:, [0, 3, 23, 24, 25, 26, 27, 28]]
new_CD_table.iloc[:, 2:8] = new_CD_table.iloc[:, 2:8].apply(pd.to_numeric, errors='coerce')


# Compute the Mean values (row-wise) for each set of samples.
new_CD_table.insert(2, 'Area Mean (Genuine)', new_CD_table.iloc[:, 2:5].mean(axis=1, skipna=True))    # Indices 2, 3, 4 are the Area columns for Genuine samples.
new_CD_table.insert(3, 'Area Mean (Suspect)', new_CD_table.iloc[:, 6:9].mean(axis=1, skipna=True))    # Indices 6, 7, 8 are the Area columns for Suspect samples.


# Remove the individual Area columns (indices 4:9) since they are no longer necessary.
new_CD_table = new_CD_table.drop(new_CD_table.columns[4:10], axis=1)
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


# Add Table(s)
# We will create two new columns, 'New CD Table ID' and 'New CD Table WorkflowID'. 
# CAUTION: these ID columns are important in how Compound Discoverer indexes the objects of a data table and how it associates them with other objects in other data tables. 
# Therefore, the analyst must follow the proper format and convention to ensure that these two columns' data are correct.
# Define 'New CD Table' 'ID' column (that will eventually have the attribute 'ID' = 'ID' in the JSON file structure). 
# In this example, we will create a new column 'New CD Table ID'.
new_CD_table['New CD Table ID'] = list(range(1, len(new_CD_table) + 1))


# Create another column 'New CD Table WorkflowID'.
new_CD_table['New CD Table WorkflowID'] = node_response['CurrentWorkflowID']


# Create 'Connection Table' data frame, which will eventually be written as a 'Connection Table' text file. 
# This table only requires the ID columns: 'GC EI Compounds ID', 'New CD Table ID', and 'New CD Table WorkflowID'.
# These columns should be maintained in the following order: Original Table ID column, New Table ID column, etc.
connection_table = new_CD_table[['GC EI Compounds ID', 'New CD Table ID', 'New CD Table WorkflowID']]


# Create a second instance of 'new_CD_table', which will be named 'CD_table_2'. 
# This table will be appended to the 'node_response' object and, eventually, to the 'node_response.json' file. 
# This table will serve as the JSON structure file for the newly created table ('New CD Table'), which will be imported back into Compound Discoverer.
# First, get the directory, basename, and extension of the original table's datafile.
table_directory, table_filename = os.path.split(node_response['Tables'][0]['DataFile'])
table_basename, table_extension = os.path.splitext(table_filename)


# Create a variable that defines the new text file name.
new_table_file = os.path.join(table_directory, 'NewCDTable.out.txt')


# Create/update 'CD_table_2' table structure.
CD_table_2 = dict(
    TableName = 'New CD Table',
    DataFile = new_table_file,
    DataFormat = 'CSV',
    Options = {},
    ColumnDescriptions = []
    )


# Update the New Table's (CD_table_2) Column Descriptions. 
# It is important that the first 'ColumnDescription' 'ColumnName' value reflect the new table's ID column (here, 'New CD Table ID')
# The 'ColumnDescription' 'Options' list will be updated for the Area columns in order to display values in scientific e notation with 2 decimal places of precision.
CD_table_2['ColumnDescriptions'] = [
    {
        'ColumnName': 'New CD Table ID',    # This should reflect the new table's ID column.
        'ID': 'ID',
        'DataType': 'Int',
        'Options': {}
    },
    {
        'ColumnName': 'Name',
        'ID': '',
        'DataType': 'String',
        'Options': {}    # Assuming no options; can be updated later.
    },
    {
        'ColumnName': 'Area Mean (Genuine)',
        'ID': '',
        'DataType': 'Float',
        'Options': {'FormatString': 'e2'}    # Updating the format to display values in scientific e notation and 2 decimal places of precision.
    },
    {
        'ColumnName': 'Area Mean (Suspect)',
        'ID': '',
        'DataType': 'Float',
        'Options': {'FormatString': 'e2'}    # Updating the format to display values in scientific e notation and 2 decimal places of precision.
    },
    {
        'ColumnName': 'New CD Table WorkflowID',
        'ID': 'WorkflowID',
        'DataType': 'Int',
        'Options': {}    # Assuming no options; can be updated later.
    }
]


# Create a third instance of 'new_CD_table', which will be named 'CD_table_3'. 
# This table will be appended to the 'node_response' object and, eventually, to the 'node_response.json' file. 
# This table will serve as the JSON structure file for the 'Connection Table' between the original table exported out of Compound Discoverer and the newly created table ('New CD Table'), which will be imported back into Compound Discoverer.
# Create a variable that defines the new text file name.
connection_table_file = os.path.join(table_directory, table_basename + '-NewCDTable.out.txt')


# Create/update 'CD_table_3' table structure.
CD_table_3 = dict(
    TableName = 'GC EI Compounds - New CD Table',
    DataFile = connection_table_file,
    DataFormat = 'CSVConnectionTable',
    Options = {
        'FirstTable': 'GC EI Compounds',
        'SecondTable': 'New CD Table'
    },
    ColumnDescriptions = []
    )


# Update 'Connection Table' (CD_table_3) Column Descriptions. 
# Be sure to use the 'ID' columns (previously referenced) and order the columns in a manner consistent with the tables' connection structure - Original Table followed by the (new) one connected to it.
CD_table_3['ColumnDescriptions'] = [
        {
            'ColumnName': 'GC EI Compounds ID',
            'ID': 'ID',
            'DataType': 'Int',
            'Options': {}    # Assuming no options; can be updated later.
        },
        {
            'ColumnName': 'New CD Table ID',
            'ID': 'ID',
            'DataType': 'Int',
            'Options': {}    # Assuming no options; can be updated later.
        },
        {
            'ColumnName': 'New CD Table WorkflowID',
            'ID': 'WorkflowID',
            'DataType': 'Int',
            'Options': {}    # Assuming no options; can be updated later.
        }
    ]


# Update 'node_response' variable to include the newly created tables. 
# In this example, we are creating (appending) two additional tables to 'node_response'.
# 'CD_table_2' is the structure of the new table ('new_CD_table').
# 'CD_table_3' is the structure of the 'Connection Table' ('connection_table').
node_response['Tables'] = node_response['Tables'] + [CD_table_2, CD_table_3]
#==============================


# Write Files.
# In this section, we will modify and write text (.out.txt) and JSON (.json) files. 
# The text files will reflect our newly created data (calculations performed in Python) and the JSON files will serve to instruct Compound Discoverer as to the structure of those files, where to find them, and how to read them.
# Write newly created results table as a 'txt' ('.out.txt') file to temporary ('scratch') folder. 
# The '.out.txt' file will be stored in the 'DataFile' field of the 'tables' section of 'node_response' file.
# Substitute 'out.txt' for 'txt' in the would be 'node_response.json' file. 
# Write the information for 'modified_GCEI_Compounds_table'.
result_out_txt = node_response['Tables'][0]['DataFile'].replace('txt', 'out.txt')


# Write newly created table results to file. Note: write files as tab-separated (CSV) text files.
modified_GCEI_Compounds_Table.to_csv(result_out_txt, sep='\t', index=False, encoding='utf-8')


# Update 'node_response.json' table 'DataFile' path (with '.out.txt').
node_response['Tables'][0]['DataFile'] = result_out_txt


# Write newly created table results to file. Note: write files as tab-separated (CSV) text files.
new_CD_table.to_csv(node_response['Tables'][1]['DataFile'], sep='\t', index=False, encoding='utf-8')


# Write newly created table to 'Connection Table' portion of the file.
connection_table.to_csv(node_response['Tables'][2]['DataFile'], sep='\t', index=False, encoding='utf-8')


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
