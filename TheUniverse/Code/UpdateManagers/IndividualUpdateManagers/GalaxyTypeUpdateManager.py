'''

----SUMMARY---
Allows the user to update
a galaxy type

---IMPORTS---
BaseUpdateManager:

Used to obtain base functionality
for a more specific update, since this
class is for the specific update on
galaxy types

tkinter - for all of the UI

mysql:

for performing the update queries and
search query needed to display the initial
record to the user

'''

# from BaseInsertionManager import BaseInsertionManager
from Code.UpdateManagers.BaseUpdateManager import BaseUpdateManager
from tkinter import *
import mysql

class GalaxyTypeUpdateManager(BaseUpdateManager):


    global galaxyTypesToChooseFromDropDown

    # initial record UI
    global initialGalaxyTypeNameLabel

    # updating UI
    global newGalaxyNameInsertionBox

    # this will store the name of the galaxy type to query for (aka the primary key)
    global selectedGalaxyType

    # perform the galaxy type update right here
    def confirm(self):
        thereWasAnError = False

        if (self.insertionValidator.validateWord(False, self.selectedGalaxyType.get(), "[INITIAL RECORD] Selected Galaxy type") == False):
            thereWasAnError = True

        newTypeName = self.newGalaxyNameInsertionBox.get()
        if (self.insertionValidator.validateWord(False, newTypeName, "[NEW RECORD] New galaxy type name cannot be left empty!") == False):
            thereWasAnError = True

        if (thereWasAnError == False):

            messageToDisplay = "1.) Change galaxy type from " + self.selectedGalaxyType.get() + " to " + newTypeName

            recordChanges = []
            recordChanges.append(newTypeName)

            # form the query based on the new values the user has inputed:
            query = '''
            
                UPDATE GalaxyTypes 
                SET GalaxyType = %s 
                        
            '''

            newDescriptionDir = self.rightFrameTextBoxManager.descriptionDirectory
            if (self.insertionValidator.validateWord(False, newDescriptionDir, "")):
                # user wants to change the description dir as well:
                query += ", Description = %s"
                recordChanges.append(newDescriptionDir)
                messageToDisplay += "\n" + "2.) Change galaxy type description dir to: " + newDescriptionDir

            query += "WHERE GalaxyType = %s;"

            recordChanges.append(self.selectedGalaxyType.get())

            try:
                database = self.makeConnectionToDatabase()
                cursor = database.cursor()
                cursor.execute(query, recordChanges)

                if (self.showConfirmationPopUp(messageToDisplay) == True):
                    self.showSuccessMessage(3, 0, 2)

                    # clear all UI:
                    self.selectedGalaxyType.set('N/A')
                    self.leftFrameTextBoxManager.resetDescriptionUI(4, 0)
                    self.rightFrameTextBoxManager.resetDescriptionUI(2, 0)
                    self.newGalaxyNameInsertionBox.delete(0, END)

                    database.commit()

                    # after making the commit, update the galaxy type drop down to reflect the new value:
                    query = '''

                                SELECT GalaxyType 
                                FROM GalaxyTypes;

                            '''
                    cursor.execute(query)

                    galaxyTypesToChooseFrom = []
                    galaxyTypesToChooseFrom.append('N/A')
                    records = cursor.fetchall()
                    for galaxyType in records:
                        galaxyTypesToChooseFrom.append(galaxyType[0])

                    self.galaxyTypesToChooseFromDropDown.grid_forget()
                    self.galaxyTypesToChooseFromDropDown.destroy()

                    self.galaxyTypesToChooseFromDropDown = OptionMenu(self.leftFrame, self.selectedGalaxyType,
                                                                      *galaxyTypesToChooseFrom,
                                                                      command=self.selectGalaxyType)
                    self.galaxyTypesToChooseFromDropDown.grid(row=0, column=1, sticky=W + E)

                else:
                    database.rollback()

                database.close()

            except mysql.connector.Error as error:
                self.insertionValidator.errorMessage = self.errorMessageForWhenCommitFailsDueToSqlError + ": " + str(error)
                database.rollback()
                self.showErrorMessage(3, 0, 2)
        else:
            self.showErrorMessage(3, 0, 2)
        self.insertionValidator.errorMessage = ''

    # select the galaxy type to update and populate fields accordingly
    # this method linked to the galaxiesToChooseFromDropDown
    def selectGalaxyType(self, selectedGalaxyTypeName):

        if (selectedGalaxyTypeName != 'N/A'):

            # query for this record and display its current attributes for updating:
            database = self.makeConnectionToDatabase()
            cursor = database.cursor()
            query = '''
            
                SELECT * 
                FROM GalaxyTypes 
                WHERE GalaxyType = %s;
            
            '''
            cursor.execute(query, [selectedGalaxyTypeName])
            record = cursor.fetchone()

            if (record != None):
                galaxyTypeRecord = []
                for attribute in record:
                    galaxyTypeRecord.append(attribute)

                # display the results in input fields so that the player can modify them and submit:
                self.initialGalaxyTypeNameLabel.configure(text="Current Galaxy Type Name: " + galaxyTypeRecord[0])

                # display the choose description directory and current directory:
                self.leftFrameTextBoxManager.loadDescriptionWithoutPromptingUser(galaxyTypeRecord[1])

            database.close()

    # present all UI needed to update a galaxy type
    def manageUpdate(self, windowToPutFrameOnto, updateManager, updateTitle):
        BaseUpdateManager.manageUpdate(self, windowToPutFrameOnto, updateManager, updateTitle)

        Label(self.leftFrame, text="Select the galaxy type you wish to modify: ").grid(row=0, column=0)

        self.selectedGalaxyType = StringVar()
        self.selectedGalaxyType.set('N/A')

        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        query = '''
        
            SELECT GalaxyType 
            FROM GalaxyTypes;
        
        '''
        cursor.execute(query)

        galaxyTypesToChooseFrom = []
        galaxyTypesToChooseFrom.append('N/A')
        records = cursor.fetchall()
        if (records != None):
            for galaxyType in records:
                galaxyTypesToChooseFrom.append(galaxyType[0])

        database.close()

        self.galaxyTypesToChooseFromDropDown = OptionMenu(self.leftFrame, self.selectedGalaxyType, *galaxyTypesToChooseFrom, command=self.selectGalaxyType)
        self.galaxyTypesToChooseFromDropDown.grid(row=0, column=1, sticky=W + E)

        self.initialGalaxyTypeNameLabel = Label(self.leftFrame, text="Current Galaxy Type Name: N/A")
        self.initialGalaxyTypeNameLabel.grid(row=1, column=0, columnspan=2)
        self.leftFrameTextBoxManager.initializeDescriptionBoxForReadingOnlyAndNotLoading(self.leftFrame, 4, 0, 5, 0)

        # new record stuff:
        Label(self.rightFrame, text="New Galaxy Type Name: ").grid(row=0, column=0)
        self.newGalaxyNameInsertionBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newGalaxyNameInsertionBox.grid(row=0, column=1)

        self.rightFrameTextBoxManager.initializeDescriptionFormForUserLoading(self.rightFrame, 1, 0, 2, 0, 3, 0)

        # position the cancel and confirm buttons:
        self.cancelButton.grid(row=2, column=0, sticky=W+E)
        self.confirmButton.grid(row=2, column=1, sticky=W+E)
