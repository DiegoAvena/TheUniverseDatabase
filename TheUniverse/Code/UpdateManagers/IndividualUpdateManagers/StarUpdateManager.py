'''

----SUMMARY---
Allows the user to update
a star

---IMPORTS---
BaseUpdateManager:

Used to obtain base functionality
for a more specific update, since this
class is for the specific update on
star

tkinter - for all of the UI

mysql:

for performing the update queries and
search query needed to display the initial
record to the user

ImageDisplayerManager:

This is used to display an image of the
star on the initial record,
and to allow the user to update this
star image

messageBox from tkinter:

used to ask the user if they did not
insert a new star because they wish
to delete the initial star image (provided
that the star does currently have an image for it), this
item is also used for the same reason for the
description insertion option (if user leaves description empty,
and the initial record has a description, a pop up will show
asking if they left this empty because they want to delete
the old description and leave it blank)

TextBoxManager:

used to display a description of the star on
the initial record side, and to allow the user
to insert a description on the update side

'''

from Code.UpdateManagers.BaseUpdateManager import BaseUpdateManager
from Code.Displayers.ImageDisplayerManager import ImageDisplayerManager
from tkinter import *
from tkinter import messagebox
import mysql

class StarUpdateManager(BaseUpdateManager):

    # initial star UI
    global initialStarMassLabel
    global initialStarRadiusLabel
    global initialStarEvolutionaryTypeLabel
    global initialStarDistanceFromEarthLabel
    global initialSystemStarIsInLabel
    global initialStarImageDisplayerManager

    # star updating UI
    global newStarNameInputBox
    global newStarMassInputBox
    global newStarRadiusInputBox
    global newStarEvolutionaryStageDropdown
    global newSelectedEvolutionaryStage
    global newStarDistanceFromEarthInputBox
    global newSystemStarIsInDropDownBox
    global newSelectedStarSystem
    global newStarImageManager

    global deleteOldImage

    # perform the update for the selected star
    def confirm(self):
        thereWasAnError = False

        if (self.insertionValidator.validateWord(False, self.selectedThingToUpdate.get(), "Name of star to update") == False):
            thereWasAnError = True

        newStarName = self.newStarNameInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(self.newStarNameInputBox.get())):
            self.insertionValidator.errorMessage += "New star name has the deletion code, but a star name cannot be empty!" + "\n"
            thereWasAnError = True

        newStarMass = self.newStarMassInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newStarMass) == False):
            if (self.insertionValidator.validateDecimalValue(newStarMass, False, "New Star Mass", True) == False):
                thereWasAnError = True

        newStarRadius = self.newStarRadiusInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newStarRadius) == False):
            if (self.insertionValidator.validateDecimalValue(newStarRadius, False, "New Star Radius", True) == False):
                thereWasAnError = True

        newStarDistanceFromEarth = self.newStarDistanceFromEarthInputBox.get()
        if (self.insertionValidator.checkIfUserTryingToDeleteValue(newStarDistanceFromEarth)):
            self.insertionValidator.errorMessage += "New star distance from earth has the erase code, but this value cannot be empty" + "\n"
            thereWasAnError = True
        elif (self.insertionValidator.validateDecimalValue(newStarDistanceFromEarth, False, "New star distance from earth", True) == False):
            thereWasAnError = True


        if (thereWasAnError == False):

            # form the query:
            newChanges = []
            query = '''
            
                UPDATE Stars 
                SET
            
            '''
            messageToDisplayInPopUp = ""

            if (len(newStarName) > 0):
                query += " Name = %s"
                messageToDisplayInPopUp += "-Update star name from " + self.initialRecord[0] + " to " + newStarName + "\n"
                newChanges.append(newStarName)

            if (len(newStarMass) > 0):
                if (len(newChanges) > 0):
                    query += ","
                query += " Mass = %s"
                messageToDisplayInPopUp += "-Update star mass from " + str(self.initialRecord[1]) + " to " + newStarMass + "\n"
                newChanges.append(self.insertionValidator.obtainFinalValue(newStarMass))

            if (len(newStarRadius) > 0):
                if (len(newChanges) > 0):
                    query += ","
                query += " Radius = %s"
                messageToDisplayInPopUp += "-Update star radius from " + str(self.initialRecord[2]) + " to " + newStarRadius + "\n"
                newChanges.append(self.insertionValidator.obtainFinalValue(newStarRadius))

            if (len(self.newSelectedEvolutionaryStage.get()) > 0):
                if (len(newChanges) > 0):
                    query += ","
                query += " EvolutionaryStage = %s"
                messageToDisplayInPopUp += "-Update star evolutionary stage from " + str(self.initialRecord[3]) + " to " + self.newSelectedEvolutionaryStage.get() + "\n"
                newChanges.append(self.newSelectedEvolutionaryStage.get())

            if (len(newStarDistanceFromEarth) > 0):
                if (len(newChanges) > 0):
                    query += ","
                query += " DistanceFromEarth = %s"
                messageToDisplayInPopUp += "-Update star distance from earth from " + str(self.initialRecord[4]) + " to " + newStarDistanceFromEarth + "\n"
                newChanges.append(newStarDistanceFromEarth)

            if (len(self.newSelectedStarSystem.get()) > 0):
                if (len(newChanges) > 0):
                    query += ","
                query += " PlanetarySystem = %s"
                messageToDisplayInPopUp += "-Update system star is in from " + str(self.initialRecord[5]) + " to " + self.newSelectedStarSystem.get() + "\n"
                newChanges.append(self.newSelectedStarSystem.get())

            if (self.newStarImageManager.imageLoaded):
                if (len(newChanges) > 0):
                    query += ","
                query += "ImageDirectory = %s"
                messageToDisplayInPopUp += "-Update star image directory from " + str(self.initialRecord[6]) + " to " + self.newStarImageManager.imageDir + "\n"
                newChanges.append(self.newStarImageManager.imageDir)
            elif (self.initialStarImageDisplayerManager.imageLoaded):
                # show a dialogue asking the user if they left the image dir empty because they want to delete initial image:
                if (messagebox.askyesno("Delete initial image?",
                                        "Detected that you have not loaded an image in, is this because you want to delete the current image?")):
                    if (len(newChanges) > 0):
                        # add a comma:
                        query += ","
                    query += "ImageDirectory = NULL"
                    messageToDisplayInPopUp += "-Update star image directory from " + str(self.initialRecord[6]) + " to N/A" + "\n"

                    self.deleteOldImage = True

            if ((len(newChanges) > 0) or self.deleteOldImage):

                # there is something to update
                query += " WHERE Name = %s;"
                newChanges.append(self.selectedThingToUpdate.get())

                database = self.makeConnectionToDatabase()
                try:
                    cursor = database.cursor()
                    cursor.execute(query, newChanges)
                    if (self.showConfirmationPopUp(messageToDisplayInPopUp)):
                        database.commit()
                        self.showSuccessMessage(2, 0, 2)
                        self.resetAllUI(True)
                        self.resetThingToSelectDropdownMenu()
                        self.deleteOldImage = False
                    else:
                        database.rollback()
                except mysql.connector.Error as error:
                    self.insertionValidator.errorMessage = self.errorMessageForWhenCommitFailsDueToSqlError + ": " + str(error)
                    self.showErrorMessage(2, 0, 2)
                    database.rollback()

            else:
                self.insertionValidator.errorMessage = "NOTHING TO UPDATE..."
                self.showErrorMessage(2, 0, 2)

        else:
            self.showErrorMessage(2, 0, 2)

        self.insertionValidator.errorMessage = ''

    def resetAllUI(self, includingUpdateUI):

        self.resetThingToSelectDropdownMenu()
        self.initialStarMassLabel.configure(text='N/A')
        self.initialStarRadiusLabel.configure(text='N/A')
        self.initialStarEvolutionaryTypeLabel.configure(text='N/A')
        self.initialStarDistanceFromEarthLabel.configure(text='N/A')
        self.initialSystemStarIsInLabel.configure(text='N/A')
        self.initialStarImageDisplayerManager.resetImageUI()

        if (includingUpdateUI):
            self.newStarNameInputBox.delete(0, END)
            self.newStarMassInputBox.delete(0, END)
            self.newStarRadiusInputBox.delete(0, END)
            self.newSelectedEvolutionaryStage.set('')
            self.newStarDistanceFromEarthInputBox.delete(0, END)
            self.newSelectedStarSystem.set('')
            self.newStarImageManager.resetImageUI()

    def selectThingToUpdate(self, nameOfThingSelected):
        if (nameOfThingSelected != 'N/A'):
            database = self.makeConnectionToDatabase()
            cursor = database.cursor()
            query = '''
            
                SELECT *
                FROM Stars 
                WHERE Name = %s;
            
            '''
            cursor.execute(query, [nameOfThingSelected])
            record = cursor.fetchone()
            self.initialRecord = []
            for attribute in record:
                self.initialRecord.append(attribute)

            self.initialStarMassLabel.configure(text=str(self.initialRecord[1]))
            self.initialStarRadiusLabel.configure(text=str(self.initialRecord[2]))
            self.initialStarEvolutionaryTypeLabel.configure(text=str(self.initialRecord[3]))
            self.initialStarDistanceFromEarthLabel.configure(text=str(self.initialRecord[4]))
            self.initialSystemStarIsInLabel.configure(text=str(self.initialRecord[5]))
            self.initialStarImageDisplayerManager.openImage(False, self.initialRecord[6])

        else:
            self.resetAllUI(False)

    # initialize all UI needed to perform a star record update
    def manageUpdate(self, windowToPutFrameOnto, updateManager, updateTitle):
        BaseUpdateManager.manageUpdate(self, windowToPutFrameOnto, updateManager, updateTitle)
        self.deleteOldImage = False

        query = '''
        
            SELECT Name 
            FROM Stars;
        
        '''
        self.setUpThingToUpdateSelector(0, 1, query, "Selected Star: ")

        Label(self.leftFrame, text="Star mass: ").grid(row=1, column=0)
        self.initialStarMassLabel = Label(self.leftFrame, text="N/A")
        self.initialStarMassLabel.grid(row=1, column=1)

        Label(self.leftFrame, text="Star Radius: ").grid(row=2, column=0)
        self.initialStarRadiusLabel = Label(self.leftFrame, text="N/A")
        self.initialStarRadiusLabel.grid(row=2, column=1)

        Label(self.leftFrame, text="Star Evolutionary Stage: ").grid(row=3, column=0)
        self.initialStarEvolutionaryTypeLabel = Label(self.leftFrame, text="N/A")
        self.initialStarEvolutionaryTypeLabel.grid(row=3, column=1)

        Label(self.leftFrame, text="Star Distance From Earth: ").grid(row=4, column=0)
        self.initialStarDistanceFromEarthLabel = Label(self.leftFrame, text="N/A")
        self.initialStarDistanceFromEarthLabel.grid(row=4, column=1)

        Label(self.leftFrame, text="System star is in: ").grid(row=5, column=0)
        self.initialSystemStarIsInLabel = Label(self.leftFrame, text="N/A")
        self.initialSystemStarIsInLabel.grid(row=5, column=1)

        self.initialStarImageDisplayerManager = ImageDisplayerManager()
        self.initialStarImageDisplayerManager.initializeImageDisplayer(6, 0, 2, self.leftFrame, None, False)

        # set up the updating UI now:
        Label(self.rightFrame, text="New Star Name: ").grid(row=0, column=0)
        self.newStarNameInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newStarNameInputBox.grid(row=0, column=1)

        Label(self.rightFrame, text="New Star Mass: ").grid(row=1, column=0)
        self.newStarMassInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newStarMassInputBox.grid(row=1, column=1)

        Label(self.rightFrame, text="New Star Radius: ").grid(row=2, column=0)
        self.newStarRadiusInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newStarRadiusInputBox.grid(row=2, column=1)

        # user will be able to change the evolutionary stage of a star
        # from here, so another dropdown is needed that displays the
        # possible stages the user can update to
        database = self.makeConnectionToDatabase()
        cursor = database.cursor()
        query = '''
        
            SELECT EvolutionaryStage
            FROM EvolutionaryStages;
        
        '''
        cursor.execute(query)
        records = cursor.fetchall()
        stages = []
        stages.append('')
        for stage in records:
            stages.append(stage[0])

        self.newSelectedEvolutionaryStage = StringVar()
        self.newSelectedEvolutionaryStage.set('')

        Label(self.rightFrame, text="Evolutionary Stage: ").grid(row=3, column=0)
        self.newStarEvolutionaryStageDropdown = OptionMenu(self.rightFrame, self.newSelectedEvolutionaryStage, *stages)
        self.newStarEvolutionaryStageDropdown.grid(row=3, column=1)

        Label(self.rightFrame, text="Star Distance from Earth: ").grid(row=4, column=0)
        self.newStarDistanceFromEarthInputBox = Entry(self.rightFrame, width=50, borderwidth=1)
        self.newStarDistanceFromEarthInputBox.grid(row=4, column=1)

        # the user will be able to update the planetary system the star
        # is in from here, so a dropdown menu for this is also needed
        query = '''
        
            SELECT Name 
            FROM PlanetarySystems;
        
        '''
        cursor.execute(query)
        records = cursor.fetchall()
        systems = []
        systems.append('')
        if (records != None):
            for system in records:
                systems.append(system[0])

        self.newSelectedStarSystem = StringVar()
        self.newSelectedStarSystem.set('')

        Label(self.rightFrame, text="System Star is in: ").grid(row=5, column=0)
        self.newSystemStarIsInDropDownBox = OptionMenu(self.rightFrame, self.newSelectedStarSystem, *systems)
        self.newSystemStarIsInDropDownBox.grid(row=5, column=1)

        self.newStarImageManager = ImageDisplayerManager()
        self.newStarImageManager.initializeImageDisplayer(6, 0, 2, self.rightFrame, None, True)

        self.confirmButton.grid(row=1, column=0, sticky=W+E)
        self.cancelButton.grid(row=1, column=1, sticky=W+E)