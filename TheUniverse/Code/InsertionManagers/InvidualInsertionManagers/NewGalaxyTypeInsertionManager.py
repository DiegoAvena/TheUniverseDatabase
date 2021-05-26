'''

----SUMMARY---
Allows the user to insert
a new galaxy type

---IMPORTS---
BaseInsertionManager:

Used to obtain base functionality
for a more specific insertion, since this
class is for the specific insertion of new
galaxy types

tkinter - for all of the UI

connector - for performing the insertion queries

'''

from Code.InsertionManagers.BaseInsertionManager import BaseInsertionManager
from tkinter import *
import mysql.connector

class NewGalaxyTypeInsertionManager(BaseInsertionManager):

    global galaxyTypeNameInputBox

    def confirm(self):

        thereWasAnError = False

        # check if data is valid:
        galaxyTypeName = self.galaxyTypeNameInputBox.get()
        if (self.insertionValidator.validateWord(False, galaxyTypeName, "Galaxy Type Name") == False):
            thereWasAnError = True

        if (self.insertionValidator.validateWord(False, self.descriptionDirectory, "Galaxy Type Description Directory") == False):
            thereWasAnError = True

        if (thereWasAnError == False):
            newGalaxyTypeRecord = [galaxyTypeName, self.descriptionDirectory]

            try:
                database = self.makeConnectionToDatabase()
                cursor = database.cursor()
                query = '''

                               INSERT IGNORE 
                               INTO GalaxyTypes VALUES (%s, %s);

                           '''
                cursor.execute(query, newGalaxyTypeRecord)

                messageToDisplayInPopUp = "Galaxy type name: " + str(galaxyTypeName) + "\n" + \
                                          "Galaxy type description directory: " + str(self.descriptionDirectory)

                if (self.showConfirmationPopUp(messageToDisplayInPopUp) == True):
                    self.showSuccessMessage(5, 0, 2)

                    # clear all text fields:
                    self.galaxyTypeNameInputBox.delete(0, END)
                    self.resetDescriptionUI(2, 0)

                    # commit
                    database.commit()
                else:
                    database.rollback()
            except mysql.connector.Error:
                self.insertionValidator.errorMessage = self.errorMessageForWhenCommitFailsDueToSqlError
                self.showErrorMessage(5, 0, 2)

            database.close()

        else:
            self.showErrorMessage(5, 0, 2)

        self.insertionValidator.errorMessage = ""

    def manageInsertion(self, windowToPutFrameOnto, insertionManager, insertionTitle):
        BaseInsertionManager.manageInsertion(self, windowToPutFrameOnto, insertionManager, insertionTitle)

        # place galaxy type name input box
        Label(self.insertionFrame, text="Galaxy Type Name: ").grid(row=0, column=0)
        self.galaxyTypeNameInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.galaxyTypeNameInputBox.grid(row=0, column=1)

        # place galaxy type load description file button
        self.initializeDescriptionForm(1, 0, 2, 0, 3, 0)

        # position the confirm button
        self.confirmButton.grid(row=4, column=0, sticky=W + E)

        # position the cancel button
        self.cancelButton.grid(row=4, column=1, sticky=W + E)
