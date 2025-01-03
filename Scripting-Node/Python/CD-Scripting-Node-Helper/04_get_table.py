#==============================================================================
# Name   : get_table
# Author : Ahmad Alamiri
# Version: v1.0 (for Compound Discoverer 3.3 SP3; CD3.3.3)
# Aim    : Demonstrate the 'get_table' method of the Compound Discoverer Scripting Node "Helper" (CDScriptingNodeHelper) file. The method is defined in the CDScriptingNodeHelper and is used to get a table from the node file.
#==============================================================================


# Load Libraries
# Load a package/module that is capable of reading JSON files.
from CDScriptingNodeHelper import CDScriptingResponse    # Import the CDScriptingResponse class from the CDScriptingNodeHelper module.
#==============================


# Define a variable to store the CDScriptingResponse object.
response = CDScriptingResponse()


# Define a variable to store the node file and use the method 'get_node_file' to get the node file.
node_args = response.get_node_file()


# Define a variable to store the table and use the method 'get_table' to get the table.
# Parameters
# ----------
# node_file : dict
#     The node file dictionary containing the tables.
# TableName : str
#     The name of the table to retrieve.

# Returns
# -------
# dict
#     The table dictionary corresponding to the specified table name.
CD_table_1 = response.get_table(node_args, 'GC EI Compounds')