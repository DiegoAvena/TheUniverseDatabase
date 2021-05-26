'''
----SUMMARY----
Allows the user to search
for multiple stars with various
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

SingleStarSearchManager:

This is used for the displaying of multiple
star records that get turned up after a search is
confirmed.

'''

from Code.SearchManagers.BaseSearchManagers.BaseMultiSearchManager import BaseMultiSearchManager
from Code.SearchManagers.SingleSearchManagers.SingleStarSearchManager import SingleStarSearchManager
from tkinter import *

class MultiStarSearchManager(BaseMultiSearchManager):

    # sorting filters
    global sortByMassCheckBox
    global sortByMass

    global sortByRadiusCheckBox
    global sortByRadius

    global sortByEvolutionaryStageCheckBox
    global sortByEvolutionaryStage

    global sortByDistanceFromEarthCheckBox
    global sortByDistance

    global sortByPlanetarySystemCheckBox
    global sortByPlanetarySystem

    global sortByGalaxyCheckBox
    global sortByGalaxy

    # attribute filters:
    global showMass
    global showMassCheckBox

    global showRadius
    global showRadiusCheckBox

    global showEvolutionaryStageCheckBox
    global showEvolutionaryStage

    global showDistanceFromEarthCheckBox
    global showDistanceFromEarth

    global showPlanetarySystemCheckBox
    global showPlanetarySystem

    global showImage
    global showImageCheckBox

    global showGalaxy
    global showGalaxyCheckBox

    def determineIfThereIsASortingClause(self):
        sortingClause = ""
        if (self.sortByMass.get() == 1):
            sortingClause += " ORDER BY Mass DESC "
        elif (self.sortByRadius.get() == 1):
            sortingClause += " ORDER BY Radius DESC "
        elif (self.sortByEvolutionaryStage.get() == 1):
            sortingClause += " ORDER BY EvolutionaryStage DESC "
        elif (self.sortByDistance.get() == 1):
            sortingClause += " ORDER BY DistanceFromEarth DESC "
        elif (self.sortByPlanetarySystem.get() == 1):
            sortingClause += " ORDER BY PlanetarySystem"
        elif (self.sortByGalaxy.get() == 1):
            sortingClause += " ORDER BY GalaxyName "
        return sortingClause

    def toggleMass(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for planet in self.recordDisplayersSpawnedInSoFar:
            planet.showMass.set(self.showMass.get())
            planet.toggleMass()

    def toggleRadius(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for star in self.recordDisplayersSpawnedInSoFar:
            star.showRadius.set(self.showRadius.get())
            star.toggleRadius()

    def toggleEvolutionaryStage(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for star in self.recordDisplayersSpawnedInSoFar:
            star.showEvolutionaryStage.set(self.showEvolutionaryStage.get())
            star.toggleEvolutionaryStage()

    def toggleDistanceFromEarth(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for star in self.recordDisplayersSpawnedInSoFar:
            star.showDistanceFromEarth.set(self.showDistanceFromEarth.get())
            star.toggleDistanceFromEarth()

    def togglePlanetarySystem(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for star in self.recordDisplayersSpawnedInSoFar:
            star.showPlanetarySystem.set(self.showPlanetarySystem.get())
            star.togglePlanetarySystem()

    def toggleImage(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for star in self.recordDisplayersSpawnedInSoFar:
            star.showImage.set(self.showImage.get())
            star.toggleImage()

    def toggleGalaxy(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for star in self.recordDisplayersSpawnedInSoFar:
            star.showGalaxy.set(self.showGalaxy.get())
            star.toggleGalaxy()

    def performSearch(self):
        BaseMultiSearchManager.performSearch(self)

        query = '''
        
            SELECT Stars.Name
            FROM Stars
        
        '''

        if (self.sortByPlanetarySystem.get() == 1):
            query = '''
            
                SELECT Stars.Name, PlanetarySystems.Name 
                FROM Stars INNER JOIN PlanetarySystems 
                ON PlanetarySystem = PlanetarySystems.Name
            
            '''
        elif(self.sortByGalaxy.get() == 1):
            query = '''
            
                SELECT Stars.Name, PlanetarySystems.GalaxyName
                FROM Stars INNER JOIN PlanetarySystems 
                ON PlanetarySystem = PlanetarySystems.Name
            
            '''
        elif (self.sortByEvolutionaryStage.get() == 1):
            query = '''

                SELECT Stars.Name, EvolutionaryStage
                FROM Stars 
                
            '''
        query += self.determineIfThereIsASortingClause() + ";"
        print("Final query that will run: " + "\n" + query)

        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        cursor.execute(query)

        starNames = []
        systemOrGalaxyOrStageNames = []
        records = cursor.fetchall()
        database.close()

        for record in records:
            starNames.append(record[0])
            if (self.sortByPlanetarySystem.get() == 1):
                systemOrGalaxyOrStageNames.append(record[1])
            elif (self.sortByGalaxy.get() == 1):
                systemOrGalaxyOrStageNames.append(record[1])
            elif (self.sortByEvolutionaryStage.get() == 1):
                systemOrGalaxyOrStageNames.append(record[1])

        currentNameOfGalaxyOrSystemOrStage = ""
        currentFrame = self.resultsFrame
        currentFrameColumn = 0
        for i in range(0, len(starNames)):
            if (len(systemOrGalaxyOrStageNames) > 0):
                if ((systemOrGalaxyOrStageNames[i] != currentNameOfGalaxyOrSystemOrStage) and (currentNameOfGalaxyOrSystemOrStage != 'unknown')):
                    if (systemOrGalaxyOrStageNames[i] == None):
                        currentNameOfGalaxyOrSystemOrStage = 'unknown'
                    else:
                        currentNameOfGalaxyOrSystemOrStage = systemOrGalaxyOrStageNames[i]

                    currentFrame = LabelFrame(self.resultsFrame, text=currentNameOfGalaxyOrSystemOrStage)
                    currentFrame.grid(row=currentFrameColumn, column=0, pady=20, sticky=W)
                    currentFrameColumn += 1
                    self.anySortingFramesThatSpawned.append(currentFrame)

            starDisplayer = SingleStarSearchManager(self.localMySqlInstancePassword)
            starDisplayer.initializeSingleSearchForDisplayOnMultiSearchFrame(currentFrame, 0, i, starNames[i], self.insertionManager)
            self.recordDisplayersSpawnedInSoFar.append(starDisplayer)

        self.toggleMass()
        self.toggleRadius()
        self.toggleEvolutionaryStage()
        self.toggleDistanceFromEarth()
        self.togglePlanetarySystem()
        self.toggleImage()
        self.toggleGalaxy()

    def manageMultiSearch(self, windowToPutFrameOnto, mainSearchManager, searchTitle):
        BaseMultiSearchManager.manageMultiSearch(self, windowToPutFrameOnto, mainSearchManager, searchTitle)
        self.defaultReportName = "Star Search"

        starNames = []
        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        query = '''

                    SELECT Name 
                    FROM Stars; 

                '''
        cursor.execute(query)
        records = cursor.fetchall()
        for name in records:
            starNames.append(name[0])

        print(str(starNames))
        database.close()

        # show all stars by default:
        self.recordDisplayersSpawnedInSoFar = []
        for i in range(0, len(starNames)):
            starDisplayer = SingleStarSearchManager(self.localMySqlInstancePassword)
            starDisplayer.initializeSingleSearchForDisplayOnMultiSearchFrame(self.resultsFrame, 0, i, starNames[i], self.insertionManager)
            self.recordDisplayersSpawnedInSoFar.append(starDisplayer)

        # create filter checkboxes:
        # sorting filters
        startingRow = 3
        Label(self.insertionFrame, text="-------------------SORTING FILTERS-------------------").grid(row=startingRow, column=0, columnspan=4)

        startingRow += 1

        self.sortByMass = IntVar()
        self.sortByMassCheckBox = Checkbutton(self.insertionFrame, text="Sort by mass descending?", variable=self.sortByMass, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(0))
        self.sortByMassCheckBox.grid(row=startingRow, column=0)

        self.sortByRadius = IntVar()
        self.sortByRadiusCheckBox = Checkbutton(self.insertionFrame, text="Sort by radius descending?", variable=self.sortByRadius, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(1))
        self.sortByRadiusCheckBox.grid(row=startingRow, column=1)

        self.sortByEvolutionaryStage = IntVar()
        self.sortByEvolutionaryStageCheckBox = Checkbutton(self.insertionFrame, text="Sort by evolutionary stage?", variable=self.sortByEvolutionaryStage, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(2))
        self.sortByEvolutionaryStageCheckBox.grid(row=startingRow, column=2)

        self.sortByDistance = IntVar()
        self.sortByDistanceFromEarthCheckBox = Checkbutton(self.insertionFrame, text="Sort by distance from Earth?", variable=self.sortByDistance, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(3))
        self.sortByDistanceFromEarthCheckBox.grid(row=startingRow, column=3)

        startingRow += 1

        self.sortByPlanetarySystem = IntVar()
        self.sortByPlanetarySystemCheckBox = Checkbutton(self.insertionFrame, text="Sort by planetary system?", variable=self.sortByPlanetarySystem, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(4))
        self.sortByPlanetarySystemCheckBox.grid(row=startingRow, column=0, columnspan=2)

        self.sortByGalaxy = IntVar()
        self.sortByGalaxyCheckBox = Checkbutton(self.insertionFrame, text="Sort by galaxy?", variable=self.sortByGalaxy, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(5))
        self.sortByGalaxyCheckBox.grid(row=startingRow, column=2, columnspan=2)

        self.sortingSwitches.append(self.sortByMassCheckBox)
        self.sortingSwitches.append(self.sortByRadiusCheckBox)
        self.sortingSwitches.append(self.sortByEvolutionaryStageCheckBox)
        self.sortingSwitches.append(self.sortByDistanceFromEarthCheckBox)
        self.sortingSwitches.append(self.sortByPlanetarySystemCheckBox)
        self.sortingSwitches.append(self.sortByGalaxyCheckBox)


        # attribute filters:
        startingRow += 1
        Label(self.insertionFrame, text="-------------------ATTRIBUTE FILTERS-------------------").grid(row=startingRow, column=0, columnspan=4)

        startingRow += 1
        self.showMass = IntVar()
        self.showMass.set(1)
        self.showMassCheckBox = Checkbutton(self.insertionFrame, text="Show mass", variable=self.showMass, onvalue=1, offvalue=0, command=self.toggleMass)
        self.showMassCheckBox.grid(row=startingRow, column=0)

        self.showRadius = IntVar()
        self.showRadius.set(1)
        self.showRadiusCheckBox = Checkbutton(self.insertionFrame, text="Show Radius", variable=self.showRadius, onvalue=1, offvalue=0, command=self.toggleRadius)
        self.showRadiusCheckBox.grid(row=startingRow, column=1)

        self.showEvolutionaryStage = IntVar()
        self.showEvolutionaryStage.set(1)
        self.showEvolutionaryStageCheckBox = Checkbutton(self.insertionFrame, text="Show Evolutionary Stage", variable=self.showEvolutionaryStage, onvalue=1, offvalue=0, command=self.toggleEvolutionaryStage)
        self.showEvolutionaryStageCheckBox.grid(row=startingRow, column=2)

        self.showDistanceFromEarth = IntVar()
        self.showDistanceFromEarth.set(1)
        self.showDistanceFromEarthCheckBox = Checkbutton(self.insertionFrame, text="Show distance from Earth", variable=self.showDistanceFromEarth, onvalue=1, offvalue=0, command=self.toggleDistanceFromEarth)
        self.showDistanceFromEarthCheckBox.grid(row=startingRow, column=3)

        startingRow += 1
        self.showPlanetarySystem = IntVar()
        self.showPlanetarySystem.set(1)
        self.showPlanetarySystemCheckBox = Checkbutton(self.insertionFrame, text="Show Planetary System", variable=self.showPlanetarySystem, onvalue=1, offvalue=0, command=self.togglePlanetarySystem)
        self.showPlanetarySystemCheckBox.grid(row=startingRow, column=0, columnspan=2)

        self.showImage = IntVar()
        self.showImage.set(1)
        self.showImageCheckBox = Checkbutton(self.insertionFrame, text="Show Image", variable=self.showImage, onvalue=1, offvalue=0, command=self.toggleImage)
        self.showImageCheckBox.grid(row=startingRow, column=2)

        self.showGalaxy = IntVar()
        self.showGalaxy.set(1)
        self.showGalaxyCheckBox = Checkbutton(self.insertionFrame, text="Show Galaxy", variable=self.showGalaxy, onvalue=1, offvalue=0, command=self.toggleGalaxy)
        self.showGalaxyCheckBox.grid(row=startingRow, column=3)

        startingRow += 1
        self.positionConfirmationUI(startingRow)
