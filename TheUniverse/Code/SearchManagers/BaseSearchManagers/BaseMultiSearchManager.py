'''

---SUMMARY---
Contains the base functionality needed for
a specific multi search option, such as
creation of the results frame that will
allow the user to scroll through all of the
individual records, the creation of the confirm
search button, the initialization of the collections
for all of the sorting filters, etc.

---IMPORTS---
BaseDataBaseInteractionManager:

used for base data base modifying functionality,
since this specific option will be interacting with the
table via multiple searches

tkinter - for all of the UI

'''

from Code.BaseDataBaseInteractionManager import BaseDataBaseInteractionManager
from tkinter import *

class BaseMultiSearchManager(BaseDataBaseInteractionManager):

    global scrollContainer
    global resultsCanvas
    global scrollbar
    global verticalScrollbar
    global resultsFrame

    global recordDisplayersSpawnedInSoFar
    global confirmSearchButton

    global reportNameInputBox

    global anySortingFramesThatSpawned
    global sortingSwitches

    global defaultReportName
    global reportUIRow

    def showSuccessMessage(self, row, column, columnspan):
        Label(self.insertionFrame, text=self.successMessage).grid(row=row, column=column, columnspan=columnspan)

    def chooseSortingScheme(self, indexOfSortingSwitchToLeaveAlone):
        for i in range(0, len(self.sortingSwitches)):
            if (i != indexOfSortingSwitchToLeaveAlone):
                self.sortingSwitches[i].deselect()

    def confirm(self):

        if (self.reportNameInputBox.get() != ''):
            self.insertionManager.reportGenerator.saveGeneratedReports(self.reportNameInputBox.get())
        else:
            self.insertionManager.reportGenerator.saveGeneratedReports(self.defaultReportName)

        self.reportNameInputBox.grid_forget()
        self.reportNameInputBox.grid(row=self.reportUIRow, column=2)
        self.showSuccessMessage(self.reportUIRow, 3, 1)
        self.reportNameInputBox.delete(0, END)

    # use this method to perform the search and display the data
    def performSearch(self):
        self.insertionManager.reportGenerator.refreshReportGenerator()

        # despawn all the planet displayers to make room for the new results:
        for planetDisplayer in self.recordDisplayersSpawnedInSoFar:
            planetDisplayer.insertionFrame.grid_forget()
            planetDisplayer.insertionFrame.destroy()

        for sortingFrame in self.anySortingFramesThatSpawned:
            sortingFrame.grid_forget()
            sortingFrame.destroy()

        self.anySortingFramesThatSpawned.clear()
        self.recordDisplayersSpawnedInSoFar.clear()

    def determineIfThereIsASortingClause(self):
        pass

    def positionConfirmationUI(self, startingRow):
        self.confirmSearchButton.grid(row=startingRow, column=0, columnspan=4, sticky=W + E)

        startingRow += 1
        self.confirmButton.grid(row=startingRow, column=0, columnspan=2, sticky=W + E)
        self.confirmButton.configure(state=ACTIVE)
        self.cancelButton.grid(row=startingRow, column=2, columnspan=2, sticky=W + E)

        startingRow += 1
        Label(self.insertionFrame, text="Enter the name of the report to generate: ").grid(row=startingRow, column=0,
                                                                                           columnspan=2)
        self.reportNameInputBox.grid(row=startingRow, column=2, columnspan=2, sticky=E + W)

        self.reportUIRow = startingRow

    def manageMultiSearch(self, windowToPutFrameOnto, mainSearchManager, searchTitle):
        self.successMessage = "Report generated!"

        self.initializeInteractionBase(windowToPutFrameOnto, mainSearchManager, searchTitle)

        self.confirmSearchButton = Button(self.insertionFrame, text="CONFIRM SEARCH", font=self.buttonFontStyle,
                                          padx=80,
                                          pady=5, command=self.performSearch)

        Label(self.insertionFrame, text="SEARCH RESULTS:").grid(row=1, column=0, columnspan=4)
        self.scrollContainer = LabelFrame(self.insertionFrame)
        self.scrollContainer.grid(row=2, column=0, columnspan=4)
        self.resultsCanvas = Canvas(self.scrollContainer, width=1200, height=400)
        self.scrollbar = Scrollbar(self.scrollContainer, orient="horizontal", command=self.resultsCanvas.xview)
        self.verticalScrollbar = Scrollbar(self.scrollContainer, orient="vertical", command=self.resultsCanvas.yview)
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

        # configure the results canvas so that when its x and y pos changes, the scrollbars move:
        self.resultsCanvas.configure(xscrollcommand=self.scrollbar.set, yscrollcommand=self.verticalScrollbar.set)

        # add this scroll canvas and scroll to the main frame now:
        self.resultsCanvas.grid(row=0, column=0)
        self.scrollbar.grid(row=1, column=0, sticky=E+W)
        self.verticalScrollbar.grid(row=0, column=1, sticky=N+S)

        self.confirmButton.configure(state=DISABLED)

        self.reportNameInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)

        self.anySortingFramesThatSpawned = []
        self.sortingSwitches = []