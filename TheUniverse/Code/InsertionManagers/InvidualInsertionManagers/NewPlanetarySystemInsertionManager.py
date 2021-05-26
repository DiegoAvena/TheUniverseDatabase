'''

----SUMMARY---
Allows the user to insert
a new planetary systems

---IMPORTS---
BaseInsertionManager:

Used to obtain base functionality
for a more specific insertion, since this
class is for the specific insertion of new
planetary systems

tkinter - for all of the UI

connector - for performing the insertion queries

'''

from Code.InsertionManagers.BaseInsertionManager import BaseInsertionManager
from tkinter import *
import mysql.connector

class NewPlanetarySystemInsertionManager(BaseInsertionManager):

    global planetarySystemNameInputBox
    global planetaryDistanceFromEarthInputBox

    global selectedGalaxy
    global galaxiesDropDownBox

    def confirm(self):

        thereWasAnError = False

        systemName = self.planetarySystemNameInputBox.get()
        if (self.insertionValidator.validateWord(False, systemName, "Planetary System Name") == False):
            thereWasAnError = True

        systemDistanceFromEarth = self.planetaryDistanceFromEarthInputBox.get()
        if (self.insertionValidator.validateDecimalValue(systemDistanceFromEarth, False, "System Distance from Earth", True) == False):
            thereWasAnError = True

        if (self.insertionValidator.validateWord(False, self.selectedGalaxy.get(), "Galaxy System is in") == False):
            thereWasAnError = True

        if (thereWasAnError == False):

            plantarySystemRecord = []
            plantarySystemRecord.append(systemName)
            plantarySystemRecord.append(self.insertionValidator.obtainFinalValue(systemDistanceFromEarth))
            plantarySystemRecord.append(self.selectedGalaxy.get())

            try:
                database = self.makeConnectionToDatabase()
                cursor = database.cursor()
                query = '''

                                INSERT INTO PlanetarySystems 
                                VALUES (%s, %s, %s);

                            '''

                cursor.execute(query, plantarySystemRecord)

                messageToShowInPopUp = "Planetary system name: " + plantarySystemRecord[0] + "\n" + \
                                       "Planetary system distance from Earth: " + str(plantarySystemRecord[1]) + "\n" + \
                                       "Planetary system galaxy name: " + str(plantarySystemRecord[2])

                if (self.showConfirmationPopUp(messageToShowInPopUp)):
                    database.commit()

                    # reset all input fields and values:
                    self.planetarySystemNameInputBox.delete(0, END)
                    self.planetaryDistanceFromEarthInputBox.delete(0, END)
                    self.selectedGalaxy.set('N/A')
                    self.showSuccessMessage(4, 0, 2)
                else:
                    database.rollback()
            except mysql.connector.Error as error:
                self.insertionValidator.errorMessage = self.errorMessageForWhenCommitFailsDueToSqlError + ": " + str(error)
                self.showErrorMessage(4, 0, 2)
                database.rollback()

            database.close()
        else:
            self.showErrorMessage(4, 0, 2)

        self.insertionValidator.errorMessage = ''

    def manageInsertion(self, windowToPutFrameOnto, insertionManager, insertionTitle):
        BaseInsertionManager.manageInsertion(self, windowToPutFrameOnto, insertionManager, insertionTitle)

        Label(self.insertionFrame, text="System Name (Required): ").grid(row=0, column=0)
        self.planetarySystemNameInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.planetarySystemNameInputBox.grid(row=0, column=1)

        Label(self.insertionFrame, text="System distance from earth (ly): ").grid(row=1, column=0)
        self.planetaryDistanceFromEarthInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.planetaryDistanceFromEarthInputBox.grid(row=1, column=1)

        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        query = '''
        
            SELECT Name 
            FROM Galaxies
        
        '''

        cursor.execute(query)
        records = cursor.fetchall()
        database.close()

        galaxies = []
        galaxies.append('N/A')

        self.selectedGalaxy = StringVar()
        self.selectedGalaxy.set(galaxies[0])
        for galaxy in records:
            galaxies.append(galaxy[0])

        Label(self.insertionFrame, text="Select the galaxy this system is in (required): ").grid(row=2, column=0)
        self.galaxiesDropDownBox = OptionMenu(self.insertionFrame, self.selectedGalaxy, *galaxies)
        self.galaxiesDropDownBox.grid(row=2, column=1)

        self.confirmButton.grid(row=3, column=0, sticky=W+E)
        self.cancelButton.grid(row=3, column=1, sticky=W+E)
