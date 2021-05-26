'''

----SUMMARY----
Contains functionality needed for the deletion of
records from single primary key tables

----IMPORTS----

BaseDeletionManager:
Used to obtain the base functionality needed for
a deletion, since this is a deletion as well, but it
builds on that base functionality by overriding the
manageDeletion method

tkinter - for all of the UI

mysql - for performing the deletion query
'''

from Code.DeletionManagers.BaseDeletionManager import BaseDeletionManager
from tkinter import*
import mysql

class CompositeDeletionManager(BaseDeletionManager):

    global IDOfSecondItemToDeleteDropDown
    global selectedIDOfSecondItemToDelete
    global secondSearchQuery

    def manageDeletion(self, windowToPutFrameOnto, insertionManager, insertionTitle, labelText, tableName, searchQuery, secondSearchQuery, deletionQuery, labelTwoText):
        BaseDeletionManager.manageBaseModifierManager(self, windowToPutFrameOnto, insertionManager, insertionTitle)
        self.successMessage = "Record Deleted!"
        self.errorMessageForWhenCommitFailsDueToSqlError = "Failed to delete a record due to a mysql error: "
        self.tableName = tableName
        self.deletionQuery = deletionQuery
        self.secondSearchQuery = secondSearchQuery
        self.initializeItemsToDeleteDropDown(0, 1, labelText, searchQuery, self.insertionFrame)
        self.initializeSecondIDDropDown(labelTwoText)
        self.confirmButton.grid(row=2, column=0, sticky=W + E)
        self.cancelButton.grid(row=2, column=1, sticky=W + E)

    def selectFirstID(self, firstIDSelected):
        if (firstIDSelected != 'N/A'):
            database = self.makeConnectionToDatabase()
            cursor = database.cursor()
            cursor.execute(self.secondSearchQuery, [firstIDSelected])
            records = cursor.fetchall()
            if (records != None):
                secondIDList = []
                secondIDList.append('N/A')
                for secondID in records:
                    secondIDList.append(secondID[0])

            # now display all of the second IDs for the record the user wants to delete:
            self.IDOfSecondItemToDeleteDropDown.grid_forget()
            self.IDOfSecondItemToDeleteDropDown.destroy()
            self.IDOfSecondItemToDeleteDropDown = OptionMenu(self.insertionFrame, self.selectedIDOfSecondItemToDelete, *secondIDList)
            self.IDOfSecondItemToDeleteDropDown.grid(row=self.positionOfDropDown[0] + 1,
                                                     column=self.positionOfDropDown[1], sticky=W + E)
        else:
            self.resetIDOfSecondItemToDeleteDropDown()

    def confirm(self):
        thereWasAnError = False
        if ((self.insertionValidator.validateWord(False, self.selectedItemToDelete.get(), "ID of first item to delete: ") == False) or
                (self.insertionValidator.validateWord(False, self.selectedIDOfSecondItemToDelete.get(), "Second ID of item to delete: ") == False)):
            thereWasAnError = True

        if (thereWasAnError == False):
            confirmationMessage = "-Remove record with ID One " + self.selectedItemToDelete.get() + " and ID Two "+ self.selectedIDOfSecondItemToDelete.get() +" from " + self.tableName
            database = self.makeConnectionToDatabase()
            cursor = database.cursor()

            try:
                cursor.execute(self.deletionQuery, [self.selectedItemToDelete.get(), self.selectedIDOfSecondItemToDelete.get()])
                if (self.showConfirmationPopUp(confirmationMessage)):
                    database.commit()
                    self.showSuccessMessage(3, 0, 2)
                    self.resetItemsToDeleteDropDown()
                    self.resetIDOfSecondItemToDeleteDropDown()
                else:
                    database.rollback()
            except mysql.connector.Error as error:
                self.insertionValidator.errorMessage = self.errorMessageForWhenCommitFailsDueToSqlError + ": " + str(error)
                self.showErrorMessage(3, 0, 2)
            database.close()
        else:
            self.showErrorMessage(3, 0, 2)
        self.insertionValidator.errorMessage = ''

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
        self.thingsToUpdateDropDown = OptionMenu(self.insertionFrame, self.selectedItemToDelete, *names, command=self.selectFirstID)
        self.thingsToUpdateDropDown.grid(row=self.positionOfDropDown[0], column=self.positionOfDropDown[1], sticky=W + E)
        database.close()

    def resetIDOfSecondItemToDeleteDropDown(self):
        self.selectedIDOfSecondItemToDelete.set('N/A')
        self.IDOfSecondItemToDeleteDropDown.grid_forget()
        self.IDOfSecondItemToDeleteDropDown.destroy()
        self.IDOfSecondItemToDeleteDropDown = OptionMenu(self.insertionFrame, self.selectedIDOfSecondItemToDelete, *['N/A'])
        self.IDOfSecondItemToDeleteDropDown.grid(row=self.positionOfDropDown[0] + 1,
                                                 column=self.positionOfDropDown[1], sticky=W + E)

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
        self.thingsToUpdateDropDown = OptionMenu(self.insertionFrame, self.selectedItemToDelete, *names, command=self.selectFirstID)
        self.thingsToUpdateDropDown.grid(row=dropDownRow, column=dropDownColumn, sticky=W + E)
        self.positionOfDropDown = [dropDownRow, dropDownColumn]
        database.close()

    def initializeSecondIDDropDown(self, labelTwoText):
        Label(self.frameToPlaceItemsOnto, text=labelTwoText).grid(row=self.positionOfDropDown[0] + 1, column=self.positionOfDropDown[1] - 1)

        self.selectedIDOfSecondItemToDelete = StringVar()
        self.selectedIDOfSecondItemToDelete.set('N/A')

        self.IDOfSecondItemToDeleteDropDown = OptionMenu(self.insertionFrame, self.selectedIDOfSecondItemToDelete, ['N/A'])
        self.IDOfSecondItemToDeleteDropDown.grid(row=self.positionOfDropDown[0] + 1, column=self.positionOfDropDown[1], sticky=W+E)
