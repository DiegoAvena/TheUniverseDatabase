'''

----SUMMARY---
Allows the user to update
a moon

---IMPORTS---
BaseUpdateManager:

Used to obtain base functionality
for a more specific update, since this
class is for the specific update on
galaxies

tkinter - for all of the UI

mysql:

for performing the update queries and
search query needed to display the initial
record to the user

ImageDisplayerManager:

This is used to display an image of the
moon on the initial record,
and to allow the user to update this
moon image

messageBox from tkinter:

used to ask the user if they did not
insert a new image because they wish
to delete the initial moon image (provided
that the moon does currently have an image for it), this
item is also used for the same reason for the
description insertion option (if user leaves description empty,
and the initial record has a description, a pop up will show
asking if they left this empty because they want to delete
the old description and leave it blank)

TextBoxManager:

used to display a description of the moon on
the initial record side, and to allow the user
to insert a description on the update side

'''

from Code.UpdateManagers.BaseUpdateManager import BaseUpdateManager
from tkinter import *
from Code.Displayers.ImageDisplayerManager import ImageDisplayerManager
from Code.Displayers.TextBoxManager import TextBoxManager
from tkinter import messagebox
import mysql

class MoonUpdateManager(BaseUpdateManager):

    # these bools needed for changes
    # that are not reflected by the newChanges collection
    # that forms in the confirm method; without these bools,
    # these 2 changes would go unnoticed if they are the only
    # changes the user wants to perform
    global deleteOldImage
    global deleteOldDescription

    # initial record UI
    global initialMoonMassLabel
    global initialPlanetMoonOrbitsLabel
    global initialMoonGravityLabel
    global initialMoonRadiusLabel
    global initialMoonDistanceFromEarthLabel
    global initialMoonSurfaceTemperatureLabel
    global initialMoonEscapeVelocityLabel
    global initialMoonRotationPeriodLabel
    global initialMoonOrbitalPeriodLabel
    global initialMoonImageDisplayer
    global initialMoonDescriptionDisplayer
    global initialMoonDistanceFromPlanetItOrbitsLabel

    # updating UI
    global newMoonNameInputBox
    global newMoonMassInputBox
    global newPlanetMoonOrbitsDropdownBox
    global selectedNewPlanetMoonOrbits
    global newMoonGravityInputBox
    global newMoonRadiusInputBox
    global newMoonDistanceFromEarthInputBox
    global newMoonSurfaceTemperatureInputBox
    global newMoonEscapeVelocityInputBox
    global newMoonRotationPeriodInputBox
    global newMoonOrbitalPeriodInputBox
    global newMoonImageDisplayer
    global newMoonDescriptionDisplayer
    global newMoonDistancefromPlanetItOrbitsInputBox

    # select the moon to update or no moon to update
    # and populate fields accordingly
    def selectThingToUpdate(self, nameOfThingSelected):
        if (nameOfThingSelected != 'N/A'):

            self.initialRecord = []

            database = self.makeConnectionToDatabase()
            cursor = database.cursor()
            query = '''
            
                SELECT * 
                FROM Moons
                WHERE Name = %s;
            
            
            '''
            cursor.execute(query, [nameOfThingSelected])
            record = cursor.fetchone()
            for attribute in record:
                self.initialRecord.append(attribute)
            database.close()

            self.initialMoonMassLabel.configure(text=str(self.initialRecord[1]))
            self.initialPlanetMoonOrbitsLabel.configure(text=str(self.initialRecord[2]))
            self.initialMoonGravityLabel.configure(text=str(self.initialRecord[3]))
            self.initialMoonRadiusLabel.configure(text=str(self.initialRecord[4]))
            self.initialMoonDistanceFromEarthLabel.configure(text=str(self.initialRecord[5]))
            self.initialMoonSurfaceTemperatureLabel.configure(text=str(self.initialRecord[6]))
            self.initialMoonEscapeVelocityLabel.configure(text=str(self.initialRecord[7]))
            self.initialMoonRotationPeriodLabel.configure(text=str(self.initialRecord[8]))
            self.initialMoonOrbitalPeriodLabel.configure(text=str(self.initialRecord[9]))
            self.initialMoonImageDisplayer.openImage(False, self.initialRecord[10])
            self.initialMoonDescriptionDisplayer.loadDescriptionWithoutPromptingUser(self.initialRecord[11])
            self.initialMoonDistanceFromPlanetItOrbitsLabel.configure(text=str(self.initialRecord[12]))
        else:
            self.resetAllUI(False)

    def resetAllUI(self, includingUpdatingUI):

        self.selectedThingToUpdate.set('N/A')
        self.initialMoonMassLabel.configure(text='N/A')
        self.initialPlanetMoonOrbitsLabel.configure(text='N/A')
        self.initialMoonGravityLabel.configure(text='N/A')
        self.initialMoonRadiusLabel.configure(text='N/A')
        self.initialMoonDistanceFromEarthLabel.configure(text='N/A')
        self.initialMoonSurfaceTemperatureLabel.configure(text='N/A')
        self.initialMoonEscapeVelocityLabel.configure(text='N/A')
        self.initialMoonRotationPeriodLabel.configure(text='N/A')
        self.initialMoonOrbitalPeriodLabel.configure(text='N/A')
        self.initialMoonImageDisplayer.resetImageUI()
        self.initialMoonDescriptionDisplayer.resetDescriptionUI(12, 0)
        self.initialMoonDistanceFromPlanetItOrbitsLabel.configure(text='N/A')

        if (includingUpdatingUI):
            self.newMoonNameInputBox.delete(0, END)
            self.selectedNewPlanetMoonOrbits.set('')
            self.newMoonGravityInputBox.delete(0, END)
            self.newMoonRadiusInputBox.delete(0, END)
            self.newMoonDistanceFromEarthInputBox.delete(0, END)
            self.newMoonSurfaceTemperatureInputBox.delete(0, END)
            self.newMoonEscapeVelocityInputBox.delete(0, END)
            self.newMoonRotationPeriodInputBox.delete(0, END)
            self.newMoonOrbitalPeriodInputBox.delete(0, END)
            self.newMoonImageDisplayer.resetImageUI()
            self.newMoonDescriptionDisplayer.resetDescriptionUI(15, 0)
            self.newMoonDistancefromPlanetItOrbitsInputBox.delete(0, END)

    # perform the moon update
    def confirm(self):
        thereWasAnError = False

        if (self.insertionValidator.validateWord(False, self.selectedThingToUpdate.get(), "Name of the moon to update") == False):
            thereWasAnError = True

        newMoonName = self.newMoonNameInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newMoonName)):
            thereWasAnError = True
            self.insertionValidator.errorMessage += "Deletion code for new moon name inserted, but this value cannot be left empty" + "\n"

        newMoonMass = self.newMoonMassInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newMoonMass) == False):
            if (self.insertionValidator.validateDecimalValue(newMoonMass, False, "New moon mass", True) == False):
                thereWasAnError = True

        newMoonGravity = self.newMoonGravityInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newMoonGravity) == False):
            if (self.insertionValidator.validateDecimalValue(newMoonGravity, False, "New moon gravity", True) == False):
                thereWasAnError = True

        newMoonRadius = self.newMoonRadiusInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newMoonRadius) == False):
            if (self.insertionValidator.validateDecimalValue(newMoonRadius, False, "New moon radius", True) == False):
                thereWasAnError = True

        newMoonDistanceFromEarth = self.newMoonDistanceFromEarthInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newMoonDistanceFromEarth) == False):
            if (self.insertionValidator.validateDecimalValue(newMoonDistanceFromEarth, False, "New moon distance from earth", True) == False):
                thereWasAnError = True

        newMoonMeanSurfaceTemperature = self.newMoonSurfaceTemperatureInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newMoonMeanSurfaceTemperature) == False):
            if (self.insertionValidator.validateDecimalValue(newMoonMeanSurfaceTemperature, False, "New moon mean surface temperature", True) == False):
                thereWasAnError = True

        newMoonEscapeVelocity = self.newMoonEscapeVelocityInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newMoonEscapeVelocity) == False):
            if (self.insertionValidator.validateDecimalValue(newMoonEscapeVelocity, False, "New moon escape velocity", True) == False):
                thereWasAnError = True

        newMoonRotationPeriod = self.newMoonRotationPeriodInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newMoonRotationPeriod) == False):
            if (self.insertionValidator.validateDecimalValue(newMoonRotationPeriod, False, "New moon rotation period", True) == False):
                thereWasAnError = True

        newMoonOrbitalPeriod = self.newMoonOrbitalPeriodInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newMoonOrbitalPeriod) == False):
            if (self.insertionValidator.validateDecimalValue(newMoonOrbitalPeriod, False, "New moon rotation period", True) == False):
                thereWasAnError = True

        newMoonDistanceFromPlanetItOrbits = self.newMoonDistancefromPlanetItOrbitsInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newMoonDistanceFromPlanetItOrbits) == False):
            if (self.insertionValidator.validateDecimalValue(newMoonDistanceFromPlanetItOrbits, False, "New moon distance from planet it orbits", True) == False):
                thereWasAnError = True

        if (thereWasAnError == False):

            # start forming the query
            newChanges = []
            confirmationMessage = ""

            query = '''
            
                UPDATE Moons
                SET
            
            '''
            if (len(newMoonName) > 0):
                newChanges.append(newMoonName)
                query += " Name = %s"
                confirmationMessage += "-Update moon name from " + self.initialRecord[0]+ " to " + newMoonName + "\n"

            if (len(newMoonMass) > 0):
                if (len(newChanges) > 0):
                    query += ","
                newChanges.append(self.insertionValidator.obtainFinalValue(newMoonMass))
                confirmationMessage += "-Update moon mass from " + str(self.initialRecord[1]) + " to " + newMoonMass + "\n"
                query += " Mass = %s"

            if (len(self.selectedNewPlanetMoonOrbits.get()) > 0):
                if (len(newChanges) > 0):
                    query += ","
                newChanges.append(self.selectedNewPlanetMoonOrbits.get())
                confirmationMessage += "-Update planet moon orbits from" + str(self.initialRecord[2]) +" to " + self.selectedNewPlanetMoonOrbits.get()
                query += " PlanetItOrbits = %s"

            if (len(newMoonGravity) > 0):
                if (len(newChanges) > 0):
                    query += ","
                newChanges.append(self.insertionValidator.obtainFinalValue(newMoonGravity))
                confirmationMessage += "-Update moon gravity from " + str(self.initialRecord[3]) + " to " + newMoonGravity + "\n"
                query += " Gravity = %s"

            if (len(newMoonRadius) > 0):
                if (len(newChanges) > 0):
                    query += ","
                newChanges.append(self.insertionValidator.obtainFinalValue(newMoonRadius))
                confirmationMessage += "-Update moon radius from " + str(self.initialRecord[4]) + " to " + newMoonRadius + "\n"
                query += " Radius = %s"

            if (len(newMoonDistanceFromEarth) > 0):
                if (len(newChanges) > 0):
                    query += ","
                newChanges.append(self.insertionValidator.obtainFinalValue(newMoonDistanceFromEarth))
                confirmationMessage += "-Update moon distance from earth from " + str(self.initialRecord[5]) + " to " + newMoonDistanceFromEarth + "\n"
                query += " DistanceFromEarth = %s"

            if (len(newMoonMeanSurfaceTemperature) > 0):
                if (len(newChanges) > 0):
                    query += ","
                newChanges.append(self.insertionValidator.obtainFinalValue(newMoonMeanSurfaceTemperature))
                confirmationMessage += "-Update moon surface temperature from " + str(self.initialRecord[6]) + " to " + newMoonMeanSurfaceTemperature + "\n"
                query += " MeanSurfaceTemperature = %s"

            if (len(newMoonEscapeVelocity) > 0):
                if (len(newChanges) > 0):
                    query += ","
                newChanges.append(self.insertionValidator.obtainFinalValue(newMoonEscapeVelocity))
                confirmationMessage += "-Update moon escape velocity from " + str(self.initialRecord[7]) + " to " + newMoonEscapeVelocity + "\n"
                query += " EscapeVelocity = %s"

            if (len(newMoonRotationPeriod) > 0):
                if (len(newChanges) > 0):
                    query += ","
                newChanges.append(self.insertionValidator.obtainFinalValue(newMoonRotationPeriod))
                confirmationMessage += "-Update moon rotation period from " + str(self.initialRecord[8]) + " to " + newMoonEscapeVelocity + "\n"
                query += " RotationPeriod  = %s"

            if (len(newMoonOrbitalPeriod) > 0):
                if (len(newChanges) > 0):
                    query += ","
                newChanges.append(self.insertionValidator.obtainFinalValue(newMoonOrbitalPeriod))
                confirmationMessage += "-Update moon orbital period from " + str(self.initialRecord[9]) + " to " + newMoonOrbitalPeriod + "\n"
                query += " OrbitalPeriod = %s"

            if (self.newMoonImageDisplayer.imageLoaded):
                if (len(newChanges) > 0):
                    query += ","
                query += "ImageDirectory = %s"
                confirmationMessage += "Update image directory to " + self.newMoonImageDisplayer.imageDir + "\n"
                newChanges.append(self.newMoonImageDisplayer.imageDir)
            elif (self.initialMoonImageDisplayer.imageLoaded):
                # show a dialogue asking the user if they left the image dir empty because they want to delete initial image:
                if (messagebox.askyesno("Delete initial image?",
                                        "Detected that you have not loaded an image in, is this because you want to delete the current image?")):
                    if (len(newChanges) > 0):
                        # add a comma:
                        query += ","
                    query += "ImageDirectory = NULL"
                    confirmationMessage += "Update image directory from to N/A"
                    self.deleteOldImage = True

            if (self.newMoonDescriptionDisplayer.descriptionLoaded):
                if (len(newChanges) > 0):
                    query += ","
                query += "Description = %s"
                confirmationMessage += "Update description directory to " + self.newMoonDescriptionDisplayer.descriptionDirectory + "\n"
                newChanges.append(self.insertionValidator.obtainFinalValue(self.newMoonDescriptionDisplayer.descriptionDirectory))
            elif (self.initialMoonDescriptionDisplayer.descriptionLoaded):
                if (messagebox.askyesno("Delete initial description?", "Detected that you have not loaded a description in, is this because you want to delete the current description?")):
                    if ((len(newChanges) > 0) or self.deleteOldImage):
                        # add a comma:
                        query += ","
                    query += "Description = NULL"
                    confirmationMessage += "Update description directory to N/A"
                    self.deleteOldDescription = True

            if (len(newMoonDistanceFromPlanetItOrbits) > 0):
                if (len(newChanges) > 0):
                    query += ","
                newChanges.append(self.insertionValidator.obtainFinalValue(newMoonDistanceFromPlanetItOrbits))
                confirmationMessage += "-Update distance from planet moon orbits from " + str(self.initialRecord[12]) + " to " + newMoonDistanceFromPlanetItOrbits + "\n"
                query += " DistanceFromPlanetItOrbits = %s"

            if ((len(newChanges) > 0) or self.deleteOldDescription or self.deleteOldImage):
                query += " WHERE Name = %s;"
                newChanges.append(self.selectedThingToUpdate.get())

                database = self.makeConnectionToDatabase()
                cursor = database.cursor()
                try:
                    cursor.execute(query, newChanges)
                    if (self.showConfirmationPopUp(confirmationMessage)):
                        database.commit()
                        self.showSuccessMessage(2, 0, 2)
                        self.resetAllUI(True)
                        self.resetThingToSelectDropdownMenu()
                        self.deleteOldImage = False
                        self.deleteOldDescription = False
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

    # present the UI needed for a moon update
    def manageUpdate(self, windowToPutFrameOnto, updateManager, updateTitle):
        BaseUpdateManager.manageUpdate(self, windowToPutFrameOnto, updateManager, updateTitle)

        self.deleteOldDescription = False
        self.deleteOldImage = False

        query = '''
        
            SELECT Name 
            FROM Moons;
        
        '''
        self.setUpThingToUpdateSelector(0, 1, query, "Moon to update: ")

        Label(self.leftFrame, text="Moon mass (kg): ").grid(row=1, column=0)
        self.initialMoonMassLabel = Label(self.leftFrame, text="N/A")
        self.initialMoonMassLabel.grid(row=1, column=1)

        Label(self.leftFrame, text="Planet moon orbits: ").grid(row=2, column=0)
        self.initialPlanetMoonOrbitsLabel = Label(self.leftFrame, text="N/A")
        self.initialPlanetMoonOrbitsLabel.grid(row=2, column=1)

        Label(self.leftFrame, text="Moon Gravity (m/s^2): ").grid(row=3, column=0)
        self.initialMoonGravityLabel = Label(self.leftFrame, text="N/A")
        self.initialMoonGravityLabel.grid(row=3, column=1)

        Label(self.leftFrame, text="Moon Radius (km): ").grid(row=4, column=0)
        self.initialMoonRadiusLabel = Label(self.leftFrame, text="N/A")
        self.initialMoonRadiusLabel.grid(row=4, column=1)

        Label(self.leftFrame, text="Moon Distance from Earth (km): ").grid(row=5, column=0)
        self.initialMoonDistanceFromEarthLabel = Label(self.leftFrame, text="N/A")
        self.initialMoonDistanceFromEarthLabel.grid(row=5, column=1)

        Label(self.leftFrame, text="Moon mean surface temperature (K): ").grid(row=6, column=0)
        self.initialMoonSurfaceTemperatureLabel = Label(self.leftFrame, text="N/A")
        self.initialMoonSurfaceTemperatureLabel.grid(row=6, column=1)

        Label(self.leftFrame, text="Moon escape velocity (km/h): ").grid(row=7, column=0)
        self.initialMoonEscapeVelocityLabel = Label(self.leftFrame, text="N/A")
        self.initialMoonEscapeVelocityLabel.grid(row=7, column=1)

        Label(self.leftFrame, text="Moon rotational period (Earth days): ").grid(row=8, column=0)
        self.initialMoonRotationPeriodLabel = Label(self.leftFrame, text="N/A")
        self.initialMoonRotationPeriodLabel.grid(row=8, column=1)

        Label(self.leftFrame, text="Moon orbital period (Earth days): ").grid(row=9, column=0)
        self.initialMoonOrbitalPeriodLabel = Label(self.leftFrame, text="N/A")
        self.initialMoonOrbitalPeriodLabel.grid(row=9, column=1)

        self.initialMoonImageDisplayer = ImageDisplayerManager()
        self.initialMoonImageDisplayer.initializeImageDisplayer(10, 0, 2, self.leftFrame, None, False)

        self.initialMoonDescriptionDisplayer = TextBoxManager()
        self.initialMoonDescriptionDisplayer.initializeDescriptionBoxForReadingOnlyAndNotLoading(self.leftFrame, 12, 0, 13, 0)

        Label(self.leftFrame, text="Moon distance from planet it orbits (km): ").grid(row=14, column=0)
        self.initialMoonDistanceFromPlanetItOrbitsLabel = Label(self.leftFrame, text="N/A")
        self.initialMoonDistanceFromPlanetItOrbitsLabel.grid(row=14, column=1)

        # updating UI:
        Label(self.rightFrame, text="New moon name: ").grid(row=0, column=0)
        self.newMoonNameInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newMoonNameInputBox.grid(row=0, column=1)

        Label(self.rightFrame, text="New moon mass (kg): ").grid(row=1, column=0)
        self.newMoonMassInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newMoonMassInputBox.grid(row=1, column=1)

        Label(self.rightFrame, text="New planet moon orbits: ").grid(row=2, column=0)

        # user will be able to change the planet a moon orbits from
        # here, so I create a dropdown for that right here
        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        planetsToChooseFrom = []
        planetsToChooseFrom.append('')
        query = '''
        
            SELECT Name 
            FROM Planets;
        
        '''
        cursor.execute(query)
        records = cursor.fetchall()
        if (records != None):
            for planetName in records:
                planetsToChooseFrom.append(planetName[0])

        self.selectedNewPlanetMoonOrbits = StringVar()
        self.selectedNewPlanetMoonOrbits.set('')
        self.newPlanetMoonOrbitsDropdownBox = OptionMenu(self.rightFrame, self.selectedNewPlanetMoonOrbits, *planetsToChooseFrom)
        self.newPlanetMoonOrbitsDropdownBox.grid(row=2, column=1)

        database.close()

        Label(self.rightFrame, text="New moon gravity (m/s^2): ").grid(row=3, column=0)
        self.newMoonGravityInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newMoonGravityInputBox.grid(row=3, column=1)

        Label(self.rightFrame, text="New moon radius (km): ").grid(row=4, column=0)
        self.newMoonRadiusInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newMoonRadiusInputBox.grid(row=4, column=1)

        Label(self.rightFrame, text="New moon distance from Earth (km): ").grid(row=5, column=0)
        self.newMoonDistanceFromEarthInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newMoonDistanceFromEarthInputBox.grid(row=5, column=1)

        Label(self.rightFrame, text="New moon mean surface temperature (K): ").grid(row=6, column=0)
        self.newMoonSurfaceTemperatureInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newMoonSurfaceTemperatureInputBox.grid(row=6, column=1)

        Label(self.rightFrame, text="New moon escape velocity: (km/h): ").grid(row=7, column=0)
        self.newMoonEscapeVelocityInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newMoonEscapeVelocityInputBox.grid(row=7, column=1)

        Label(self.rightFrame, text="New moon rotational period (Earth Days): ").grid(row=8, column=0)
        self.newMoonRotationPeriodInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newMoonRotationPeriodInputBox.grid(row=8, column=1)

        Label(self.rightFrame, text="New moon orbital period (Earth Days): ").grid(row=9, column=0)
        self.newMoonOrbitalPeriodInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newMoonOrbitalPeriodInputBox.grid(row=9, column=1)

        self.newMoonImageDisplayer = ImageDisplayerManager()
        self.newMoonImageDisplayer.initializeImageDisplayer(10, 0, 2, self.rightFrame, None, True)

        self.newMoonDescriptionDisplayer = TextBoxManager()
        self.newMoonDescriptionDisplayer.initializeDescriptionFormForUserLoading(self.rightFrame, 14, 0, 15, 0, 16, 0)

        Label(self.rightFrame, text="New distance from planet moon orbits (km): ").grid(row=17, column=0)
        self.newMoonDistancefromPlanetItOrbitsInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newMoonDistancefromPlanetItOrbitsInputBox.grid(row=17, column=1)

        self.confirmButton.grid(row=1, column=0, sticky=W+E)
        self.cancelButton.grid(row=1, column=1, sticky=W+E)