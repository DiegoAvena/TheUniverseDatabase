'''

-----SUMMARY-----
Contains all of the base functionality needed for each
of the more specific update managers (like Galaxy Update,
Galaxy Type update, etc)

This base functionality includes things like the dropdown needed
to select the item to update, the initialization of the left
and right frames needed to display the initial and new records,
etc.

----IMPORTS----
tkinter - used for the UI

BaseDataModifierManager:
used for base data base modifying functionality,
since this specific option will be modifying the table
with updates

'''

from tkinter import *
# from Code.InsertionManagers.BaseInsertionManager import BaseInsertionManager
from Code.BaseDataModifierManager import BaseDataModifierManager
from Code.Displayers.TextBoxManager import TextBoxManager

class BaseUpdateManager(BaseDataModifierManager):

    # stores any chunk of text for the initial record
    global leftFrameTextBoxManager

    # displays a new chunk of text the user wants to load
    # in as part of the update
    global rightFrameTextBoxManager

    # displays the contents of the initial record
    # the user is trying to update
    global leftFrame

    # allows user to input new changes they
    # want as part of the update
    global rightFrame

    global selectedThingToUpdate # stores the name of the thing to update (the primary key column basically)
    global locationOfThingToUpdateDropdown

    # stores the initial contents of the current record as is
    # in the database
    global initialRecord

    # stores the query needed to display all of the
    # things the user can select from and update
    global searchQuery

    def selectThingToUpdate(self, nameOfThingSelected):
        pass

    def resetThingToSelectDropdownMenu(self):
        self.selectedThingToUpdate.set('N/A')
        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        cursor.execute(self.searchQuery)
        records = cursor.fetchall()
        names = []
        names.append('N/A')
        if (records != None):
            for name in records:
                names.append(name[0])
        database.close()

    # initializes the dropdown menu
    def setUpThingToUpdateSelector(self, row, column, query, labelText):
        self.searchQuery = query
        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        names = []
        names.append('N/A')
        if (records != None):
            for name in records:
                names.append(name[0])

        self.selectedThingToUpdate = StringVar()
        self.selectedThingToUpdate.set('N/A')

        Label(self.leftFrame, text=labelText).grid(row=row, column=column - 1)
        self.thingsToUpdateDropDown = OptionMenu(self.leftFrame, self.selectedThingToUpdate, *names,
                                                command=self.selectThingToUpdate)
        self.thingsToUpdateDropDown.grid(row=row, column=column, sticky=W + E)
        self.locationOfThingToUpdateDropdown = [row, column]
        database.close()

    # initialize all UI needed for the user to perform an update
    def manageUpdate(self, windowToPutFrameOnto, updateManager, updateTitle):
        BaseDataModifierManager.manageBaseModifierManager(self, windowToPutFrameOnto, updateManager, updateTitle)

        self.successMessage = "Record Updated!"
        self.errorMessageForWhenCommitFailsDueToSqlError = "Failed to update record due to an sql error"

        # show all initial values on left side, and all new values on right side?
        self.leftFrame = LabelFrame(self.insertionFrame, text="INITIAL RECORD VALUES")
        self.leftFrame.grid(row=0, column=0)

        self.rightFrame = LabelFrame(self.insertionFrame, text="NEW VALUES")
        self.rightFrame.grid(row=0, column=1)

        self.leftFrameTextBoxManager = TextBoxManager()
        self.rightFrameTextBoxManager = TextBoxManager()