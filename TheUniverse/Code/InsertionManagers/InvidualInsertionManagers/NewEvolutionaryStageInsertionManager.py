'''

----SUMMARY---
Allows the user to insert
a new evolutionary stage

---IMPORTS---
BaseInsertionManager:

Used to obtain base functionality
for a more specific insertion, since this
class is for the specific insertion of new
Evolutionary Stages

tkinter - for all of the UI

connector - for performing the insertion queries

'''

from Code.InsertionManagers.BaseInsertionManager import BaseInsertionManager
from tkinter import *
import mysql.connector

class NewEvolutionaryStageInsertionManager(BaseInsertionManager):

    global evolutionaryStageInputField

    def confirm(self):
        thereWasAnError = False

        # check if data is valid:
        stageTypeName = self.evolutionaryStageInputField.get()
        if (self.insertionValidator.validateWord(False, stageTypeName, "Evolutionary Stage Type Name") == False):
            thereWasAnError = True

        if (self.insertionValidator.validateWord(False, self.descriptionDirectory,
                                                 "Evolutionary Stage Type Description Directory") == False):
            thereWasAnError = True

        if (thereWasAnError == False):

            print("Can enter new record")
            newEvolutionaryStageTypeRecord = [stageTypeName, self.descriptionDirectory]
            print("The new evolutionary stage type record: " + str(newEvolutionaryStageTypeRecord))

            try:
                database = self.makeConnectionToDatabase()
                cursor = database.cursor()
                query = '''

                                        INSERT IGNORE 
                                        INTO EvolutionaryStages VALUES (%s, %s);

                                    '''
                cursor.execute(query, newEvolutionaryStageTypeRecord)

                messageToShowInPopUp = "Evolutionary stage name: " + str(newEvolutionaryStageTypeRecord[0]) + '\n' + \
                                       "Evolutionary stage description directory: " + str(newEvolutionaryStageTypeRecord[1])

                if (self.showConfirmationPopUp(messageToShowInPopUp) == True):
                    self.showSuccessMessage(5, 0, 2)

                    # clear all text fields:
                    self.evolutionaryStageInputField.delete(0, END)

                    self.resetDescriptionUI(2, 0)
                    self.descriptionDirectory = ''
                    database.commit()
                else:
                    database.rollback()
            except mysql.connector.Error:
                self.insertionValidator.errorMessage = self.errorMessageForWhenCommitFailsDueToSqlError
                self.showErrorMessage(5, 0, 2)
                database.rollback()

            database.close()

        else:
            self.showErrorMessage(5, 0, 2)

        self.insertionValidator.errorMessage = ""

    def manageInsertion(self, windowToPutFrameOnto, insertionManager, insertionTitle):
        BaseInsertionManager.manageInsertion(self, windowToPutFrameOnto, insertionManager, insertionTitle)

        # place the evolutionary stage label and input fields:
        Label(self.insertionFrame, text="Evolutionary Stage Name: ").grid(row=0, column=0)
        self.evolutionaryStageInputField = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.evolutionaryStageInputField.grid(row=0, column=1)

        # place galaxy type load description file button
        self.initializeDescriptionForm(1, 0, 2, 0, 3, 0)

        # position the confirm button
        self.confirmButton.grid(row=4, column=0, sticky=W + E)

        # position the cancel button
        self.cancelButton.grid(row=4, column=1, sticky=W + E)
