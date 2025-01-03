#==============================================================================
# Name   : add_node_file
# Author : Ahmad Alamiri
# Version: v1.0 (for Compound Discoverer 3.3 SP3; CD3.3.3)
# Aim    : Demonstrate the 'add_node_file' method of the Compound Discoverer Scripting Node "Helper" (CDScriptingNodeHelper) file. The method is defined in the CDScriptingNodeHelper and is used to add a node file to the CDScriptingResponse object. Returns the completed node file dictionary.
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