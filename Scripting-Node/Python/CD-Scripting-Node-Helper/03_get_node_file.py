#==============================================================================
# Name   : get_node_file
# Author : Ahmad Alamiri
# Version: v1.0 (for Compound Discoverer 3.3 SP3; CD3.3.3)
# Aim    : Demonstrate the 'get_node_file' method of the Compound Discoverer Scripting Node "Helper" (CDScriptingNodeHelper) file. The method is defined in the CDScriptingNodeHelper and is used to get the node file. The method reads the node file from disk and returns a copy of its contents.
#==============================================================================


# Load Libraries
# Load a package/module that is capable of reading JSON files.
from CDScriptingNodeHelper import CDScriptingResponse    # Import the CDScriptingResponse class from the CDScriptingNodeHelper module.
#==============================


# Define a variable to store the CDScriptingResponse object.
response = CDScriptingResponse()


# Define a variable to store the node file and use the method 'get_node_file' to get the node file.
# Parameters
# ----------
# None

# Returns
# -------
# dict
#     The node file contents as a dictionary.
node_args = response.get_node_file()