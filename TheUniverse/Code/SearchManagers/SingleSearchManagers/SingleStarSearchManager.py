'''
----SUMMARY----
Allows the user to search
for individual stars and produce
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
since this is a specific option for searching for a single star

tkinter - Used for all the UI

ImageDisplayerManager -
This is used to display an image of the
star the user searches for

TextBoxManager -
Used to display a description of the
evolutionary stage the star the user searches
for is currently in
'''

from Code.SearchManagers.BaseSearchManagers.BaseSingleSearchManager import BaseSingleSearchManager
from Code.Displayers.ImageDisplayerManager import ImageDisplayerManager
from Code.Displayers.TextBoxManager import TextBoxManager
from tkinter import *

class SingleStarSearchManager(BaseSingleSearchManager):

    global galaxyStarIsIn

    global starNameLabel
    global starNameResultsLabel

    global starMassLabel
    global starMassResultsLabel

    global starRadiusLabel
    global starRadiusResultsLabel

    global starEvolutionaryStageLabel
    global starEvolutionaryStageResultsLabel

    global starDistanceFromEarthLabel
    global starDistanceFromEarthResultsLabel

    global starSystemLabel
    global starSystemResultsLabel

    global imageDisplayer
    global evolutionaryStageDescriptionDisplayer

    global galaxyStarIsInLabel
    global galaxyStarIsInResultsLabel

    # filters:
    global showMassCheckBox
    global showMass

    global showRadiusCheckBox
    global showRadius

    global showEvolutionaryStageCheckBox
    global showEvolutionaryStage

    global showDistanceFromEarthCheckBox
    global showDistanceFromEarth

    global showPlanetarySystemCheckBox
    global showPlanetarySystem

    global showImageCheckBox
    global showImage

    global showGalaxyStarIsInCheckBox
    global showGalaxy

    def resetAllUI(self):
        BaseSingleSearchManager.resetAllUI(self)
        self.evolutionaryStageDescriptionDisplayer.resetDescriptionUI(4, 0)
        self.imageDisplayer.resetImageUI()

        self.toggleGalaxy()
        self.toggleMass()
        self.toggleImage()
        self.toggleRadius()
        self.togglePlanetarySystem()
        self.toggleDistanceFromEarth()
        self.toggleEvolutionaryStage()

        self.record.clear()


    def initializeReportContents(self):
        try:
            if (self.initializedForMultiDisplay == False):
                self.insertionManager.reportGenerator.refreshReportGenerator()

            allPossibleAttributeNames = [
                "Star Mass (Solar Mass): ",
                "Star Radius (Solar Radius): ",
                "Star Evolutionary Stage: ",
                "Star Distance From Earth (ly): ",
                "Star System: ",
                "Image Directory: ",
            ]

            recordToReport = []
            attributeNames = []
            exclusionFilters = []
            exclusionFilters.append(self.showMass.get())
            exclusionFilters.append(self.showRadius.get())
            exclusionFilters.append(self.showEvolutionaryStage.get())
            exclusionFilters.append(self.showDistanceFromEarth.get())
            exclusionFilters.append(self.showPlanetarySystem.get())
            exclusionFilters.append(self.showImage.get())
            recordToReport.append(self.record[0])
            attributeNames.append("Star Name: ")

            for i in range(0, len(exclusionFilters)):
                if (exclusionFilters[i] == 1):
                    recordToReport.append(str(self.record[i + 1]))
                    attributeNames.append(allPossibleAttributeNames[i])
                else:
                    print(allPossibleAttributeNames[i] + " will not be shown")

            if (self.showGalaxy.get() == 1):
                recordToReport.append(self.galaxyStarIsIn.strip('\n'))
                attributeNames.append("Galaxy Star is in: ")

            imageURL = None
            if (self.showImage.get() == 1):
                imageURL = self.record[len(self.record) - 1]

            # generate report, but do not save it yet:
            self.insertionManager.reportGenerator.generateReports(recordToReport, imageURL, attributeNames)
        except:
            return

    def populateFields(self):
        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        query = '''

                                SELECT * 
                                FROM Stars
                                WHERE Name = %s;

                            '''
        cursor.execute(query, [self.selectedItemToSearchFor.get()])
        record = cursor.fetchone()

        self.record = []
        for attribute in record:
            self.record.append(attribute)

        evolutionaryStageDescriptionDir = "Unknown"

        # get the description dir for the stage this star is
        query = '''

                        SELECT Description
                        FROM EvolutionaryStages 
                        WHERE EvolutionaryStage = %s;

                    '''
        cursor.execute(query, [self.record[3]])
        record = cursor.fetchone()

        if (record != None):
            evolutionaryStageDescriptionDir = record[0]

        # get the galaxy the star is in:
        query = '''
        
            SELECT GalaxyName 
            FROM Galaxies INNER JOIN (
            
                SELECT GalaxyName
                FROM PlanetarySystems 
                INNER JOIN Stars 
                    ON PlanetarySystems.Name = %s 
            
            ) AS SystemStarIsIn 
                ON Galaxies.Name = SystemStarIsIn.GalaxyName;
        
        '''
        self.galaxyStarIsIn = "Unknown"
        cursor.execute(query, [self.record[5]])
        record = cursor.fetchone()
        if (record != None):
            self.galaxyStarIsIn = record[0]

        database.close()

        self.starNameResultsLabel.configure(text=str(self.record[0]))
        self.starMassResultsLabel.configure(text=str(self.record[1]))
        self.starRadiusResultsLabel.configure(text=str(self.record[2]))
        self.starEvolutionaryStageResultsLabel.configure(text=str(self.record[3]))
        self.starDistanceFromEarthResultsLabel.configure(text=str(self.record[4]))
        self.starSystemResultsLabel.configure(text=str(self.record[5]))
        self.imageDisplayer.openImage(False, str(self.record[6]))

        self.evolutionaryStageDescriptionDisplayer.loadDescriptionWithoutPromptingUser(evolutionaryStageDescriptionDir)
        self.galaxyStarIsInResultsLabel.configure(text=str(self.galaxyStarIsIn))

        if (self.showImage.get() == 0):
            self.imageDisplayer.hideAllImageUI()

        if (self.showEvolutionaryStage.get() == 0):
            self.evolutionaryStageDescriptionDisplayer.hideDescriptionUI()

        self.initializeReportContents()

        if (self.confirmButton != None):
            self.confirmButton.configure(state=ACTIVE)

    def toggleMass(self):
        if (self.showMass.get() == 0):
            self.starMassLabel.grid_forget()
            self.starMassResultsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.starMassLabel, self.starMassResultsLabel, 1)
        self.initializeReportContents()

    def toggleRadius(self):
        if (self.showRadius.get() == 0):
            self.starRadiusLabel.grid_forget()
            self.starRadiusResultsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.starRadiusLabel, self.starRadiusResultsLabel, 2)
        self.initializeReportContents()

    def toggleDistanceFromEarth(self):
        if (self.showDistanceFromEarth.get() == 0):
            self.starDistanceFromEarthLabel.grid_forget()
            self.starDistanceFromEarthResultsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.starDistanceFromEarthLabel, self.starDistanceFromEarthResultsLabel, 6)
        self.initializeReportContents()

    def toggleImage(self):
        if (self.showImage.get() == 0):
            self.imageDisplayer.hideAllImageUI()
        else:
            self.imageDisplayer.showAllImageUI()
        self.initializeReportContents()

    def toggleEvolutionaryStage(self):
        if (self.showEvolutionaryStage.get() == 0):
            self.starEvolutionaryStageLabel.grid_forget()
            self.starEvolutionaryStageResultsLabel.grid_forget()
            self.evolutionaryStageDescriptionDisplayer.hideDescriptionUI()
        else:
            self.setUpLabelPositions(self.starEvolutionaryStageLabel, self.starEvolutionaryStageResultsLabel, 3)
            self.evolutionaryStageDescriptionDisplayer.showAllDescriptionUI()
        self.initializeReportContents()

    def togglePlanetarySystem(self):
        if (self.showPlanetarySystem.get() == 0):
            self.starSystemLabel.grid_forget()
            self.starSystemResultsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.starSystemLabel, self.starSystemResultsLabel, 7)
        self.initializeReportContents()

    def toggleGalaxy(self):
        if (self.showGalaxy.get() == 0):
            self.galaxyStarIsInLabel.grid_forget()
            self.galaxyStarIsInResultsLabel.grid_forget()
        else:
            self.setUpLabelPositions(self.galaxyStarIsInLabel, self.galaxyStarIsInResultsLabel, 10)
        self.initializeReportContents()


    def manageSingleStarSearch(self, windowToPutFrameOnto, mainSearchManager):
        dropdownSearchQuery = '''

                    SELECT Name
                    FROM Stars;

                '''
        labelText = "Select star to search for: "
        searchTitle = "Single Star Search"

        self.defaultReportName = "SingleStarSearchReport"
        self.successMessageRow = 9

        self.manageSingleSearch(dropdownSearchQuery, windowToPutFrameOnto, mainSearchManager, searchTitle, labelText)

        self.showMass = IntVar()
        self.showMass.set(1)
        self.showMassCheckBox = Checkbutton(self.insertionFrame, text="Show mass", variable=self.showMass, onvalue=1,
                                            offvalue=0, command=self.toggleMass)
        self.showMassCheckBox.grid(row=3, column=0)

        self.showRadius = IntVar()
        self.showRadius.set(1)
        self.showRadiusCheckBox = Checkbutton(self.insertionFrame, text="Show radius", variable=self.showRadius, onvalue=1,
                                            offvalue=0, command=self.toggleRadius)
        self.showRadiusCheckBox.grid(row=3, column=1)

        self.showEvolutionaryStage = IntVar()
        self.showEvolutionaryStage.set(1)
        self.showEvolutionaryStageCheckBox = Checkbutton(self.insertionFrame, text="Show Evolutionary Stage", variable=self.showEvolutionaryStage, onvalue=1,
                                            offvalue=0, command=self.toggleEvolutionaryStage)
        self.showEvolutionaryStageCheckBox.grid(row=4, column=0)

        self.showDistanceFromEarth = IntVar()
        self.showDistanceFromEarth.set(1)
        self.showDistanceFromEarthCheckBox = Checkbutton(self.insertionFrame, text="Show Distance From Earth", variable=self.showDistanceFromEarth, onvalue=1,
                                            offvalue=0, command=self.toggleDistanceFromEarth)
        self.showDistanceFromEarthCheckBox.grid(row=4, column=1)

        self.showPlanetarySystem = IntVar()
        self.showPlanetarySystem.set(1)
        self.showPlanetarySystemCheckBox = Checkbutton(self.insertionFrame, text="Show Star System", variable=self.showPlanetarySystem, onvalue=1,
                                            offvalue=0, command=self.togglePlanetarySystem)
        self.showPlanetarySystemCheckBox.grid(row=5, column=0)

        self.showImage = IntVar()
        self.showImage.set(1)
        self.showImageCheckBox = Checkbutton(self.insertionFrame, text="Show Image", variable=self.showImage, onvalue=1, offvalue=0, command=self.toggleImage)
        self.showImageCheckBox.grid(row=5, column=1)

        self.showGalaxy = IntVar()
        self.showGalaxy.set(1)
        self.showGalaxyStarIsInCheckBox = Checkbutton(self.insertionFrame, text="Show Galaxy", variable=self.showGalaxy, onvalue=1, offvalue=0, command=self.toggleGalaxy)
        self.showGalaxyStarIsInCheckBox.grid(row=6, column=0, columnspan=2)

        self.confirmButton.grid(row=7, column=0, sticky=W + E)
        self.cancelButton.grid(row=7, column=1, sticky=W + E)

        Label(self.insertionFrame, text="Name to save report as: ").grid(row=8, column=0)
        self.reportNameInputBox.grid(row=8, column=1, sticky=W + E)

        self.allResultsLabels = []
        self.allResultsLabels.append(self.starNameResultsLabel)
        self.allResultsLabels.append(self.starMassResultsLabel)
        self.allResultsLabels.append(self.starRadiusResultsLabel)
        self.allResultsLabels.append(self.starEvolutionaryStageResultsLabel)
        self.allResultsLabels.append(self.starDistanceFromEarthResultsLabel)
        self.allResultsLabels.append(self.starSystemResultsLabel)
        self.allResultsLabels.append(self.galaxyStarIsInResultsLabel)

        self.allCheckBoxes = []
        self.allCheckBoxes.append(self.showMassCheckBox)
        self.allCheckBoxes.append(self.showRadiusCheckBox)
        self.allCheckBoxes.append(self.showEvolutionaryStageCheckBox)
        self.allCheckBoxes.append(self.showDistanceFromEarthCheckBox)
        self.allCheckBoxes.append(self.showPlanetarySystemCheckBox)
        self.allCheckBoxes.append(self.showImageCheckBox)
        self.allCheckBoxes.append(self.showImageCheckBox)
        self.allCheckBoxes.append(self.showGalaxyStarIsInCheckBox)

    def initializeSingleSearchForDisplayOnMultiSearchFrame(self, frameToPutInsertionFrameOnto, row, column, nameToQueryFor, searchManager):
        BaseSingleSearchManager.initializeSingleSearchForDisplayOnMultiSearchFrame(self, frameToPutInsertionFrameOnto, row, column, nameToQueryFor, searchManager)

        self.showMass = IntVar()
        self.showMass.set(1)

        self.showRadius = IntVar()
        self.showRadius.set(1)

        self.showEvolutionaryStage = IntVar()
        self.showEvolutionaryStage.set(1)

        self.showDistanceFromEarth = IntVar()
        self.showDistanceFromEarth.set(1)

        self.showPlanetarySystem = IntVar()
        self.showPlanetarySystem.set(1)

        self.showImage = IntVar()
        self.showImage.set(1)

        self.showGalaxy = IntVar()
        self.showGalaxy.set(1)

        self.populateFields()

    def initializeAllDataDisplayerUI(self):

        self.starNameLabel = Label(self.resultsFrame, text="Star Name: ")
        self.starNameResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.starNameLabel, self.starNameResultsLabel, 0)

        self.starMassLabel = Label(self.resultsFrame, text="Star Mass: ")
        self.starMassResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.starMassLabel, self.starMassResultsLabel, 1)

        self.starRadiusLabel = Label(self.resultsFrame, text="Star Radius: ")
        self.starRadiusResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.starRadiusLabel, self.starRadiusResultsLabel, 2)

        self.starEvolutionaryStageLabel = Label(self.resultsFrame, text="Star Evolutionary Stage: ")
        self.starEvolutionaryStageResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.starEvolutionaryStageLabel, self.starEvolutionaryStageResultsLabel, 3)

        self.evolutionaryStageDescriptionDisplayer = TextBoxManager()
        self.evolutionaryStageDescriptionDisplayer.initializeDescriptionBoxForReadingOnlyAndNotLoading(self.resultsFrame, 4, 0, 5, 0)

        self.starDistanceFromEarthLabel = Label(self.resultsFrame, text="Star Distance From Earth: ")
        self.starDistanceFromEarthResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.starDistanceFromEarthLabel, self.starDistanceFromEarthResultsLabel, 6)

        self.starSystemLabel = Label(self.resultsFrame, text="System star is in: ")
        self.starSystemResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.starSystemLabel, self.starSystemResultsLabel, 7)

        self.imageDisplayer = ImageDisplayerManager()
        self.imageDisplayer.initializeImageDisplayer(8, 0, 2, self.resultsFrame, None, False)

        self.galaxyStarIsInLabel = Label(self.resultsFrame, text="Galaxy star is in: ")
        self.galaxyStarIsInResultsLabel = Label(self.resultsFrame, text="N/A")
        self.setUpLabelPositions(self.galaxyStarIsInLabel, self.galaxyStarIsInResultsLabel, 10)
