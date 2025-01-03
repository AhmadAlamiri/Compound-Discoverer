#===============================================================================
# Name   : new_column
# Author : Ahmad Alamiri
# Version: v1.0 (for Compound Discoverer 3.3 SP3; CD3.3.3)
# Aim    : An R script that creates a new column and imports it back into Compound Discoverer. 
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


# Define Templates
# Define 'node_response.json' File
# Define the 'node_response' variable using the data derived from the imported JSON file (here, 'read_CD_json'). 
node_response <- list(CurrentWorkflowID = read_CD_json$CurrentWorkflowID,
                      ExpectedResponsePath = read_CD_json$ExpectedResponsePath,
                      ResultFilePath = read_CD_json$ResultFilePath,
                      NodeParameters = read_CD_json$NodeParameters,
                      Version = read_CD_json$Version,
                      Tables = read_CD_json$Tables
)
#==============================


# Load Table(s)
# Read table(s) exported from Compound Discoverer. 
# Tables are exported as tab-separated text files. 
# In this example, read the contents of the first table's datafile.
# Define new variable 'GCEI_Compounds_table' and read the 'GC EI Compounds' data into it.
GCEI_Compounds_table <- read.table(file = read_CD_json$Tables[[1]]$DataFile, 
                                   header = TRUE,
                                   check.names = FALSE,
                                   stringsAsFactors = FALSE
)
#==============================


# Create Column(s)
# In this example, we will create a column 'New CD Column'.
# We will assign this column values 1 to number of rows of 'GC EI Compounds' table (the actual values of the column are irrelevant, in this case).
# We will use this column to demonstrate how to add a column to be imported back into Compound Discoverer.
new_CD_column <- 1:nrow(GCEI_Compounds_table)
#==============================


# Add Column(s).
# Add new column to the data table (here, 'modified_GCEI_Compounds_Table').
# By defining a column name, we can have both the data frame and Compound Discoverer (upon import) display 'New CD Column' as the column's heading (name).
modified_GCEI_Compounds_table <- cbind(GCEI_Compounds_table, 'New CD Column' = new_CD_column)


# Create a new column using the JSON structure.
# Note: the 'ColumnName' value is the same as that of 'New CD Column' defined above (modified_GCEI_Compounds_table$new_CD_column in the table/data frame).
# In this example, we will override the 'new_CD_column' now that we are done using it (though, this may not be good practice).
new_CD_column <- list(ColumnName = 'New CD Column',
                      ID = '',    
                      DataType = 'Int',    
                      Options = list()
)


# Add new column to JSON structure (to be used by 'node_response.json' file). 
# Update the 'node_response' variable previously created - append the list of Tables' 'ColumnDescriptions' by one (for 'new_CD_column').
# Repeat this process for each new column as necessary.
node_response$Tables[[1]]$ColumnDescriptions[[length(node_response$Tables[[1]]$ColumnDescriptions) + 1 ]] <- new_CD_column
#==============================


# Write Files.
# Write newly created results table as a 'txt' ('.out.txt') file to temporary ('scratch') folder. 
# The '.out.txt' file will be stored in the 'DataFile' field of the 'tables' section of 'node_response' file.
# Substitute 'out.txt' for 'txt' in the would be 'node_response.json' file. 
# Write the information for 'modified_GCEI_Compounds_table'.
result_out_txt <- gsub('txt', 'out.txt', node_response$Tables[[1]]$DataFile)


# Write newly created table results to file. Note: write files as tab-separated (CSV) text files.
write.table(modified_GCEI_Compounds_table, file = result_out_txt, sep = '\t', row.names = FALSE)


# Update 'node_response.json' table 'DataFile' path (with '.out.txt').
node_response$Tables[[1]]$DataFile = result_out_txt


# Write 'node_response.json' file. Define 'ExpectedResponsePath' location.
json_out_file <- node_response$ExpectedResponsePath


# Convert 'node_response' to JSON structure.
response_json <- toJSON(node_response, indent = 1, method = 'C')


# The 'response_json' process generates incorrect format for the empty 'Options' lists.
# Use a regular expression to find and replace the '[\n\n]' with the {} characters.
#In this example, we will overwrite the existing 'response_json' variable (though that may not be good practice).
response_json <- gsub("\\[\n\n[[:blank:]]+\\]", "{}", response_json)


# Open JSON file connection (to write to file).
json_file_conn <- file(json_out_file)


# Write lines to file ('response_json').
writeLines(response_json, json_file_conn)


# Close JSON file connection (writing procedure has been completed).
close(json_file_conn)
#==============================


# OPTIONAL
# Debugging/Development
# Save data ('Rimage.dat').
# This will save the 'Rimage.dat' file in the same location as the script used in the Scripting Node - adjust file save location as desired.
save.image(file = paste0(
  dirname(
    sub('.*=', '', args[4])
  ), '/CD node Rimage.dat')
)


# OPTIONAL
# Load the saved 'Rimage.dat' file for debugging or script development purposes.
# Uncomment/use command line below as needed.
# load('CD node Rimage.dat')
#==============================
