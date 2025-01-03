#==============================================================================
# Name   : add_column
# Author : Ahmad Alamiri
# Version: v1.0 (for Compound Discoverer 3.3 SP3; CD3.3.3)
# Aim    : Demonstrate the 'add_column' method of the Compound Discoverer Scripting Node "Helper" (CDScriptingNodeHelper) file. The method is defined in the CDScriptingNodeHelper and is used to dds a new column to the specified table in the node file. Returns the updated node file dictionary with the new column.
#==============================================================================


# Load Libraries
# Load a package/module that is capable of reading JSON files.
from CDScriptingNodeHelper import CDScriptingResponse    # Import the CDScriptingResponse class from the CDScriptingNodeHelper module.
#==============================


# Define a variable to store the CDScriptingResponse object.
response = CDScriptingResponse()


# Define a variable to store the node file and use the method 'get_node_file' to get the node file.
node_args = response.get_node_file()


# Define a variable to store the node file and use the method 'add_node_file' to add the node file.
# Parameters
# ----------
# node_file : dict
#     The node file dictionary to add to the CDScriptingResponse object.
# **kwargs : dict, optional
#     Additional attributes for the new node file, including:
#     - 'CurrentWorkflowID' : str (default is an empty string)
#     - 'ExpectedResponsePath' : str (default is an empty string)
#     - 'ResultFilePath' : str (default is an empty string)
#     - 'NodeParameters' : dict (default is an empty dictionary)
#     - 'Version' : str (default is an empty string)
#     - 'Tables' : list (default is an empty list)

# Returns
# -------
# dict
#     The updated node file dictionary with the new node file.
node_response = response.add_node_file(node_args)    # No other parameters given/assigned in this example.

# Use the method 'add_table' to add the table.
# Parameters
# ----------
# node_file : dict
#     The node file dictionary to which the table is added.
# TableName : str
#     The name of the table to add.
# **kwargs : dict, optional
#     Additional attributes for the new table, including:
#     - 'DataFile' : str (default is an empty string)
#     - 'DataFormat' : str (default is an empty string)
#     - 'Options' : dict (default is an empty dictionary)
#     - 'ColumnDescriptions' : list (default is an empty list)

# Returns
# -------
# dict
#     The updated node file dictionary with the new table.
response.add_table(node_response, 'New CD Table')


# Optional
# Define a variable to store the table and use the method 'get_table' to get the table.
new_CD_table = response.get_table(node_response, 'New CD Table')


# Use the method 'add_column' to add a new column to the table.
# Parameters
# ----------
# node_file : dict
#     The node file dictionary containing the tables.
# TableName : str
#     The name of the table to which the column is added.
# ColumnName : str
#     The name of the column to add.
# **kwargs : dict, optional
#     Additional attributes for the new column, including:
#     - 'ID' : str (default is an empty string)
#     - 'DataType' : str (default is an empty string)
#     - 'Options' : dict (default is an empty dictionary)

# Returns
# -------
# dict
#     The updated node file dictionary with the new column.
response.add_column(node_response, 'New CD Table', 'New CD Column')


# Optional
# Define a variable to store the column and use the method 'get_column' to get the column.
new_CD_column = response.get_column(node_response, 'New CD Table', 'New CD Column')
