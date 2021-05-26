'''

----SUMMARY---
Allows the user to update
an evolutionary stage

---IMPORTS---
BaseUpdateManager:

Used to obtain base functionality
for a more specific update, since this
class is for the specific update on
Evolutionary Stages

tkinter - for all of the UI

mysql:

for performing the update queries and
search query needed to display the initial
record to the user

'''

from Code.UpdateManagers.BaseUpdateManager import BaseUpdateManager
from tkinter import *
import mysql

class EvolutionaryStageUpdateManager(BaseUpdateManager):

    global evolutionaryStagesToChooseFromDropdown
    global initialEvolutionaryStageNameLabel
    global newEvolutionaryStageNameInsertionBox

    # this will store the name of the galaxy type to query for (aka the primary key)
    global selectedEvolutionaryStage

    def confirm(self):
        thereWasAnError = False

        if (self.insertionValidator.validateWord(False, self.selectedEvolutionaryStage.get(),
                                                 "[INITIAL RECORD] Selected Evolutionary Stage") == False):
            thereWasAnError = True

        newStageName = self.newEvolutionaryStageNameInsertionBox.get()
        if (self.insertionValidator.validateWord(False, newStageName,
                                                 "[NEW RECORD] New evolutionary stage name cannot be left empty!") == False):
            thereWasAnError = True

        if (thereWasAnError == False):

            messageToDisplay = "1.) Change evolutionary stage from " + self.selectedEvolutionaryStage.get() + " to " + newStageName

            recordChanges = []
            recordChanges.append(newStageName)

            # form the query based on the new values the user has inputed:
            query = '''

                UPDATE EvolutionaryStages 
                SET EvolutionaryStage = %s 

            '''

            newDescriptionDir = self.rightFrameTextBoxManager.descriptionDirectory
            if (self.insertionValidator.validateWord(False, newDescriptionDir, "")):
                # user wants to change the description dir as well:
                query += ", Description = %s"
                recordChanges.append(newDescriptionDir)
                messageToDisplay += "\n" + "2.) Change evolutionary stage description dir to: " + newDescriptionDir

            query += "WHERE EvolutionaryStage = %s;"

            recordChanges.append(self.selectedEvolutionaryStage.get())

            try:
                database = self.makeConnectionToDatabase()
                cursor = database.cursor()
                cursor.execute(query, recordChanges)

                if (self.showConfirmationPopUp(messageToDisplay) == True):
                    self.showSuccessMessage(3, 0, 2)

                    # clear all UI:
                    self.selectedEvolutionaryStage.set('N/A')
                    self.leftFrameTextBoxManager.resetDescriptionUI(4, 0)
                    self.rightFrameTextBoxManager.resetDescriptionUI(2, 0)
                    self.newEvolutionaryStageNameInsertionBox.delete(0, END)

                    database.commit()

                    # after making the commit, update the galaxy type drop down to reflect the new value:
                    query = '''

                                SELECT EvolutionaryStage
                                FROM EvolutionaryStages;

                            '''
                    cursor.execute(query)

                    stagesToChooseFrom = []
                    stagesToChooseFrom.append('N/A')
                    records = cursor.fetchall()
                    for stage in records:
                        stagesToChooseFrom.append(stage[0])

                    self.evolutionaryStagesToChooseFromDropdown.grid_forget()
                    self.evolutionaryStagesToChooseFromDropdown.destroy()

                    self.evolutionaryStagesToChooseFromDropdown = OptionMenu(self.leftFrame, self.selectedEvolutionaryStage,
                                                                      *stagesToChooseFrom,
                                                                      command=self.selectedEvolutionaryStage)
                    self.evolutionaryStagesToChooseFromDropdown.grid(row=0, column=1, sticky=W + E)

                else:
                    database.rollback()

                database.close()

            except mysql.connector.Error as error:
                self.insertionValidator.errorMessage = self.errorMessageForWhenCommitFailsDueToSqlError + ": " + str(
                    error)
                database.rollback()
                self.showErrorMessage(3, 0, 2)
        else:
            self.showErrorMessage(3, 0, 2)
        self.insertionValidator.errorMessage = ''

    def selectEvolutionaryStage(self, selectedStage):

        if (selectedStage != 'N/A'):

            # query for this record and display its current attributes for updating:
            database = self.makeConnectionToDatabase()
            cursor = database.cursor()
            query = '''

                SELECT * 
                FROM EvolutionaryStages 
                WHERE EvolutionaryStage = %s;

            '''
            cursor.execute(query, [selectedStage])
            record = cursor.fetchone()

            if (record != None):
                stageRecord = []
                for attribute in record:
                    stageRecord.append(attribute)

                # display the results in input fields so that the player can modify them and submit:
                self.initialEvolutionaryStageNameLabel.configure(text="Current Stage Name: " + stageRecord[0])

                # display the choose description directory and current directory:
                self.leftFrameTextBoxManager.loadDescriptionWithoutPromptingUser(stageRecord[1])

            database.close()



    def manageUpdate(self, windowToPutFrameOnto, updateManager, updateTitle):
        BaseUpdateManager.manageUpdate(self, windowToPutFrameOnto, updateManager, updateTitle)

        Label(self.leftFrame, text="Select the evolutionary stage you wish to modify: ").grid(row=0, column=0)

        self.selectedEvolutionaryStage = StringVar()
        self.selectedEvolutionaryStage.set('N/A')

        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        query = '''

                    SELECT EvolutionaryStage 
                    FROM EvolutionaryStages;

                '''
        cursor.execute(query)

        stagesToChooseFrom = []
        stagesToChooseFrom.append('N/A')
        records = cursor.fetchall()
        for stage in records:
            stagesToChooseFrom.append(stage[0])

        database.close()

        self.evolutionaryStagesToChooseFromDropdown = OptionMenu(self.leftFrame, self.selectedEvolutionaryStage,
                                                          *stagesToChooseFrom, command=self.selectEvolutionaryStage)
        self.evolutionaryStagesToChooseFromDropdown.grid(row=0, column=1, sticky=W + E)

        self.initialEvolutionaryStageNameLabel = Label(self.leftFrame, text="Current Evolutionary Stage: N/A")
        self.initialEvolutionaryStageNameLabel.grid(row=1, column=0, columnspan=2)
        self.leftFrameTextBoxManager.initializeDescriptionBoxForReadingOnlyAndNotLoading(self.leftFrame, 4, 0, 5, 0)

        # new record stuff:
        Label(self.rightFrame, text="New Evolutionary Stage Name: ").grid(row=0, column=0)
        self.newEvolutionaryStageNameInsertionBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newEvolutionaryStageNameInsertionBox.grid(row=0, column=1)

        self.rightFrameTextBoxManager.initializeDescriptionFormForUserLoading(self.rightFrame, 1, 0, 2, 0, 3, 0)

        # position the cancel and confirm buttons:
        self.cancelButton.grid(row=2, column=0, sticky=W + E)
        self.confirmButton.grid(row=2, column=1, sticky=W + E)
