#===============================================================================
# Name   : new_table
# Author : Ahmad Alamiri
# Version: v1.0 (for Compound Discoverer 3.3 SP3; CD3.3.3)
# Aim    : An R script that creates a new table and imports it back into Compound Discoverer. 
#===============================================================================

# Load Libraries
# Load R library that is capable of reading JSON files.
library(rjson)    # JSON for R.
#==============================


# Read Command Line Arguments
# Read the Command Line arguments passed by Compound Discoverer upon initiation of the scripting node feature. 
args <- commandArgs()


# We are only interested in the 6th argument, which contains the location of the would be newly-created 'node_args.json' file. 
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
# In this example, read the contents of the first table's data file.
# Define new variable 'GCEI_Compounds_table' and read the 'GC EI Compounds' data into it.
GCEI_Compounds_table <- read.table(file = read_CD_json$Tables[[1]]$DataFile, 
                                   header = TRUE,
                                   check.names = FALSE,
                                   stringsAsFactors = FALSE
)
#==============================


# Create Table(s).
# In this example, we will create a table 'New CD Table' that computes the 'Area Mean' for each 'Genuine' (Control) samples and 'Suspect' (Test) samples (the contents of the table are irrelevant - perform any desired calculation instead).
# We will use this table to demonstrate how to add a table to be imported back into Compound Discoverer.
# Subset 'GCEI_Compounds_table' indices 1, 4, and 24-29, corresponding to 'GC EI Compounds ID', 'Name', and individual Area columns for each of the 6 samples (3 Genuine and 3 Suspect).
new_CD_table <- GCEI_Compounds_table[, c(1, 4, 24:29)]


# Compute the Mean values (row-wise) for each set of samples.
new_CD_table$'Area Mean (Genuine)' <- rowMeans(new_CD_table[, grepl('.*Genuine', colnames(new_CD_table))])
new_CD_table$'Area Mean (Suspect)' <- rowMeans(new_CD_table[, grepl('.*Suspect', colnames(new_CD_table))])


# Remove the individual Area columns since they are no longer necessary.
new_CD_table <- new_CD_table[, -c(3:8)]
#==============================


# Add Table(s)
# We will create two new columns, 'New CD Table ID' and 'New CD Table WorkflowID'. 
# CAUTION: these ID columns are important in how Compound Discoverer indexes the objects of a data table and how it associates them with other objects in other data tables. 
# Therefore, the analyst must follow the proper format and convention to ensure that these two columns' data are correct.
# Define 'New CD Table' 'ID' column (that will eventually have the attribute 'ID' = 'ID' in the JSON file structure). 
# In this example, we will create a new column 'New CD Table ID'.
new_CD_table['New CD Table ID'] <- 1:nrow(new_CD_table)


# Create another column 'New CD Table WorkflowID'.
new_CD_table['New CD Table WorkflowID'] <- node_response$CurrentWorkflowID


# Create 'Connection Table' data frame, which will eventually be written as a 'Connection Table' text file. 
# This table only requires the ID columns: 'GC EI Compounds ID', 'New CD Table ID', and 'New CD Table WorkflowID'.
# These columns should be maintained in the following order: Original Table ID column, New Table ID column, etc.
connection_table <- new_CD_table[, c('GC EI Compounds ID', 'New CD Table ID', 'New CD Table WorkflowID')]


# Create a second instance of 'new_CD_table', which will be named 'CD_table_2'. 
# This table will be appended to the 'node_response' object and, eventually, to the 'node_response.json' file. 
# This table will serve as the JSON structure file for the newly created table ('New CD Table'), which will be imported back into Compound Discoverer.
CD_table_2 <- list(TableName = 'New CD Table',
                   DataFile = sub(basename(node_response$Tables[[1]]$DataFile), 'NewCDTable.out.txt', node_response$Tables[[1]]$DataFile),
                   DataFormat = 'CSV',
                   Options = list(),
                   ColumnDescriptions = list()
)


