'''
----SUMMARY----
contains the base functionality needed for a
record deletion from a table that has a single
column primary key. This behavior includes things like
the dropdown menu needed to select the thing to delete,
etc.

----IMPORTS----

BaseDataModifierManager:
used for base data base modifying functionality,
since this specific option will be modifying the table
with insertions

tkinter - for all of the UI

mysql - for performing the deletion query
'''

from tkinter import *
from Code.BaseDataModifierManager import BaseDataModifierManager
import mysql

class BaseDeletionManager(BaseDataModifierManager):

    global selectedItemToDelete
    global itemsToDeleteDropDown
    global positionOfDropDown
    global dropdownColumnspan
    global searchQuery
    global deletionQuery
    global tableName

    def confirm(self):
        thereWasAnError = False
        if (self.insertionValidator.validateWord(False, self.selectedItemToDelete.get(), "Item to delete") == False):
            thereWasAnError = True

        if (thereWasAnError == False):
            confirmationMessage = "-Remove record with ID " + self.selectedItemToDelete.get() + " from " + self.tableName
            database = self.makeConnectionToDatabase()
            cursor = database.cursor()

            try:
                cursor.execute(self.deletionQuery, [self.selectedItemToDelete.get()])
                if (self.showConfirmationPopUp(confirmationMessage)):
                    database.commit()
                    self.showSuccessMessage(2, 0, 2)
                    self.resetItemsToDeleteDropDown()
                else:
                    database.rollback()
            except mysql.connector.Error as error:
                self.insertionValidator.errorMessage = self.errorMessageForWhenCommitFailsDueToSqlError + ": " + str(error)
                self.showErrorMessage(2, 0, 2)
            database.close()
        else:
            self.showErrorMessage(2, 0, 2)
        self.insertionValidator.errorMessage = ''

    def manageDeletion(self, windowToPutFrameOnto, insertionManager, insertionTitle, labelText, tableName, searchQuery, deletionQuery):
        BaseDeletionManager.manageBaseModifierManager(self, windowToPutFrameOnto, insertionManager, insertionTitle)
        self.successMessage = "Record Deleted!"
        self.errorMessageForWhenCommitFailsDueToSqlError = "Failed to delete a record due to a mysql error: "
        self.tableName = tableName
        self.deletionQuery = deletionQuery
        self.initializeItemsToDeleteDropDown(0, 1, labelText, searchQuery, self.insertionFrame)
        self.confirmButton.grid(row=1, column=0, sticky=W+E)
        self.cancelButton.grid(row=1, column=1, sticky=W+E)

    def resetItemsToDeleteDropDown(self):
        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        cursor.execute(self.searchQuery)
        records = cursor.fetchall()
        names = []
        names.append('N/A')
        if (records != None):
            for name in records:
                names.append(name[0])
        self.selectedItemToDelete.set('N/A')
        self.thingsToUpdateDropDown.grid_forget()
        self.thingsToUpdateDropDown.destroy()
        self.thingsToUpdateDropDown = OptionMenu(self.insertionFrame, self.selectedItemToDelete, *names)
        self.thingsToUpdateDropDown.grid(row=self.positionOfDropDown[0], column=self.positionOfDropDown[1], sticky=W + E)
        database.close()

    def initializeItemsToDeleteDropDown(self, dropDownRow, dropDownColumn, labelText, searchQuery, frameToPlaceItemsOnto):

        self.searchQuery = searchQuery
        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        cursor.execute(self.searchQuery)
        records = cursor.fetchall()
        names = []
        names.append('N/A')
        if (records != None):
            for name in records:
                names.append(name[0])

        self.selectedItemToDelete = StringVar()
        self.selectedItemToDelete.set('N/A')

        self.frameToPlaceItemsOnto = frameToPlaceItemsOnto
        Label(self.frameToPlaceItemsOnto, text=labelText).grid(row=dropDownRow, column=dropDownColumn - 1)
        self.thingsToUpdateDropDown = OptionMenu(self.insertionFrame, self.selectedItemToDelete, *names)
        self.thingsToUpdateDropDown.grid(row=dropDownRow, column=dropDownColumn, sticky=W + E)
        self.positionOfDropDown = [dropDownRow, dropDownColumn]
        database.close()
