'''
----SUMMARY---
Allows the user to insert
a new planet

---IMPORTS---
BaseInsertionManager:

Used to obtain base functionality
for a more specific insertion, since this
class is for the specific insertion of new
planets

tkinter - for all of the UI

connector - for performing the insertion queries
'''

from Code.InsertionManagers.BaseInsertionManager import BaseInsertionManager
from tkinter import *
import mysql.connector

class NewPlanetInsertionManager(BaseInsertionManager):

    global planetNameInputBox
    global planetMassInputBox
    global planetGravityInputBox
    global planetRadiusInputbox
    global planetDistanceFromEarthInputBox
    global planetEquilibriumTemperatureInputBox
    global ESIInputBox
    global rotationPeriodInputBox
    global orbitalPeriodInputbox
    global escapeVelocityInputBox
    global planetIsADwarfCheckBox
    global planetIsInTheHabitZoneBox

    # planet atmosphere
    global atmosphereInputBox
    global currentAtmosphereComponents
    global confirmAtmosphereComponent
    global currentAtmosphereComponentsLabel

    global selectedStar
    global starPlanetOrbitsDropDownBox

    global planetIsADwarfCheckBox
    global planetIsADwarf

    global planetIsInTheHabitZoneCheckBox
    global planetIsInTheHabitZone

    def insertNewAtmosphereComponent(self, newAtmosphereComponent):
        if (self.insertionValidator.validateWord(False, newAtmosphereComponent, "New atmospheric gas")):

            # insure no dups are added in
            thisAtmosphereIsUnique = True
            for atmosphere in self.currentAtmosphereComponents:
                if (atmosphere == newAtmosphereComponent):
                    thisAtmosphereIsUnique = False
                    break

            if (thisAtmosphereIsUnique == False):
                return

            self.currentAtmosphereComponents.append(newAtmosphereComponent)
            self.currentAtmosphereComponentsLabel.grid_forget()
            self.currentAtmosphereComponentsLabel.destroy()
            self.currentAtmosphereComponentsLabel = Label(self.insertionFrame, text=str(self.currentAtmosphereComponents))
            self.currentAtmosphereComponentsLabel.grid(row=19, column=0, columnspan=2)
            self.atmosphereInputBox.delete(0, END)

        else:
            self.atmosphereInputBox.delete(0, END)

        self.insertionValidator.errorMessage = ''

    def confirm(self):

        thereWasAnError = False

        planetName = self.planetNameInputBox.get()
        if (self.insertionValidator.validateWord(False, planetName, "Planet Name") == False):
            thereWasAnError = True

        planetMass = self.planetMassInputBox.get()
        if (self.insertionValidator.validateDecimalValue(planetMass, False, "Planet Mass", True) == False):
            thereWasAnError = True

        planetGravity = self.planetGravityInputBox.get()
        if (self.insertionValidator.validateDecimalValue(planetGravity, False, "Planet Gravity", True) == False):
            thereWasAnError = True

        planetRadius = self.planetRadiusInputbox.get()
        if (self.insertionValidator.validateDecimalValue(planetRadius, False, "Planet Radius", True) == False):
            thereWasAnError = True

        planetDistanceFromEarth = self.planetDistanceFromEarthInputBox.get()
        if (self.insertionValidator.validateDecimalValue(planetDistanceFromEarth, False, "Planet Distance From Earth", False) == False):
            thereWasAnError = True

        planetEquilibriumTemperature = self.planetEquilibriumTemperatureInputBox.get()
        if (self.insertionValidator.validateDecimalValue(planetEquilibriumTemperature, False, "Planet Equilibrium temperature", True) == False):
            thereWasAnError = True

        planetESI = self.ESIInputBox.get()
        if (self.insertionValidator.makeSureDecimalIsWithinACertainRange(planetESI, "Planet ESI", True, 0, 1) == False):
            thereWasAnError = True

        planetRotationalPeriod = self.rotationPeriodInputBox.get()
        if (self.insertionValidator.validateDecimalValue(planetRotationalPeriod, False, "Planet Rotational Period", True) == False):
            thereWasAnError = True

        planetOrbitalPeriod = self.orbitalPeriodInputbox.get()
        if (self.insertionValidator.validateDecimalValue(planetOrbitalPeriod, False, "Planet orbital period", True) == False):
            thereWasAnError = True

        planetEscapeVelocity = self.escapeVelocityInputBox.get()
        if (self.insertionValidator.validateDecimalValue(planetEscapeVelocity, False, "Planet Escape Velocity", True) == False):
            thereWasAnError = True

        if (self.insertionValidator.validateWord(False, self.selectedStar.get(), "Star planet Orbits") == False):
            thereWasAnError = True

        if (thereWasAnError == False):

            # can insert the planet into the database:
            planetRecord = []
            planetRecord.append(planetName)
            planetRecord.append(self.insertionValidator.obtainFinalValue(planetMass))
            planetRecord.append(self.insertionValidator.obtainFinalValue(planetGravity))
            planetRecord.append(self.insertionValidator.obtainFinalValue(planetRadius))
            planetRecord.append(self.insertionValidator.obtainFinalValue(planetDistanceFromEarth))
            planetRecord.append(self.insertionValidator.obtainFinalValue(planetEquilibriumTemperature))
            planetRecord.append(self.insertionValidator.obtainFinalValue(planetESI))
            planetRecord.append(self.insertionValidator.obtainFinalValue(planetRotationalPeriod))
            planetRecord.append(self.insertionValidator.obtainFinalValue(planetOrbitalPeriod))
            planetRecord.append(self.insertionValidator.obtainFinalValue(planetEscapeVelocity))
            planetRecord.append(self.insertionValidator.obtainFinalValue(self.imageDir))
            planetRecord.append(self.insertionValidator.obtainFinalValue(self.descriptionDirectory))

            dwarfPlanetRecord = []
            if (self.planetIsADwarf.get() == 1):
                dwarfPlanetRecord.append(planetName)

            habitZonePlanetRecord = []
            if (self.planetIsInTheHabitZone.get() == 1):
                habitZonePlanetRecord.append(planetName)

            starThisPlanetOrbitsRecord = [self.selectedStar.get(), planetName]

            planetAtmosphereRecords = []
            if (len(self.currentAtmosphereComponents) > 0):
                for gas in self.currentAtmosphereComponents:
                    planetAtmosphereRecords.append([planetName, gas])

            try:
                database = self.makeConnectionToDatabase()
                cursor = database.cursor()

                query = '''

                                INSERT INTO Planets 
                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);

                            '''

                cursor.execute(query, planetRecord)
                messageToShowInPopUp = "Planet Name: " + planetRecord[0] + "\n" + \
                                       "Planet Mass: " + str(planetRecord[1]) + "\n" + \
                                       "Planet Gravity: " + str(planetRecord[2]) + "\n" + \
                                       "Planet Radius: " + str(planetRecord[3]) + "\n" + \
                                       "Distance from Earth: " + str(planetRecord[4]) + "\n" + \
                                       "Equilibrium Temperature: " + str(planetRecord[5]) + "\n" + \
                                       "ESI: " + str(planetRecord[6]) + "\n" + \
                                       "Planet Rotation Period: " + str(planetRecord[7]) + "\n" + \
                                       "Planet Orbital Period: " + str(planetRecord[8]) + "\n" + \
                                       "Planet Escape Velocity: " + str(planetRecord[9]) + "\n" + \
                                       "Planet Image Directory: " + str(planetRecord[10]) + "\n" + \
                                       "Planet Description Directory: " + str(planetRecord[11])

                if (len(planetAtmosphereRecords)):
                    messageToShowInPopUp += "\n" + "Planet Atmospheres: " + str(planetAtmosphereRecords)
                    for atmosphereRecord in planetAtmosphereRecords:
                        query = '''

                                        INSERT INTO PlanetAtmospheres 
                                        VALUES(%s, %s);

                                    '''
                        cursor.execute(query, atmosphereRecord)

                query = '''
                                INSERT INTO StarsPlanetsOrbit 
                                VALUES(%s, %s);
                            '''
                cursor.execute(query, starThisPlanetOrbitsRecord)
                messageToShowInPopUp += "\n" + "Star this planet orbits: " + starThisPlanetOrbitsRecord[0]
                messageToShowInPopUp += "\n" + "Planet is a dwarf planet? "

                if (self.planetIsADwarf.get() == 1):
                    messageToShowInPopUp += "yes"
                    query = '''

                                    INSERT INTO DwarfPlanets 
                                    VALUES(%s);

                                '''
                    cursor.execute(query, [planetName])
                else:
                    messageToShowInPopUp += "no"

                messageToShowInPopUp += "\n" + "Planet is in the habit zone: "
                if (self.planetIsInTheHabitZone.get() == 1):
                    messageToShowInPopUp += "yes"
                    query = '''

                                    INSERT INTO PlanetsInHabitZone 
                                    VALUES(%s);

                                '''
                    cursor.execute(query, [planetName])
                else:
                    messageToShowInPopUp += "no"

                if (self.showConfirmationPopUp(messageToShowInPopUp) == True):
                    self.showSuccessMessage(22, 0, 2)

                    database.commit()

                    # Clear all text boxes:
                    self.planetNameInputBox.delete(0, END)
                    self.planetMassInputBox.delete(0, END)
                    self.planetGravityInputBox.delete(0, END)
                    self.planetRadiusInputbox.delete(0, END)
                    self.planetDistanceFromEarthInputBox.delete(0, END)
                    self.planetEquilibriumTemperatureInputBox.delete(0, END)
                    self.ESIInputBox.delete(0, END)
                    self.rotationPeriodInputBox.delete(0, END)
                    self.orbitalPeriodInputbox.delete(0, END)
                    self.escapeVelocityInputBox.delete(0, END)

                    self.resetDescriptionUI(15, 0)
                    self.resetImageUI(2)

                    self.currentAtmosphereComponents.clear()
                    self.currentAtmosphereComponentsLabel.grid_forget()
                    self.currentAtmosphereComponentsLabel.destroy()
                    self.currentAtmosphereComponentsLabel = Label(self.insertionFrame,
                                                                  text="Current atmosphere components" + str(
                                                                      self.currentAtmosphereComponents))
                    self.currentAtmosphereComponentsLabel.grid(row=19, column=0, columnspan=2)

                    self.planetIsADwarfCheckBox.deselect()
                    self.planetIsInTheHabitZoneCheckBox.deselect()

                    self.selectedStar.set('N/A')
                else:
                    database.rollback()
            except mysql.connector.Error as error:
                self.insertionValidator.errorMessage = self.errorMessageForWhenCommitFailsDueToSqlError + ": " + str(error)
                self.showErrorMessage(22, 0, 2)
                database.rollback()

            database.commit()
            database.close()

        else:
            self.showErrorMessage(22, 0, 2)

        self.insertionValidator.errorMessage = ''

    def manageInsertion(self, windowToPutFrameOnto, insertionManager, insertionTitle):
        BaseInsertionManager.manageInsertion(self, windowToPutFrameOnto, insertionManager, insertionTitle)

        Label(self.insertionFrame, text="Planet Name (Required): ").grid(row=0, column=0)
        self.planetNameInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.planetNameInputBox.grid(row=0, column=1)

        Label(self.insertionFrame, text="Planet Mass (Earth = 1): ").grid(row=1, column=0)
        self.planetMassInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.planetMassInputBox.grid(row=1, column=1)

        Label(self.insertionFrame, text="Planet Gravity (Earth = 1): ").grid(row=2, column=0)
        self.planetGravityInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.planetGravityInputBox.grid(row=2, column=1)

        Label(self.insertionFrame, text="Planet Radius (Earth = 1): ").grid(row=3, column=0)
        self.planetRadiusInputbox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.planetRadiusInputbox.grid(row=3, column=1)

        Label(self.insertionFrame, text="Planet distance from Earth (ly): ").grid(row=4, column=0)
        self.planetDistanceFromEarthInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.planetDistanceFromEarthInputBox.grid(row=4, column=1)

        Label(self.insertionFrame, text="Planet equilibrium temperature (K): ").grid(row=5, column=0)
        self.planetEquilibriumTemperatureInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.planetEquilibriumTemperatureInputBox.grid(row=5, column=1)

        Label(self.insertionFrame, text="Planet ESI (0-1): ").grid(row=6, column=0)
        self.ESIInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.ESIInputBox.grid(row=6, column=1)

        Label(self.insertionFrame, text="Rotation Period (Earth days): ").grid(row=7, column=0)
        self.rotationPeriodInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.rotationPeriodInputBox.grid(row=7, column=1)

        Label(self.insertionFrame, text="Orbital  Period (Earth days)").grid(row=8, column=0)
        self.orbitalPeriodInputbox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.orbitalPeriodInputbox.grid(row=8, column=1)

        Label(self.insertionFrame, text="Escape Velocity (km/h): ").grid(row=9, column=0)
        self.escapeVelocityInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.escapeVelocityInputBox.grid(row=9, column=1)

        Label(self.insertionFrame, text="Select the star this planet orbits: ").grid(row=10, column=0)
        database = self.makeConnectionToDatabase()
        cursor = database.cursor()

        query = '''
        
            SELECT Name 
            FROM Stars;
        
        '''
        cursor.execute(query)
        records = cursor.fetchall()
        stars = []
        stars.append('N/A')

        self.selectedStar = StringVar()
        self.selectedStar.set(stars[0])

        for star in records:
            stars.append(star[0])

        self.starPlanetOrbitsDropDownBox = OptionMenu(self.insertionFrame, self.selectedStar, *stars)
        self.starPlanetOrbitsDropDownBox.grid(row=10, column=1)

        self.loadImageDirectoryButton.grid(row=11, column=0, columnspan=2, sticky=W+E)
        self.initializeImageDirLabelPos(12, 0, 2)
        self.imageCanvas.grid(row=13, column=0, columnspan=2)

        self.initializeDescriptionForm(14, 0, 15, 0, 16, 0)

        Label(self.insertionFrame, text="Insert a new atmosphere component: ").grid(row=17, column=0)
        self.atmosphereInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.atmosphereInputBox.grid(row=17, column=1)

        self.confirmAtmosphereComponent = Button(self.insertionFrame, text="CONFIRM ATMOSPHERE", font=self.buttonFontStyle, padx=80, pady=10, command= lambda: self.insertNewAtmosphereComponent(self.atmosphereInputBox.get()))
        self.confirmAtmosphereComponent.grid(row=18, column=0, columnspan=2, sticky=W+E)

        self.currentAtmosphereComponents = []
        self.currentAtmosphereComponentsLabel = Label(self.insertionFrame, text="Current Atmosphere components: " + str(self.currentAtmosphereComponents))
        self.currentAtmosphereComponentsLabel.grid(row=19, column=0, columnspan=2)

        self.planetIsADwarf = IntVar()
        self.planetIsADwarfCheckBox = Checkbutton(self.insertionFrame, text="Planet is a dwarf?", variable=self.planetIsADwarf, onvalue=1, offvalue=0)
        self.planetIsADwarfCheckBox.deselect()
        self.planetIsADwarfCheckBox.grid(row=20, column=0)

        self.planetIsInTheHabitZone = IntVar()
        self.planetIsInTheHabitZoneCheckBox = Checkbutton(self.insertionFrame, text="Planet is in the habit zone?", variable=self.planetIsInTheHabitZone, onvalue=1, offvalue=0)
        self.planetIsInTheHabitZoneCheckBox.deselect()
        self.planetIsInTheHabitZoneCheckBox.grid(row=20, column=1)

        self.confirmButton.grid(row=21, column=0, sticky=W + E)
        self.cancelButton.grid(row=21, column=1, stick=W + E)

