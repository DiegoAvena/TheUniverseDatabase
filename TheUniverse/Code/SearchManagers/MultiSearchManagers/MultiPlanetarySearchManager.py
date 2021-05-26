'''
----SUMMARY----
Allows the user to search
for multiple planets with various
filters and produce
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
BaseMultiSearchManager:

Used to obtain base functionality for a more specific multi search option,
since this is a specific option for searching for multiple planets

tkinter - Used for all the UI

SinglePlanetarySearchManager:

This is used for the displaying of multiple
planet records that get turned up after a search is
confirmed.

'''

from Code.SearchManagers.BaseSearchManagers.BaseMultiSearchManager import BaseMultiSearchManager
from Code.SearchManagers.SingleSearchManagers.SinglePlanetarySearchManager import SinglePlanetarySearchManager
from tkinter import *

class MultiPlantarySearchManager(BaseMultiSearchManager):

    # attribute filters
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

    # criteria filters
    global onlyShowExoPlanetsCheckBox
    global onlyShowExoPlanets

    global onlyShowPlanetsInTheHabitZoneCheckBox
    global onlyShowPlanetsInTheHabitZone

    global onlyShowDwarfPlanetsCheckBox
    global onlyShowDwarfPlanets

    # sorting filters
    global sortByESIDescendingCheckbox
    global sortByESI

    global sortByEscapeVelocityDescendingCheckBox
    global sortByEscapeVelocity

    global sortBySizeDescendingCheckBox
    global sortBySize

    global sortByGrabityDescendingCheckBox
    global sortByGravity

    global sortByTemperatureDescendingCheckBox
    global sortByTemperature

    global sortByNumberOfMoonsDescendingCheckBox
    global sortByNumberOfMoons

    global sortByGreatestDistanceFromEarthDescendingCheckBox
    global sortByDistanceFromEarth

    global sortByPlanetRotationalPeriodDescendingCheckBox
    global sortBYPlanetRotationalPeriod

    global sortByPlanetOrbitalPeriodDescendingCheckBox
    global sortByPlanetOrbitalPeriod

    global sortByStarCheckBox
    global sortByStar

    def determineIfThereIsASortingClause(self):

        sortingClause = ""

        if (self.sortByESI.get() == 1):
            sortingClause += " ORDER BY ESI DESC "

        if (self.sortByEscapeVelocity.get() == 1):
            sortingClause += " ORDER BY EscapeVelocity DESC "

        if (self.sortBySize.get() == 1):
            sortingClause += " ORDER BY Radius DESC "

        if (self.sortByNumberOfMoons.get() == 1):
            sortingClause += " ORDER BY MoonCount DESC"

        if (self.sortByGravity.get() == 1):
            sortingClause += " ORDER BY Gravity DESC "

        if (self.sortByTemperature.get() == 1):
            sortingClause += " ORDER BY EquilibriumTemperature DESC "

        if (self.sortByDistanceFromEarth.get() == 1):
            sortingClause += " ORDER BY DistanceFromEarth DESC "

        if (self.sortBYPlanetRotationalPeriod.get() == 1):
            sortingClause += " ORDER BY RotationPeriod DESC "

        if (self.sortByPlanetOrbitalPeriod.get() == 1):
            sortingClause += " ORDER BY OrbitalPeriod DESC "

        if (self.sortByStar.get() == 1):
            sortingClause += " ORDER BY StarName"
        return sortingClause

    def performSearch(self):

        BaseMultiSearchManager.performSearch(self)

        query = '''
        
            SELECT Planets.Name
            FROM Planets
        
        '''

        if (self.sortByNumberOfMoons.get() == 1):
            query = '''
            
                SELECT Planets.Name, COUNT(Moons.Name) AS MoonCount
                FROM Moons, Planets 
            
            '''
        elif (self.sortByStar.get() == 1):
            query = '''
            
                SELECT Planets.Name, StarsPlanetsOrbit.StarName 
                FROM Planets 
            
            '''

        if (self.sortByStar.get() == 1):
            query += " INNER JOIN StarsPlanetsOrbit ON Planets.Name = StarsPlanetsOrbit.PlanetName "

        whereClause = ""
        if (self.onlyShowExoPlanets.get() == 1):
            if (self.onlyShowPlanetsInTheHabitZone.get() == 1):
                query += " INNER JOIN ExoPlanetsInHabitZone ON Planets.Name = ExoPlanetsInHabitZone.PlanetName "
                if (self.onlyShowDwarfPlanets.get() == 1):
                    query += " INNER JOIN DwarfPlanets ON ExoPlanetsInHabitZone.PlanetName = DwarfPlanets.Name "
            else:
                query += " INNER JOIN ExoPlanets ON Planets.name = ExoPlanets.PlanetName "
                if (self.onlyShowDwarfPlanets.get() == 1):
                    query += " INNER JOIN DwarfPlanets ON ExoPlanets.PlanetName = DwarfPlanets.Name "

        else:
            if (self.onlyShowPlanetsInTheHabitZone.get() == 1):
                query += " INNER JOIN PlanetsInHabitZone ON Planets.Name = PlanetsInHabitZone.Name "

            if (self.onlyShowDwarfPlanets.get() == 1):
                query += " INNER JOIN DwarfPlanets ON Planets.Name = DwarfPlanets.Name "

        if (self.sortByNumberOfMoons.get() == 1):
            if (len(whereClause) > 0):
                whereClause += " AND Planets.Name = Moons.PlanetItOrbits "
            else:
                whereClause += " WHERE Planets.Name = Moons.PlanetItOrbits "
            query += whereClause + " GROUP BY Planets.Name " + self.determineIfThereIsASortingClause() + ";"
        else:
            query += whereClause + self.determineIfThereIsASortingClause() + ";"

        print("FINAL QUERY THAT WILL RUN: " +"\n"+query)
        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        cursor.execute(query)

        planetNames = []
        starNames = []
        records = cursor.fetchall()
        database.close()

        for record in records:
            planetNames.append(record[0])
            if (self.sortByStar.get() == 1):
                starNames.append(record[1])

        currentStarName = ""
        currentFrame = self.resultsFrame
        currentFrameColumn = 0
        for i in range(0, len(planetNames)):
            if (len(starNames) > 0):
                if (starNames[i] != currentStarName):
                    currentStarName = starNames[i]
                    currentFrame = LabelFrame(self.resultsFrame, text=currentStarName)
                    currentFrame.grid(row=currentFrameColumn, column=0, pady=20, sticky=W)
                    currentFrameColumn += 1
                    self.anySortingFramesThatSpawned.append(currentFrame)


            planetDisplayer = SinglePlanetarySearchManager(self.localMySqlInstancePassword)
            planetDisplayer.initializeSingleSearchForDisplayOnMultiSearchFrame(currentFrame, 0, i, planetNames[i], self.insertionManager)
            self.recordDisplayersSpawnedInSoFar.append(planetDisplayer)

        self.toggleMass()
        self.toggleESI()
        self.toggleStars()
        self.toggleGravity()
        self.togglePlanetAtmospheres()
        self.toggleRadius()
        self.toggleDistance()
        self.toggleTemperature()
        self.toggleRotationalPeriod()
        self.toggleOrbitalPeriod()
        self.toggleEscapeVelocity()
        self.toggleImage()
        self.toggleDescription()
        self.toggleInHabitZone()
        self.toggleMoons()
        self.toggleDwarf()
        self.toggleExo()

    def toggleMass(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for planet in self.recordDisplayersSpawnedInSoFar:
            planet.showMass.set(self.showMass.get())
            planet.toggleMass()

    def toggleGravity(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for planet in self.recordDisplayersSpawnedInSoFar:
            planet.showGravity.set(self.showGravity.get())
            planet.toggleGravity()

    def toggleRadius(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for planet in self.recordDisplayersSpawnedInSoFar:
            planet.showRadius.set(self.showRadius.get())
            planet.toggleRadius()

    def toggleDistance(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for planet in self.recordDisplayersSpawnedInSoFar:
            planet.showDistanceFromEarth.set(self.showDistanceFromEarth.get())
            planet.toggleDistance()

    def toggleTemperature(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for planet in self.recordDisplayersSpawnedInSoFar:
            planet.showTemperature.set(self.showTemperature.get())
            planet.toggleTemperature()

    def toggleESI(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for planet in self.recordDisplayersSpawnedInSoFar:
            planet.showESI.set(self.showESI.get())
            planet.toggleESI()

    def toggleRotationalPeriod(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for planet in self.recordDisplayersSpawnedInSoFar:
            planet.showRotationalPeriod.set(self.showRotationalPeriod.get())
            planet.toggleRotationalPeriod()

    def toggleOrbitalPeriod(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for planet in self.recordDisplayersSpawnedInSoFar:
            planet.showOrbitalPeriod.set(self.showOrbitalPeriod.get())
            planet.toggleOrbitalPeriod()

    def toggleEscapeVelocity(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for planet in self.recordDisplayersSpawnedInSoFar:
            planet.showEscapeVelocity.set(self.showEscapeVelocity.get())
            planet.toggleEscapeVelocity()

    def toggleImage(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for planet in self.recordDisplayersSpawnedInSoFar:
            planet.showImage.set(self.showImage.get())
            planet.toggleImage()

    def toggleDescription(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for planet in self.recordDisplayersSpawnedInSoFar:
            planet.showDescription.set(self.showDescription.get())
            planet.toggleDescription()

    def toggleDwarf(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for planet in self.recordDisplayersSpawnedInSoFar:
            planet.showPlanetIsADwarf.set(self.showPlanetIsADwarf.get())
            planet.toggleDwarf()

    def toggleExo(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for planet in self.recordDisplayersSpawnedInSoFar:
            planet.showPlanetIsAnExoPlanet.set(self.showPlanetIsAnExoPlanet.get())
            planet.toggleExo()

    def toggleInHabitZone(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for planet in self.recordDisplayersSpawnedInSoFar:
            planet.showPlanetIsInHabitZone.set(self.showPlanetIsInHabitZone.get())
            planet.toggleInHabitZone()

    def togglePlanetAtmospheres(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for planet in self.recordDisplayersSpawnedInSoFar:
            planet.showPlanetAtmospheres.set(self.showPlanetAtmospheres.get())
            planet.togglePlanetAtmospheres()

    def toggleMoons(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for planet in self.recordDisplayersSpawnedInSoFar:
            planet.showMoons.set(self.showMoons.get())
            planet.toggleMoons()

    def toggleStars(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for planet in self.recordDisplayersSpawnedInSoFar:
            planet.showStars.set(self.showStars.get())
            planet.toggleStars()

    def manageMultiSearch(self, windowToPutFrameOnto, mainSearchManager, searchTitle):
        BaseMultiSearchManager.manageMultiSearch(self, windowToPutFrameOnto, mainSearchManager, searchTitle)
        self.defaultReportName = "Multi-Planetary Search"
        planetNames = []
        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        query = '''
        
            SELECT Name 
            FROM Planets; 
        
        '''
        cursor.execute(query)
        records = cursor.fetchall()
        for name in records:
            planetNames.append(name[0])

        database.close()

        self.recordDisplayersSpawnedInSoFar = []
        for i in range(0, len(planetNames)):
            planetDisplayer = SinglePlanetarySearchManager(self.localMySqlInstancePassword)
            planetDisplayer.initializeSingleSearchForDisplayOnMultiSearchFrame(self.resultsFrame, 0, i, planetNames[i], self.insertionManager)
            self.recordDisplayersSpawnedInSoFar.append(planetDisplayer)

        # create the filter checkboxes:

        # criteria filters
        startingRow = 3
        Label(self.insertionFrame, text="-------------------EXCLUSION FILTERS-------------------").grid(row=startingRow, column=0, columnspan=4)

        startingRow += 1
        self.onlyShowExoPlanets = IntVar()
        self.onlyShowExoPlanetsCheckBox = Checkbutton(self.insertionFrame, text="Only show exo planets?", variable=self.onlyShowExoPlanets, onvalue=1, offvalue=0)
        self.onlyShowExoPlanetsCheckBox.grid(row=startingRow, column=0)

        self.onlyShowPlanetsInTheHabitZone = IntVar()
        self.onlyShowPlanetsInTheHabitZoneCheckBox = Checkbutton(self.insertionFrame, text="Only show planets in the habit zone?", variable=self.onlyShowPlanetsInTheHabitZone, onvalue=1, offvalue=0)
        self.onlyShowPlanetsInTheHabitZoneCheckBox.grid(row=startingRow, column=1)

        self.onlyShowDwarfPlanets = IntVar()
        self.onlyShowDwarfPlanetsCheckBox = Checkbutton(self.insertionFrame, text="Only show dwarf planets?", variable=self.onlyShowDwarfPlanets, onvalue=1, offvalue=0)
        self.onlyShowDwarfPlanetsCheckBox.grid(row=startingRow, column=2, columnspan=2)

        # sorting filters
        startingRow += 1
        Label(self.insertionFrame, text="-------------------SORTING FILTERS-------------------").grid(row=startingRow, column=0, columnspan=4)

        startingRow += 1
        self.sortByESI = IntVar()
        self.sortByESIDescendingCheckbox = Checkbutton(self.insertionFrame, text="Sort by ESI Descending? ", variable=self.sortByESI, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(0))
        self.sortByESIDescendingCheckbox.grid(row=startingRow, column=0)

        self.sortByEscapeVelocity = IntVar()
        self.sortByEscapeVelocityDescendingCheckBox = Checkbutton(self.insertionFrame, text="Sort by Escape Velocity Descending? ", variable=self.sortByEscapeVelocity, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(1))
        self.sortByEscapeVelocityDescendingCheckBox.grid(row=startingRow, column=1)

        # startingRow += 1
        self.sortBySize = IntVar()
        self.sortBySizeDescendingCheckBox = Checkbutton(self.insertionFrame, text="Sort by size descending? ", variable=self.sortBySize, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(2))
        self.sortBySizeDescendingCheckBox.grid(row=startingRow, column=2)

        self.sortByGravity = IntVar()
        self.sortByGrabityDescendingCheckBox = Checkbutton(self.insertionFrame, text="Sort by gravity descending? ", variable=self.sortByGravity, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(3))
        self.sortByGrabityDescendingCheckBox.grid(row=startingRow, column=3)

        startingRow += 1
        self.sortByTemperature = IntVar()
        self.sortByTemperatureDescendingCheckBox = Checkbutton(self.insertionFrame, text="Sort by temperature descending? ", variable=self.sortByTemperature, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(4))
        self.sortByTemperatureDescendingCheckBox.grid(row=startingRow, column=0)

        self.sortByNumberOfMoons = IntVar()
        self.sortByNumberOfMoonsDescendingCheckBox = Checkbutton(self.insertionFrame, text="Sort by number of moons descending? ", variable=self.sortByNumberOfMoons, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(5))
        self.sortByNumberOfMoonsDescendingCheckBox.grid(row=startingRow, column=1)

        self.sortByDistanceFromEarth = IntVar()
        self.sortByGreatestDistanceFromEarthDescendingCheckBox = Checkbutton(self.insertionFrame, text="Sort by distance from earth descending? ", variable=self.sortByDistanceFromEarth, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(6))
        self.sortByGreatestDistanceFromEarthDescendingCheckBox.grid(row=startingRow, column=2)

        self.sortBYPlanetRotationalPeriod = IntVar()
        self.sortByPlanetRotationalPeriodDescendingCheckBox = Checkbutton(self.insertionFrame, text="Sort by planet rotational period descending? ", variable=self.sortBYPlanetRotationalPeriod, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(7))
        self.sortByPlanetRotationalPeriodDescendingCheckBox.grid(row=startingRow, column=3)

        startingRow += 1
        self.sortByPlanetOrbitalPeriod = IntVar()
        self.sortByPlanetOrbitalPeriodDescendingCheckBox = Checkbutton(self.insertionFrame, text="Sort by planet orbital period descending? ", variable=self.sortByPlanetOrbitalPeriod, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(8))
        self.sortByPlanetOrbitalPeriodDescendingCheckBox.grid(row=startingRow, column=0, columnspan=2)

        self.sortByStar = IntVar()
        self.sortByStarCheckBox = Checkbutton(self.insertionFrame, text="Sort by star planet orbits? ", variable=self.sortByStar, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(9))
        self.sortByStarCheckBox.grid(row=startingRow, column=2, columnspan=2)

        self.sortingSwitches = []
        self.sortingSwitches.append(self.sortByESIDescendingCheckbox)
        self.sortingSwitches.append(self.sortByEscapeVelocityDescendingCheckBox)
        self.sortingSwitches.append(self.sortBySizeDescendingCheckBox)
        self.sortingSwitches.append(self.sortByGrabityDescendingCheckBox)
        self.sortingSwitches.append(self.sortByTemperatureDescendingCheckBox)
        self.sortingSwitches.append(self.sortByNumberOfMoonsDescendingCheckBox)
        self.sortingSwitches.append(self.sortByGreatestDistanceFromEarthDescendingCheckBox)
        self.sortingSwitches.append(self.sortByPlanetRotationalPeriodDescendingCheckBox)
        self.sortingSwitches.append(self.sortByPlanetOrbitalPeriodDescendingCheckBox)
        self.sortingSwitches.append(self.sortByStarCheckBox)

        # attribute filters
        startingRow += 1
        Label(self.insertionFrame, text="-------------------ATTRIBUTE FILTERS-------------------").grid(row=startingRow, column=0, columnspan=4)

        startingRow += 1

        self.showMass = IntVar()
        self.showMass.set(1)
        self.showMassCheckBox = Checkbutton(self.insertionFrame, text="Show mass", variable=self.showMass, onvalue=1, offvalue=0, command=self.toggleMass)
        self.showMassCheckBox.grid(row=startingRow, column=0)

        self.showGravity = IntVar()
        self.showGravity.set(1)
        self.showGravityCheckBox = Checkbutton(self.insertionFrame, text="Show gravity", variable=self.showGravity, onvalue=1, offvalue=0, command=self.toggleGravity)
        self.showGravityCheckBox.grid(row=startingRow, column=1)

        self.showRadius = IntVar()
        self.showRadius.set(1)
        self.showRadiusCheckBox = Checkbutton(self.insertionFrame, text="Show radius", variable=self.showRadius, onvalue=1, offvalue=0, command=self.toggleRadius)
        self.showRadiusCheckBox.grid(row=startingRow, column=2)

        self.showDistanceFromEarth = IntVar()
        self.showDistanceFromEarth.set(1)
        self.showDistanceFromEarthCheckBox = Checkbutton(self.insertionFrame, text="Show distance", variable=self.showDistanceFromEarth, onvalue=1, offvalue=0, command=self.toggleDistance)
        self.showDistanceFromEarthCheckBox.grid(row=startingRow, column=3)

        startingRow += 1
        self.showTemperature = IntVar()
        self.showTemperature.set(1)
        self.showEquilibriumTemperatureCheckBox = Checkbutton(self.insertionFrame, text="Show Temperature", variable=self.showTemperature, onvalue=1, offvalue=0, command=self.toggleTemperature)
        self.showEquilibriumTemperatureCheckBox.grid(row=startingRow, column=0)

        self.showESI = IntVar()
        self.showESI.set(1)
        self.showESICheckBox = Checkbutton(self.insertionFrame, text="Show ESI", variable=self.showESI, onvalue=1, offvalue=0, command=self.toggleESI)
        self.showESICheckBox.grid(row=startingRow, column=1)

        self.showRotationalPeriod = IntVar()
        self.showRotationalPeriod.set(1)
        self.showRotationalPeriodCheckBox = Checkbutton(self.insertionFrame, text="Show rotational period", variable=self.showRotationalPeriod, onvalue=1, offvalue=0, command=self.toggleRotationalPeriod)
        self.showRotationalPeriodCheckBox.grid(row=startingRow, column=2)

        self.showOrbitalPeriod = IntVar()
        self.showOrbitalPeriod.set(1)
        self.showOrbitalPeriodCheckBox = Checkbutton(self.insertionFrame, text="Show Orbital Period", variable=self.showOrbitalPeriod, onvalue=1, offvalue=0, command=self.toggleOrbitalPeriod)
        self.showOrbitalPeriodCheckBox.grid(row=startingRow, column=3)

        startingRow += 1
        self.showEscapeVelocity = IntVar()
        self.showEscapeVelocity.set(1)
        self.showEscapeVelocityCheckBox = Checkbutton(self.insertionFrame, text="Show escape velocity", variable=self.showEscapeVelocity, onvalue=1, offvalue=0, command=self.toggleEscapeVelocity)
        self.showEscapeVelocityCheckBox.grid(row=startingRow, column=0)

        self.showImage = IntVar()
        self.showImage.set(1)
        self.showImageCheckBox = Checkbutton(self.insertionFrame, text="Show Image", variable=self.showImage, onvalue=1, offvalue=0, command=self.toggleImage)
        self.showImageCheckBox.grid(row=startingRow, column=1)

        # startingRow += 1
        self.showDescription = IntVar()
        self.showDescription.set(1)
        self.showDescriptionCheckBox = Checkbutton(self.insertionFrame, text="Show Description",
                                                   variable=self.showDescription, onvalue=1,
                                                   offvalue=0, command=self.toggleDescription)
        self.showDescriptionCheckBox.grid(row=startingRow, column=2)

        self.showPlanetIsADwarf = IntVar()
        self.showPlanetIsADwarf.set(1)
        self.showPlanetIsDwarfPlanetCheckBox = Checkbutton(self.insertionFrame, text="Show Planet is a Dwarf",
                                                           variable=self.showPlanetIsADwarf, onvalue=1,
                                                           offvalue=0, command=self.toggleDwarf)
        self.showPlanetIsDwarfPlanetCheckBox.grid(row=startingRow, column=3)

        startingRow += 1
        self.showPlanetIsAnExoPlanet = IntVar()
        self.showPlanetIsAnExoPlanet.set(1)
        self.showPlanetIsAnExoPlanetCheckBox = Checkbutton(self.insertionFrame, text="Show Planet is an exo planet",
                                                           variable=self.showPlanetIsAnExoPlanet, onvalue=1,
                                                           offvalue=0, command=self.toggleExo)
        self.showPlanetIsAnExoPlanetCheckBox.grid(row=startingRow, column=0)

        self.showPlanetIsInHabitZone = IntVar()
        self.showPlanetIsInHabitZone.set(1)
        self.showPlanetIsInHabitZoneCheckBox = Checkbutton(self.insertionFrame, text="Show Planet is in habit zone",
                                                           variable=self.showPlanetIsInHabitZone, onvalue=1,
                                                           offvalue=0, command=self.toggleInHabitZone)
        self.showPlanetIsInHabitZoneCheckBox.grid(row=startingRow, column=1)

        self.showPlanetAtmospheres = IntVar()
        self.showPlanetAtmospheres.set(1)
        self.showPlanetAtmospheresCheckBox = Checkbutton(self.insertionFrame, text="Show Planet Atmospheres Check box",
                                                         variable=self.showPlanetAtmospheres, onvalue=1,
                                                         offvalue=0, command=self.togglePlanetAtmospheres).grid(row=startingRow, column=2)

        self.showMoons = IntVar()
        self.showMoons.set(1)
        self.showMoonsCheckBox = Checkbutton(self.insertionFrame, text="Show Moons Check box", variable=self.showMoons, onvalue=1, offvalue=0, command=self.toggleMoons).grid(row=startingRow, column=3)

        startingRow += 1
        self.showStars = IntVar()
        self.showStars.set(1)
        self.showStarsCheckBox = Checkbutton(self.insertionFrame, text="Show Stars Check box", variable=self.showStars, onvalue=1, offvalue=0, command=self.toggleStars).grid(row=startingRow, column=0, columnspan=4)

        startingRow += 1
        self.positionConfirmationUI(startingRow)
