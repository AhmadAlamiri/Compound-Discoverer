#===============================================================================
# Name   : development
# Author : Ahmad Alamiri
# Version: v1.0 (for Compound Discoverer 3.3 SP3; CD3.3.3)
# Aim    : An R script that saves data exported from Compound Discoverer in the form of an 'Rimage.dat' file, which can subsequently be used in script debugging and development. 
#===============================================================================

# Load Libraries
# Load R library that is capable of reading JSON files.
library(rjson)    # JSON for R.
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


# Debugging/Development
# Save data ('Rimage.dat').
# This will save the 'Rimage.dat' file in the same location as the script used in the Scripting Node - adjust file save location as desired.
save.image(file = paste0(
  dirname(
    sub('.*=', '', args[4])
  ), '/CD node Rimage.dat')
)


# Load the saved 'Rimage.dat' file for debugging or script development purposes.
# Uncomment/use command line below as needed.
# load('CD node Rimage.dat')
#==============================


# Continue script development...