# Update the New Table's (CD_table_2) Column Descriptions. 
# It is important that the first 'ColumnDescription' 'ColumnName' value reflect the new table's ID column (here, 'New CD Table ID')
# The 'ColumnDescription' 'Options' list will be updated for the Area columns in order to display values in scientific e notation with 2 decimal places of precision.
CD_table_2$ColumnDescriptions <- list(
  list(
    ColumnName = 'New CD Table ID',    # This should reflect the new table's ID column.
    ID = 'ID',
    DataType = 'Int',
    Options = list()
  ),
  list(
    ColumnName = 'Name',
    ID = '',
    DataType = 'String',
    Options = list()    # Assuming no options; can be updated later.
  ),
  list(
    ColumnName = 'Area Mean (Genuine)',
    ID = '',
    DataType = 'Float',
    Options = list(FormatString = 'e2')    # Updating the format to display values in scientific e notation and 2 decimal places of precision.
  ),
  list(
    ColumnName = 'Area Mean (Suspect)',
    ID = '',
    DataType = 'Float',
    Options = list(FormatString = 'e2')    # Updating the format to display values in scientific e notation and 2 decimal places of precision.
  ),
  list(
    ColumnName = 'New CD Table WorkflowID',
    ID = 'WorkflowID',
    DataType = 'Int',
    Options = list()    # Assuming no options; can be updated later.
  )
)


# Create a third instance of 'new_CD_table', which will be named 'CD_table_3'. 
# This table will be appended to the 'node_response' object and, eventually, to the 'node_response.json' file. 
# This table will serve as the JSON structure file for the 'Connection Table' between the original table exported out of Compound Discoverer and the newly created table ('New CD Table'), which will be imported back into Compound Discoverer.
# First, create a variable that defines the new text file name.
connection_table_file <- paste(sub('\\..*', '', basename(node_response$Tables[[1]]$DataFile)), 'NewCDTable.out.txt', sep = '-')


# Update the table parameters.
CD_table_3 <- list(TableName = 'GC EI Compounds - New CD Table',
                   DataFile = sub(basename(node_response$Tables[[1]]$DataFile), connection_table_file, node_response$Tables[[1]]$DataFile),
                   DataFormat = 'CSVConnectionTable',
                   Options = list(
                     FirstTable = 'GC EI Compounds',
                     SecondTable = 'New CD Table'
                   ),
                   ColumnDescriptions = list()
)


# Update 'Connection Table' (CD_table_3) Column Descriptions. 
# Be sure to use the 'ID' columns (previously referenced) and order the columns in a manner consistent with the tables' connection structure - Original Table followed by the (new) one connected to it.
CD_table_3$ColumnDescriptions <- list(
  list(
    ColumnName = 'GC EI Compounds ID',
    ID = 'ID',
    DataType = 'Int',
    Options = list()    # Assuming no options; can be updated later.
  ),
  list(
    ColumnName = 'New CD Table ID',
    ID = 'ID',
    DataType = 'Int',
    Options = list()    # Assuming no options; can be updated later.
  ),
  list(
    ColumnName = 'New CD Table WorkflowID',
    ID = 'WorkflowID',
    DataType = 'Int',
    Options = list()    # Assuming no options; can be updated later.
  )
)


# Update 'node_response' variable to include the newly created tables. 
# In this example, we are creating (appending) two additional tables to 'node_response'.
# 'CD_table_2' is the structure of the new table ('new_CD_table').
# 'CD_table_3' is the structure of the 'Connection Table' ('connection_table').
node_response$Tables[[2]] <- CD_table_2
node_response$Tables[[3]] <- CD_table_3
#==============================


# Write Files.
# In this section, we will modify and write text (.out.txt) and JSON (.json) files. 
# The text files will reflect our newly created data (calculations performed in R) and the JSON files will serve to instruct Compound Discoverer as to the structure of those files, where to find them, and how to read them.
# Write newly created table results to file. Note: write files as tab-separated (CSV) text files.
write.table(new_CD_table,
            file = node_response$Tables[[2]]$DataFile, sep = '\t', row.names = FALSE)


# Write newly created table to 'Connection Table' portion of the file.
write.table(connection_table,
            file = node_response$Tables[[3]]$DataFile, sep = '\t', row.names = FALSE)


# Write 'node_response.json' file. Define 'ExpectedResponsePath' location.
json_out_file <- node_response$ExpectedResponsePath


# Convert 'node_response' to JSON structure.
response_json <- toJSON(node_response, indent = 1, method = 'C')


# The 'response_json' process generates incorrect format for the empty Options lists. Use a regular expression to find and replace the '[\n\n]' with the {} characters. 
# In this example, we will overwrite the existing 'response_json' variable (though that may not be good practice).
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
