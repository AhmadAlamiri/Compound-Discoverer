# Compound Discoverer

This repository contains information pertaining to Thermo Fisher Scientific Compound Discoverer software. It includes demonstrations, guides, and tutorials that may be useful while using few of the data analysis features of the software.

## Scripting Node Feature

The Scripting Node is a customizable node that allows the user to run an executable file as the final node in a workflow and to incorporate the result data into the application’s result file.

To use the Scripting Node feature, the user declares desired tables and/or columns to be exported using a script written in his/her preferred programming language. To create a script for the Scripting Node, programmers can use any programming language that supports running code from the command line, for example, Python, R, C#, C++, and so on. The desired objects are then exported from Compound Discoverer in the form of tab-separated text files along with JSON files describing the location(s) and structure(s) of these files. Using the script, the user can opt to perform data analysis and calculations outside of Compound Discoverer (with no intention of importing the data back into the application). Alternatively, using the script and following data analysis, the user can opt to import the data back into Compound Discoverer and save it as part of a typical Result file. The import process requires the user to submit the modified data in the form of text files along with JSON files describing the location(s) and structure(s) of these files.

Please refer to the Python and R directories for examples demonstrating the export and import processes.

## Requirements

-   [Compound Discoverer Software (3.3+)](https://www.thermofisher.com/us/en/home/industrial/mass-spectrometry/liquid-chromatography-mass-spectrometry-lc-ms/lc-ms-software/multi-omics-data-analysis/compound-discoverer-software.html "Compound Discoverer Software")

-   [Python (version 3.11 +)](https://www.python.org/ "Python") (though, previous versions may also be suitable).

-   [R (version 4.0 +)](https://www.r-project.org/ "The R Project for Statistical Computing") (though, previous versions may also be suitable).

## Disclaimer

While the author may be affiliated with Thermo Fisher Scientific at the time of this writing, his work reflects his own views, opinions, guidelines, and/or recommendations. In no way, shape, or form does the author's work reflect the views, opinions, or recommendations of Thermo Fisher Scientific, Inc., its affiliates, or its employees. Further, the author is not part of the Compound Discoverer (or Proteome Discoverer) software development or management teams and has no additional insight as to the underlying mechanism of the software, its code, or any other details beyond that of the typical software user. As such, in no way, shape, or form does the author's work reflect the views, opinions, or recommendations of the Compound Discoverer (or Proteome Discoverer) software development and/or management teams.

The work presented in the guides and scripts has been tested with limited scope using Compound Discoverer 3.3 SP3 (CD 3.3.3) primarily using the GC Workflows. The work is only meant to serve as a guide rather than best practice recommendations. The code and scripts have not been validated or tested extensively; they are intended for **Research Use Only** and not for use in diagnostic procedures, regulated environments, or the like.

In an effort to keep the guides and scripts clear and simple, the author attempted to complete the work while strictly using base software distributions (for Python and R) and employing the minimal amount of features and functionality afforded by the base distributions. In situations where that was not possible, the author attempted to maintain the level of clarity and simplicity to the best of his abilities. It is quite possible that more efficient, effective, and flexible scripts, processes, or workflows can be accomplished with the use of additional packages or tools.

It is assumed that the user is already familiar with and/or has had formal training pertaining to the Compound Discoverer software. In no way, shape, or form does this repository constitute a form of training or a replacement to formal training. Furthermore, in no way, shape, or form does this repository constitute or represent a medium through which any type of training or troubleshooting should be sought, expected, or administered.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

BY DOWNLOADING OR USING ANY SOFTWARE, SCRIPTS, TEMPLATES, DOCUMENTATION AND/OR OTHER MATERIALS (COLLECTIVELY “MATERIALS”), YOU AND ANY COMPANY OR INSTITUTION YOU REPRESENT (COLLECTIVELY “YOU”) ACKNOWLEDGE AND AGREE AS FOLLOWS: (1) THE MATERIALS ARE PROVIDED “AS IS” WITHOUT WARRANTY OF ANY KIND, EXPRESSED OR IMPLIED, AND (2) THERMO FISHER SCIENTIFIC INC., ITS AFFILIATES AND EMPLOYEES WILL NOT BE RESPONSIBLE FOR ANY DAMAGES ARISING FROM YOUR USE OF THE MATERIALS, INCLUDING BUT NOT LIMITED TO DAMAGES ASSOCIATED WITH LOSS OR CORRUPTION OF DATA, INACCURATE RESULTS, AND/OR DIMINISHED INSTRUMENT PERFORMANCE.