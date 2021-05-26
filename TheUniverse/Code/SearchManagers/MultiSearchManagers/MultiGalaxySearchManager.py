'''
----SUMMARY----
Allows the user to search
for multiple galaxies with various
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
since this is a specific option for searching for multiple galaxies

tkinter - Used for all the UI

SingleGalaxySearchManager:

This is used for the displaying of multiple
galaxy records that get turned up after a search is
confirmed.

'''

from Code.SearchManagers.BaseSearchManagers.BaseMultiSearchManager import BaseMultiSearchManager
from tkinter import *
from Code.SearchManagers.SingleSearchManagers.SingleGalaxySearchManager import SingleGalaxySearchManager

class MultiGalaxySearchManager(BaseMultiSearchManager):

    # attribute exclusion filters
    global showNumberofStarsCheckBox
    global showNumberOfStars

    global showAgeCheckBox
    global showAge

    global showDistanceFromEarthCheckBox
    global showDistanceFromEarth

    global showMassCheckBox
    global showMass

    global showYearDiscoveredCheckBox
    global showYearDiscovered

    global showImageCheckBox
    global showImage

    global showGalaxyTypeCheckBox
    global showGalaxyType

    global showGalaxyDiscovererCheckBox
    global showGalaxyDiscoverer

    # sorting filters:
    global sortByAge
    global sortByAgeCheckBox

    global sortByNumberOfStars
    global sortByNumberOfStarsCheckBox

    global sortByDistanceFromEarth
    global sortByDistanceFromEarthCheckBox

    global sortByMass
    global sortByMassCheckBox

    global sortByYearDiscovered
    global sortByYearDiscoveredCheckBox

    global sortByGalaxyDiscoverer
    global sortByGalaxyDiscovererCheckBox

    global sortByGalaxyType
    global sortByGalaxyTypeCheckBox

    def determineIfThereIsASortingClause(self):

        sortingClause = ""

        if (self.sortByNumberOfStars.get() == 1):
            sortingClause += " ORDER BY NumberOfStars DESC "
        elif (self.sortByAge.get() == 1):
            sortingClause += " ORDER BY Age DESC "
        elif (self.sortByDistanceFromEarth.get() == 1):
            sortingClause += " ORDER BY DistanceFromEarth DESC "
        elif (self.sortByMass.get() == 1):
            sortingClause += " ORDER BY Mass "
        elif (self.sortByYearDiscovered.get() == 1):
            sortingClause += " ORDER BY YearDiscovered DESC "
        elif (self.sortByGalaxyDiscoverer.get() == 1):
            sortingClause += " ORDER BY Name DESC "
        elif (self.sortByGalaxyType.get() == 1):
            sortingClause += " ORDER BY GalaxyType DESC "

        return sortingClause

    def performSearch(self):
        BaseMultiSearchManager.performSearch(self)
        query = '''
        
            SELECT Name
            FROM Galaxies
        
        '''

        if (self.sortByYearDiscovered.get() == 1):
            query = '''
            
                SELECT Name, YearDiscovered
                FROM Galaxies 
            
            '''
        elif (self.sortByGalaxyDiscoverer.get() == 1):
            query = '''
            
                SELECT Name, DiscovererName
                FROM Galaxies INNER JOIN GalaxyDiscovers
                    ON Name = GalaxyName
            
            '''
        elif (self.sortByGalaxyType.get() == 1):
            query = '''
            
                SELECT Name, GalaxyType 
                FROM Galaxies
            
            '''

        query += self.determineIfThereIsASortingClause() + ";"
        print("FINAL QUERY THAT WILL RUN: " + "\n" + query)
        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        database.close()

        galaxyNames = []
        galaxyDiscovererNamesOrYearDiscoveredOrGalaxyTypeNames = []
        for record in records:
            galaxyNames.append(record[0])
            if (self.sortByYearDiscovered.get() == 1):
                galaxyDiscovererNamesOrYearDiscoveredOrGalaxyTypeNames.append(record[1])
            elif (self.sortByGalaxyDiscoverer.get() == 1):
                galaxyDiscovererNamesOrYearDiscoveredOrGalaxyTypeNames.append(record[1])
            elif (self.sortByGalaxyType.get() == 1):
                galaxyDiscovererNamesOrYearDiscoveredOrGalaxyTypeNames.append(record[1])

        # spawn in the individual galaxy frames:
        currentYearOrGalaxyTypeOrDiscovererName = ""
        currentFrame = self.resultsFrame
        currentFrameRow = 0
        for i in range(0, len(galaxyNames)):
            if (len(galaxyDiscovererNamesOrYearDiscoveredOrGalaxyTypeNames) > 0):
                if ((galaxyDiscovererNamesOrYearDiscoveredOrGalaxyTypeNames[i] != currentYearOrGalaxyTypeOrDiscovererName) and (currentYearOrGalaxyTypeOrDiscovererName != 'unknown')):

                    if (galaxyDiscovererNamesOrYearDiscoveredOrGalaxyTypeNames[i] == None):
                        currentYearOrGalaxyTypeOrDiscovererName = 'unknown'
                    else:
                        currentYearOrGalaxyTypeOrDiscovererName = galaxyDiscovererNamesOrYearDiscoveredOrGalaxyTypeNames[i]
                    currentFrame = LabelFrame(self.resultsFrame, text=currentYearOrGalaxyTypeOrDiscovererName)
                    currentFrame.grid(row=currentFrameRow, column=0, pady=20, sticky=W)
                    currentFrameRow += 1
                    self.anySortingFramesThatSpawned.append(currentFrame)
            galaxyDisplayer = SingleGalaxySearchManager(self.localMySqlInstancePassword)
            galaxyDisplayer.initializeSingleSearchForDisplayOnMultiSearchFrame(currentFrame, 0, i, galaxyNames[i], self.insertionManager)
            self.recordDisplayersSpawnedInSoFar.append(galaxyDisplayer)

        self.toggleNumberOfStars()
        self.toggleAge()
        self.toggleDistanceFromEarth()
        self.toggleMass()
        self.toggleYearDiscovered()
        self.toggleImage()
        self.toggleGalaxyType()
        self.toggleGalaxyDiscoverer()

    def toggleNumberOfStars(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for galaxy in self.recordDisplayersSpawnedInSoFar:
            galaxy.showNumberOfStars.set(self.showNumberOfStars.get())
            galaxy.toggleNumberOfStars()

    def toggleAge(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for galaxy in self.recordDisplayersSpawnedInSoFar:
            galaxy.showAge.set(self.showAge.get())
            galaxy.toggleAge()

    def toggleDistanceFromEarth(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for galaxy in self.recordDisplayersSpawnedInSoFar:
            galaxy.showDistanceFromEarth.set(self.showDistanceFromEarth.get())
            galaxy.toggleDistanceFromEarth()

    def toggleMass(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for galaxy in self.recordDisplayersSpawnedInSoFar:
            galaxy.showMass.set(self.showMass.get())
            galaxy.toggleMass()

    def toggleYearDiscovered(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for galaxy in self.recordDisplayersSpawnedInSoFar:
            galaxy.showYearDiscovered.set(self.showYearDiscovered.get())
            galaxy.toggleYearDiscovered()

    def toggleImage(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for galaxy in self.recordDisplayersSpawnedInSoFar:
            galaxy.showImage.set(self.showImage.get())
            galaxy.toggleImage()

    def toggleGalaxyType(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for galaxy in self.recordDisplayersSpawnedInSoFar:
            galaxy.showGalaxyType.set(self.showGalaxyType.get())
            galaxy.toggleGalaxyType()

    def toggleGalaxyDiscoverer(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()
        for galaxy in self.recordDisplayersSpawnedInSoFar:
            galaxy.showGalaxyDiscoverer.set(self.showGalaxyDiscoverer.get())
            galaxy.toggleGalaxyDiscoverer()

    def manageMultiSearch(self, windowToPutFrameOnto, mainSearchManager, searchTitle):

        BaseMultiSearchManager.manageMultiSearch(self, windowToPutFrameOnto, mainSearchManager, searchTitle)
        self.defaultReportName = "Multi-Galaxy Search"

        galaxyNames = []

        database = self.makeConnectionToDatabase()
        cursor = database.cursor()

        query = '''
        
            SELECT Name 
            FROM Galaxies; 
        
        '''
        cursor.execute(query)
        records = cursor.fetchall()
        for record in records:
           galaxyNames.append(record[0])

        database.close()

        self.recordDisplayersSpawnedInSoFar = []
        for i in range(0, len(galaxyNames)):
            galaxyDisplayer = SingleGalaxySearchManager(self.localMySqlInstancePassword)
            galaxyDisplayer.initializeSingleSearchForDisplayOnMultiSearchFrame(self.resultsFrame, 0, i, galaxyNames[i], self.insertionManager)
            self.recordDisplayersSpawnedInSoFar.append(galaxyDisplayer)

        # criterial filters:
        startingRow = 3
        Label(self.insertionFrame, text="-------------------ATTRIBUTE FILTERS-------------------").grid(row=startingRow, column=0, columnspan=4)

        startingRow += 1
        self.showNumberOfStars = IntVar()
        self.showNumberOfStars.set(1)
        self.showNumberofStarsCheckBox = Checkbutton(self.insertionFrame, text="Show Number of Stars", variable=self.showNumberOfStars, onvalue=1, offvalue=0, command=self.toggleNumberOfStars)
        self.showNumberofStarsCheckBox.grid(row=startingRow, column=0)

        self.showAge = IntVar()
        self.showAge.set(1)
        self.showAgeCheckBox = Checkbutton(self.insertionFrame, text="Show age", variable=self.showAge, onvalue=1, offvalue=0, command=self.toggleAge)
        self.showAgeCheckBox.grid(row=startingRow, column=1)

        self.showDistanceFromEarth = IntVar()
        self.showDistanceFromEarth.set(1)
        self.showDistanceFromEarthCheckBox = Checkbutton(self.insertionFrame, text="Show Distance from Earth", variable=self.showDistanceFromEarth, onvalue=1, offvalue=0, command=self.toggleDistanceFromEarth)
        self.showDistanceFromEarthCheckBox.grid(row=startingRow, column=2)

        self.showMass = IntVar()
        self.showMass.set(1)
        self.showMassCheckBox = Checkbutton(self.insertionFrame, text="Show mass", variable=self.showMass, onvalue=1, offvalue=0, command=self.toggleMass)
        self.showMassCheckBox.grid(row=startingRow, column=3)

        startingRow += 1
        self.showYearDiscovered = IntVar()
        self.showYearDiscovered.set(1)
        self.showYearDiscoveredCheckBox = Checkbutton(self.insertionFrame, text="Show Year Discovered", variable=self.showYearDiscovered, onvalue=1, offvalue=0, command=self.toggleYearDiscovered)
        self.showYearDiscoveredCheckBox.grid(row=startingRow, column=0)

        self.showImage = IntVar()
        self.showImage.set(1)
        self.showImageCheckBox = Checkbutton(self.insertionFrame, text="Show Galaxy Image", variable=self.showImage, onvalue=1, offvalue=0, command=self.toggleImage)
        self.showImageCheckBox.grid(row=startingRow, column=1)

        self.showGalaxyType = IntVar()
        self.showGalaxyType.set(1)
        self.showGalaxyTypeCheckBox = Checkbutton(self.insertionFrame, text="Show Galaxy Type", variable=self.showGalaxyType, onvalue=1, offvalue=0, command=self.toggleGalaxyType)
        self.showGalaxyTypeCheckBox.grid(row=startingRow, column=2)

        self.showGalaxyDiscoverer = IntVar()
        self.showGalaxyDiscoverer.set(1)
        self.showGalaxyDiscovererCheckBox = Checkbutton(self.insertionFrame, text="Show Galaxy Discoverer", variable=self.showGalaxyDiscoverer, onvalue=1, offvalue=0, command=self.toggleGalaxyDiscoverer)
        self.showGalaxyDiscovererCheckBox.grid(row=startingRow, column=3)

        startingRow += 1
        Label(self.insertionFrame, text="-------------------SORTING FILTERS-------------------").grid(row=startingRow, column=0, columnspan=4)

        startingRow += 1
        self.sortByNumberOfStars = IntVar()
        self.sortByNumberOfStarsCheckBox = Checkbutton(self.insertionFrame, text="Sort by number of stars descending?", variable=self.sortByNumberOfStars, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(0))
        self.sortByNumberOfStarsCheckBox.grid(row=startingRow, column=0)

        self.sortByAge = IntVar()
        self.sortByAgeCheckBox = Checkbutton(self.insertionFrame, text="Sort by age descending?", variable=self.sortByAge, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(1))
        self.sortByAgeCheckBox.grid(row=startingRow, column=1)

        self.sortByDistanceFromEarth = IntVar()
        self.sortByDistanceFromEarthCheckBox = Checkbutton(self.insertionFrame, text="Sort by distance from Earth descending?", variable=self.sortByDistanceFromEarth, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(2))
        self.sortByDistanceFromEarthCheckBox.grid(row=startingRow, column=2)

        self.sortByMass = IntVar()
        self.sortByMassCheckBox = Checkbutton(self.insertionFrame, text="Sort by mass descending?", variable=self.sortByMass, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(3))
        self.sortByMassCheckBox.grid(row=startingRow, column=3)

        startingRow += 1
        self.sortByYearDiscovered = IntVar()
        self.sortByYearDiscoveredCheckBox = Checkbutton(self.insertionFrame, text="Sort by year discovered descending?", variable=self.sortByYearDiscovered, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(4))
        self.sortByYearDiscoveredCheckBox.grid(row=startingRow, column=0)

        self.sortByGalaxyDiscoverer = IntVar()
        self.sortByGalaxyDiscovererCheckBox = Checkbutton(self.insertionFrame, text="Sort by galaxy discoverer?", variable=self.sortByGalaxyDiscoverer, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(5))
        self.sortByGalaxyDiscovererCheckBox.grid(row=startingRow, column=1)

        self.sortByGalaxyType = IntVar()
        self.sortByGalaxyTypeCheckBox = Checkbutton(self.insertionFrame, text="Sort by galaxy type? ", variable=self.sortByGalaxyType, onvalue=1, offvalue=0, command=lambda: self.chooseSortingScheme(6))
        self.sortByGalaxyTypeCheckBox.grid(row=startingRow, column=2, columnspan=2)

        startingRow += 1
        self.sortingSwitches = []
        self.sortingSwitches.append(self.sortByNumberOfStarsCheckBox)
        self.sortingSwitches.append(self.sortByAgeCheckBox)
        self.sortingSwitches.append(self.sortByDistanceFromEarthCheckBox)
        self.sortingSwitches.append(self.sortByMassCheckBox)
        self.sortingSwitches.append(self.sortByYearDiscoveredCheckBox)
        self.sortingSwitches.append(self.sortByGalaxyDiscovererCheckBox)
        self.sortingSwitches.append(self.sortByGalaxyTypeCheckBox)

        self.positionConfirmationUI(startingRow)
        pass

