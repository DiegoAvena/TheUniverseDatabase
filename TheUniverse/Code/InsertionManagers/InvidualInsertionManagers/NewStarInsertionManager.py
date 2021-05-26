'''
----SUMMARY---
Allows the user to insert
a new star

---IMPORTS---
BaseInsertionManager:

Used to obtain base functionality
for a more specific insertion, since this
class is for the specific insertion of new
stars

tkinter - for all of the UI

connector - for performing the insertion queries
'''

from Code.InsertionManagers.BaseInsertionManager import BaseInsertionManager
from tkinter import *
import mysql.connector

class NewStarInsertionManager(BaseInsertionManager):

    global starNameInputBox
    global starMassInputBox
    global starRadiusInputBox
    global distanceFromEarthInputBox

    global selectedEvolutionaryStage
    global evolutionaryStageDropDownBox

    global selectedPlanetarySystem
    global planetarySystemDropDownBox

    def confirm(self):

        thereWasAnError = False

        starName = self.starNameInputBox.get()

        if (self.insertionValidator.validateWord(False, starName, "Star Name") == False):
            thereWasAnError = True

        starMass = self.starMassInputBox.get()
        if (self.insertionValidator.validateDecimalValue(starMass, False, "Star Mass", True) == False):
            thereWasAnError = True

        starRadius = self.starRadiusInputBox.get()
        if (self.insertionValidator.validateDecimalValue(starRadius, False, "Star Radius", True) == False):
            thereWasAnError = True

        distanceFromEarth = self.distanceFromEarthInputBox.get()
        if (self.insertionValidator.validateDecimalValue(distanceFromEarth, False, "Distance From Earth", True) == False):
            thereWasAnError = True

        if (self.insertionValidator.validateWord(False, self.selectedPlanetarySystem.get(), "Planetary System") == False):
            thereWasAnError = True

        if (thereWasAnError == False):

            starRecord = []
            starRecord.append(starName)
            starRecord.append(self.insertionValidator.obtainFinalValue(starMass))
            starRecord.append(self.insertionValidator.obtainFinalValue(starRadius))
            starRecord.append(self.insertionValidator.obtainFinalValue(self.selectedEvolutionaryStage.get()))
            starRecord.append(self.insertionValidator.obtainFinalValue(distanceFromEarth))
            starRecord.append(self.selectedPlanetarySystem.get())
            starRecord.append(self.insertionValidator.obtainFinalValue(self.imageDir))

            try:
                database = self.makeConnectionToDatabase()
                cursor = database.cursor()
                query = '''

                                INSERT INTO Stars 
                                VALUES (%s, %s, %s, %s, %s, %s, %s);

                            '''
                cursor.execute(query, starRecord)

                messageToShowInPopUp = "Star Name: " + str(starRecord[0]) + "\n" + \
                                       "Star Mass: " + str(starRecord[1]) + "\n" + \
                                       "Star Radius: " + str(starRecord[2]) + "\n" + \
                                       "Star Evolutionary Stage: " + str(starRecord[3]) + "\n" + \
                                       "Star Distance From Earth: " + str(starRecord[4]) + "\n" + \
                                       "Star System: " + str(starRecord[5]) + "\n" + \
                                       "Star Image Directory: " + str(starRecord[6])

                if (self.showConfirmationPopUp(messageToShowInPopUp) == True):
                    database.commit()
                    self.showSuccessMessage(10, 0, 2)

                    # reset all UI
                    self.starNameInputBox.delete(0, END)
                    self.starMassInputBox.delete(0, END)
                    self.starRadiusInputBox.delete(0, END)
                    self.distanceFromEarthInputBox.delete(0, END)

                    self.selectedEvolutionaryStage.set('N/A')

                    self.selectedPlanetarySystem.set('N/A')
                    self.resetImageUI(2)
                else:
                    database.rollback()
            except mysql.connector.Error:
                self.insertionValidator.errorMessage = self.errorMessageForWhenCommitFailsDueToSqlError
                self.showErrorMessage(10, 0, 2)
                database.rollback()

            database.close()

        else:
            self.showErrorMessage(10, 0, 2)

        self.insertionValidator.errorMessage = ''

    def manageInsertion(self, windowToPutFrameOnto, insertionManager, insertionTitle):
        BaseInsertionManager.manageInsertion(self, windowToPutFrameOnto, insertionManager, insertionTitle)

        Label(self.insertionFrame, text="Star Name (Required): ").grid(row=0, column=0)
        self.starNameInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.starNameInputBox.grid(row=0, column=1)

        Label(self.insertionFrame, text="Star Mass (Solar Mass): ").grid(row=1, column=0)
        self.starMassInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.starMassInputBox.grid(row=1, column=1)

        Label(self.insertionFrame, text="Star Radius (Solar Radius): ").grid(row=2, column=0)
        self.starRadiusInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.starRadiusInputBox.grid(row=2, column=1)

        Label(self.insertionFrame, text="Star Distance From Earth (ly): ").grid(row=3, column=0)
        self.distanceFromEarthInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.distanceFromEarthInputBox.grid(row=3, column=1)

        Label(self.insertionFrame, text="Select an evolutionary stage: ").grid(row=4, column=0)

        database = self.makeConnectionToDatabase()
        cursor = database.cursor()

        query = '''

            SELECT EvolutionaryStage 
            FROM EvolutionaryStages;

        '''
        cursor.execute(query)
        records = cursor.fetchall()
        evolutionaryStages = []
        evolutionaryStages.append('N/A')
        for evolutionaryStage in records:
            evolutionaryStages.append(evolutionaryStage[0])

        self.selectedEvolutionaryStage = StringVar()
        self.selectedEvolutionaryStage.set(evolutionaryStages[0])

        self.evolutionaryStageDropDownBox = OptionMenu(self.insertionFrame, self.selectedEvolutionaryStage, *evolutionaryStages)
        self.evolutionaryStageDropDownBox.grid(row=4, column=1)

        query = '''
        
            SELECT Name 
            FROM PlanetarySystems;
        
        '''
        cursor.execute(query)
        records = cursor.fetchall()
        planetarySystems = []
        planetarySystems.append('N/A')
        for plantarySystem in records:
            planetarySystems.append(plantarySystem[0])

        self.selectedPlanetarySystem = StringVar()
        self.selectedPlanetarySystem.set(planetarySystems[0])

        Label(self.insertionFrame, text="Select planetary system: ").grid(row=5, column=0)
        self.planetarySystemDropDownBox = OptionMenu(self.insertionFrame, self.selectedPlanetarySystem, *planetarySystems)
        self.planetarySystemDropDownBox.grid(row=5, column=1)

        self.loadImageDirectoryButton.grid(row=6, column=0, columnspan=2)
        self.initializeImageDirLabelPos(7, 0, 2)
        self.imageCanvas.grid(row=8, column=0, columnspan=2)

        self.confirmButton.grid(row=9, column=0, sticky=W + E)
        self.cancelButton.grid(row=9, column=1, sticky=W + E)
