'''

----SUMMARY---
Allows the user to update
a planetary system

---IMPORTS---
BaseUpdateManager:

Used to obtain base functionality
for a more specific update, since this
class is for the specific update on
planetary system

tkinter - for all of the UI

mysql:

for performing the update queries and
search query needed to display the initial
record to the user

'''

from Code.UpdateManagers.BaseUpdateManager import BaseUpdateManager
from tkinter import *
import mysql

class PlanetarySystemUpdateManager(BaseUpdateManager):

    # initial record UI
    global initialDistanceFromEarthLabel
    global initialGalaxyNameLabel

    # new changes UI
    global newSystemNameInputBox
    global newDistanceFromEarthInputBox
    global newSelectedGalaxy
    global galaxiesToChooseFromDropDownBox

    # perform the planetary system update
    def confirm(self):
        thereWasAnError = False

        if (self.insertionValidator.validateWord(False, self.selectedThingToUpdate.get(), "Name of system to update") == False):
            thereWasAnError = True

        newSystemName = self.newSystemNameInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newSystemName)):
            thereWasAnError = True
            self.insertionValidator.errorMessage += "Deletion code set for new system name, but system name cannot be empty" + "\n"

        newSystemDistanceFromEarth = self.newDistanceFromEarthInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newSystemDistanceFromEarth)):
            thereWasAnError = True
            self.insertionValidator.errorMessage += "Deletion code set for new system distance from earth, but this cannot be left empty" + "\n"
        elif (self.insertionValidator.validateDecimalValue(newSystemDistanceFromEarth, False, "New system distance from earth", True) == False):
            thereWasAnError = True

        if (thereWasAnError == False):
            # form the query:
            query = '''
            
                UPDATE PlanetarySystems
                SET
            
            '''
            newChanges = []
            messageToShowInConfirmation = ""
            if (len(newSystemName) > 0):
                messageToShowInConfirmation += "Change system name from " + self.initialRecord[0] + " to " + newSystemName + "\n"
                query += " Name = %s"
                newChanges.append(newSystemName)

            if (len(newSystemDistanceFromEarth) > 0):
                if (len(newChanges) > 0):
                    query += ","
                messageToShowInConfirmation += "Change system distance from Earth from " + str(self.initialRecord[1]) + " to " + newSystemDistanceFromEarth + "\n"
                query += " DistanceFromEarth = %s"
                newChanges.append(newSystemDistanceFromEarth)

            if (len(self.newSelectedGalaxy.get()) > 0):
                if (len(newChanges) > 0):
                    query += ","
                messageToShowInConfirmation += "Change galaxy system is in from " + str(self.initialRecord[2]) + " to " + self.newSelectedGalaxy.get() + "\n"
                newChanges.append(self.newSelectedGalaxy.get())
                query += " GalaxyName = %s"

            if (len(newChanges) > 0):
                query += " WHERE Name = %s;"
                newChanges.append(self.selectedThingToUpdate.get())

                database = self.makeConnectionToDatabase()

                try:
                    cursor = database.cursor()
                    cursor.execute(query, newChanges)

                    if (self.showConfirmationPopUp(messageToShowInConfirmation)):
                        database.commit()
                        self.resetAllUI(True)
                        self.resetThingToSelectDropdownMenu()
                        self.showSuccessMessage(2, 0, 2)
                    else:
                        database.rollback()

                except mysql.connector.Error as error:
                    self.insertionValidator.errorMessage = self.errorMessageForWhenCommitFailsDueToSqlError + ": " + str(error)
                    self.showErrorMessage(2, 0, 2)
                    database.rollback()

                database.close()
            else:
                self.insertionValidator.errorMessage = "NOTHING TO UPDATE..."
                self.showErrorMessage(2, 0, 2)
        else:
            self.showErrorMessage(2, 0, 2)

        self.insertionValidator.errorMessage = ''

    # select the system to update or no system to update
    # and populate fields accordingly
    # linked to the things to update dropdown
    def selectThingToUpdate(self, nameOfThingSelected):
        if (nameOfThingSelected != 'N/A'):
            database = self.makeConnectionToDatabase()
            cursor = database.cursor()
            query = '''

                        SELECT * 
                        FROM PlanetarySystems
                        WHERE Name = %s;

                    '''
            cursor.execute(query, [nameOfThingSelected])
            record = cursor.fetchone()
            self.initialRecord = []
            for attribute in record:
                self.initialRecord.append(attribute)

            self.initialDistanceFromEarthLabel.configure(text=record[1])
            self.initialGalaxyNameLabel.configure(text=record[2])
            database.close()
        else:
            self.resetAllUI(False)

    def resetAllUI(self, resetUpdatingUIAsWell):
        self.resetThingToSelectDropdownMenu()
        self.initialGalaxyNameLabel.configure(text='N/A')
        self.initialDistanceFromEarthLabel.configure(text='N/A')

        if (resetUpdatingUIAsWell):
            self.newSelectedGalaxy.set('')
            self.newSystemNameInputBox.delete(0, END)
            self.newDistanceFromEarthInputBox.delete(0, END)

    # initialize all UI needed for performing a system update
    def manageUpdate(self, windowToPutFrameOnto, updateManager, updateTitle):
        BaseUpdateManager.manageUpdate(self, windowToPutFrameOnto, updateManager, updateTitle)
        query = '''
        
            SELECT Name 
            FROM PlanetarySystems;
        
        '''
        self.setUpThingToUpdateSelector(0, 1, query, "Name of system to update: ")

        Label(self.leftFrame, text="Initial distance from earth: ").grid(row=1, column=0)
        self.initialDistanceFromEarthLabel = Label(self.leftFrame, text="N/A")
        self.initialDistanceFromEarthLabel.grid(row=1, column=1)

        Label(self.leftFrame, text="Galaxy system is in: " ).grid(row=2, column=0)
        self.initialGalaxyNameLabel = Label(self.leftFrame, text="N/A")
        self.initialGalaxyNameLabel.grid(row=2, column=1)

        Label(self.rightFrame, text="New system name: ").grid(row=0, column=0)
        self.newSystemNameInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newSystemNameInputBox.grid(row=0, column=1)

        Label(self.rightFrame, text = "New distance from Earth: ").grid(row=1, column=0)
        self.newDistanceFromEarthInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newDistanceFromEarthInputBox.grid(row=1, column=1)

        Label(self.rightFrame, text= "New Galaxy: ").grid(row=2, column=0)

        # user will be able to change the galaxy
        # a system is in from here, so I create a dropdown menu
        # for this right here
        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        query = '''
        
            SELECT Name 
            FROM Galaxies;
        
        '''
        cursor.execute(query)
        records = cursor.fetchall()
        galaxyNames = []
        galaxyNames.append('')
        if (records != None):
            for galaxyName in records:
                galaxyNames.append(galaxyName[0])

        self.newSelectedGalaxy = StringVar()
        self.newSelectedGalaxy.set('')
        self.galaxiesToChooseFromDropDownBox = OptionMenu(self.rightFrame, self.newSelectedGalaxy, *galaxyNames)
        self.galaxiesToChooseFromDropDownBox.grid(row=2, column=1, sticky=W + E)

        self.confirmButton.grid(row=1, column=0, sticky=W+E)
        self.cancelButton.grid(row=1, column=1, sticky=W+E)
