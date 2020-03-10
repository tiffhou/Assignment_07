#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# THou, 2020-Feb-27, added try statement to check for existing save file; 
#   added functions for adding entry, deleting entry; updated display
# THou, 2020-Feb-29, added auto-generating ID for new CD entries; cleaned up formatting
# THou, 2020-Mar-02, added more formatting and comments; tweaked naming conventions; 
#   added get_int_input()
# THou, 2020-Mar-07, incorporated feedback from mod 6 submission; 
#   added error handling for initial load, loading from file;
#   imported the pickle module and implemented in load/save functions
# THou, 2020-Mar-09, updated docstrings; updated data file to .dat
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object
intID = '' #variable to hold a CD ID
strTitle = '' #variable to hold a CD title
strArtist = '' #variable to hold a CD's artist

# -- PROCESSING -- #
class DataProcessor:
    """processess data in memory"""

    @staticmethod
    def add_entry(cd_id, cd_title, cd_artist, inv_table):
        """Adds the CD entry to a dictionary and appends it to the lstTbl.
        
        Args:
            cd_id (int): CD ID to be added to the dictionary
            cd_title (string): CD title to be added to the dictionary
            cd_artist (string): CD artist to be added to the dictionary
            inv_table (list): current inventory list
        
        Return:
            inv_table (list): updated inventory list
        """
        dicRow = {'ID': cd_id, 'Title': cd_title, 'Artist': cd_artist}
        inv_table.append(dicRow)
        return inv_table

    @staticmethod
    def delete_entry(delID, table):
        """Deletes a CD entry based on inputted ID (delID).
        
        Args:
            delID (int): the ID inputted by the user for the entry to be deleted
            table (list): the current inventory list
        
        Return:
            table (list): the updated inventory list
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == delID:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed.\n')
        else:
            print('Could not find this CD!\n')
        return table

    @staticmethod
    def generate_id(inv_table):
        """Generates a CD ID based on lstTbl length. Starts at 1 and increments until CD ID is a unique value.
        
        Args:
            inv_table (list): the current inventory list
        
        Returns:
            cd_id (int): the auto-generated CD ID
        """
        cd_id = '' #local variable for generating CD ID
        cd_id = 1
        while any(cd_id == row['ID'] for row in inv_table):
            cd_id = cd_id + 1
        return cd_id

    @staticmethod
    def get_int_input(input_val):
        """Attempts to cast the inputted value as an integer.
        
        Args:
            input_val (string): the inputted value
        
        Returns:
            int_val (int): the input value cast as an integer
        """
        try:
            int_val = int(input_val)
            return int_val
        except ValueError:
            print ('Input must be an integer. Returning to menu.')
            return None


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Attempts to load and unpickle a 2D list of dictionaries from the data file
        
        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
        
        Returns:
            table (list): the updated inventory table
        """
        try:
            with open(file_name, 'rb') as fileObj:
                table = pickle.load(fileObj)
        except FileNotFoundError:
            print('\nNo save file available.')
        except EOFError: #if file is blank
            print('\nNo data in file to load.')
        except pickle.UnpicklingError:
            print('\nUnable to load from file.')
        
        return table


    @staticmethod
    def write_file(file_name, table):
        """Attempts to write the lstTbl in inventory to the data file via pickling.
        
        Includes error processing.
        
        Args:
            file_name (str): the name of the file we are saving to
            table (list): the current inventory table
        
        Returns:
            None
        """
        try:
            with open(file_name, 'wb') as fileObj:
                pickle.dump(table, fileObj)
            print('The inventory was saved to {}'.format(file_name))
        except pickle.PicklingError:
            print('The save attempt was not successful.')


# -- PRESENTATION (Input/Output) -- #
class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user
        
        Args:
            None.
        
        Returns:
            None.
        """
        print('\n\n[[ Menu ]]\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection.
        
        Args:
            None.
            
        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x
        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table.
        
        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
        
        Returns:
            None.
        """
        if len(table) > 0:
            print('======= The Current Inventory: =======')
            print('ID\tCD Title (by: Artist)\n')
            for row in table:
                print('{}\t{} (by: {})'.format(*row.values()))
            print('======================================')
        else:
            print('No entries in inventory table to show.\n')

    @staticmethod
    def input_cd(cd_id, inv_table):
        """Gets the CD entry fields (ID, Title, Artist). Calls generate_id() to get auto ID instead of user input.
        
        Args:
            cd_id (int): the auto-generated ID from DataProcessor.generate_id()
            inv_table (list): the current inventory table
            
        Returns:
            cd_id (int): cleaned and validated inputted ID for a CD
            cd_title (str): cleaned inputted CD title
            cd_artist (string): cleaned inputted CD artist
        """
        print('CD ID: ', cd_id)
        cd_title = input('What is the CD\'s title? ').strip()
        cd_artist = input('What is the Artist\'s name? ').strip()
        return cd_id, cd_title, cd_artist


# -- MAIN BODY -- #
# 1. When program starts, read in the currently saved Inventory
lstTbl = FileProcessor.read_file(strFileName, lstTbl)
IO.show_inventory(lstTbl)


# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()


    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break


    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file, otherwise reload will be canceled.\n')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.


    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        intID = DataProcessor.generate_id(lstTbl)
        intID, strTitle, strArtist = IO.input_cd(intID, lstTbl)
        
        # 3.3.2 Add item to the table
        lstTbl = DataProcessor.add_entry(intID, strTitle, strArtist, lstTbl)
        
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.


    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.


    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        strID = input('Which ID would you like to delete? ').strip()
        intIDDel = DataProcessor.get_int_input(strID) #tries to cast as int
        
        # 3.5.2 search thru table and delete CD
        if intIDDel:
            lstTbl = DataProcessor.delete_entry(intIDDel, lstTbl)

        IO.show_inventory(lstTbl)
        continue  # start loop back at top.


    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.


    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')
