'''

----SUMMARY----
Allows the user to search
for individual planets and produce
reports on these.

A reminder to myself for how report generation works from here:

The report behavior is a bit hidden, but since this
class inherits from BaseSingleSearchManager, and BaseSingleSearchManager
inherits from BaseDataBaseInteractionManager, this class
has the ability to call on the report generator instance
and make a report.

This is because inside of the BaseDataBaseInteractionManager, there
is a member called insertionManager; this member is always of the OptionBase
type (its always a class that extends from this class); inside of OptionBase,
I have a member called reportGenerator, which is always of type ReportGenerator; hence,
this class will be able to call the generateReport() method from the ReportGenerator
via this reportGenerator member of the OptionBase.

I chose this setup because it made things easier for a multisearch option to only have 1 instance
of the report generator loaded when the more specific option menu loads up (so when RecordSearchManager is
loaded up, 1 instance of the report generator is created); it makes things easier because this insures
all of the data from the different records can be funneled into 1 report generator, allowing for, in the end,
the combining of all the seperate records turned up by a multi search option into 1 pdf and 1 csv report. If
I were only doing single search methods then I would have gone with a simpler approach and just have each
single search manager initialize its own report generator, but this was not the case here.

----IMPORTS----
BaseSingleSearchManager:

Used to obtain base functionality for a single search option,
since this is a specific option for searching for a single planet

tkinter - Used for all the UI

ImageDisplayerManager -
This is used to display an image of the
planet the user searches for

TextBoxManager -
Used to display a description of the
planet the user searches for

'''

from Code.SearchManagers.BaseSearchManagers.BaseSingleSearchManager import BaseSingleSearchManager
from tkinter import *
from Code.Displayers.ImageDisplayerManager import ImageDisplayerManager
from Code.Displayers.TextBoxManager import TextBoxManager

