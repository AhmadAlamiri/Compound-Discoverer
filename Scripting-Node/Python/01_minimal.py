#===============================================================================
# Name   : minimal
# Author : Ahmad Alamiri
# Version: v1.0 (for Compound Discoverer 3.3 SP3; CD3.3.3)
# Aim    : A Python script that represents the minimal code required to read data exported from Compound Discoverer.
#===============================================================================


# Load Libraries
# Load a package/module that is capable of reading JSON files.
import json    # JSON encoder and decoder.
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
