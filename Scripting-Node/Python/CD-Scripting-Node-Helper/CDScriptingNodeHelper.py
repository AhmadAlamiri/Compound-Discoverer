#==============================================================================
# Name   : CDScriptingNodeHelper
# Author : Ahmad Alamiri
# Version: v1.0 (for Compound Discoverer 3.3 SP3; CD3.3.3)
# Aim    : Compound Discoverer Scripting Node "Helper" used to define functions and methods that may be useful in developing scripts and understanding the structure and mechanism of the file and data exchange process used by the Scripting Node feature.
#==============================================================================


import copy    # Shallow and deep copy operations.
import json    # JSON encoder and decoder.
import os    # Miscellaneous operating system interfaces.
import sys    # System-specific parameters and functions.
import traceback    # Print or retrieve a stack traceback.


class CDScriptingResponse:
    def __init__(self):
        """
        Initialize the CDScriptingResponse object.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----
        The constructor extracts the directory and filename from the first command line argument (sys.argv[1]), and initializes empty dictionaries for the node file, tables, and columns.
        """
        self.__directory = os.path.dirname(sys.argv[1])
        self.__basename = os.path.basename(sys.argv[1])
        self.__node_file = dict()
        self.__tables = dict()
        self.__columns = dict()

    
    def get_node_file(self):
        """
        Reads the node file from disk and returns a copy of its contents.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            The node file contents as a dictionary.

        Raises
        ------
        Exception
            If the node file cannot be read from disk.

        Notes
        -----
        The method reads the node file from disk using the directory and filename stored in the CDScriptingResponse object, and returns a deep copy of its contents as a dictionary. If the node file cannot be read from disk, the method prints an error message and returns None.
        """
        node_file = None
        try:
            with open(os.path.join(self.__directory, self.__basename), 'r') as f:
                self.__node_file = json.load(f)
        
        except Exception as e:
            print(f'Failed to read node file: {str(e)}')
        
        node_file = copy.deepcopy(self.__node_file)
        return node_file
    

    def get_table(self, node_file: dict, TableName: str):
        """
        Retrieves a table from the node file by table name.

        Parameters
        ----------
        node_file : dict
            The node file dictionary containing the tables.
        TableName : str
            The name of the table to retrieve.

        Returns
        -------
        dict
            The table dictionary corresponding to the specified table name.

        Raises
        ------
        Exception
            If the table with the specified name cannot be found in the node file.
        """
        tables = node_file.get('Tables', [])

        table = next((table for table in tables if table['TableName'] == TableName), None)

        if table is None:
            raise Exception(f'Cannot find table {TableName} in node file.')

        return table


    def get_column(self, node_file: dict, TableName: str, ColumnName: str):
        """
        Retrieves a column from the node file by table name and column name.

        Parameters
        ----------
        node_file : dict
            The node file dictionary containing the tables.
        TableName : str
            The name of the table from which to retrieve the column.
        ColumnName : str
            The name of the column to retrieve.

        Returns
        -------
        dict
            The column dictionary corresponding to the specified table name and column name.

        Raises
        ------
        Exception
            If the table with the specified name does not exist in the node file, or if the column with the specified name does not exist in the table.
        """
        table = self.get_table(node_file, TableName)

        column = next((column for column in table.get('ColumnDescriptions', []) if column['ColumnName'] == ColumnName), None)

        if column is None:
            raise Exception(f'Cannot find column {ColumnName} in table {TableName}.')

        return column


    def add_node_file(self, node_file, **kwargs):
        """
        Adds a new node file to the CDScriptingResponse object.

        Parameters
        ----------
        node_file : dict
            The node file dictionary to add to the CDScriptingResponse object.
        **kwargs : dict, optional
            Additional attributes for the new node file, including:
            - 'CurrentWorkflowID' : str (default is an empty string)
            - 'ExpectedResponsePath' : str (default is an empty string)
            - 'ResultFilePath' : str (default is an empty string)
            - 'NodeParameters' : dict (default is an empty dictionary)
            - 'Version' : str (default is an empty string)
            - 'Tables' : list (default is an empty list)

        Returns
        -------
        dict
            The updated node file dictionary with the new node file.

        Notes
        -----
        The function adds the new node file to the CDScriptingResponse object and returns the updated node file dictionary. The function raises an exception if the node file cannot be added to the CDScriptingResponse object.
        """
        node_file = copy.deepcopy(node_file) or {}

        for key, default in [
            ('CurrentWorkflowID', node_file.get('CurrentWorkflowID')),
            ('ExpectedResponsePath', node_file.get('ExpectedResponsePath')),
            ('ResultFilePath', node_file.get('ResultFilePath')),
            ('NodeParameters', node_file.get('NodeParameters')),
            ('Version', node_file.get('Version')),
            ('Tables', node_file.get('Tables'))
        ]:
            node_file[key] = kwargs.get(key, default)

        return node_file



    def add_table(self, node_file: dict, TableName: str, **kwargs):
        """
        Adds a new table to the node file.

        Parameters
        ----------
        node_file : dict
            The node file dictionary to which the table is added.
        TableName : str
            The name of the table to add.
        **kwargs : dict, optional
            Additional attributes for the new table, including:
            - 'DataFile' : str (default is an empty string)
            - 'DataFormat' : str (default is an empty string)
            - 'Options' : dict (default is an empty dictionary)
            - 'ColumnDescriptions' : list (default is an empty list)

        Returns
        -------
        dict
            The updated node file dictionary with the new table.

        Raises
        ------
        Exception
            If a table with the same name already exists in the node file.
        """
        if any(table['TableName'] == TableName for table in node_file.get('Tables', [])):
            raise Exception(f'Table {TableName} already exists in node file.')

        new_table = {
            'TableName': TableName,
            'DataFile': kwargs.get('DataFile', ''),
            'DataFormat': kwargs.get('DataFormat', ''),
            'Options': kwargs.get('Options', {}),
            'ColumnDescriptions': kwargs.get('ColumnDescriptions', [])
        }

        node_file['Tables'].append(new_table)

        return node_file


    def add_column(self, node_file: dict, TableName: str, ColumnName: str, **kwargs):
        """
        Adds a new column to the specified table in the node file.

        Parameters
        ----------
        node_file : dict
            The node file dictionary containing the tables.
        TableName : str
            The name of the table to which the column is added.
        ColumnName : str
            The name of the column to add.
        **kwargs : dict, optional
            Additional attributes for the new column, including:
            - 'ID' : str (default is an empty string)
            - 'DataType' : str (default is an empty string)
            - 'Options' : dict (default is an empty dictionary)

        Returns
        -------
        dict
            The updated node file dictionary with the new column.

        Raises
        ------
        Exception
            If a column with the same name already exists in the table, or if the table with the specified name does not exist in the node file.

        Notes
        -----
        The function adds the new column to the specified table in the node file and returns the updated node file dictionary.
        The function raises an exception if a column with the same name already exists in the table, or if the table with the specified name does not exist in the node file.
        """
        for table in node_file['Tables']:
            if table['TableName'] == TableName:
                if any(column['ColumnName'] == ColumnName for column in table['ColumnDescriptions']):
                    raise Exception(f'Column {ColumnName} already exists in table {TableName}.')

                new_column = {
                    'ColumnName': ColumnName,
                    'ID': kwargs.get('ID', ''),
                    'DataType': kwargs.get('DataType', ''),
                    'Options': kwargs.get('Options', {})
                }

                table['ColumnDescriptions'].append(new_column)
                return node_file

        raise Exception(f'Table {TableName} not found.')


    def update_node_file(self, node_file: dict, **kwargs):
        """
        Updates the node file with the specified options.

        Parameters
        ----------
        node_file : dict
            The node file dictionary to update.
        **kwargs : dict, optional
            Additional attributes for the node file, including:
            - 'CurrentWorkflowID' : str (default is an empty string)
            - 'ExpectedResponsePath' : str (default is an empty string)
            - 'ResultFilePath' : str (default is an empty string)
            - 'NodeParameters' : dict (default is an empty dictionary)
            - 'Version' : str (default is an empty string)
            - 'Tables' : list (default is an empty list)

        Returns
        -------
        dict
            The updated node file dictionary with the new options.

        Notes
        -----
        The function updates the options for the node file both in the node file.
        """
        for key, default in [
            ('CurrentWorkflowID', node_file.get('CurrentWorkflowID')),
            ('ExpectedResponsePath', node_file.get('ExpectedResponsePath')),
            ('ResultFilePath', node_file.get('ResultFilePath')),
            ('NodeParameters', node_file.get('NodeParameters')),
            ('Version', node_file.get('Version')),
            ('Tables', node_file.get('Tables'))
        ]:
            node_file[key] = kwargs.get(key, default)

        return node_file
  

    def set_table_options(self, node_file: dict, TableName: str, Options: dict):
        """
        Sets the options for the specified table in the node file.

        Parameters
        ----------
        node_file : dict
            The node file dictionary containing the tables.
        TableName : str
            The name of the table for which to set the options.
        Options : dict
            A dictionary of options to set for the table.

        Returns
        -------
        dict
            The updated node file dictionary with the new options set for the specified table.

        Raises
        ------
        Exception
            If the table with the specified name cannot be found in the node file.

        Notes
        -----
        The function updates the options for the specified table both in the node file.
        """
        for table in node_file['Tables']:
            if table['TableName'] == TableName:
                table['Options'] = Options
                return node_file
        
        raise Exception(f'Cannot find table {TableName} in node file; cannot set options.')
        

    def set_column_options(self, node_file: dict, TableName: str, ColumnName: str, Options: dict):   
        """
        Sets the options for the specified column in the specified table in the node file.

        Parameters
        ----------
        node_file : dict
            The node file dictionary containing the tables.
        TableName : str
            The name of the table containing the column for which to set the options.
        ColumnName : str
            The name of the column for which to set the options.
        Options : dict
            A dictionary of options to set for the column.

        Returns
        -------
        dict
            The updated node file dictionary with the new options set for the specified column.

        Raises
        ------
        Exception
            If the column with the specified name cannot be found in the table, or if the table cannot be found in the node file.

        Notes
        -----
        The function updates the options for the specified column both in the node file.
        """
        for table in node_file['Tables']:
            if table['TableName'] == TableName:
                for column in table['ColumnDescriptions']:
                    if column['ColumnName'] == ColumnName:
                        column['Options'] = Options
                        return node_file

        raise Exception(f'Cannot find column {ColumnName} in table {TableName}; cannot set options.')


    def remove_table(self, node_file: dict, TableName: str):   
        """
        Removes the specified table from the node file.

        Parameters
        ----------
        node_file : dict
            The node file dictionary containing the tables.
        TableName : str
            The name of the table to remove.

        Returns
        -------
        dict
            The updated node file dictionary with the table removed.

        Raises
        ------
        Exception
            If the table with the specified name cannot be found in the node file.

        Notes
        -----
        The function removes the specified table from the node file.
        """
        for table in node_file['Tables']:
            if table['TableName'] == TableName:
                node_file['Tables'].remove(table)
                return node_file
        
        raise Exception(f'Cannot find table {TableName} in node file; cannot remove.')
    
    
    def remove_column(self, node_file: dict, TableName: str, ColumnName: str):   
        """
        Removes the specified column from the node file.

        Parameters
        ----------
        node_file : dict
            The node file dictionary containing the tables and columns.
        TableName : str
            The name of the table containing the column to remove.
        ColumnName : str
            The name of the column to remove.

        Returns
        -------
        dict
            The updated node file dictionary with the column removed.

        Raises
        ------
        Exception
            If the column with the specified name cannot be found in the table, or if the table cannot be found in the node file.

        Notes
        -----
        The function removes the specified column both from the node file.
        """
        for table in node_file['Tables']:
            if table['TableName'] == TableName:
                for column in table['ColumnDescriptions']:
                    if column['ColumnName'] == ColumnName:
                        table['ColumnDescriptions'].remove(column)
                        return node_file

        raise Exception(f'Cannot find column {ColumnName} in table {TableName}; cannot remove.')


    def save_to_file(self, node_file: dict, filename: str):   
        """
        Saves the node file to a file on disk.

        Parameters
        ----------
        node_file : dict
            The node file dictionary to save.
        filename : str
            The filename to which to save the node file. If not an absolute path, then the
            file is saved in the same directory as the script.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If an error occurs while attempting to save the node file.

        Notes
        -----
        The function saves the specified node file to the file system. If the directory does not
        exist, it is created. If the file already exists, it is overwritten.
        """
        if not os.path.isabs(filename):
            filename = os.path.join(self.__directory, filename)

        node_file = node_file

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        try:
            with open(filename, mode='w', encoding='utf-8') as f:
                json.dump(node_file, f, indent=4, ensure_ascii=False)
            print(f'Successfully saved node file to {filename}!')
        
        except Exception as e:
            print(f'Failed to save node file to {filename}: {str(e)}')
            print(traceback.format_exc())

