#==============================================================================
# Name   : basename
# Author : Ahmad Alamiri
# Version: v1.0 (for Compound Discoverer 3.3 SP3; CD3.3.3)
# Aim    : Demonstrate the 'basename' method of the Compound Discoverer Scripting Node "Helper" (CDScriptingNodeHelper) file. The method is defined in the CDScriptingNodeHelper and is used to set the basename.
#==============================================================================


# Load Libraries
# Load a package/module that is capable of reading JSON files.
from CDScriptingNodeHelper import CDScriptingResponse    # Import the CDScriptingResponse class from the CDScriptingNodeHelper module.
#==============================


# Define a variable to store the CDScriptingResponse object.
response = CDScriptingResponse()


# Define a variable to store the basename and use the method '__CDScriptingResponse__basename' to set the basename.
basename = response._CDScriptingResponse__basename