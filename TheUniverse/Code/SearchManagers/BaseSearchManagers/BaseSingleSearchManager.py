'''

---SUMMARY---
Contains the base functionality needed for
a specific single search option, such as
creation of the drop down the user will
need in order to select the thing they
want to search for, the scroll bar and
scrollable frame needed to contain all
of the display UI, the creation
of the report file name insertion box, etc.

---IMPORTS---
BaseDataBaseInteractionManager:

used for base data base modifying functionality,
since this specific option will be interacting
with the table via single searches

tkinter - for all of the UI

'''

from Code.BaseDataBaseInteractionManager import BaseDataBaseInteractionManager
from tkinter import *

class BaseSingleSearchManager(BaseDataBaseInteractionManager):

    global allResultsLabels
    global allCheckBoxes

    global initializedForMultiDisplay

    global dropdownSearchQuery
    global selectedItemToSearchFor
    global record

    global reportNameInputBox

    global defaultReportName
    global successMessageRow

    global mainDropDown

    # the frame to display the results on, has a vertical scroll in case results extend beyond screen height
    global scrollContainer
    global resultsCanvas
    global scrollbar
    global resultsFrame

    def setUpLabelPositions(self, titleLabel, resultLabel, row):
        titleLabel.grid(row=row, column=0)
        resultLabel.grid(row=row, column=1)

    def resetAllUI(self):
        for checkbox in self.allCheckBoxes:
            checkbox.select()

        for resultLabel in self.allResultsLabels:
            resultLabel.configure(text='N/A')

        self.record.clear()
        self.selectedItemToSearchFor.set('N/A')
        self.confirmButton.configure(state=DISABLED)

    def initializeAllDataDisplayerUI(self):
        pass

    def populateFields(self):
        pass

    def initializeReportContents(self):
        pass

    def showSuccessMessage(self, row, column, columnspan):
        Label(self.insertionFrame, text=self.successMessage).grid(row=row, column=column, columnspan=columnspan)

    def confirm(self):
        # generate report:
        reportName = self.defaultReportName
        if (self.reportNameInputBox.get() != ''):
            reportName = self.reportNameInputBox.get()

        self.reportNameInputBox.delete(0, END)
        self.insertionManager.reportGenerator.saveGeneratedReports(reportName)
        self.showSuccessMessage(self.successMessageRow, 0, 2)
        self.resetAllUI()

    # use this method to perform the search and display the data
    def confirmSearch(self, nameOfThingSelected):
        if (self.selectedItemToSearchFor.get() != 'N/A'):

            self.populateFields()

        else:
            self.resetAllUI()

    def initializeSingleSearchForDisplayOnMultiSearchFrame(self, frameToPutInsertionFrameOnto, row, column, nameToQueryFor, searchManager):

        self.selectedItemToSearchFor = StringVar()
        self.selectedItemToSearchFor.set(nameToQueryFor)

        self.initializedForMultiDisplay = True

        self.insertionManager = searchManager

        self.insertionFrame = LabelFrame(frameToPutInsertionFrameOnto)
        self.insertionFrame.grid(row=row, column=column)

        self.scrollContainer = LabelFrame(self.insertionFrame)
        self.scrollContainer.grid(row=1, column=0, columnspan=2)
        self.resultsCanvas = Canvas(self.scrollContainer, width=590, height=400)
        self.scrollbar = Scrollbar(self.scrollContainer, orient="vertical", command=self.resultsCanvas.yview)
        self.resultsFrame = LabelFrame(self.resultsCanvas)

        # Call the configure function of canvas whenever the the
        # the size of the results frame changes so that the canvas
        # knows how much it can scroll
        # code for this taken from:
        self.resultsFrame.bind(

            "<Configure>",
            lambda e: self.resultsCanvas.configure(

                scrollregion=self.resultsCanvas.bbox("all")

            )

        )

        # tell the results canvas to draw the results frame inside of it:
        self.resultsCanvas.create_window((0, 0), window=self.resultsFrame, anchor="nw")

        # configure the results canvas so that when its y pos changes, the scrollbar moves:
        self.resultsCanvas.configure(yscrollcommand=self.scrollbar.set)

        # add this scroll canvas and scroll to the main frame now:
        self.resultsCanvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.confirmButton = None
        self.initializeAllDataDisplayerUI()

    def manageSingleSearch(self, dropDownSearchQuery, windowToPutFrameOnto, mainSearchManager, searchTitle, labelText):

        self.initializedForMultiDisplay = False

        self.successMessage = "Report generated!"

        self.dropdownSearchQuery = dropDownSearchQuery
        self.initializeInteractionBase(windowToPutFrameOnto, mainSearchManager, searchTitle)

        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        cursor.execute(self.dropdownSearchQuery)
        records = cursor.fetchall()
        thingsToList = []
        thingsToList.append('N/A')
        for record in records:
            thingsToList.append(record[0])

        self.selectedItemToSearchFor = StringVar()
        self.selectedItemToSearchFor.set('N/A')

        Label(self.insertionFrame, text=labelText).grid(row=0, column=0)
        self.thingsToUpdateDropDown = OptionMenu(self.insertionFrame, self.selectedItemToSearchFor, *thingsToList, command=self.confirmSearch)
        self.thingsToUpdateDropDown.grid(row=0, column=1, sticky=W + E)

        Label(self.insertionFrame, text="SEARCH RESULTS:").grid(row=1, column=0, columnspan=2)
        self.scrollContainer = LabelFrame(self.insertionFrame)
        self.scrollContainer.grid(row=2, column=0, columnspan=2)
        self.resultsCanvas = Canvas(self.scrollContainer, width=590, height=400)
        self.scrollbar = Scrollbar(self.scrollContainer, orient="vertical", command=self.resultsCanvas.yview)
        self.resultsFrame = LabelFrame(self.resultsCanvas)

        # Call the configure function of canvas whenever the the
        # the size of the results frame changes so that the canvas
        # knows how much it can scroll
        # code for this taken from:
        self.resultsFrame.bind(

            "<Configure>",
            lambda e: self.resultsCanvas.configure(

                scrollregion=self.resultsCanvas.bbox("all")

            )

        )

        # tell the results canvas to draw the results frame inside of it:
        self.resultsCanvas.create_window((0, 0), window=self.resultsFrame, anchor="nw")

        # configure the results canvas so that when its y pos changes, the scrollbar moves:
        self.resultsCanvas.configure(yscrollcommand=self.scrollbar.set)

        # add this scroll canvas and scroll to the main frame now:
        self.resultsCanvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.confirmButton.configure(state=DISABLED)
        self.reportNameInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.initializeAllDataDisplayerUI()

