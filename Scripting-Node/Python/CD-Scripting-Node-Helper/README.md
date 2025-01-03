# Compound Discoverer

## Scripting Node - Python

### CD Scripting Node Helper

This section of the repository is for developing Python scripts to be used with Thermo Fisher Scientific Compound Discoverer 3.3 SP3 (CD 3.3.3) software via the Scripting Node feature. This section features the Compound Discoverer Scripting Node "Helper" file in script development.

The *CDScriptingNodeHelper* is used to define functions and methods that may be useful in developing scripts and understanding the structure and mechanism of the file and data exchange process used by the Scripting Node feature. The work presented in this section has been tested with limited scope in CD 3.3.3 primarily using the GC Workflows. It is assumed that the user has already read and understood the [Scripting Node - Custom Script Integration](https://docs.thermofisher.com/r/Proteome-Discoverer-3.1-User-Guide/en-US1325195659v1 "Scripting Node - Custom Script Integration") section of the Compound Discoverer (or Proteome Discoverer) User Guide.

The objectives of this work are as follows:

-   Demonstrate how to read (load) data previously exported from Compound Discoverer into a Python environment to perform calculations and computations outside of Compound Discoverer.

-   Demonstrate how to import data back into Compound Discoverer (after having performed the desired calculations) and how to display the new data in the form of a new column, a new table, or both.

-   Clarify the mechanism of the data export out of and import into Compound Discoverer as well as the structures of the JSON files associated with these processes and how to read, modify, and write them.

Please refer to the scripts referenced in this section of the repository for examples.

## Requirements

Depending on the Integrated Development Environment (IDE) software used, to import and use the *CDScriptingNodeHelper* file in a Python environment, it may be necessary to direct the IDE to the path where the *CDScriptingNodeHelper* file is saved. If necessary, this can be accomplished using a command such as the one referenced below. Typically, the IDE will compile the file prior to using it - the user should not have to perform this step or do anything beyond appending the file location (if at all).

```{python}
import sys    # System-specific parameters and functions.
sys.path.append('your/path/to/CDScriptingNodeHelper')    # Append CDScriptingNodeHelper file location.
from CDScriptingNodeHelper import CDScriptingResponse    # Import CDScriptingResponse Class.
```

## Disclaimer

The purpose of the *CDScriptingNodeHelper* file is to introduce functions and methods that may be useful in script development. However, using this file is completely to the discretion of the user and not at all essential to using the Compound Discoverer Scripting Node feature. It is quite possible that more efficient, effective, and flexible scripts, processes, or workflows can be accomplished without the use of this file and/or with the use of additional packages or tools.