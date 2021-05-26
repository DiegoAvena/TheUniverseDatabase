

from tkinter import *
import mysql.connector
from Code.InsertionManagers.BaseInsertionManager import BaseInsertionManager

class NewGalaxyInsertionManager(BaseInsertionManager):

    global galaxyNameInputBox
    global numberofStarsInGalaxyInputBox
    global galaxyAgeInputBox
    global galaxyDistanceFromEarthInputBox
    global galaxyMassInputBox
    global galaxyYearDiscoveredInputBox

    global galaxyTypeDropdown
    global selectedGalaxyType
    global selectedGalaxyTypeLabel

    global newDiscoverNameLabel
    global newDiscoverNameInputBox
    global enterNewDiscovererCheckBox
    global insertingNewDiscoverer
    global selectedDiscoverer
    global discovererNameDropDownBox

    global galaxyTypeOptions
    global discovererNames

    # this method will need to make sure all the data is valid and then submit it to the DB
    def confirm(self):

        thereWasAnError = False

        # check if data is valid:
        galaxyName = self.galaxyNameInputBox.get()

        if (self.insertionValidator.validateWord(False, galaxyName, "Galaxy Name") == False):
            thereWasAnError = True

        numberOfStarsInGalaxy = self.numberofStarsInGalaxyInputBox.get()

        if (self.insertionValidator.validateInteger(numberOfStarsInGalaxy, False, "Number of stars in galaxy", True) == False):
            thereWasAnError = True

        galaxyAge = self.galaxyAgeInputBox.get()
        if (self.insertionValidator.validateInteger(galaxyAge, False, "Galaxy age", True) == False):
            thereWasAnError = True

        galaxyDistanceFromEarth = self.galaxyDistanceFromEarthInputBox.get()
        if (self.insertionValidator.validateDecimalValue(galaxyDistanceFromEarth, False, "Galaxy distance from Earth", False) == False):
            thereWasAnError = True

        galaxyMass = self.galaxyMassInputBox.get()
        if (self.insertionValidator.validateDecimalValue(galaxyMass, False, "Galaxy Mass", True) == False):
            thereWasAnError = True

        galaxyYearDiscovered = self.galaxyYearDiscoveredInputBox.get()
        if (self.insertionValidator.validateYear(galaxyYearDiscovered, "Galaxy year discovered") == False):
            thereWasAnError = True

        discovererName = ""
        if (self.insertingNewDiscoverer.get() == 1):
            discovererName = self.newDiscoverNameInputBox.get()
        else:
            discovererName = self.selectedDiscoverer.get()
            if (discovererName == 'N/A'):
                discovererName = ''

        createADiscovererRecordAsWell = False
        if (len(discovererName) > 0):
            createADiscovererRecordAsWell = True

        if (thereWasAnError == False):

            # Form the final records to place into the database:
            finalGalaxyRecord = []
            finalGalaxyRecord.append(galaxyName)
            finalGalaxyRecord.append(self.insertionValidator.obtainFinalValue(numberOfStarsInGalaxy))
            finalGalaxyRecord.append(self.insertionValidator.obtainFinalValue(galaxyAge))
            finalGalaxyRecord.append(self.insertionValidator.obtainFinalValue(galaxyDistanceFromEarth))
            finalGalaxyRecord.append(self.insertionValidator.obtainFinalValue(galaxyMass))
            finalGalaxyRecord.append(self.insertionValidator.obtainFinalValue(galaxyYearDiscovered))
            finalGalaxyRecord.append(self.insertionValidator.obtainFinalValue(self.imageDir))
            finalGalaxyRecord.append(self.insertionValidator.obtainFinalValue(self.selectedGalaxyType.get()))

            discovererRecord = []
            if (createADiscovererRecordAsWell):
                discovererRecord = [galaxyName, discovererName]
                self.discovererNames.append(discovererName)

                self.discovererNameDropDownBox.grid_forget()
                self.discovererNameDropDownBox.destroy()
                self.discovererNameDropDownBox = OptionMenu(self.insertionFrame, self.selectedDiscoverer,
                                                            *self.discovererNames)

            try:
                # Make a connection to the database and put these new records into it:
                dataBase = self.makeConnectionToDatabase()
                cursor = dataBase.cursor()

                # enter the galaxy record:
                query = '''

                                INSERT INTO Galaxies 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);

                            '''
                cursor.execute(query, finalGalaxyRecord)

                if (createADiscovererRecordAsWell):
                    # enter the galaxy discoverer record:
                    query = ''' 

                                    INSERT IGNORE INTO GalaxyDiscovers 
                                    VALUES (%s, %s);

                                '''
                    cursor.execute(query, discovererRecord)

                messageToDisplayInConfirmationPopUp = "Galaxy Name: " + finalGalaxyRecord[0] + "\n" + \
                                                      "Number of stars in galaxy: " + str(finalGalaxyRecord[1]) + "\n" + \
                                                      "Galaxy Age: " + str(finalGalaxyRecord[2]) + "\n" + \
                                                      "Galaxy Distance From Earth: " + str(
                    finalGalaxyRecord[3]) + "\n" + \
                                                      "Galaxy Mass: " + str(finalGalaxyRecord[4]) + "\n" + \
                                                      "Galaxy Year Discovered: " + str(finalGalaxyRecord[5]) + "\n" + \
                                                      "Galaxy Image directory: " + str(finalGalaxyRecord[6]) + "\n" + \
                                                      "Galaxy Type: " + str(finalGalaxyRecord[7]) + "\n" + \
                                                      "Galaxy Discoverer: " + str(
                    self.insertionValidator.obtainFinalValue(discovererName))

                if (self.showConfirmationPopUp(messageToDisplayInConfirmationPopUp) == True):
                    self.showSuccessMessage(13, 0, 2)
                    dataBase.commit()

                    self.selectedGalaxyType.set('N/A')
                    self.selectedDiscoverer.set('N/A')

                    self.imageDir = ''

                    # clear all text fields
                    self.galaxyNameInputBox.delete(0, END)
                    self.newDiscoverNameInputBox.delete(0, END)
                    self.galaxyMassInputBox.delete(0, END)
                    self.galaxyAgeInputBox.delete(0, END)
                    self.galaxyDistanceFromEarthInputBox.delete(0, END)
                    self.numberofStarsInGalaxyInputBox.delete(0, END)
                    self.newDiscoverNameInputBox.delete(0, END)
                    self.galaxyYearDiscoveredInputBox.delete(0, END)

                    self.resetImageUI(2)

                else:
                    dataBase.rollback()
            except mysql.connector.Error:
                self.insertionValidator.errorMessage = self.errorMessageForWhenCommitFailsDueToSqlError
                self.showErrorMessage(13, 0, 2)
                dataBase.rollback()

            dataBase.close()
        else:
            self.showErrorMessage(13, 0, 2)

        self.insertionValidator.errorMessage = ""

    def disableOrEnableNewDiscovererInsertion(self, ):
        if (self.insertingNewDiscoverer.get() == 1):
            self.discovererNameDropDownBox.grid_forget()
            self.newDiscoverNameInputBox.grid(row=11, column=1)
        else:
            self.newDiscoverNameInputBox.grid_forget()
            self.discovererNameDropDownBox.grid(row=11, column=0, columnspan=3)

    def manageInsertion(self, windowToPutFrameOnto, insertionManager, insertionTitle):

        BaseInsertionManager.manageInsertion(self, windowToPutFrameOnto, insertionManager, insertionTitle)

        # place the input fields:
        Label(self.insertionFrame, text="Galaxy Name (REQUIRED): ").grid(row=0, column=0)
        self.galaxyNameInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.galaxyNameInputBox.grid(row=0, column=1)

        Label(self.insertionFrame, text="Number of stars in this galaxy: ").grid(row=1, column=0)
        self.numberofStarsInGalaxyInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.numberofStarsInGalaxyInputBox.grid(row=1, column=1)

        Label(self.insertionFrame, text="Galaxy age (years): ").grid(row=2, column=0)
        self.galaxyAgeInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.galaxyAgeInputBox.grid(row=2, column=1)

        Label(self.insertionFrame, text="Galaxy distance from Earth (Required) (Light years): ").grid(row=3, column=0)
        self.galaxyDistanceFromEarthInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.galaxyDistanceFromEarthInputBox.grid(row=3, column=1)

        Label(self.insertionFrame, text="Galaxy Mass (Solar Mass): ").grid(row=4, column=0)
        self.galaxyMassInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.galaxyMassInputBox.grid(row=4, column=1)

        Label(self.insertionFrame, text="Galaxy Year Discovered: ").grid(row=5, column=0)
        self.galaxyYearDiscoveredInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)
        self.galaxyYearDiscoveredInputBox.grid(row=5, column=1)

        # need to perform a quick query for all the galaxy type names to display them to the user:
        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        query = '''
        
            SELECT GalaxyType FROM GalaxyTypes;
        
        '''
        cursor.execute(query)
        galaxyTypes = cursor.fetchall()
        self.galaxyTypeOptions = []
        self.galaxyTypeOptions.append('N/A')
        for galaxyType in galaxyTypes:
            self.galaxyTypeOptions.append(galaxyType[0])

        self.selectedGalaxyType = StringVar()
        self.selectedGalaxyType.set(self.galaxyTypeOptions[0])

        Label(self.insertionFrame, text="Select Galaxy Type: ").grid(row=6, column=0)
        self.galaxyTypeDropdown = OptionMenu(self.insertionFrame, self.selectedGalaxyType, *self.galaxyTypeOptions)
        self.galaxyTypeDropdown.grid(row=6, column=1)

        # place the buttons needed to ask for the galaxy image directory and to confirm:
        self.loadImageDirectoryButton.grid(row=7, column=0, columnspan=2)

        self.initializeImageDirLabelPos(8, 0, 2)
        self.imageCanvas.grid(row=9, column=0, columnspan=2)

        # place the galaxy discoverer input box in:
        self.insertingNewDiscoverer = IntVar()
        self.insertingNewDiscoverer.set(0)
        self.enterNewDiscovererCheckBox = Checkbutton(self.insertionFrame, text="Enter New discoverer Name?", font=self.buttonFontStyle,variable=self.insertingNewDiscoverer, onvalue=1, offvalue=0, command=self.disableOrEnableNewDiscovererInsertion)
        self.enterNewDiscovererCheckBox.grid(row=10, column=0, columnspan=2)

        query = '''

            SELECT DISTINCT DiscovererName
            FROM GalaxyDiscovers;

        '''
        cursor.execute(query)
        records = cursor.fetchall()
        self.discovererNames = []
        self.discovererNames.append('N/A')
        for discovererName in records:
            self.discovererNames.append(discovererName[0])

        self.newDiscoverNameLabel = Label(self.insertionFrame, text="Enter new discoverer name: ",
                                          font=self.buttonFontStyle)
        self.newDiscoverNameLabel.grid(row=11, column=0)
        self.newDiscoverNameInputBox = Entry(self.insertionFrame, width=50, borderwidth=1)

        self.selectedDiscoverer = StringVar()
        self.selectedDiscoverer.set(self.discovererNames[0])

        self.discovererNameDropDownBox = OptionMenu(self.insertionFrame, self.selectedDiscoverer, *self.discovererNames)
        self.discovererNameDropDownBox.grid(row=11, column=1, columnspan=3)

        # place the confirm button:
        self.confirmButton.grid(row=12, column=0, sticky=W+E)

        # place the cancel button
        self.cancelButton.grid(row=12, column=1, sticky=W+E)

        database.close()