class SinglePlanetarySearchManager(BaseSingleSearchManager):

    global atmosphericGases
    global numberOfMoons

    global planetNameLabel
    global planetNameResultLabel

    global planetAtmospheresLabel
    global planetAtmosphereResultsLabel

    global planetMassLabel
    global planetMassResultLabel

    global planetGravityLabel
    global planetGravityResultLabel

    global planetRadiusLabel
    global planetRadiusResultsLabel

    global planetDistanceFromEarthLabel
    global planetDistanceFromEarthResultsLabel

    global planetEquilibriumTemperatureLabel
    global planetEquilibriumTemperatureResultsLabel

    global planetESILabel
    global planetESIResultsLabel

    global planetRotationalPeriodLabel
    global planetRotationalPeriodResultsLabel

    global planetOrbitalPeriodLabel
    global planetOrbitalPeriodResultsLabel

    global planetEscapeVelocityLabel
    global planetEscapeVelocityResultsLabel

    global planetIsADwarfLabel
    global planetIsADwarfResultsLabel

    global planetIsInTheHabitZoneLabel
    global planetIsInTheHabitZoneResultsLabel

    global planetIsAnExoPlanetLabel
    global planetIsAnExoPlanetResultsLabel

    global planetImageDisplayer

    global planetDescriptionDisplayer

    global numberOfMoonsLabel
    global numberOfMoonsResultLabel

    global moonNamesTextBox

    global starsPlanetOrbitsLabel
    global starsPlanetOrbitsResultLabel

    # filters:
    global showMassCheckBox
    global showMass

    global showGravityCheckBox
    global showGravity

    global showRadiusCheckBox
    global showRadius

    global showDistanceFromEarthCheckBox
    global showDistanceFromEarth

    global showEquilibriumTemperatureCheckBox
    global showTemperature

    global showESICheckBox
    global showESI

    global showRotationalPeriodCheckBox
    global showRotationalPeriod

    global showOrbitalPeriodCheckBox
    global showOrbitalPeriod

    global showEscapeVelocityCheckBox
    global showEscapeVelocity

    global showImageCheckBox
    global showImage

    global showDescriptionCheckBox
    global showDescription

    global showPlanetIsInHabitZoneCheckBox
    global showPlanetIsInHabitZone

    global showPlanetIsAnExoPlanetCheckBox
    global showPlanetIsAnExoPlanet

    global showPlanetIsDwarfCheckBox
    global showPlanetIsADwarf

    global showPlanetAtmospheresCheckBox
    global showPlanetAtmospheres

    global showMoonsCheckBox
    global showMoons

    global showStarsCheckBox
    global showStars
    global starNames

    # text that gets displayed:
    global moonNameMessage
    global gases
    global starNamesMessage
    global planetIsADwarf
    global planetIsAnExoPlanet

    def initializeReportContents(self):
        try:
            if (self.initializedForMultiDisplay == False):
                self.insertionManager.reportGenerator.refreshReportGenerator()

            allPossibleAttributeNames = [
                "Planet Mass (Earth = 1): ",
                "Planet Gravity (Earth = 1): ",
                "Planet Radius (Earth = 1): ",
                "Planet Distance from Earth (ly): ",
                "Planet Equilibrium Temperature (K): ",
                "Planet ESI: ",
                "Planet Rotation Period (Earth Days): ",
                "Planet Orbital Period (Earth Years): ",
                "Planet Escape Velocity (km/s): ",
                "Image Directory: ",
                "Description Located At: ",
                "Moons: ",
                "Star Planet Orbits: ",
                "Atmosphere: ",
                "isDwarf: ",
                "isExoPlanet: "]
            recordToReport = []
            attributeNames = []
            exclusionFilters = []
            exclusionFilters.append(self.showMass.get())
            exclusionFilters.append(self.showGravity.get())
            exclusionFilters.append(self.showRadius.get())
            exclusionFilters.append(self.showDistanceFromEarth.get())
            exclusionFilters.append(self.showTemperature.get())
            exclusionFilters.append(self.showESI.get())
            exclusionFilters.append(self.showRotationalPeriod.get())
            exclusionFilters.append(self.showOrbitalPeriod.get())
            exclusionFilters.append(self.showEscapeVelocity.get())
            exclusionFilters.append(self.showImage.get())
            exclusionFilters.append(self.showDescription.get())
            recordToReport.append(self.record[0])
            attributeNames.append("Planet Name: ")

            for i in range(0, len(exclusionFilters)):
                if (exclusionFilters[i] == 1):
                    recordToReport.append(str(self.record[i + 1]))
                    attributeNames.append(allPossibleAttributeNames[i])
                else:
                    print(allPossibleAttributeNames[i] + " will not be shown")

            if (self.showMoons.get() == 1):
                recordToReport.append(self.moonNameMessage.strip('\n'))
                attributeNames.append("Moons: ")

            if (self.showStars.get() == 1):
                recordToReport.append(self.starNamesMessage)
                attributeNames.append("Star Planet Orbits: ")

            if (self.showPlanetAtmospheres.get() == 1):
                recordToReport.append(self.gases)
                attributeNames.append("Atmosphere: ")

            if (self.showPlanetIsADwarf.get() == 1):
                recordToReport.append(self.planetIsADwarf)
                attributeNames.append("isDwarf: ")

            if (self.showPlanetIsAnExoPlanet.get() == 1):
                recordToReport.append(self.planetIsAnExoPlanet)
                attributeNames.append("isExoPlanet: ")

            imageURL = None
            if (self.showImage.get() == 1):
                imageURL = self.record[10]

            # generate report, but do not save it yet:
            self.insertionManager.reportGenerator.generateReports(recordToReport, imageURL, attributeNames)
        except:
            return

    def populateFields(self):

        # run the query, get the record, display results:
        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        query = '''

                        SELECT * 
                        FROM Planets 
                        WHERE Name = %s;

                    '''
        cursor.execute(query, [self.selectedItemToSearchFor.get()])
        record = cursor.fetchone()

        self.record = []
        for attribute in record:
            self.record.append(attribute)

        query = '''

                                    SELECT COUNT(*)
                                    FROM PlanetsInHabitZone
                                    WHERE Name = %s;

                                '''

        cursor.execute(query, [self.selectedItemToSearchFor.get()])
        record = cursor.fetchone()
        if (record != None):
            if (record[0] == 0):
                self.planetIsInTheHabitZoneResultsLabel.configure(text="no")
            else:
                self.planetIsInTheHabitZoneResultsLabel.configure(text="yes")
        else:
            self.planetIsInTheHabitZoneResultsLabel.configure(text="no")

        query = '''

                        SELECT COUNT(*)
                        FROM DwarfPlanets 
                        WHERE Name = %s;

                    '''
        cursor.execute(query, [self.selectedItemToSearchFor.get()])
        record = cursor.fetchone()
        self.planetIsADwarf = "no"
        if (record != None):
            if (record[0] == 0):
                self.planetIsADwarfResultsLabel.configure(text="no")
            else:
                self.planetIsADwarfResultsLabel.configure(text="yes")
                self.planetIsADwarf = "yes"
        else:
            self.planetIsADwarfResultsLabel.configure(text="no")

        query = '''

                        SELECT Gas
                        FROM PlanetAtmospheres 
                        WHERE Name = %s;

                    '''
        cursor.execute(query, [self.selectedItemToSearchFor.get()])
        records = cursor.fetchall()

        # determine if planet is an exoplanet:
        query = '''

                        SELECT COUNT(*) 
                        FROM ExoPlanets
                        WHERE PlanetName = %s;

                    '''
        cursor.execute(query, [self.selectedItemToSearchFor.get()])
        record = cursor.fetchone()
        self.planetIsAnExoPlanet = "no"
        if (record != None):
            if (record[0] == 0):
                self.planetIsAnExoPlanetResultsLabel.configure(text="no")
            else:
                self.planetIsAnExoPlanetResultsLabel.configure(text="yes")
                self.planetIsAnExoPlanet = "yes"
        else:
            self.planetIsAnExoPlanetResultsLabel.configure(text="no")

        self.atmosphericGases = []
        for gas in records:
            self.atmosphericGases.append(gas[0])

        self.gases = "["
        for gas in self.atmosphericGases:
            self.gases += " " + gas + " "
        self.gases += "]"
        self.planetAtmosphereResultsLabel.configure(text=self.gases)

        query = '''
        
            SELECT Moons.Name
            FROM Moons INNER JOIN Planets
                ON Moons.PlanetItOrbits = Planets.Name
            WHERE Planets.Name = %s;
        
        '''
        cursor.execute(query, [self.selectedItemToSearchFor.get()])
        moonNameRecord = cursor.fetchall()
        self.moonNameMessage = ""
        index = 0
        if (moonNameRecord != None):
            for moonName in moonNameRecord:
                self.moonNameMessage += str(moonName[0])
                if ((len(moonNameRecord) > 1) and ((index + 1) < len(moonNameRecord))):
                    self.moonNameMessage += "\n"
                index += 1
        else:
            self.moonNameMessage = "None"

        # get star information for this planet:
        query = '''
        
                SELECT StarName
                FROM Planets INNER JOIN StarsPlanetsOrbit
                    ON PlanetName = Name
                WHERE Name = %s;
        
        '''
        cursor.execute(query, [self.selectedItemToSearchFor.get()])

        starNameRecord = cursor.fetchall()
        self.starNamesMessage = ""

        index = 0
        if (starNameRecord != None):
            for starName in starNameRecord:
                self.starNamesMessage += str(starName[0])
                if ((len(starNameRecord) > 1) and ((index + 1) < len(starNameRecord))):
                    self.starNamesMessage += "\n"
                index += 1
        else:
            self.starNamesMessage = "Unknown"

        database.close()

        self.starsPlanetOrbitsResultLabel.configure(text=self.starNamesMessage)
        self.numberOfMoonsResultLabel.configure(text=self.moonNameMessage)
        self.planetNameResultLabel.configure(text=self.record[0])
        self.planetMassResultLabel.configure(text=str(self.record[1]))
        self.planetGravityResultLabel.configure(text=str(self.record[2]))
        self.planetRadiusResultsLabel.configure(text=str(self.record[3]))
        self.planetDistanceFromEarthResultsLabel.configure(text=str(self.record[4]))
        self.planetEquilibriumTemperatureResultsLabel.configure(text=str(self.record[5]))
        self.planetESIResultsLabel.configure(text=str(self.record[6]))
        self.planetRotationalPeriodResultsLabel.configure(text=str(self.record[7]))
        self.planetOrbitalPeriodResultsLabel.configure(text=str(self.record[8]))
        self.planetEscapeVelocityResultsLabel.configure(text=str(self.record[9]))
        self.planetImageDisplayer.openImage(False, self.record[10])
        if (self.showImage.get() == 0):
            self.planetImageDisplayer.hideAllImageUI()

        self.planetDescriptionDisplayer.loadDescriptionWithoutPromptingUser(self.record[11])
        if (self.showDescription.get() == 0):
            self.planetDescriptionDisplayer.hideDescriptionUI()

        self.initializeReportContents()

        if (self.confirmButton != None):
            self.confirmButton.configure(state=ACTIVE)

    def resetAllUI(self):
        BaseSingleSearchManager.resetAllUI(self)

        self.planetDescriptionDisplayer.resetDescriptionUI(16, 0)
        self.planetImageDisplayer.resetImageUI()

        self.toggleMass()
        self.toggleESI()
        self.toggleStars()
        self.toggleExo()
        self.toggleDwarf()
        self.toggleMoons()
        self.togglePlanetAtmospheres()
        self.toggleInHabitZone()
        self.toggleDescription()
        self.toggleImage()
        self.toggleEscapeVelocity()
        self.toggleOrbitalPeriod()
        self.toggleRotationalPeriod()
        self.toggleTemperature()
        self.toggleDistance()
        self.toggleRadius()
        self.toggleGravity()

        self.atmosphericGases.clear()

    def toggleMass(self):
        if (self.showMass.get() == 0):
            self.planetMassLabel.grid_forget()
            self.planetMassResultLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.planetMassLabel, self.planetMassResultLabel, 1)
        self.initializeReportContents()

    def toggleGravity(self):
        if (self.showGravity.get() == 0):
            self.planetGravityLabel.grid_forget()
            self.planetGravityResultLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.planetGravityLabel, self.planetGravityResultLabel, 2)
        self.initializeReportContents()

    def toggleRadius(self):
        if (self.showRadius.get() == 0):
            self.planetRadiusLabel.grid_forget()
            self.planetRadiusResultsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.planetRadiusLabel, self.planetRadiusResultsLabel, 3)
        self.initializeReportContents()

    def toggleDistance(self):
        if (self.showDistanceFromEarth.get() == 0):
            self.planetDistanceFromEarthLabel.grid_forget()
            self.planetDistanceFromEarthResultsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.planetDistanceFromEarthLabel, self.planetDistanceFromEarthResultsLabel, 4)
        self.initializeReportContents()

    def toggleTemperature(self):
        if (self.showTemperature.get() == 0):
            self.planetEquilibriumTemperatureLabel.grid_forget()
            self.planetEquilibriumTemperatureResultsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.planetEquilibriumTemperatureLabel,
                                     self.planetEquilibriumTemperatureResultsLabel,
                                     5)
        self.initializeReportContents()

    def toggleESI(self):
        if (self.showESI.get() == 0):
            self.planetESILabel.grid_forget()
            self.planetESIResultsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.planetESILabel, self.planetESIResultsLabel, 6)
        self.initializeReportContents()

    def toggleRotationalPeriod(self):
        if (self.showRotationalPeriod.get() == 0):
            self.planetRotationalPeriodLabel.grid_forget()
            self.planetRotationalPeriodResultsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.planetRotationalPeriodLabel, self.planetRotationalPeriodResultsLabel, 7)
        self.initializeReportContents()

    def toggleOrbitalPeriod(self):
        if (self.showOrbitalPeriod.get() == 0):
            self.planetOrbitalPeriodLabel.grid_forget()
            self.planetOrbitalPeriodResultsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.planetOrbitalPeriodLabel, self.planetOrbitalPeriodResultsLabel, 8)
        self.initializeReportContents()

    def toggleEscapeVelocity(self):
        if (self.showEscapeVelocity.get() == 0):
            self.planetEscapeVelocityLabel.grid_forget()
            self.planetEscapeVelocityResultsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.planetEscapeVelocityLabel, self.planetEscapeVelocityResultsLabel, 9)
        self.initializeReportContents()

    def toggleImage(self):
        if (self.showImage.get() == 0):
            self.planetImageDisplayer.hideAllImageUI()
        else:
            self.planetImageDisplayer.showAllImageUI()
        self.initializeReportContents()

    def toggleDescription(self):
        if (self.showDescription.get() == 0):
            self.planetDescriptionDisplayer.hideDescriptionUI()
        else:
            self.planetDescriptionDisplayer.showAllDescriptionUI()
        self.initializeReportContents()

    def toggleDwarf(self):
        if (self.showPlanetIsADwarf.get() == 0):
            self.planetIsADwarfLabel.grid_forget()
            self.planetIsADwarfResultsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.planetIsADwarfLabel, self.planetIsADwarfResultsLabel, 10)
        self.initializeReportContents()

    def toggleExo(self):
        if (self.showPlanetIsAnExoPlanet.get() == 0):
            self.planetIsAnExoPlanetLabel.grid_forget()
            self.planetIsAnExoPlanetResultsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.planetIsAnExoPlanetLabel, self.planetIsAnExoPlanetResultsLabel, 12)
        self.initializeReportContents()

    def toggleInHabitZone(self):
        if (self.showPlanetIsInHabitZone.get() == 0):
            self.planetIsInTheHabitZoneLabel.grid_forget()
            self.planetIsInTheHabitZoneResultsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.planetIsInTheHabitZoneLabel, self.planetIsInTheHabitZoneResultsLabel, 11)
        self.initializeReportContents()

    def togglePlanetAtmospheres(self):
        if (self.showPlanetAtmospheres.get() == 0):
            self.planetAtmospheresLabel.grid_forget()
            self.planetAtmosphereResultsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.planetAtmospheresLabel, self.planetAtmosphereResultsLabel, 18)
        self.initializeReportContents()

    def toggleMoons(self):
        if (self.showMoons.get() == 0):
            self.numberOfMoonsLabel.grid_forget()
            self.numberOfMoonsResultLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.numberOfMoonsLabel, self.numberOfMoonsResultLabel, 19)
        self.initializeReportContents()

    def toggleStars(self):
        if (self.showStars.get() == 0):
            self.starsPlanetOrbitsResultLabel.grid_forget()
            self.starsPlanetOrbitsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.starsPlanetOrbitsLabel, self.starsPlanetOrbitsResultLabel, 20)
        self.initializeReportContents()

    def initializeSingleSearchForDisplayOnMultiSearchFrame(self, frameToPutInsertionFrameOnto, row, column, nameToQueryFor, searchManager):

        BaseSingleSearchManager.initializeSingleSearchForDisplayOnMultiSearchFrame(self, frameToPutInsertionFrameOnto, row, column, nameToQueryFor, searchManager)

        self.showMass = IntVar()
        self.showMass.set(1)

        self.showGravity = IntVar()
        self.showGravity.set(1)

        self.showRadius = IntVar()
        self.showRadius.set(1)

        self.showDistanceFromEarth = IntVar()
        self.showDistanceFromEarth.set(1)

        self.showTemperature = IntVar()
        self.showTemperature.set(1)

        self.showESI = IntVar()
        self.showESI.set(1)

        self.showRotationalPeriod = IntVar()
        self.showRotationalPeriod.set(1)

        self.showOrbitalPeriod = IntVar()
        self.showOrbitalPeriod.set(1)

        self.showEscapeVelocity = IntVar()
        self.showEscapeVelocity.set(1)

        self.showImage = IntVar()
        self.showImage.set(1)

        self.showDescription = IntVar()
        self.showDescription.set(1)

        self.showPlanetIsADwarf = IntVar()
        self.showPlanetIsADwarf.set(1)

        self.showPlanetIsAnExoPlanet = IntVar()
        self.showPlanetIsAnExoPlanet.set(1)

        self.showPlanetIsInHabitZone = IntVar()
        self.showPlanetIsInHabitZone.set(1)

        self.showPlanetAtmospheres = IntVar()
        self.showPlanetAtmospheres.set(1)

        self.showMoons = IntVar()
        self.showMoons.set(1)

        self.showStars = IntVar()
        self.showStars.set(1)

        self.populateFields()

    def initializeAllDataDisplayerUI(self):
        self.planetNameLabel = Label(self.resultsFrame, text="Planet Name: ")
        self.planetNameResultLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.planetNameLabel, self.planetNameResultLabel, 0)

        self.planetMassLabel = Label(self.resultsFrame, text="Planet mass (Earth =1): ")
        self.planetMassResultLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.planetMassLabel, self.planetMassResultLabel, 1)

        self.planetGravityLabel = Label(self.resultsFrame, text="Planet gravity (Earth = 1): ")
        self.planetGravityResultLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.planetGravityLabel, self.planetGravityResultLabel, 2)

        self.planetRadiusLabel = Label(self.resultsFrame, text="Planet Radius (Earth = 1): ")
        self.planetRadiusResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.planetRadiusLabel, self.planetRadiusResultsLabel, 3)

        self.planetDistanceFromEarthLabel = Label(self.resultsFrame, text="Planet distance from Earth (ly): ")
        self.planetDistanceFromEarthResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.planetDistanceFromEarthLabel, self.planetDistanceFromEarthResultsLabel, 4)

        self.planetEquilibriumTemperatureLabel = Label(self.resultsFrame, text="Planet equilibrium temperature (K): ")
        self.planetEquilibriumTemperatureResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.planetEquilibriumTemperatureLabel, self.planetEquilibriumTemperatureResultsLabel,
                                 5)

        self.planetESILabel = Label(self.resultsFrame, text="Planet ESI: ")
        self.planetESIResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.planetESILabel, self.planetESIResultsLabel, 6)

        self.planetRotationalPeriodLabel = Label(self.resultsFrame, text="Planet rotational period (In Earth Days): ")
        self.planetRotationalPeriodResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.planetRotationalPeriodLabel, self.planetRotationalPeriodResultsLabel, 7)

        self.planetOrbitalPeriodLabel = Label(self.resultsFrame, text="Planet orbital period (Earth years): ")
        self.planetOrbitalPeriodResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.planetOrbitalPeriodLabel, self.planetOrbitalPeriodResultsLabel, 8)

        self.planetEscapeVelocityLabel = Label(self.resultsFrame, text="Planet escape velocity (km/s): ")
        self.planetEscapeVelocityResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.planetEscapeVelocityLabel, self.planetEscapeVelocityResultsLabel, 9)

        self.planetIsADwarfLabel = Label(self.resultsFrame, text="Planet is a dwarf: ")
        self.planetIsADwarfResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.planetIsADwarfLabel, self.planetIsADwarfResultsLabel, 10)

        self.planetIsInTheHabitZoneLabel = Label(self.resultsFrame, text="Planet is in the habit zone: ")
        self.planetIsInTheHabitZoneResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.planetIsInTheHabitZoneLabel, self.planetIsInTheHabitZoneResultsLabel, 11)

        self.planetIsAnExoPlanetLabel = Label(self.resultsFrame, text="Planet is an exo planet: ")
        self.planetIsAnExoPlanetResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.planetIsAnExoPlanetLabel, self.planetIsAnExoPlanetResultsLabel, 12)

        self.planetImageDisplayer = ImageDisplayerManager()
        self.planetImageDisplayer.initializeImageDisplayer(14, 0, 2, self.resultsFrame, None, False)

        self.planetDescriptionDisplayer = TextBoxManager()
        self.planetDescriptionDisplayer.initializeDescriptionBoxForReadingOnlyAndNotLoading(self.resultsFrame, 16, 0,
                                                                                            17, 0)

        self.planetAtmospheresLabel = Label(self.resultsFrame, text="Planet Atmosphere: ")
        self.planetAtmosphereResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.planetAtmospheresLabel, self.planetAtmosphereResultsLabel, 18)

        self.numberOfMoonsLabel = Label(self.resultsFrame, text="Moon Name or names: ")
        self.numberOfMoonsResultLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.numberOfMoonsLabel, self.numberOfMoonsResultLabel, 19)

        self.starsPlanetOrbitsLabel = Label(self.resultsFrame, text="Star or stars planet orbits: ")
        self.starsPlanetOrbitsResultLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.starsPlanetOrbitsLabel, self.starsPlanetOrbitsResultLabel, 20)

    def manageSinglePlanetarySearch(self, windowToPutFrameOnto, mainSearchManager):

        self.defaultReportName = "SinglePlanetarySearchReport"
        self.successMessageRow = 14

        dropdownSearchQuery = '''
        
            SELECT Name
            FROM Planets;
        
        '''
        labelText = "Select planet to search for: "
        searchTitle = "Single Planet Search"
        self.numberOfMoons = 0

        self.manageSingleSearch(dropdownSearchQuery, windowToPutFrameOnto, mainSearchManager, searchTitle, labelText)

        self.showMass = IntVar()
        self.showMass.set(1)
        self.showMassCheckBox = Checkbutton(self.insertionFrame, text="Show mass", variable=self.showMass, onvalue=1, offvalue=0, command=self.toggleMass)
        self.showMassCheckBox.grid(row=3, column=0)

        self.showGravity = IntVar()
        self.showGravity.set(1)
        self.showGravityCheckBox = Checkbutton(self.insertionFrame, text="Show gravity", variable=self.showGravity, onvalue=1, offvalue=0, command=self.toggleGravity)
        self.showGravityCheckBox.grid(row=3, column=1)

        self.showRadius = IntVar()
        self.showRadius.set(1)
        self.showRadiusCheckBox = Checkbutton(self.insertionFrame, text="Show radius", variable=self.showRadius, onvalue=1,
                                            offvalue=0, command=self.toggleRadius)
        self.showRadiusCheckBox.grid(row=4, column=0)

        self.showDistanceFromEarth = IntVar()
        self.showDistanceFromEarth.set(1)
        self.showDistanceFromEarthCheckBox = Checkbutton(self.insertionFrame, text="Show distance", variable=self.showDistanceFromEarth, onvalue=1,
                                            offvalue=0, command=self.toggleDistance)
        self.showDistanceFromEarthCheckBox.grid(row=4, column=1)

        self.showTemperature = IntVar()
        self.showTemperature.set(1)
        self.showEquilibriumTemperatureCheckBox = Checkbutton(self.insertionFrame, text="Show Temperature", variable=self.showTemperature, onvalue=1,
                                            offvalue=0, command=self.toggleTemperature)
        self.showEquilibriumTemperatureCheckBox.grid(row=5, column=0)

        self.showESI = IntVar()
        self.showESI.set(1)
        self.showESICheckBox = Checkbutton(self.insertionFrame, text="Show ESI", variable=self.showESI, onvalue=1,
                                            offvalue=0, command=self.toggleESI)
        self.showESICheckBox.grid(row=5, column=1)

        self.showRotationalPeriod = IntVar()
        self.showRotationalPeriod.set(1)
        self.showRotationalPeriodCheckBox = Checkbutton(self.insertionFrame, text="Show rotational period", variable=self.showRotationalPeriod, onvalue=1,
                                            offvalue=0, command=self.toggleRotationalPeriod)
        self.showRotationalPeriodCheckBox.grid(row=6, column=0)

        self.showOrbitalPeriod = IntVar()
        self.showOrbitalPeriod.set(1)
        self.showOrbitalPeriodCheckBox = Checkbutton(self.insertionFrame, text="Show Orbital Period", variable=self.showOrbitalPeriod, onvalue=1,
                                            offvalue=0, command=self.toggleOrbitalPeriod)
        self.showOrbitalPeriodCheckBox.grid(row=6, column=1)

        self.showEscapeVelocity = IntVar()
        self.showEscapeVelocity.set(1)
        self.showEscapeVelocityCheckBox = Checkbutton(self.insertionFrame, text="Show escape velocity", variable=self.showEscapeVelocity, onvalue=1,
                                            offvalue=0, command=self.toggleEscapeVelocity)
        self.showEscapeVelocityCheckBox.grid(row=7, column=0)

        self.showImage = IntVar()
        self.showImage.set(1)
        self.showImageCheckBox = Checkbutton(self.insertionFrame, text="Show Image", variable=self.showImage, onvalue=1,
                                            offvalue=0, command=self.toggleImage)
        self.showImageCheckBox.grid(row=7, column=1)

        self.showDescription = IntVar()
        self.showDescription.set(1)
        self.showDescriptionCheckBox = Checkbutton(self.insertionFrame, text="Show Description", variable=self.showDescription, onvalue=1,
                                            offvalue=0, command=self.toggleDescription)
        self.showDescriptionCheckBox.grid(row=8, column=0)


        self.showPlanetIsADwarf = IntVar()
        self.showPlanetIsADwarf.set(1)
        self.showPlanetIsDwarfPlanetCheckBox = Checkbutton(self.insertionFrame, text="Show Planet is a Dwarf",
                                                   variable=self.showPlanetIsADwarf, onvalue=1,
                                                   offvalue=0, command=self.toggleDwarf)
        self.showPlanetIsDwarfPlanetCheckBox.grid(row=8, column=1)

        self.showPlanetIsAnExoPlanet = IntVar()
        self.showPlanetIsAnExoPlanet.set(1)
        self.showPlanetIsAnExoPlanetCheckBox = Checkbutton(self.insertionFrame, text="Show Planet is an exo planet",
                                                   variable=self.showPlanetIsAnExoPlanet, onvalue=1,
                                                   offvalue=0, command=self.toggleExo)
        self.showPlanetIsAnExoPlanetCheckBox.grid(row=9, column=0)

        self.showPlanetIsInHabitZone = IntVar()
        self.showPlanetIsInHabitZone.set(1)
        self.showPlanetIsInHabitZoneCheckBox = Checkbutton(self.insertionFrame, text="Show Planet is in habit zone",
                                                           variable=self.showPlanetIsInHabitZone, onvalue=1,
                                                           offvalue=0, command=self.toggleInHabitZone)
        self.showPlanetIsInHabitZoneCheckBox.grid(row=9, column=1)

        self.showPlanetAtmospheres = IntVar()
        self.showPlanetAtmospheres.set(1)
        self.showPlanetAtmospheresCheckBox = Checkbutton(self.insertionFrame, text="Show Planet Atmospheres Check box",
                                                           variable=self.showPlanetAtmospheres, onvalue=1,
                                                           offvalue=0, command=self.togglePlanetAtmospheres)
        self.showPlanetAtmospheresCheckBox.grid(row=10, column=0)

        self.showMoons = IntVar()
        self.showMoons.set(1)
        self.showMoonsCheckBox = Checkbutton(self.insertionFrame, text="Show Moons: ",
                                                           variable=self.showMoons, onvalue=1,
                                                           offvalue=0, command=self.toggleMoons)
        self.showMoonsCheckBox.grid(row=10, column=1)

        self.showStars = IntVar()
        self.showStars.set(1)
        self.showStarsCheckBox = Checkbutton(self.insertionFrame, text="Show Stars: ",
                                                           variable=self.showStars, onvalue=1,
                                                           offvalue=0, command=self.toggleStars)
        self.showStarsCheckBox.grid(row=11, column=0, columnspan=2)

        self.allResultsLabels = []
        self.allResultsLabels.append(self.planetNameResultLabel)
        self.allResultsLabels.append(self.planetMassResultLabel)
        self.allResultsLabels.append(self.planetGravityResultLabel)
        self.allResultsLabels.append(self.planetRadiusResultsLabel)
        self.allResultsLabels.append(self.planetDistanceFromEarthResultsLabel)
        self.allResultsLabels.append(self.planetEquilibriumTemperatureResultsLabel)
        self.allResultsLabels.append(self.planetESIResultsLabel)
        self.allResultsLabels.append(self.planetRotationalPeriodResultsLabel)
        self.allResultsLabels.append(self.planetOrbitalPeriodResultsLabel)
        self.allResultsLabels.append(self.planetEscapeVelocityResultsLabel)
        self.allResultsLabels.append(self.planetAtmosphereResultsLabel)
        self.allResultsLabels.append(self.starsPlanetOrbitsResultLabel)
        self.allResultsLabels.append(self.planetIsInTheHabitZoneResultsLabel)
        self.allResultsLabels.append(self.planetIsADwarfResultsLabel)
        self.allResultsLabels.append(self.planetIsAnExoPlanetResultsLabel)
        self.allResultsLabels.append(self.numberOfMoonsResultLabel)

        self.allCheckBoxes = []
        self.allCheckBoxes.append(self.showMassCheckBox)
        self.allCheckBoxes.append(self.showGravityCheckBox)
        self.allCheckBoxes.append(self.showRadiusCheckBox)
        self.allCheckBoxes.append(self.showDistanceFromEarthCheckBox)
        self.allCheckBoxes.append(self.showEquilibriumTemperatureCheckBox)
        self.allCheckBoxes.append(self.showESICheckBox)
        self.allCheckBoxes.append(self.showRotationalPeriodCheckBox)
        self.allCheckBoxes.append(self.showOrbitalPeriodCheckBox)
        self.allCheckBoxes.append(self.showEscapeVelocityCheckBox)
        self.allCheckBoxes.append(self.showStarsCheckBox)
        self.allCheckBoxes.append(self.showMoonsCheckBox)
        self.allCheckBoxes.append(self.showPlanetIsInHabitZoneCheckBox)
        self.allCheckBoxes.append(self.showPlanetAtmospheresCheckBox)
        self.allCheckBoxes.append(self.showPlanetIsAnExoPlanetCheckBox)
        self.allCheckBoxes.append(self.showDescriptionCheckBox)
        self.allCheckBoxes.append(self.showImageCheckBox)

        self.confirmButton.grid(row=12, column=0, sticky=W+E)
        self.cancelButton.grid(row=12, column=1, sticky=W+E)

        Label(self.insertionFrame, text="Name to save report as: ").grid(row=13, column=0)
        self.reportNameInputBox.grid(row=13, column=1, sticky=W+E)