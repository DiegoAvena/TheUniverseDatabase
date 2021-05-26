'''
----SUMMARY----
Allows the user to search
for individual galaxies and produce
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
since this is a specific option for searching for a single galaxy

tkinter - Used for all the UI

ImageDisplayerManager -
This is used to display an image of the
galaxy the user searches for

TextBoxManager -
Used to display a description of the type the
galaxy the user searches for is

'''

from Code.SearchManagers.BaseSearchManagers.BaseSingleSearchManager import BaseSingleSearchManager
from tkinter import *
from Code.Displayers.ImageDisplayerManager import ImageDisplayerManager
from Code.Displayers.TextBoxManager import TextBoxManager

class SingleGalaxySearchManager(BaseSingleSearchManager):

    global galaxyNameLabel
    global galaxyNameResultsLabel

    global galaxyNumberOfStarsLabel
    global galaxyNumberOfStarsResultsLabel

    global galaxyAgeLabel
    global galaxyAgeResultsLabel

    global galaxyDistanceFromEarthLabel
    global galaxyDistanceFromEarthResultsLabel

    global galaxyMassLabel
    global galaxyMassResultsLabel

    global galaxyYearDiscoveredLabel
    global galaxyYearDiscoveredResultsLabel

    global galaxyImageDisplayer

    global galaxyTypeLabel
    global galaxyTypeResultsLabel
    global galaxyTypeDescriptionDisplayer

    global galaxyDiscovererNameLabel
    global galaxyDiscovererNameResultsLabel

    # attribute filters:
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

    global typeDescriptionURL
    global galaxyDiscoverer

    def toggleGalaxyDiscoverer(self):
        if (self.showGalaxyDiscoverer.get() == 0):
            self.galaxyDiscovererNameResultsLabel.grid_forget()
            self.galaxyDiscovererNameLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.galaxyDiscovererNameLabel, self.galaxyDiscovererNameResultsLabel, 11)
        self.initializeReportContents()

    def toggleNumberOfStars(self):
        if (self.showNumberOfStars.get() == 0):
            self.galaxyNumberOfStarsResultsLabel.grid_forget()
            self.galaxyNumberOfStarsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.galaxyNumberOfStarsLabel, self.galaxyNumberOfStarsResultsLabel, 1)
        self.initializeReportContents()

    def toggleAge(self):
        if (self.showAge.get() == 0):
            self.galaxyAgeLabel.grid_forget()
            self.galaxyAgeResultsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.galaxyAgeLabel, self.galaxyAgeResultsLabel, 2)
        self.initializeReportContents()

    def toggleDistanceFromEarth(self):
        if (self.showDistanceFromEarth.get() == 0):
            self.galaxyDistanceFromEarthResultsLabel.grid_forget()
            self.galaxyDistanceFromEarthLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.galaxyDistanceFromEarthLabel, self.galaxyDistanceFromEarthResultsLabel, 3)
        self.initializeReportContents()

    def toggleYearDiscovered(self):
        if (self.showYearDiscovered.get() == 0):
            self.galaxyYearDiscoveredLabel.grid_forget()
            self.galaxyYearDiscoveredResultsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.galaxyYearDiscoveredLabel, self.galaxyYearDiscoveredResultsLabel, 5)
        self.initializeReportContents()

    def toggleImage(self):
        if (self.showImage.get() == 0):
            self.galaxyImageDisplayer.hideAllImageUI()
        else:
            self.galaxyImageDisplayer.showAllImageUI()
        self.initializeReportContents()

    def toggleGalaxyType(self):
        if (self.showGalaxyType.get() == 0):
            self.galaxyTypeResultsLabel.grid_forget()
            self.galaxyTypeLabel.grid_forget()
            self.galaxyTypeDescriptionDisplayer.hideDescriptionUI()
        else:
            self.setUpLabelPositions(self.galaxyTypeLabel, self.galaxyTypeResultsLabel, 8)
            self.galaxyTypeDescriptionDisplayer.showAllDescriptionUI()
        self.initializeReportContents()

    def toggleMass(self):
        if (self.showMass.get() == 0):
            self.galaxyMassLabel.grid_forget()
            self.galaxyMassResultsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.galaxyMassLabel, self.galaxyMassResultsLabel, 4)
        self.initializeReportContents()

    def initializeReportContents(self):
        try:
            if (self.initializedForMultiDisplay == False):
                self.insertionManager.reportGenerator.refreshReportGenerator()

            allPossibleAttributeNames = [

                "Number of Stars in Galaxy: ",
                "Galaxy Age: ",
                "Galaxy Distance From Earth (ly): ",
                "Galaxy Mass (Solar Mass): ",
                "Year Discovered: ",
                "Image Directory: ",
                "Galaxy Type: ",

            ]

            recordToReport = []
            attributeNames = []
            exclusionFilters = []

            exclusionFilters.append(self.showNumberOfStars.get())
            exclusionFilters.append(self.showAge.get())
            exclusionFilters.append(self.showDistanceFromEarth.get())
            exclusionFilters.append(self.showMass.get())
            exclusionFilters.append(self.showYearDiscovered.get())
            exclusionFilters.append(self.showImage.get())
            exclusionFilters.append(self.showGalaxyType.get())

            recordToReport.append(self.record[0])
            attributeNames.append("Galaxy Name: ")

            for i in range(0, len(exclusionFilters)):
                if (exclusionFilters[i] == 1):
                    recordToReport.append(str(self.record[i + 1]))
                    attributeNames.append(allPossibleAttributeNames[i])
                else:
                    print(allPossibleAttributeNames[i] + " will not be shown")

            if (self.showGalaxyDiscoverer.get() == 1):
                recordToReport.append(self.galaxyDiscoverer)
                attributeNames.append("Galaxy Discoverer: ")

            imageURL = None
            if (self.showImage.get() == 1):
                imageURL = self.record[len(self.record) - 2]

            # generate the report but do not save it yet:
            self.insertionManager.reportGenerator.generateReports(recordToReport, imageURL, attributeNames)
        except:
            return

    def populateFields(self):
        # run the query, get the record, display results:
        database = self.makeConnectionToDatabase()

        # without the buffered param, I was running into
        # a sql error where it was saying there was an unread value
        # this solution is taken from here:
        # https://stackoverflow.com/questions/38350816/python-mysql-connector-internalerror-unread-result-found-when-close-cursor
        cursor = database.cursor(buffered=True)
        query = '''

                                SELECT * 
                                FROM Galaxies 
                                WHERE Name = %s;

                            '''
        cursor.execute(query, [self.selectedItemToSearchFor.get()])
        record = cursor.fetchone()

        self.record = []
        for attribute in record:
            self.record.append(attribute)

        # determine the name of the galaxy discoverer:
        query = '''
        
            SELECT DiscovererName 
            FROM GalaxyDiscovers INNER JOIN Galaxies 
                ON GalaxyName = %s 
                AND GalaxyName = Name;
        
        '''
        cursor.execute(query, [self.selectedItemToSearchFor.get()])
        records = cursor.fetchall()
        self.galaxyDiscoverer = ""
        galaxyDiscovers = []
        if (records != None):
            for discoverer in records:
                galaxyDiscovers.append(discoverer[0])

        for i in range(0, len(galaxyDiscovers)):
            self.galaxyDiscoverer += galaxyDiscovers[i]
            if (len(galaxyDiscovers) > 1 and ((i + 1) < len(galaxyDiscovers))):
                self.galaxyDiscoverer += '\n'

        # get the galaxy type description URL:
        query = '''
        
            SELECT Description 
            FROM GalaxyTypes INNER JOIN Galaxies 
                ON GalaxyTypes.GalaxyType = Galaxies.GalaxyType 
                    AND Galaxies.Name = %s;
        
        '''
        cursor.execute(query, [self.selectedItemToSearchFor.get()])
        record = cursor.fetchone()
        self.typeDescriptionURL = 'N/A'
        if (record != None):
            self.typeDescriptionURL = record[0]

        database.close()

        self.galaxyNameResultsLabel.configure(text=self.record[0])
        self.galaxyNumberOfStarsResultsLabel.configure(text=str(self.record[1]))
        self.galaxyAgeResultsLabel.configure(text=str(self.record[2]))
        self.galaxyDistanceFromEarthResultsLabel.configure(text=str(self.record[3]))
        self.galaxyMassResultsLabel.configure(text=str(self.record[4]))
        self.galaxyYearDiscoveredResultsLabel.configure(text=str(self.record[5]))
        self.galaxyImageDisplayer.openImage(False, self.record[6])
        self.galaxyTypeResultsLabel.configure(text=str(self.record[7]))
        self.galaxyTypeDescriptionDisplayer.loadDescriptionWithoutPromptingUser(self.typeDescriptionURL)
        self.galaxyDiscovererNameResultsLabel.configure(text=self.galaxyDiscoverer)

        if (self.showImage.get() == 0):
            self.galaxyImageDisplayer.hideAllImageUI()

        if (self.showGalaxyType.get() == 0):
            self.galaxyTypeDescriptionDisplayer.hideDescriptionUI()

        self.initializeReportContents()

        if (self.confirmButton != None):
            self.confirmButton.configure(state=ACTIVE)

    def resetAllUI(self):
        BaseSingleSearchManager.resetAllUI(self)
        self.galaxyTypeDescriptionDisplayer.resetDescriptionUI(8, 0)
        self.galaxyImageDisplayer.resetImageUI()

        self.toggleNumberOfStars()
        self.toggleAge()
        self.toggleDistanceFromEarth()
        self.toggleYearDiscovered()
        self.toggleImage()
        self.toggleGalaxyType()
        self.toggleGalaxyDiscoverer()

    def initializeSingleSearchForDisplayOnMultiSearchFrame(self, frameToPutInsertionFrameOnto, row, column, nameToQueryFor, searchManager):
        BaseSingleSearchManager.initializeSingleSearchForDisplayOnMultiSearchFrame(self, frameToPutInsertionFrameOnto, row, column, nameToQueryFor, searchManager)

        self.showNumberOfStars = IntVar()
        self.showNumberOfStars.set(1)

        self.showAge = IntVar()
        self.showAge.set(1)

        self.showDistanceFromEarth = IntVar()
        self.showDistanceFromEarth.set(1)

        self.showMass = IntVar()
        self.showMass.set(1)

        self.showYearDiscovered = IntVar()
        self.showYearDiscovered.set(1)

        self.showImage = IntVar()
        self.showImage.set(1)

        self.showGalaxyDiscoverer = IntVar()
        self.showGalaxyDiscoverer.set(1)

        self.showGalaxyType = IntVar()
        self.showGalaxyType.set(1)

        self.populateFields()

    def initializeAllDataDisplayerUI(self):
        self.galaxyNameLabel = Label(self.resultsFrame, text="Galaxy Name:")
        self.galaxyNameResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.galaxyNameLabel, self.galaxyNameResultsLabel, 0)

        self.galaxyNumberOfStarsLabel = Label(self.resultsFrame, text="Number of Stars in Galaxy:")
        self.galaxyNumberOfStarsResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.galaxyNumberOfStarsLabel, self.galaxyNumberOfStarsResultsLabel, 1)

        self.galaxyAgeLabel = Label(self.resultsFrame, text="Galaxy Age:")
        self.galaxyAgeResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.galaxyAgeLabel, self.galaxyAgeResultsLabel, 2)

        self.galaxyDistanceFromEarthLabel = Label(self.resultsFrame, text="Galaxy Distance from Earth:")
        self.galaxyDistanceFromEarthResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.galaxyDistanceFromEarthLabel, self.galaxyDistanceFromEarthResultsLabel, 3)

        self.galaxyMassLabel = Label(self.resultsFrame, text="Galaxy Mass:")
        self.galaxyMassResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.galaxyMassLabel, self.galaxyMassResultsLabel, 4)

        self.galaxyYearDiscoveredLabel = Label(self.resultsFrame, text="Galaxy Year Discovered:")
        self.galaxyYearDiscoveredResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.galaxyYearDiscoveredLabel, self.galaxyYearDiscoveredResultsLabel, 5)

        self.galaxyImageDisplayer = ImageDisplayerManager()
        self.galaxyImageDisplayer.initializeImageDisplayer(6, 0, 2, self.resultsFrame, None, False)

        self.galaxyTypeLabel = Label(self.resultsFrame, text="Galaxy type:")
        self.galaxyTypeResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.galaxyTypeLabel, self.galaxyTypeResultsLabel, 8)
        self.galaxyTypeDescriptionDisplayer = TextBoxManager()
        self.galaxyTypeDescriptionDisplayer.initializeDescriptionBoxForReadingOnlyAndNotLoading(self.resultsFrame, 9, 0, 10, 0)

        self.galaxyDiscovererNameLabel = Label(self.resultsFrame, text="Galaxy Discoverer:")
        self.galaxyDiscovererNameResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.galaxyDiscovererNameLabel, self.galaxyDiscovererNameResultsLabel, 11)

    def manageSingleGalaxySearch(self, windowToPutFrameOnto, mainSearchManager):

        self.defaultReportName = "SingleGalaxySearch"
        self.successMessageRow = 14

        dropdownSearchQuery = '''

                    SELECT Name
                    FROM Galaxies;

                '''
        labelText = "Select Galaxy to search for: "
        searchTitle = "Single Galaxy Search"

        self.manageSingleSearch(dropdownSearchQuery, windowToPutFrameOnto, mainSearchManager, searchTitle, labelText)

        self.showNumberOfStars = IntVar()
        self.showNumberOfStars.set(1)
        self.showNumberofStarsCheckBox = Checkbutton(self.insertionFrame, text="Show Number of Stars", variable=self.showNumberOfStars, onvalue=1, offvalue=0, command=self.toggleNumberOfStars)
        self.showNumberofStarsCheckBox.grid(row=3, column=0)

        self.showAge = IntVar()
        self.showAge.set(1)
        self.showAgeCheckBox = Checkbutton(self.insertionFrame, text="Show age", variable=self.showAge, onvalue=1, offvalue=0, command=self.toggleAge)
        self.showAgeCheckBox.grid(row=3, column=1)

        self.showDistanceFromEarth = IntVar()
        self.showDistanceFromEarth.set(1)
        self.showDistanceFromEarthCheckBox = Checkbutton(self.insertionFrame, text="Show Distance", variable=self.showDistanceFromEarth, onvalue=1, offvalue=0, command=self.toggleDistanceFromEarth)
        self.showDistanceFromEarthCheckBox.grid(row=4, column=0)

        self.showMass = IntVar()
        self.showMass.set(1)
        self.showMassCheckBox = Checkbutton(self.insertionFrame, text="Show mass", variable=self.showMass, onvalue=1, offvalue=0, command=self.toggleMass)
        self.showMassCheckBox.grid(row=4, column=1)

        self.showYearDiscovered = IntVar()
        self.showYearDiscovered.set(1)
        self.showYearDiscoveredCheckBox = Checkbutton(self.insertionFrame, text="Show Year Discovered", variable=self.showYearDiscovered, onvalue=1, offvalue=0, command=self.toggleYearDiscovered)
        self.showYearDiscoveredCheckBox.grid(row=5, column=0)

        self.showImage = IntVar()
        self.showImage.set(1)
        self.showImageCheckBox = Checkbutton(self.insertionFrame, text="Show Galaxy Image", variable=self.showImage, onvalue=1, offvalue=0, command=self.toggleImage)
        self.showImageCheckBox.grid(row=5, column=1)

        self.showGalaxyType = IntVar()
        self.showGalaxyType.set(1)
        self.showGalaxyTypeCheckBox = Checkbutton(self.insertionFrame, text="Show Galaxy Type", variable=self.showGalaxyType, onvalue=1, offvalue=0, command=self.toggleGalaxyType)
        self.showGalaxyTypeCheckBox.grid(row=6, column=0)

        self.showGalaxyDiscoverer = IntVar()
        self.showGalaxyDiscoverer.set(1)
        self.showGalaxyDiscovererCheckBox = Checkbutton(self.insertionFrame, text="Show Galaxy Discoverer", variable=self.showGalaxyDiscoverer, onvalue=1, offvalue=0, command=self.toggleGalaxyDiscoverer)
        self.showGalaxyDiscovererCheckBox.grid(row=6, column=1)

        self.allCheckBoxes = []
        self.allCheckBoxes.append(self.showNumberofStarsCheckBox)
        self.allCheckBoxes.append(self.showAgeCheckBox)
        self.allCheckBoxes.append(self.showDistanceFromEarthCheckBox)
        self.allCheckBoxes.append(self.showMassCheckBox)
        self.allCheckBoxes.append(self.showYearDiscoveredCheckBox)
        self.allCheckBoxes.append(self.showImageCheckBox)
        self.allCheckBoxes.append(self.showGalaxyTypeCheckBox)
        self.allCheckBoxes.append(self.showGalaxyDiscovererCheckBox)

        self.allResultsLabels = []
        self.allResultsLabels.append(self.galaxyNameResultsLabel)
        self.allResultsLabels.append(self.galaxyNumberOfStarsResultsLabel)
        self.allResultsLabels.append(self.galaxyAgeResultsLabel)
        self.allResultsLabels.append(self.galaxyDistanceFromEarthResultsLabel)
        self.allResultsLabels.append(self.galaxyMassResultsLabel)
        self.allResultsLabels.append(self.galaxyYearDiscoveredResultsLabel)
        self.allResultsLabels.append(self.galaxyTypeResultsLabel)
        self.allResultsLabels.append(self.galaxyDiscovererNameResultsLabel)

        self.confirmButton.grid(row=7, column=0, sticky=W + E)
        self.cancelButton.grid(row=7, column=1, sticky=W + E)

        Label(self.insertionFrame, text="Name to save report as: ").grid(row=8, column=0)
        self.reportNameInputBox.grid(row=8, column=1, sticky=W + E)