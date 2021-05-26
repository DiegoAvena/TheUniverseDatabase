'''

----SUMMARY---
Allows the user to update
a planet

---IMPORTS---
BaseUpdateManager:

Used to obtain base functionality
for a more specific update, since this
class is for the specific update on
planet

tkinter - for all of the UI

mysql:

for performing the update queries and
search query needed to display the initial
record to the user

ImageDisplayerManager:

This is used to display an image of the
planet on the initial record,
and to allow the user to update this
planet image

messageBox from tkinter:

used to ask the user if they did not
insert a new image because they wish
to delete the initial planet image (provided
that the planet does currently have an image for it), this
item is also used for the same reason for the
description insertion option (if user leaves description empty,
and the initial record has a description, a pop up will show
asking if they left this empty because they want to delete
the old description and leave it blank)

TextBoxManager:

used to display a description of the planet on
the initial record side, and to allow the user
to insert a description on the update side

'''

from Code.UpdateManagers.BaseUpdateManager import BaseUpdateManager
from Code.Displayers.ImageDisplayerManager import ImageDisplayerManager
from Code.Displayers.TextBoxManager import TextBoxManager
from tkinter import *
from tkinter import messagebox
import mysql

class PlanetUpdateManager(BaseUpdateManager):

    # these bools are used to indicate
    # changes in attributes that are not
    # reflected in the newChanges collection
    # that is formed inside of the confirm method,
    # meaning these changes would go unnoticed without
    # these booleans
    global deleteOldImage
    global deleteOldDescription
    global changePlanetDwarfStatus
    global changePlanetHabitZoneStatus
    global changeStarPlanetOrbits

    # initial planet UI stuff
    global initialPlanetRecord
    global planetsToChooseFromDropDown
    global selectedPlanet
    global planetMassLabel
    global planetGravityLabel
    global planetRadiusLabel
    global planetDistanceFromEarthLabel
    global planetEquilibriumTemperatureLabel
    global planetESILabel
    global planetRotationPeriodLabel
    global planetOrbitalPeriodLabel
    global planetEscapeVelocityLabel
    global initialPlanetImageDisplayerManager
    global initialPlanetDescriptionManager
    global starPlanetOrbitsLabel
    global planetIsADwarfPlanetLabel
    global planetIsInitiallyADwarfPlanet
    global planetIsInTheHabitZoneLabel
    global planetIsInitiallyInHabitZone
    global planetAtmospheresLabel

    # update UI
    global newPlanetNameInputBox
    global newPlanetMassInputBox
    global newPlanetGravityInputBox
    global newPlanetRadiusInputBox
    global newPlanetDistanceFromEarthInputBox
    global newPlanetEquilibriumTemperatureInputBox
    global newPlanetESIInputBox
    global newPlanetRotationPeriodInputBox
    global newPlanetOrbitalPeriodInputBox
    global newPlanetEscapeVelocityInputBox
    global newPlanetImageManager
    global newPlanetDescriptionManager
    global newPlanetStarDropDownMenu
    global newSelectedStar
    global planetIsADwarfCheckBox
    global planetIsADwarf
    global planetIsInTheHabitZoneCheckbox
    global planetIsInTheHabitZone

    # for updating planet atmosphere gases:
    global newAtmosphereGasInputBox
    global gasesToPotentiallyRemoveDropDownMenu
    global gasToRemove
    global gasesThatWillBeAddedLabel
    global gasesThatWillBeRemovedLabel
    global gasesToRemoveCollection
    global gasesToPotentiallyRemoveCollection
    global gasesToAddCollection

    # perform the planet update
    def confirm(self):

        thereWasAnError = False
        planetToUpdate = self.selectedPlanet.get()
        if self.insertionValidator.validateWord(False, planetToUpdate, "Name of planet to update") == False:
            thereWasAnError = True

        # validate all new input fields:
        newPlanetName = self.newPlanetNameInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newPlanetName)):
            thereWasAnError = True
            self.insertionValidator.errorMessage += "New planet name has erase code but this value cannot be deleted"

        newPlanetMass = self.newPlanetMassInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newPlanetMass) == False):
            if (self.insertionValidator.validateDecimalValue(newPlanetMass, False, "New planet mass", True) == False):
                thereWasAnError = True

        newPlanetGravity = self.newPlanetGravityInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newPlanetGravity) == False):
            if (self.insertionValidator.validateDecimalValue(newPlanetGravity, False, "New planet gravity", True) == False):
                thereWasAnError = True

        newPlanetRadius = self.newPlanetRadiusInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newPlanetRadius) == False):
            if (self.insertionValidator.validateDecimalValue(newPlanetRadius, False, "New planet radius", True) == False):
                thereWasAnError = True

        newPlanetDistanceFromEarth = self.newPlanetDistanceFromEarthInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newPlanetDistanceFromEarth)):
            thereWasAnError = True
            self.insertionValidator.errorMessage += "New planet distance from earth has the erase code but this value cannot be deleted"
        else:
            if (self.insertionValidator.validateDecimalValue(newPlanetDistanceFromEarth, False, "New planet distance from Earth", True) == False):
                thereWasAnError = True

        newPlanetEquilibriumTemperature = self.newPlanetEquilibriumTemperatureInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newPlanetEquilibriumTemperature) == False):
            if (self.insertionValidator.validateDecimalValue(newPlanetEquilibriumTemperature, False, "New planet equilibrium temperature", True) == False):
                thereWasAnError = True

        newPlanetESI = self.newPlanetESIInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newPlanetESI) == False):
            if (self.insertionValidator.makeSureDecimalIsWithinACertainRange(newPlanetESI, "New planet ESI", True, 0, 1) == False):
                thereWasAnError = True

        newPlanetRotationalPeriod = self.newPlanetRotationPeriodInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newPlanetRotationalPeriod) == False):
            if (self.insertionValidator.validateDecimalValue(newPlanetRotationalPeriod, False, "New planet rotational period", True) == False):
                thereWasAnError = True

        newPlanetOrbitalPeriod = self.newPlanetOrbitalPeriodInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newPlanetOrbitalPeriod) == False):
            if (self.insertionValidator.validateDecimalValue(newPlanetOrbitalPeriod, False, "New planet orbital period", True) == False):
                thereWasAnError = True

        newPlanetEscapeVelocity = self.newPlanetEscapeVelocityInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newPlanetEscapeVelocity) == False):
            if (self.insertionValidator.validateDecimalValue(newPlanetEscapeVelocity, False, "New planet escape velocity", True) == False):
                thereWasAnError = True

        if (thereWasAnError == False):

            # start forming the query:
            newChanges = []
            messageToShowInConfirmWindow = ""
            query = '''
            
                UPDATE Planets
                SET
            
            '''

            if (len(newPlanetName) > 0):
                query += "Name = %s"
                messageToShowInConfirmWindow += "Change planet name from " + self.initialPlanetRecord[0] + " to " + newPlanetName + "\n"
                newChanges.append(newPlanetName)

            if (len(newPlanetMass) > 0):
                if (len(newChanges) > 0):
                    # add a comma:
                    query += ","
                query += "Mass = %s"
                messageToShowInConfirmWindow += "Change planet mass from " + str(self.initialPlanetRecord[1]) + " to " + newPlanetMass + "\n"
                newChanges.append(self.insertionValidator.obtainFinalValue(newPlanetMass))

            if (len(newPlanetGravity) > 0):
                if (len(newChanges) > 0):
                    # add a comma:
                    query += ","
                query += "Gravity = %s"
                messageToShowInConfirmWindow += "Change planet gravity from " + str(self.initialPlanetRecord[2]) + " to " + newPlanetGravity + "\n"
                newChanges.append(self.insertionValidator.obtainFinalValue(newPlanetGravity))

            if (len(newPlanetRadius) > 0):
                if (len(newChanges) > 0):
                    # add a coma:
                    query += ","
                query += "Radius = %s"
                messageToShowInConfirmWindow += "Change planet radius from " + str(self.initialPlanetRecord[3]) + " to " + newPlanetRadius + "\n"
                newChanges.append(self.insertionValidator.obtainFinalValue(newPlanetRadius))

            if (len(newPlanetDistanceFromEarth) > 0):
                if (len(newChanges) > 0):
                    # add a coma:
                    query += ","
                query += "DistanceFromEarth = %s"
                messageToShowInConfirmWindow += "Change planet distance from earth from " + str(self.initialPlanetRecord[4]) + " to " + newPlanetDistanceFromEarth + "\n"
                newChanges.append(newPlanetDistanceFromEarth)

            if (len(newPlanetEquilibriumTemperature) > 0):
                if (len(newChanges) > 0):
                    # add a coma:
                    query += ","
                query += "EquilibriumTemperature = %s"
                messageToShowInConfirmWindow += "Change planet equilibrium temperature from " + str(self.initialPlanetRecord[5]) + " to " + newPlanetEquilibriumTemperature + "\n"
                newChanges.append(self.insertionValidator.obtainFinalValue(newPlanetEquilibriumTemperature))

            if (len(newPlanetESI) > 0):
                if (len(newChanges) > 0):
                    # add a coma:
                    query += ","

                query += "ESI = %s"
                messageToShowInConfirmWindow += "Change planet ESI from " + str(self.initialPlanetRecord[6]) + " to " + newPlanetESI + "\n"
                newChanges.append(self.insertionValidator.obtainFinalValue(newPlanetESI))

            if (len(newPlanetRotationalPeriod) > 0):
                if (len(newChanges) > 0):
                    # add a coma:
                    query += ","
                query += "RotationPeriod = %s"
                messageToShowInConfirmWindow += "Change planet rotation period from " + str(self.initialPlanetRecord[7]) + " to " + newPlanetRotationalPeriod + "\n"
                newChanges.append(self.insertionValidator.obtainFinalValue(newPlanetRotationalPeriod))

            if (len(newPlanetOrbitalPeriod) > 0):
                if (len(newChanges) > 0):
                    # add a coma:
                    query += ","
                query += "OrbitalPeriod = %s"
                messageToShowInConfirmWindow += "Change planet orbital period from " + str(self.initialPlanetRecord[8]) + " to "+ newPlanetOrbitalPeriod + "\n"
                newChanges.append(self.insertionValidator.obtainFinalValue(newPlanetOrbitalPeriod))

            if (len(newPlanetEscapeVelocity) > 0):
                if (len(newChanges) > 0):
                    # add a coma:
                    query += ","

                query += "EscapeVelocity = %s"
                messageToShowInConfirmWindow += "Change planet escape velocity from " + str(self.initialPlanetRecord[9]) + " to " + newPlanetEscapeVelocity + "\n"
                newChanges.append(self.insertionValidator.obtainFinalValue(newPlanetEscapeVelocity))

            if (self.newPlanetImageManager.imageLoaded):
                if (len(newChanges) > 0):
                    query += ","
                query += "ImageDirectory = %s"
                messageToShowInConfirmWindow += "Update image directory from " + str(self.initialPlanetRecord[10]) + " to " + self.newPlanetImageManager.imageDir + "\n"
                newChanges.append(self.newPlanetImageManager.imageDir)
            elif (self.initialPlanetImageDisplayerManager.imageLoaded):
                # show a dialogue asking the user if they left the image dir empty because they want to delete initial image:
                if (messagebox.askyesno("Delete initial image?",
                                        "Detected that you have not loaded an image in, is this because you want to delete the current image?")):
                    if (len(newChanges) > 0):
                        # add a comma:
                        query += ","
                    query += "ImageDirectory = NULL"
                    messageToShowInConfirmWindow += "Update image directory from " + str(self.initialPlanetRecord[11]) + " to N/A"
                    self.deleteOldImage = True

            if (self.newPlanetDescriptionManager.descriptionLoaded):
                if (len(newChanges) > 0):
                    query += ","
                query += "DescriptionDirectory = %s"
                messageToShowInConfirmWindow += "Update description directory from " +str(self.initialPlanetRecord[11]) + " to " + self.newPlanetDescriptionManager.descriptionDirectory + "\n"
                newChanges.append(self.insertionValidator.obtainFinalValue(self.newPlanetDescriptionManager.descriptionDirectory))
            elif (self.initialPlanetDescriptionManager.descriptionLoaded):
                if (messagebox.askyesno("Delete initial description?", "Detected that you have not loaded a description in, is this because you want to delete the current description?")):
                    if ((len(newChanges) > 0) or self.deleteOldImage):
                        # add a comma:
                        query += ","
                    query += "DescriptionDirectory = NULL"
                    messageToShowInConfirmWindow += "Update description directory from " + str(self.initialPlanetRecord[11]) + " to N/A"
                    self.deleteOldDescription = True

            if ((self.planetIsInitiallyADwarfPlanet and (self.planetIsADwarf.get() == 0)) or ((self.planetIsInitiallyADwarfPlanet == False) and (self.planetIsADwarf.get() == 1))):
                self.changePlanetDwarfStatus = True

            if ((self.planetIsInitiallyInHabitZone and (self.planetIsInTheHabitZone.get() == 0)) or ((self.planetIsInitiallyInHabitZone == False) and (self.planetIsInTheHabitZone.get() == 1))):
                self.changePlanetHabitZoneStatus = True

            if (len(self.newSelectedStar.get()) > 0):
                self.changeStarPlanetOrbits = True

            if ((len(newChanges) > 0) or self.deleteOldImage or (len(self.gasesToAddCollection) > 0) or (len(self.gasesToRemoveCollection) > 0) or self.deleteOldDescription or self.changePlanetDwarfStatus or self.changePlanetDwarfStatus or self.changeStarPlanetOrbits):
                query += " WHERE Name = %s;"

                # execute the query:
                database = self.makeConnectionToDatabase()
                cursor = database.cursor()
                try:

                    # check if there are any atmospheric gases to add:
                    if (self.gasesToAddCollection != None):
                        if (len(self.gasesToAddCollection) > 0):
                            messageToShowInConfirmWindow += "Add these gases into the atmosphere: " + str(self.gasesToAddCollection) + "\n"
                            for gas in self.gasesToAddCollection:
                                queryTwo = '''

                                                        INSERT INTO PlanetAtmospheres
                                                        VALUES(%s, %s); 

                                                    '''
                                cursor.execute(queryTwo, [self.selectedPlanet.get(), gas])

                    # check if there are any atmospheric gases to remove:
                    if (self.gasesToRemoveCollection != None):
                        if (len(self.gasesToRemoveCollection) > 0):
                            messageToShowInConfirmWindow += "Remove these gases from the atmosphere: " + str(self.gasesToRemoveCollection) + "\n"
                            for gas in self.gasesToRemoveCollection:
                                queryTwo = '''

                                                        DELETE FROM PlanetAtmospheres 
                                                        WHERE Name = %s AND Gas = %s;

                                                    '''
                                cursor.execute(queryTwo, [self.selectedPlanet.get(), gas])

                    if (self.changePlanetDwarfStatus):
                        if (self.planetIsADwarf.get() == 1):
                            print("Change planet to dwarf")
                            messageToShowInConfirmWindow += "Make planet a dwarf plent" + "\n"
                            queryTwo = '''
                            
                                INSERT INTO DwarfPlanets
                                VALUES(%s);
                            
                            '''
                            cursor.execute(queryTwo, [self.selectedPlanet.get()])
                        else:
                            print("Make planet not a dwarf")
                            messageToShowInConfirmWindow += "Make planet a regular none dwarf planet" + "\n"
                            queryTwo = '''
                            
                                DELETE FROM DwarfPlanets
                                WHERE Name = %s;
                            
                            '''
                            cursor.execute(queryTwo, [self.selectedPlanet.get()])

                    if (self.changePlanetHabitZoneStatus):
                        if (self.planetIsInTheHabitZone.get() == 1):
                            messageToShowInConfirmWindow += "Place Planet into the habit zone" + "\n"
                            queryTwo = '''
                            
                                INSERT INTO PlanetsInHabitZone
                                VALUES (%s); 
                            
                            '''
                            cursor.execute(queryTwo, [self.selectedPlanet.get()])
                        else:
                            messageToShowInConfirmWindow += "Take planet out of the habit zone" + "\n"
                            queryTwo = '''
                            
                                DELETE FROM PlanetsInHabitZone
                                WHERE Name = %s;
                            
                            '''
                            cursor.execute(queryTwo, [self.selectedPlanet.get()])

                    if (self.changeStarPlanetOrbits):
                        messageToShowInConfirmWindow += "Change star this planet orbits to " + self.newSelectedStar.get()

                        # check if this record is in the stars planets orbit, if not, then there will be an insertion, not an update, into this table
                        queryTwo = '''
                        
                            SELECT COUNT(*)
                            FROM StarsPlanetsOrbit
                            WHERE PlanetName = %s;
                        
                        '''
                        cursor.execute(queryTwo, [self.selectedPlanet.get()])
                        record = cursor.fetchone()
                        count = record[0]
                        if (count > 0):
                            queryTwo = '''

                                UPDATE StarsPlanetsOrbit
                                SET StarName = %s 
                                WHERE PlanetName = %s;

                            '''
                        else:
                            queryTwo = '''

                                INSERT INTO StarsPlanetsOrbit
                                VALUES(%s, %s);

                            '''
                        cursor.execute(queryTwo, [self.newSelectedStar.get(), self.selectedPlanet.get()])

                    if ((len(newChanges) > 0) or self.deleteOldImage or self.deleteOldDescription):
                        newChanges.append(self.selectedPlanet.get())
                        cursor.execute(query, newChanges)

                    if (self.showConfirmationPopUp(messageToShowInConfirmWindow)):
                        database.commit()
                        self.showSuccessMessage(2, 0, 2)

                        # reset all UI:
                        self.resetAllUI(True)

                        # make sure to update the planets to choose from list in order to get most up to date names:
                        query = '''

                                    SELECT Name
                                    From Planets;

                                '''
                        cursor.execute(query)
                        records = cursor.fetchall()
                        planetNames = []
                        planetNames.append('N/A')
                        if (records != None):
                            for planetName in records:
                                planetNames.append(planetName[0])

                        self.planetsToChooseFromDropDown.grid_forget()
                        self.planetsToChooseFromDropDown.destroy()
                        self.planetsToChooseFromDropDown = OptionMenu(self.leftFrame, self.selectedPlanet, *planetNames, command=self.selectPlanet)
                        self.planetsToChooseFromDropDown.grid(row=0, column=1, sticky=W + E)

                        self.deleteOldImage = False
                        self.deleteOldDescription = False
                        self.changeStarPlanetOrbits = False
                        self.changePlanetHabitZoneStatus = False
                        self.changePlanetDwarfStatus = False

                    else:
                        print("Roll back")
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


    def resetAllUI(self, resetUpdatingUIToo):

        self.selectedPlanet.set('N/A')
        self.planetMassLabel.configure(text='N/A')
        self.planetGravityLabel.configure(text='N/A')
        self.planetRadiusLabel.configure(text='N/A')
        self.planetDistanceFromEarthLabel.configure(text='N/A')
        self.planetEquilibriumTemperatureLabel.configure(text='N/A')
        self.planetESILabel.configure(text='N/A')
        self.planetRotationPeriodLabel.configure(text='N/A')
        self.planetOrbitalPeriodLabel.configure(text='N/A')
        self.planetEscapeVelocityLabel.configure(text='N/A')
        self.initialPlanetImageDisplayerManager.resetImageUI()
        self.initialPlanetDescriptionManager.resetDescriptionUI(16, 0)
        self.starPlanetOrbitsLabel.configure(text='N/A')
        self.planetIsADwarfPlanetLabel.configure(text='N/A')
        self.planetIsInitiallyADwarfPlanet = False
        self.planetIsInTheHabitZoneLabel.configure(text='N/A')
        self.planetIsInitiallyInHabitZone = False
        self.planetAtmospheresLabel.configure(text='N/A')

        self.refreshGasesToAdd()
        self.refreshGasesToRemoveList()

        if (resetUpdatingUIToo):
            self.newPlanetNameInputBox.delete(0, END)
            self.newPlanetMassInputBox.delete(0, END)
            self.newPlanetGravityInputBox.delete(0, END)
            self.newPlanetRadiusInputBox.delete(0, END)
            self.newPlanetDistanceFromEarthInputBox.delete(0, END)
            self.newPlanetEquilibriumTemperatureInputBox.delete(0, END)
            self.newPlanetESIInputBox.delete(0, END)
            self.newPlanetRotationPeriodInputBox.delete(0, END)
            self.newPlanetOrbitalPeriodInputBox.delete(0, END)
            self.newPlanetEscapeVelocityInputBox.delete(0, END)
            self.newPlanetImageManager.resetImageUI()
            self.newPlanetDescriptionManager.resetDescriptionUI(20, 0)
            self.newSelectedStar.set('')
            self.planetIsADwarfCheckBox.deselect()
            self.planetIsADwarf.set(0)
            self.planetIsInTheHabitZoneCheckbox.deselect()
            self.planetIsInTheHabitZone.set(0)

            # for updating planet atmosphere gases:
            self.newAtmosphereGasInputBox.delete(0, END)
            self.gasToRemove.set('')
            self.gasesThatWillBeAddedLabel.configure(text="Gases to add: []")
            self.gasesThatWillBeRemovedLabel.configure(text="Gases to remove: []")
            self.gasesToRemoveCollection.clear()
            self.gasesToPotentiallyRemoveCollection.clear()
            self.gasesToAddCollection.clear()

    # clears the list of new gases that would
    # be added into the planets atmosphere
    # this method is linked to a button that says
    # 'refresh gases to add'
    def refreshGasesToAdd(self):
        if (self.gasesToAddCollection != None):
            if (len(self.gasesToAddCollection) > 0):
                self.gasesToAddCollection.clear()
                self.gasesThatWillBeAddedLabel.configure(text="Gases to add: []")
                self.newAtmosphereGasInputBox.delete(0, END)

    # populates the gases to add collection
    # so the planet atmosphere can be updated later
    # this method is linked to a button that says 'add new gas'
    def addGasToListofGasesToAdd(self):
        theNewGas = self.newAtmosphereGasInputBox.get()
        print("New gas: " + theNewGas)
        if (len(theNewGas) > 0):
            if (self.insertionValidator.validateWord(False, theNewGas, "New atmospheric gas ") == False):
                self.showErrorMessage(2, 0, 2)
                self.insertionValidator.errorMessage = ''
            else:
                # make sure new gas is indeed new
                newGasIsIndeedNew = True
                for gas in self.gasesToPotentiallyRemoveCollection:
                    if gas.lower() == theNewGas.lower():
                        newGasIsIndeedNew = False
                        self.insertionValidator.errorMessage = "The new gas you are adding already exists"
                        self.showErrorMessage(2, 0, 2)
                        self.insertionValidator.errorMessage = ''
                        break

                if (newGasIsIndeedNew):
                    # add into the new gases to add list:
                    gasIsAlreadyInTheAddCollection = False

                    if (self.gasesToAddCollection == None):
                        self.gasesToAddCollection = []
                    else:
                        for gas in self.gasesToAddCollection:
                            if (gas.lower() == theNewGas.lower()):
                                gasIsAlreadyInTheAddCollection = True
                                break

                    if (gasIsAlreadyInTheAddCollection == False):
                        self.gasesToAddCollection.append(theNewGas)

                    gasesToAddText = "Gases that will be added: ["
                    for gas in self.gasesToAddCollection:
                        gasesToAddText += " " + gas + " "
                    gasesToAddText += "]"

                    self.gasesThatWillBeAddedLabel.configure(text=gasesToAddText)
                    self.newAtmosphereGasInputBox.delete(0, END)

    # marks gases so that they can be removed from
    # this planets atmosphere later, this methid is
    # linked to the gasesToPotentiallyRemoveDropDownMenu
    def addGasToListOfGasesToRemove(self, selectedGas):
        if (len(selectedGas) > 0):
            if (self.gasesToRemoveCollection == None):
                self.gasesToRemoveCollection = []

            print("Remove gas:" + selectedGas)
            self.gasesToRemoveCollection.append(selectedGas)

            gasesToRemove = "Gases to remove: ["
            for gas in self.gasesToRemoveCollection:
                gasesToRemove += " " + gas + " "
            gasesToRemove += "]"
            self.gasesThatWillBeRemovedLabel.configure(text=gasesToRemove)

            # remove this selected gas from the list and update the UI so that the user cannot select it again:
            modifiedGasesToChooseFrom = []
            for gas in self.gasesToPotentiallyRemoveCollection:
                if gas not in self.gasesToRemoveCollection:
                    modifiedGasesToChooseFrom.append(gas)

            self.gasToRemove.set('')
            self.gasesToPotentiallyRemoveDropDownMenu.grid_forget()
            self.gasesToPotentiallyRemoveDropDownMenu.destroy()
            self.gasesToPotentiallyRemoveDropDownMenu = OptionMenu(self.rightFrame, self.gasToRemove, *modifiedGasesToChooseFrom, command=self.addGasToListOfGasesToRemove)
            self.gasesToPotentiallyRemoveDropDownMenu.grid(row=14, column=1, sticky=W + E)

    # clears the gases to remove list,
    # linked to a button that says
    # "refresh gases to remove"
    def refreshGasesToRemoveList(self):
        if (self.gasesToRemoveCollection != None):
            if (len(self.gasesToRemoveCollection) > 0):
                # there are some things to refresh:
                self.gasesToRemoveCollection.clear()
                self.gasesThatWillBeRemovedLabel.configure(text="Gases to remove: []")

                self.gasesToPotentiallyRemoveDropDownMenu.grid_forget()
                self.gasesToPotentiallyRemoveDropDownMenu.destroy()
                self.gasesToPotentiallyRemoveDropDownMenu = OptionMenu(self.rightFrame, self.gasToRemove,
                                                                       *self.gasesToPotentiallyRemoveCollection,
                                                                       command=self.addGasToListOfGasesToRemove)
                self.gasesToPotentiallyRemoveDropDownMenu.grid(row=14, column=1, sticky=W + E)

    # selects a planet or no planet
    # and populates fields accordingly
    # this method is linked to the planets to
    # choose from dropdown
    def selectPlanet(self, selectedPlanet):

        if (selectedPlanet != 'N/A'):

            self.refreshGasesToAdd()
            self.refreshGasesToRemoveList()

            database = self.makeConnectionToDatabase()
            cursor = database.cursor()
            query = '''
            
                SELECT * 
                FROM Planets
                WHERE Name = %s; 
            
            '''
            cursor.execute(query, [selectedPlanet])
            self.initialPlanetRecord = []
            record = cursor.fetchone()
            print("Raw planet record: " + str(record))
            for attribute in record:
                self.initialPlanetRecord.append(attribute)

            query = '''
            
                SELECT *
                FROM DwarfPlanets
                WHERE Name = %s;
            
            '''
            cursor.execute(query, [selectedPlanet])
            record = cursor.fetchone()
            if (record != None):
                # this planet is a dwarf:
                self.planetIsInitiallyADwarfPlanet = True
            else:
                self.planetIsInitiallyADwarfPlanet = False

            query = '''
            
                SELECT * 
                FROM PlanetsInHabitZone
                WHERE Name = %s;
            
            '''
            cursor.execute(query, [selectedPlanet])
            record = cursor.fetchone()
            if (record != None):
                self.planetIsInitiallyInHabitZone = True
            else:
                self.planetIsInitiallyInHabitZone = False

            query = '''
            
                SELECT Gas
                FROM PlanetAtmospheres 
                WHERE Name = %s;
            
            '''
            cursor.execute(query, [selectedPlanet])
            record = cursor.fetchall()
            self.gasesToPotentiallyRemoveCollection = []

            self.gasesToPotentiallyRemoveCollection.append('')
            if (record != None):
                for gas in record:
                    self.gasesToPotentiallyRemoveCollection.append(gas[0])

            query = '''
            
                SELECT StarName
                FROM StarsPlanetsOrbit
                WHERE PlanetName = %s;
            
            '''
            cursor.execute(query, [selectedPlanet])
            record = cursor.fetchone()
            starPlanetOrbits = 'N/A'
            if (record != None):
                starPlanetOrbits = record[0]

            database.close()
            self.gasesToPotentiallyRemoveDropDownMenu.grid_forget()
            self.gasesToPotentiallyRemoveDropDownMenu.destroy()
            self.gasesToPotentiallyRemoveDropDownMenu = OptionMenu(self.rightFrame, self.gasToRemove, *self.gasesToPotentiallyRemoveCollection, command=self.addGasToListOfGasesToRemove)
            self.gasesToPotentiallyRemoveDropDownMenu.grid(row=14, column=1, sticky=W + E)

            # now ready to populate fields:
            self.planetMassLabel.configure(text=str(self.initialPlanetRecord[1]))
            self.planetGravityLabel.configure(text=str(self.initialPlanetRecord[2]))
            self.planetRadiusLabel.configure(text=str(self.initialPlanetRecord[3]))
            self.planetDistanceFromEarthLabel.configure(text=str(self.initialPlanetRecord[4]))
            self.planetEquilibriumTemperatureLabel.configure(text=str(self.initialPlanetRecord[5]))
            self.planetESILabel.configure(text=str(self.initialPlanetRecord[6]))
            self.planetRotationPeriodLabel.configure(text=str(self.initialPlanetRecord[7]))
            self.planetOrbitalPeriodLabel.configure(text=str(self.initialPlanetRecord[8]))
            self.planetEscapeVelocityLabel.configure(text=str(self.initialPlanetRecord[9]))
            self.initialPlanetImageDisplayerManager.openImage(False, self.initialPlanetRecord[10])
            self.initialPlanetDescriptionManager.loadDescriptionWithoutPromptingUser(self.initialPlanetRecord[11])

            if (self.planetIsInitiallyADwarfPlanet):
                self.planetIsADwarfPlanetLabel.configure(text="yes")
                self.planetIsADwarfCheckBox.select()
            else:
                self.planetIsADwarfPlanetLabel.configure(text="no")
                self.planetIsADwarfCheckBox.deselect()

            if (self.planetIsInitiallyInHabitZone):
                self.planetIsInTheHabitZoneLabel.configure(text="yes")
                self.planetIsInTheHabitZoneCheckbox.select()
            else:
                self.planetIsInTheHabitZoneLabel.configure(text="no")
                self.planetIsInTheHabitZoneCheckbox.deselect()

            gases = "["
            for gas in self.gasesToPotentiallyRemoveCollection:
                gases += " " + gas + " "
            gases += "]"

            self.planetAtmospheresLabel.configure(text=gases)
            self.starPlanetOrbitsLabel.configure(text=starPlanetOrbits)

        else:
            self.resetAllUI(False)

    # initialize all UI needed for a planet update
    def manageUpdate(self, windowToPutFrameOnto, updateManager, updateTitle):
        BaseUpdateManager.manageUpdate(self, windowToPutFrameOnto, updateManager, updateTitle)

        self.deleteOldImage = False
        self.deleteOldDescription = False
        self.changePlanetDwarfStatus = False
        self.changePlanetHabitZoneStatus = False
        self.changeStarPlanetOrbits = False

        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        query = '''
        
            SELECT Name
            From Planets;
        
        '''
        cursor.execute(query)
        records = cursor.fetchall()
        planetNames = []
        planetNames.append('N/A')
        if (records != None):
            for planetName in records:
                planetNames.append(planetName[0])

        self.selectedPlanet = StringVar()
        self.selectedPlanet.set('N/A')

        Label(self.leftFrame, text="Select a planet to update: ").grid(row=0, column=0)
        self.planetsToChooseFromDropDown = OptionMenu(self.leftFrame, self.selectedPlanet, *planetNames, command=self.selectPlanet)
        self.planetsToChooseFromDropDown.grid(row=0, column=1, sticky=W+E)

        Label(self.leftFrame, text="Planet mass: ").grid(row=1, column=0)
        self.planetMassLabel = Label(self.leftFrame, text="N/A")
        self.planetMassLabel.grid(row=1, column=1)

        Label(self.leftFrame, text="Planet Gravity: ").grid(row=2, column=0)
        self.planetGravityLabel = Label(self.leftFrame, text="N/A")
        self.planetGravityLabel.grid(row=2, column=1)

        Label(self.leftFrame, text="Planet Radius: ").grid(row=3, column=0)
        self.planetRadiusLabel = Label(self.leftFrame, text="N/A")
        self.planetRadiusLabel.grid(row=3, column=1)

        Label(self.leftFrame, text="Planet Distance from Earth").grid(row=4, column=0)
        self.planetDistanceFromEarthLabel = Label(self.leftFrame, text="N/A")
        self.planetDistanceFromEarthLabel.grid(row=4, column=1)

        Label(self.leftFrame, text="Planet Equilibrium temperature: ").grid(row=5, column=0)
        self.planetEquilibriumTemperatureLabel = Label(self.leftFrame, text="N/A")
        self.planetEquilibriumTemperatureLabel.grid(row=5, column=1)

        Label(self.leftFrame, text="Planet ESI: ").grid(row=6, column=0)
        self.planetESILabel = Label(self.leftFrame, text="N/A")
        self.planetESILabel.grid(row=6, column=1)

        Label(self.leftFrame, text="Planet Rotation Period: ").grid(row=7, column=0)
        self.planetRotationPeriodLabel = Label(self.leftFrame, text="N/A")
        self.planetRotationPeriodLabel.grid(row=7, column=1)

        Label(self.leftFrame, text="Planet Orbital Period: ").grid(row=8, column=0)
        self.planetOrbitalPeriodLabel = Label(self.leftFrame, text="N/A")
        self.planetOrbitalPeriodLabel.grid(row=8, column=1)

        Label(self.leftFrame, text="Planet Escape Velocity: ").grid(row=9, column=0)
        self.planetEscapeVelocityLabel = Label(self.leftFrame, text="N/A")
        self.planetEscapeVelocityLabel.grid(row=9, column=1)

        Label(self.leftFrame, text="Planet is a dwarf planet?: ").grid(row=10, column=0)
        self.planetIsADwarfPlanetLabel = Label(self.leftFrame, text="N/A")
        self.planetIsADwarfPlanetLabel.grid(row=10, column=1)

        Label(self.leftFrame, text="Planet is in the habit zone?: ").grid(row=11, column=0)
        self.planetIsInTheHabitZoneLabel = Label(self.leftFrame, text="N/A")
        self.planetIsInTheHabitZoneLabel.grid(row=11, column=1)

        Label(self.leftFrame, text="Star this planet orbits: ").grid(row=12, column=0)
        self.starPlanetOrbitsLabel = Label(self.leftFrame, text="N/A")
        self.starPlanetOrbitsLabel.grid(row=12, column=1)

        Label(self.leftFrame, text="Planet atmospheric gases: ").grid(row=13, column=0)
        self.planetAtmospheresLabel = Label(self.leftFrame, text="N/A")
        self.planetAtmospheresLabel.grid(row=13, column=1)

        self.initialPlanetImageDisplayerManager = ImageDisplayerManager()
        self.initialPlanetImageDisplayerManager.initializeImageDisplayer(14, 0, 2, self.leftFrame, None, False)

        self.initialPlanetDescriptionManager = TextBoxManager()
        self.initialPlanetDescriptionManager.initializeDescriptionBoxForReadingOnlyAndNotLoading(self.leftFrame, 16, 0, 17, 0)

        # updates UI:
        Label(self.rightFrame, text="New planet name: ").grid(row=0, column=0)
        self.newPlanetNameInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newPlanetNameInputBox.grid(row=0, column=1)

        Label(self.rightFrame, text="New Planet mass: ").grid(row=1, column=0)
        self.newPlanetMassInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newPlanetMassInputBox.grid(row=1, column=1)

        Label(self.rightFrame, text="New Planet Gravity: ").grid(row=2, column=0)
        self.newPlanetGravityInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newPlanetGravityInputBox.grid(row=2, column=1)

        Label(self.rightFrame, text="New Planet Radius: ").grid(row=3, column=0)
        self.newPlanetRadiusInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newPlanetRadiusInputBox.grid(row=3, column=1)

        Label(self.rightFrame, text="New Planet Distance from Earth ").grid(row=4, column=0)
        self.newPlanetDistanceFromEarthInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newPlanetDistanceFromEarthInputBox.grid(row=4, column=1)

        Label(self.rightFrame, text="New Planet equilibrium temperature: ").grid(row=5, column=0)
        self.newPlanetEquilibriumTemperatureInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newPlanetEquilibriumTemperatureInputBox.grid(row=5, column=1)

        Label(self.rightFrame, text="New Planet ESI: ").grid(row=6, column=0)
        self.newPlanetESIInputBox= Entry(self.rightFrame, width=50, borderwidth=1)
        self.newPlanetESIInputBox.grid(row=6, column=1)

        Label(self.rightFrame, text="New Planet Rotation Period: ").grid(row=7, column=0)
        self.newPlanetRotationPeriodInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newPlanetRotationPeriodInputBox.grid(row=7, column=1)

        Label(self.rightFrame, text="New Planet Orbital Period: ").grid(row=8, column=0)
        self.newPlanetOrbitalPeriodInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newPlanetOrbitalPeriodInputBox.grid(row=8, column=1)

        Label(self.rightFrame, text="New Planet Escape Velocity: ").grid(row=9, column=0)
        self.newPlanetEscapeVelocityInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newPlanetEscapeVelocityInputBox.grid(row=9, column=1)

        self.planetIsADwarf = IntVar()
        self.planetIsADwarfCheckBox = Checkbutton(self.rightFrame, text="Set to dwarf planet? ", variable=self.planetIsADwarf, onvalue=1, offvalue=0)
        self.planetIsADwarfCheckBox.deselect()
        self.planetIsADwarfCheckBox.grid(row=10, column=0)

        self.planetIsInTheHabitZone = IntVar()
        self.planetIsInTheHabitZoneCheckbox = Checkbutton(self.rightFrame, text="Place planet in habit zone?", variable=self.planetIsInTheHabitZone, onvalue=1, offvalue=0)
        self.planetIsInTheHabitZoneCheckbox.deselect()
        self.planetIsInTheHabitZoneCheckbox.grid(row=10, column=1)

        self.newSelectedStar = StringVar()
        self.newSelectedStar.set('')
        possibleStarNames = []
        possibleStarNames.append('')

        # user will be able to change the star this planet orbits from here
        # so I create a dropdown for them to select a new star from
        Label(self.rightFrame, text="Change star this planet orbits: ").grid(row=11, column=0)
        query = '''
        
            SELECT Name 
            FROM Stars; 
        
        '''
        cursor.execute(query)
        records = cursor.fetchall()
        if (records != None):
            for starName in records:
                possibleStarNames.append(starName[0])

        self.newPlanetStarDropDownMenu = OptionMenu(self.rightFrame, self.newSelectedStar, *possibleStarNames)
        self.newPlanetStarDropDownMenu.grid(row=11, column=1, sticky=W+E)

        self.gasesToAddCollection = []
        self.gasesToRemoveCollection = []
        self.newAtmosphereGasInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newAtmosphereGasInputBox.grid(row=12, column=1)
        Button(self.rightFrame, text="Add new gas", padx=80, pady=2, command=self.addGasToListofGasesToAdd).grid(row=12, column=0, sticky=W+E)
        Button(self.rightFrame, text="Refresh new gases to add", padx=80, pady=2, command=self.refreshGasesToAdd).grid(row=13, column=1, sticky=W+E)
        Button(self.rightFrame, text="Refresh gases to remove", padx=80, pady=2, command=self.refreshGasesToRemoveList).grid(row=13, column=0, sticky=W+E)

        Label(self.rightFrame, text="Select a gas to remove: ").grid(row=14, column=0)
        self.gasToRemove = StringVar()
        self.gasToRemove.set('')
        self.gasesToPotentiallyRemoveDropDownMenu = OptionMenu(self.rightFrame, self.gasToRemove, '')
        self.gasesToPotentiallyRemoveDropDownMenu.grid(row=14, column=1, sticky=W+E)

        self.gasesThatWillBeAddedLabel = Label(self.rightFrame, text='Gases that will be added: ')
        self.gasesThatWillBeAddedLabel.grid(row=15, column=0)

        self.gasesThatWillBeRemovedLabel = Label(self.rightFrame, text='Gases that will be removed: ')
        self.gasesThatWillBeRemovedLabel.grid(row=15, column=1)

        self.newPlanetImageManager = ImageDisplayerManager()
        self.newPlanetImageManager.initializeImageDisplayer(16, 0, 2, self.rightFrame, None, True)

        self.newPlanetDescriptionManager = TextBoxManager()
        self.newPlanetDescriptionManager.initializeDescriptionFormForUserLoading(self.rightFrame, 19, 0, 20, 0, 21, 0)

        self.cancelButton.grid(row=1, column=0, sticky=W+E)
        self.confirmButton.grid(row=1, column=1, sticky=W+E)

        database.close()
