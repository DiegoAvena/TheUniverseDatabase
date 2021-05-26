'''

----SUMMARY---
Allows the user to update
a galaxy

---IMPORTS---
BaseUpdateManager:

Used to obtain base functionality
for a more specific update, since this
class is for the specific update on
galaxies

tkinter - for all of the UI

mysql:

for performing the update queries and
search query needed to display the initial
record to the user

ImageDisplayerManager:

This is used to display an image of the
galaxy on the initial record,
and to allow the user to update this
galaxy image

messageBox from tkinter:
used to ask the user if they did not
insert a new image because they wish
to delete the initial galaxy image (provided
that the galaxy does currently have an image for it)

'''

from Code.UpdateManagers.BaseUpdateManager import BaseUpdateManager
from tkinter import *
from Code.Displayers.ImageDisplayerManager import ImageDisplayerManager
import mysql
from tkinter import messagebox

class GalaxyUpdateManager(BaseUpdateManager):

    # initial galaxy data
    global galaxiesToChooseFromDropdown
    global selectedGalaxy

    # initial record UI
    global initialNumberOfStarsLabel
    global initialGalaxyAgeLabel
    global initialGalaxyDistanceFromEarthLabel
    global initialGalaxyMassLabel
    global initialGalaxyYearDiscoveredLabel
    global initialGalaxyImageDisplayer
    global initialGalaxyTypeLabel
    global initialGalaxyRecord

    # new changes data:
    global newGalaxyNameInputBox
    global newGalaxyNumberOfStarsInputBox
    global newGalaxyAgeInputBox
    global newGalaxyDistanceFromEarthInputBox
    global newGalaxyMassInputBox
    global newGalaxyYearDiscoveredInputBox
    global galaxyTypesToChooseFromDropdown
    global newSelectedGalaxyType
    global newGalaxyImageDisplayer
    global deleteOldImage

    def confirm(self):
        thereWasAnError = False

        if (self.insertionValidator.validateWord(False, self.selectedGalaxy.get(), "Selected Galaxy to update") == False):
            thereWasAnError = True

        # check new input fields:
        newGalaxyName = self.newGalaxyNameInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newGalaxyName)):
            # user has input N/A into this field, it will get deleted, this is not allowed!
            thereWasAnError = True
            self.insertionValidator.errorMessage += "New galaxy name has the erase code but this value cannot be empty" + "\n"

        # check the new number of stars:
        newNumberOfStars = self.newGalaxyNumberOfStarsInputBox.get()
        # validate the new number of stars the user has place in:
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newNumberOfStars) == False):
            if (self.insertionValidator.validateInteger(newNumberOfStars, False, "New number of stars in this galaxy", True) == False):
                thereWasAnError = True

        # check the new galaxy age:
        newGalaxyAge = self.newGalaxyAgeInputBox.get()
        # validate the new galaxy age the user placed in:
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newGalaxyAge) == False):
            if (self.insertionValidator.validateDecimalValue(newGalaxyAge, False, "New galaxy age", True) == False):
                thereWasAnError = True

        # check new distance from earth:
        newDistanceFromEarth = self.newGalaxyDistanceFromEarthInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newDistanceFromEarth) == False):
            if (self.insertionValidator.validateDecimalValue(newDistanceFromEarth, False, "New distance from Earth", True) == False):
                thereWasAnError = True
        else:
            # user trying to delete this value but this value cannot be null:
            thereWasAnError = True
            self.insertionValidator.errorMessage += "New distance from earth contains the erase code, but this value cannot be empty" + "\n"

        # check new mass
        newMass = self.newGalaxyMassInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newMass) == False):
            if (self.insertionValidator.validateDecimalValue(newMass, False, "New galaxy mass", True) == False):
                thereWasAnError = True

        # check new year discovered:
        newYearDiscovered = self.newGalaxyYearDiscoveredInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newYearDiscovered) == False):
            if (self.insertionValidator.validateYear(newYearDiscovered, "New year galaxy was discovered") == False):
                thereWasAnError = True

        if (thereWasAnError == False):

            messageToShowInConfirmationWindow = ""

            # start forming the update query:
            query = '''

                                UPDATE Galaxies
                                SET
            
            '''

            newChanges = []
            if (len(newGalaxyName) > 0):
                query += "Name = %s"
                newChanges.append(newGalaxyName)
                messageToShowInConfirmationWindow += "-Update galaxy name from " + self.initialGalaxyRecord[0] + " to " + newGalaxyName + "\n"

            if (len(newNumberOfStars) > 0):
                if (len(newChanges) > 0):
                    # add a comma:
                    query += ","
                query += "NumberOfStars = %s"
                messageToShowInConfirmationWindow += "-Update number stars from " + str(self.initialGalaxyRecord[1]) + " to " + newNumberOfStars + "\n"
                newChanges.append(self.insertionValidator.obtainFinalValue(newNumberOfStars))

            if (len(newGalaxyAge) > 0):
                if (len(newChanges) > 0):
                    # add a comma:
                    query += ","
                query += "Age = %s"
                messageToShowInConfirmationWindow += "-Update galaxy age from " + str(self.initialGalaxyRecord[2]) + " to " + newGalaxyAge + "\n"
                newChanges.append(self.insertionValidator.obtainFinalValue(newGalaxyAge))

            if (len(newDistanceFromEarth) > 0):
                if (len(newChanges) > 0):
                    # add a comma:
                    query += ","
                query += "DistanceFromEarth = %s"
                messageToShowInConfirmationWindow += "-Update galaxy distance from earth from " + str(self.initialGalaxyRecord[3]) + " to " + newDistanceFromEarth + "\n"
                newChanges.append(self.insertionValidator.obtainFinalValue(newDistanceFromEarth))

            if (len(newMass) > 0):
                if (len(newChanges) > 0):
                    # add a comma:
                    query += ","
                query += "Mass = %s"
                messageToShowInConfirmationWindow += "-Update galaxy mass from " + str(self.initialGalaxyRecord[4]) + " to " + newMass + "\n"
                newChanges.append(self.insertionValidator.obtainFinalValue(newMass))

            if (len(newYearDiscovered) > 0):
                if (len(newChanges) > 0):
                    # add a comma:
                    query += ","
                query += "YearDiscovered = %s"
                messageToShowInConfirmationWindow += "-Update galaxy year discovered from " + str(self.initialGalaxyRecord[5]) + " to " + newYearDiscovered + "\n"
                newChanges.append(self.insertionValidator.obtainFinalValue(newYearDiscovered))

            if (self.newGalaxyImageDisplayer.imageLoaded):
                if (len(newChanges) > 0):
                    # add a comma:
                    query += ","
                query += "ImageDirectory = %s"
                messageToShowInConfirmationWindow += "-Update image directory from " + str(self.initialGalaxyRecord[6]) + " to " + self.newGalaxyImageDisplayer.imageDir + "\n"
                newChanges.append(self.newGalaxyImageDisplayer.imageDir)
            elif (self.initialGalaxyImageDisplayer.imageLoaded):
                # show a dialogue asking the user if they left the image dir empty because they want to delete initial image:
                if (messagebox.askyesno("Delete initial image?", "Detected that you have not loaded an image in, is this because you want to delete the current image?")):
                    if (len(newChanges) > 0):
                        # add a comma:
                        query += ","
                    query += "ImageDirectory = NULL"
                    messageToShowInConfirmationWindow += "-Update image directory from " + str(
                        self.initialGalaxyRecord[6]) + " to N/A" + "\n"
                    self.deleteOldImage = True

            if (len(self.newSelectedGalaxyType.get()) > 0):
                if (len(newChanges) > 0):
                    # add a comma:
                    query += ","
                query += "GalaxyType = %s"
                messageToShowInConfirmationWindow += "-Update galaxy type directory from " + str(self.initialGalaxyRecord[7]) + " to " + self.newSelectedGalaxyType.get() + "\n"
                newChanges.append(self.newSelectedGalaxyType.get())

            if ((len(newChanges) > 0) or self.deleteOldImage):
                # there are updates to be made:
                query += " WHERE Name = %s;"
                newChanges.append(self.selectedGalaxy.get())

                database = self.makeConnectionToDatabase()

                try:
                    cursor = database.cursor()
                    cursor.execute(query, newChanges)

                    if (self.showConfirmationPopUp(messageToShowInConfirmationWindow)):

                        database.commit()

                        self.showSuccessMessage(2, 0, 2)
                        self.resetAllUI(True)
                        self.deleteOldImage = False

                        # after making the commit, make sure to update the galaxy names to choose from in case a name was updated:
                        query = '''
                        
                            SELECT Name 
                            FROM Galaxies;
                        
                        '''
                        cursor.execute(query)
                        records = cursor.fetchall()
                        galaxiesToChooseFrom = []
                        galaxiesToChooseFrom.append('N/A')
                        for galaxyName in records:
                            galaxiesToChooseFrom.append(galaxyName[0])

                        self.galaxiesToChooseFromDropdown.grid_forget()
                        self.galaxiesToChooseFromDropdown.destroy()

                        self.galaxiesToChooseFromDropdown = OptionMenu(self.leftFrame, self.selectedGalaxy,
                                                                       *galaxiesToChooseFrom, command=self.selectGalaxy)
                        self.galaxiesToChooseFromDropdown.grid(row=0, column=1, sticky=W + E)

                    else:
                        database.rollback()
                except mysql.connector.Error as error:
                    self.insertionValidator.errorMessage = self.errorMessageForWhenCommitFailsDueToSqlError + ": " + str(error)
                    self.showErrorMessage(2, 0, 2)
                    database.rollback()

                database.close()
            else:
                self.insertionValidator.errorMessage = "NOTHING TO UPDATE..."
                self.showErrorMessage(2, 0, 2)

        else:
            self.showErrorMessage(2, 0, 2)
        self.insertionValidator.errorMessage = ''

    def resetAllUI(self, includingUpdatingUI):
        self.initialNumberOfStarsLabel.configure(text='N/A')
        self.initialGalaxyAgeLabel.configure(text='N/A')
        self.initialGalaxyDistanceFromEarthLabel.configure(text='N/A')
        self.initialGalaxyMassLabel.configure(text='N/A')
        self.initialGalaxyYearDiscoveredLabel.configure(text='N/A')
        self.initialGalaxyTypeLabel.configure(text='N/A')
        self.initialGalaxyImageDisplayer.resetImageUI()
        self.selectedGalaxy.set('N/A')

        if (includingUpdatingUI):
            self.newGalaxyNameInputBox.delete(0, END)
            self.newGalaxyNumberOfStarsInputBox.delete(0, END)
            self.newGalaxyAgeInputBox.delete(0, END)
            self.newGalaxyDistanceFromEarthInputBox.delete(0, END)
            self.newGalaxyMassInputBox.delete(0, END)
            self.newGalaxyYearDiscoveredInputBox.delete(0, END)
            self.newSelectedGalaxyType.set('')
            self.newGalaxyImageDisplayer.resetImageUI()

    # select the galaxy to update,
    # and populate fields accordingly, this
    # method is linked to the galaxiesToChooseFrom
    # dropdown
    def selectGalaxy(self, selectedGalaxyName):

        if (selectedGalaxyName != 'N/A'):

            # query for this record to display its current values to the user:
            database = self.makeConnectionToDatabase()
            cursor = database.cursor()
            query = '''
            
                SELECT * 
                FROM Galaxies
                WHERE Name = %s;
            
            '''
            cursor.execute(query, [selectedGalaxyName])
            record = cursor.fetchone()
            self.initialGalaxyRecord = []
            for attribute in record:
                self.initialGalaxyRecord.append(attribute)

            self.initialNumberOfStarsLabel.configure(text=str(self.initialGalaxyRecord[1]))
            self.initialGalaxyAgeLabel.configure(text=str(self.initialGalaxyRecord[2]))
            self.initialGalaxyDistanceFromEarthLabel.configure(text=str(self.initialGalaxyRecord[3]))
            self.initialGalaxyMassLabel.configure(text=str(self.initialGalaxyRecord[4]))
            self.initialGalaxyYearDiscoveredLabel.configure(text=str(self.initialGalaxyRecord[5]))

            if (self.initialGalaxyRecord[6] != None):
                self.initialGalaxyImageDisplayer.openImage(False, self.initialGalaxyRecord[6])

            self.initialGalaxyTypeLabel.configure(text=str(self.initialGalaxyRecord[7]))

        else:
            self.resetAllUI(False)

    # present all UI needed to perform a galaxy update
    def manageUpdate(self, windowToPutFrameOnto, updateManager, updateTitle):
        BaseUpdateManager.manageUpdate(self, windowToPutFrameOnto, updateManager, updateTitle)
        self.deleteOldImage = False

        # initial galaxy record UI:
        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        query = '''
        
            SELECT Name 
            FROM Galaxies;
        
        '''
        cursor.execute(query)
        records = cursor.fetchall()
        galaxiesToChooseFrom = []
        galaxiesToChooseFrom.append('N/A')
        if (records != None):
            for galaxyName in records:
                galaxiesToChooseFrom.append(galaxyName[0])

        self.selectedGalaxy = StringVar()
        self.selectedGalaxy.set(galaxiesToChooseFrom[0])

        Label(self.leftFrame, text="Select a galaxy record to update: ").grid(row=0, column=0)
        self.galaxiesToChooseFromDropdown = OptionMenu(self.leftFrame, self.selectedGalaxy,
                                                          *galaxiesToChooseFrom, command=self.selectGalaxy)
        self.galaxiesToChooseFromDropdown.grid(row=0, column=1, sticky=W + E)

        Label(self.leftFrame, text="Number of stars in this galaxy: ").grid(row=1, column=0)
        self.initialNumberOfStarsLabel = Label(self.leftFrame, text="N/A")
        self.initialNumberOfStarsLabel.grid(row=1, column=1)

        Label(self.leftFrame, text="Galaxy Age: ").grid(row=2, column=0)
        self.initialGalaxyAgeLabel = Label(self.leftFrame, text="N/A")
        self.initialGalaxyAgeLabel.grid(row=2, column=1)

        Label(self.leftFrame, text="Galaxy distance from Earth(ly): ").grid(row=3, column=0)
        self.initialGalaxyDistanceFromEarthLabel = Label(self.leftFrame, text="N/A")
        self.initialGalaxyDistanceFromEarthLabel.grid(row=3, column=1)

        Label(self.leftFrame, text="Galaxy mass (Solar mass): ").grid(row=4, column=0)
        self.initialGalaxyMassLabel = Label(self.leftFrame, text="N/A")
        self.initialGalaxyMassLabel.grid(row=4, column=1)

        Label(self.leftFrame, text="Year galaxy was discovered: ").grid(row=5, column=0)
        self.initialGalaxyYearDiscoveredLabel = Label(self.leftFrame, text="N/A")
        self.initialGalaxyYearDiscoveredLabel.grid(row=5, column=1)

        Label(self.leftFrame, text="Galaxy type: ").grid(row=6, column=0)
        self.initialGalaxyTypeLabel = Label(self.leftFrame, text="N/A")
        self.initialGalaxyTypeLabel.grid(row=6, column=1)

        self.initialGalaxyImageDisplayer = ImageDisplayerManager()
        self.initialGalaxyImageDisplayer.initializeImageDisplayer(7, 0, 2, self.leftFrame, None, False)

        # update UI:
        Label(self.rightFrame, text="Enter a new name for this galaxy: ").grid(row=0, column=0)
        self.newGalaxyNameInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newGalaxyNameInputBox.grid(row=0, column=1)

        Label(self.rightFrame, text="Enter a new number of stars for this galaxy: ").grid(row=1, column=0)
        self.newGalaxyNumberOfStarsInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newGalaxyNumberOfStarsInputBox.grid(row=1, column=1)

        Label(self.rightFrame, text="Enter a new age for this galaxy: ").grid(row=2, column=0)
        self.newGalaxyAgeInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newGalaxyAgeInputBox.grid(row=2, column=1)

        Label(self.rightFrame, text="Enter a new galaxy distance from earth (ly): ").grid(row=3, column=0)
        self.newGalaxyDistanceFromEarthInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newGalaxyDistanceFromEarthInputBox.grid(row=3, column=1)

        Label(self.rightFrame, text="Enter a new mass for this galaxy (solar mass): ").grid(row=4, column=0)
        self.newGalaxyMassInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newGalaxyMassInputBox.grid(row=4, column=1)

        Label(self.rightFrame, text="Enter a new year discovered for this galaxy: ").grid(row=5, column=0)
        self.newGalaxyYearDiscoveredInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newGalaxyYearDiscoveredInputBox.grid(row=5, column=1)

        self.newSelectedGalaxyType = StringVar()
        self.newSelectedGalaxyType.set('')

        galaxyTypesToChooseFrom = []
        galaxyTypesToChooseFrom.append('')

        # user will be able to change the galaxy type of this galaxy
        # from here so I create a dropdown for this right here
        query = '''
        
            SELECT GalaxyType 
            FROM GalaxyTypes; 
        
        '''

        cursor.execute(query)
        records = cursor.fetchall()

        if (records != None):
            for galaxyType in records:
                galaxyTypesToChooseFrom.append(galaxyType[0])

        Label(self.rightFrame, text = "Select a new galaxy type").grid(row=6, column=0)
        self.galaxyTypesToChooseFromDropdown = OptionMenu(self.rightFrame, self.newSelectedGalaxyType,
                                                          *galaxyTypesToChooseFrom)
        self.galaxyTypesToChooseFromDropdown.grid(row=6, column=1)
        self.newGalaxyImageDisplayer = ImageDisplayerManager()
        self.newGalaxyImageDisplayer.initializeImageDisplayer(7, 0, 2, self.rightFrame, None, True)

        self.cancelButton.grid(row=1, column=0, sticky=W+E)
        self.confirmButton.grid(row=1, column=1, sticky=W+E)

        database.close()
