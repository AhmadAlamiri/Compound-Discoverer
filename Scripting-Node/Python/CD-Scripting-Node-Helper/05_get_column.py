#==============================================================================
# Name   : get_column
# Author : Ahmad Alamiri
# Version: v1.0 (for Compound Discoverer 3.3 SP3; CD3.3.3)
# Aim    : Demonstrate the 'get_column' method of the Compound Discoverer Scripting Node "Helper" (CDScriptingNodeHelper) file. The method is defined in the CDScriptingNodeHelper and is used to get a column from the specified table in the node file by table and column name.
#==============================================================================


# Load Libraries
# Load a package/module that is capable of reading JSON files.
from CDScriptingNodeHelper import CDScriptingResponse    # Import the CDScriptingResponse class from the CDScriptingNodeHelper module.
#==============================


# Define a variable to store the CDScriptingResponse object.
response = CDScriptingResponse()


# Define a variable to store the node file and use the method 'get_node_file' to get the node file.
node_args = response.get_node_file()


# Define a variable to store the Column and use the method 'get_column' to get the table.
# Parameters
# ----------
# node_file : dict
#     The node file dictionary containing the tables.
# TableName : str
#     The name of the table from which to retrieve the column.
# ColumnName : str
#     The name of the column to retrieve.

# Returns
# -------
# dict
#     The column dictionary corresponding to the specified table name and column name.
CD_column_Name = response.get_column(node_args, 'GC EI Compounds', 'Name')