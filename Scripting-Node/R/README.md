# Compound Discoverer

## Scripting Node - R

This section of the repository is for developing R scripts to be used with Thermo Fisher Scientific Compound Discoverer 3.3 SP3 (CD 3.3.3) software via the Scripting Node feature. The work presented in this section has been tested with limited scope in CD 3.3.3 primarily using the GC Workflows. It is assumed that the user has already read and understood the [Scripting Node - Custom Script Integration](https://docs.thermofisher.com/r/Proteome-Discoverer-3.1-User-Guide/en-US1325195659v1 "Scripting Node - Custom Script Integration") section of the Compound Discoverer (or Proteome Discoverer) User Guide.

The objectives of this work are as follows:

-   Demonstrate how to read (load) data previously exported from Compound Discoverer into a R environment to perform calculations and computations outside of Compound Discoverer.

-   Demonstrate how to import data back into Compound Discoverer (after having performed the desired calculations) and how to display the new data in the form of a new column, a new table, or both.

-   Clarify the mechanism of the data export out of and import into Compound Discoverer as well as the structures of the JSON files associated with these processes and how to read, modify, and write them.

Please refer to the scripts referenced in this section of the repository for examples.