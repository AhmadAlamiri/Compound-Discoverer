#===============================================================================
# Name   : minimal
# Author : Ahmad Alamiri
# Version: v1.0 (for Compound Discoverer 3.3 SP3; CD3.3.3)
# Aim    : An R script that represents the minimal code required to read data exported from Compound Discoverer.
#===============================================================================

# Load Libraries
# Load R library that is capable of reading JSON files.
library(rjson)    
#==============================


# Read Command Line Arguments
# Read the Command Line arguments passed by Compound Discoverer upon initiation of the scripting node feature. 
args <- commandArgs()


# We are only interested in the 6th argument, which contains the location of the would be newly-created node_args.json file. 
# This file contains essential information about the exported data, including location(s) of the exported text files as well as the row IDs, columns, and column attributes of the exported tables.
# Define Input File ('node_args.json' file) - located in the 6th argument of the variable 'args'.
input_file <- args[6]


# Read 'node_args.json' file.
read_CD_json <- fromJSON(file = input_file)
#==============================

