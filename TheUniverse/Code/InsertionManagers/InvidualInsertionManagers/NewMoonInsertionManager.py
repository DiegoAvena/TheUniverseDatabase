'''

----SUMMARY---
Allows the user to insert
a new moon

---IMPORTS---
BaseInsertionManager:

Used to obtain base functionality
for a more specific insertion, since this
class is for the specific insertion of new
moons

tkinter - for all of the UI

connector - for performing the insertion queries

'''

from Code.InsertionManagers.BaseInsertionManager import BaseInsertionManager
from tkinter import *
import mysql.connector

class NewMoonInsertionManager(BaseInsertionManager):

    global moonNameInputBox
    global moonMassInputBox
    global moonGravityInputBox
    global moonRadiusInputBox
    global moonDistanceFromEarthInputBox
    global moonMeanSurfaceTemperatureInputBox
    global moonEscapeVelocityInputBox
    global moonRotationPeriodInputBox
    global moonOrbitalPeriodInputBox
    global moonDistanceFromPlanetItOrbitsInputBox
    global moonDiscoveryYearInputBox

    # moon discoverer:
    global enterNewMoonDiscovererCheckBox
    global selectedMoonDiscoverer
    global enteringANewMoonDiscoverer
    global moonDiscovererNameInputBox
    global moonDiscoverersDropDownBox
    global moonDiscoverers

    global planetMoonOrbitsDropdown
    global selectedPlanetMoonOrbits

    def enableOrDisableNewDiscovererInsertion(self):
        if (self.enteringANewMoonDiscoverer.get() == 1):
            self.moonDiscoverersDropDownBox.grid_forget()
            self.moonDiscovererNameInputBox.grid(row=11, column=1)
        else:
            self.moonDiscovererNameInputBox.grid_forget()
            self.moonDiscoverersDropDownBox.grid(row=11, column=0, columnspan=3)

    def confirm(self):
        thereWasAnError = False

        moonName = self.moonNameInputBox.get()
        if (self.insertionValidator.validateWord(False, moonName, "Moon Name") == False):
            thereWasAnError = True

        moonMass = self.moonMassInputBox.get()
        if (self.insertionValidator.validateDecimalValue(moonMass, False, "Moon Mass", True) == False):
            thereWasAnError = True

        planetMoonOrbits = self.selectedPlanetMoonOrbits.get()
        if (self.insertionValidator.validateWord(False, planetMoonOrbits, "Planet moon orbits") == False):
            thereWasAnError = True

        moonGravity = self.moonGravityInputBox.get()
        if (self.insertionValidator.validateDecimalValue(moonGravity, False, "Moon Gravity", True) == False):
            thereWasAnError = True

        moonRadius = self.moonRadiusInputBox.get()
        if (self.insertionValidator.validateDecimalValue(moonRadius, False, "Moon Radius", True) == False):
            thereWasAnError = True

        moonDistanceFromEarth = self.moonDistanceFromEarthInputBox.get()
        if (self.insertionValidator.validateDecimalValue(moonDistanceFromEarth, False, "Moon distance from Earth", True) == False):
            thereWasAnError = True

        moonMeanSurfaceTemperature = self.moonMeanSurfaceTemperatureInputBox.get()
        if (self.insertionValidator.validateDecimalValue(moonMeanSurfaceTemperature, False, "Moon mean surface temperature", True) == False):
            thereWasAnError = True

        moonEscapeVelocity = self.moonEscapeVelocityInputBox.get()
        if (self.insertionValidator.validateDecimalValue(moonEscapeVelocity, False, "Moon escape velocity", True) == False):
            thereWasAnError = True

        moonRotationPeriod = self.moonRotationPeriodInputBox.get()
        if (self.insertionValidator.validateDecimalValue(moonRotationPeriod, False, "Moon rotational period", True) == False):
            thereWasAnError = True

        moonOrbitalPeriod = self.moonOrbitalPeriodInputBox.get()
        if (self.insertionValidator.validateDecimalValue(moonOrbitalPeriod, False, "Moon orbital period", True) == False):
            thereWasAnError = True

        moonDistanceFromPlanetItOrbits = self.moonDistanceFromPlanetItOrbitsInputBox.get()
        if (self.insertionValidator.validateDecimalValue(moonDistanceFromPlanetItOrbits, False, "Moon distance from planet it orbits", True) == False):
            thereWasAnError = True

        moonDiscoverer = ""
        moonDiscoveryYear = ""
        if (self.enteringANewMoonDiscoverer.get() == 1):
            moonDiscoverer = self.moonDiscovererNameInputBox.get()
            if (len(moonDiscoverer) > 0):
                moonDiscoveryYear = self.moonDiscoveryYearInputBox.get()
                if (self.insertionValidator.validateYear(moonDiscoveryYear, "Moon discovery year") == False):
                    thereWasAnError = True
        elif (self.selectedMoonDiscoverer.get() != 'N/A'):
            moonDiscoverer = self.selectedMoonDiscoverer.get()
            moonDiscoveryYear = self.moonDiscoveryYearInputBox.get()
            if (self.insertionValidator.validateYear(moonDiscoveryYear, "Moon discovery year") == False):
                thereWasAnError = True

        if (thereWasAnError == False):
            moonRecord = []
            moonRecord.append(moonName)
            moonRecord.append(self.insertionValidator.obtainFinalValue(moonMass))
            moonRecord.append(planetMoonOrbits)
            moonRecord.append(self.insertionValidator.obtainFinalValue(moonGravity))
            moonRecord.append(self.insertionValidator.obtainFinalValue(moonRadius))
            moonRecord.append(self.insertionValidator.obtainFinalValue(moonDistanceFromEarth))
            moonRecord.append(self.insertionValidator.obtainFinalValue(moonMeanSurfaceTemperature))
            moonRecord.append(self.insertionValidator.obtainFinalValue(moonEscapeVelocity))
            moonRecord.append(self.insertionValidator.obtainFinalValue(moonRotationPeriod))
            moonRecord.append(self.insertionValidator.obtainFinalValue(moonOrbitalPeriod))
            moonRecord.append(self.insertionValidator.obtainFinalValue(self.imageDir))
            moonRecord.append(self.insertionValidator.obtainFinalValue(self.descriptionDirectory))
            moonRecord.append(self.insertionValidator.obtainFinalValue(moonDistanceFromPlanetItOrbits))

            moonDiscovererRecord = []
            if (len(moonDiscoverer) > 0):
                moonDiscovererRecord.append(moonDiscoverer)
                moonDiscovererRecord.append(moonName)
                moonDiscovererRecord.append(self.insertionValidator.obtainFinalValue(moonDiscoveryYear))

            # place records into the DB:
            try:
                database = self.makeConnectionToDatabase()
                cursor = database.cursor()
                query = '''

                                INSERT INTO Moons 
                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);

                            '''

                cursor.execute(query, moonRecord)

                messageToShowInPopUpBox = "Moon Name: " + moonRecord[0] + "\n" + \
                                          "Moon Mass: " + str(moonRecord[1]) + "\n" + \
                                          "Planet Moon Orbits: " + moonRecord[2] + "\n" + \
                                          "Moon Gravity: " + str(moonRecord[3]) + "\n" + \
                                          "Moon Radius: " + str(moonRecord[4]) + "\n" + \
                                          "Moon Distance From Earth: " + str(moonRecord[5]) + "\n" + \
                                          "Moon Mean Surface Temperature: " + str(moonRecord[6]) + "\n" + \
                                          "Moon Escape Velocity: " + str(moonRecord[7]) + "\n" + \
                                          "Moon Rotational Period: " + str(moonRecord[8]) + "\n" + \
                                          "Moon Orbital Period: " + str(moonRecord[9]) + "\n" + \
                                          "Moon Image Directory: " + str(moonRecord[10]) + "\n" + \
                                          "Moon Description Directory: " + str(moonRecord[11]) + \
                                          "Moon Distance From Planet it Orbits: " + str(moonRecord[12])

                if (len(moonDiscovererRecord) > 0):

                    messageToShowInPopUpBox += "Moon Discoverer: " + str(moonDiscovererRecord[0]) + "\n" + \
                                               "Moon Discovery Year: " + str(moonDiscovererRecord[2])

                    if (self.enteringANewMoonDiscoverer.get() == 1):
                        self.moonDiscoverers.append(moonDiscoverer)
                        self.moonDiscoverersDropDownBox.grid_forget()
                        self.moonDiscoverersDropDownBox.destroy()
                        self.moonDiscoverersDropDownBox = OptionMenu(self.insertionFrame, self.selectedMoonDiscoverer,
                                                                     *self.moonDiscoverers)

                    query = '''

                                                INSERT INTO MoonDiscovers
                                                VALUES(%s, %s, %s);

                                            '''
                    cursor.execute(query, moonDiscovererRecord)

                if (self.showConfirmationPopUp(messageToShowInPopUpBox) == True):
                    database.commit()
                    self.showSuccessMessage(21, 0, 2)

                    # Reset all UI:
                    self.moonNameInputBox.delete(0, END)
                    self.moonMassInputBox.delete(0, END)
                    self.moonGravityInputBox.delete(0, END)
                    self.moonRadiusInputBox.delete(0, END)
                    self.moonDistanceFromEarthInputBox.delete(0, END)
                    self.moonMeanSurfaceTemperatureInputBox.delete(0, END)
                    self.moonEscapeVelocityInputBox.delete(0, END)
                    self.moonRotationPeriodInputBox.delete(0, END)
                    self.moonOrbitalPeriodInputBox.delete(0, END)
                    self.moonDistanceFromPlanetItOrbitsInputBox.delete(0, END)
                    self.moonDiscoveryYearInputBox.delete(0, END)
                    self.moonDiscovererNameInputBox.delete(0, END)

                    self.imageDir = ''
                    self.descriptionDirectory = ''
                    self.selectedMoonDiscoverer.set('N/A')
                    self.selectedPlanetMoonOrbits.set('N/A')

                    self.resetImageUI(2)
                    self.resetDescriptionUI(14, 0)
                else:
                    database.rollback()
            except mysql.connector.Error:
                self.insertionValidator.errorMessage = self.errorMessageForWhenCommitFailsDueToSqlError
                self.showErrorMessage(21, 0, 2)
                database.rollback()

            database.close()
        else:
            self.showErrorMessage(21, 0, 2)

        self.insertionValidator.errorMessage = ''

    def manageInsertion(self, windowToPutFrameOnto, insertionManager, insertionTitle):
        BaseInsertionManager.manageInsertion(self, windowToPutFrameOnto, insertionManager, insertionTitle)

        Label(self.insertionFrame, text="Moon name (required): ").grid(row=0, column=0)
        self.moonNameInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.moonNameInputBox.grid(row=0, column=1)

        Label(self.insertionFrame, text="Moon mass (kg): ").grid(row=1, column=0)
        self.moonMassInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.moonMassInputBox.grid(row=1, column=1)

        Label(self.insertionFrame, text="Moon gravity (m/s^2): ").grid(row=2, column=0)
        self.moonGravityInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.moonGravityInputBox.grid(row=2, column=1)

        Label(self.insertionFrame, text="Moon radius (km): ").grid(row=3, column=0)
        self.moonRadiusInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.moonRadiusInputBox.grid(row=3, column=1)

        Label(self.insertionFrame, text="Moon distance from Earth (km): ").grid(row=4, column=0)
        self.moonDistanceFromEarthInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.moonDistanceFromEarthInputBox.grid(row=4, column=1)

        Label(self.insertionFrame, text="Moon mean surface temperature (K): ").grid(row=5, column=0)
        self.moonMeanSurfaceTemperatureInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.moonMeanSurfaceTemperatureInputBox.grid(row=5, column=1)

        Label(self.insertionFrame, text="Moon escape velocity (km/h): ").grid(row=6, column=0)
        self.moonEscapeVelocityInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.moonEscapeVelocityInputBox.grid(row=6, column=1)

        Label(self.insertionFrame, text="Moon rotational period (Earth Days): ").grid(row=7, column=0)
        self.moonRotationPeriodInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.moonRotationPeriodInputBox.grid(row=7, column=1)

        Label(self.insertionFrame, text="Moon orbital period (Earth Days): ").grid(row=8, column=0)
        self.moonOrbitalPeriodInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.moonOrbitalPeriodInputBox.grid(row=8, column=1)

        Label(self.insertionFrame, text="Moon distance from planet it orbits (km): ").grid(row=9, column=0)
        self.moonDistanceFromPlanetItOrbitsInputBox= Entry(self.insertionFrame, width=50, borderwidth=1)
        self.moonDistanceFromPlanetItOrbitsInputBox.grid(row=9, column=1)

        self.enteringANewMoonDiscoverer = IntVar()
        self.enteringANewMoonDiscoverer.set(0)
        self.enterNewMoonDiscovererCheckBox = Checkbutton(self.insertionFrame, text="Enter New discoverer Name?", font=self.buttonFontStyle,variable=self.enteringANewMoonDiscoverer, onvalue=1, offvalue=0, command=self.enableOrDisableNewDiscovererInsertion)
        self.enterNewMoonDiscovererCheckBox.grid(row=10, column=0, columnspan=2)

        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        query = '''
        
            SELECT DISTINCT DiscovererName
            FROM MoonDiscovers;
        
        '''
        cursor.execute(query)

        records = cursor.fetchall()
        self.moonDiscoverers = []
        self.moonDiscoverers.append('N/A')
        for moonDiscoverer in records:
            self.moonDiscoverers.append(moonDiscoverer[0])

        Label(self.insertionFrame, text="Enter the discoverer of this moon: ").grid(row=11, column=0)
        self.moonDiscovererNameInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)

        self.selectedMoonDiscoverer = StringVar()
        self.selectedMoonDiscoverer.set(self.moonDiscoverers[0])
        self.moonDiscoverersDropDownBox = OptionMenu(self.insertionFrame, self.selectedMoonDiscoverer, *self.moonDiscoverers)
        self.moonDiscoverersDropDownBox.grid(row=11, column=1)

        Label(self.insertionFrame, text="Enter the discovery year of the moon: ").grid(row=12, column=0)
        self.moonDiscoveryYearInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.moonDiscoveryYearInputBox.grid(row=12, column=1)

        # place moon load description file button
        self.initializeDescriptionForm(13, 0, 14, 0, 15, 0)

        # place moon load image file button:
        self.loadImageDirectoryButton.grid(row=16, column=0, columnspan=2)
        self.initializeImageDirLabelPos(17, 0, 2)
        self.imageCanvas.grid(row=18, column=0, columnspan=2)

        # place the planet moon orbits selection box in:
        query = '''
        
            SELECT Name 
            FROM Planets;
        
        '''
        cursor.execute(query)
        records = cursor.fetchall()
        planets = []
        planets.append('N/A')

        for planetName in records:
            planets.append(planetName[0])

        self.selectedPlanetMoonOrbits = StringVar()
        self.selectedPlanetMoonOrbits.set(planets[0])

        Label(self.insertionFrame, text="Select the planet moon orbits: ").grid(row=19, column=0)
        self.planetMoonOrbitsDropdown = OptionMenu(self.insertionFrame, self.selectedPlanetMoonOrbits, *planets)
        self.planetMoonOrbitsDropdown.grid(row=19, column=1)

        self.confirmButton.grid(row=20, column=0, sticky=W+E)
        self.cancelButton.grid(row=20, column=1, sticky=W+E)

        database.close()
